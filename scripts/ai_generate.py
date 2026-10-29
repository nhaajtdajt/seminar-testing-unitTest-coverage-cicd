#!/usr/bin/env python3
"""Source-driven Gemini unit tests and independent CSV experiments for Java classes."""
import argparse
import csv
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

import ai_context as context_builder
import ai_candidates as candidates
import ai_csv
import coverage_gaps
import gemini_client as client

ROOT = Path(__file__).resolve().parents[1]


def fresh(destination, stage, target):
    destination.mkdir(parents=True, exist_ok=False)
    client.save(destination / "stage.json", {"stage": stage, "target_class": target["fqcn"],
        "started_at_utc": client.utc(), "completed": False,
        "environment": "local demo; reads src directly and tests in a system temporary directory"})


def finish(destination, **fields):
    data = json.loads((destination / "stage.json").read_text())
    data.update(fields, finished_at_utc=client.utc())
    client.save(destination / "stage.json", data)
    return data


def render(name, values):
    text = (ROOT / "ai/prompts" / name).read_text()
    required = set(re.findall(r"\{\{([A-Z_]+)\}\}", text))
    if required - values.keys():
        raise ValueError("Unfilled prompt placeholders: " + str(required - values.keys()))
    for key in required:
        text = text.replace("{{" + key + "}}", values[key])
    return text


def java_answer(answer, name, destination, target):
    code, analysis = answer.get("test_source"), answer.get("analysis")
    if not isinstance(code, str) or not isinstance(analysis, str):
        raise ValueError("Expected test_source and analysis strings; use --keep-payloads for payload debugging")
    package = re.search(r"\bpackage\s+([\w.]+)\s*;", code)
    if ((package.group(1) if package else "") != target["package"]
            or not re.search(r"\bclass\s+" + re.escape(name) + r"\b", code)
            or "```" in code or re.search(r"@(?:Disabled\w*|Ignore|Tag)\b", code)):
        raise ValueError("Wrong package/class, disabled/tagged tests or Markdown in Java response")
    directory = destination / "generated"
    directory.mkdir(exist_ok=True)
    path = directory / f"{name}.java"
    path.write_text(code)
    (destination / "analysis.md").write_text(analysis)
    return path


def run_java(source, tests, destination, target, csv_path=None, expected_manifest=None):
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="seminar-ai-java-") as temporary:
        project = Path(temporary) / "case-study"
        expected = expected_manifest or context_builder.manifest(source)
        context_builder.copy_project(source, project, expected)
        test_directory = project / "src/test/java" / Path(*target["package"].split("."))
        test_directory.mkdir(parents=True)
        for path in tests:
            shutil.copy2(path, test_directory / path.name)
        if csv_path:
            resources = project / "src/test/resources"
            resources.mkdir(parents=True)
            shutil.copy2(csv_path, resources / "cases.csv")
        command = ["./mvnw", "-B", "-ntp", "-Dtest.pattern=**/*Test.java", "-Dtest.excludedTags=",
                   "clean", "test", "jacoco:report"]
        environment = {k: v for k, v in os.environ.items() if k not in ("GEMINI_API_KEY", "AI_MODEL")}
        started = client.utc()
        print(f"JUnit/JaCoCo: {target['fqcn']} / {destination.name}", flush=True)
        try:
            process = subprocess.run(command, cwd=project, env=environment, capture_output=True, text=True, timeout=300)
            exit_code, output = process.returncode, process.stdout + process.stderr
        except subprocess.TimeoutExpired as error:
            def text(value):
                return value.decode(errors="replace") if isinstance(value, bytes) else (value or "")
            exit_code, output = 124, text(error.stdout) + text(error.stderr) + "\nMaven timeout (300s).\n"
        key, _ = client.settings()
        if key:
            output = output.replace(key, "<redacted>")
        output = output.replace(str(project), "<project>").replace(str(Path.home()), "<home>")
        (destination / "output.log").write_text(output)
        for relative in ("surefire-reports", "site/jacoco"):
            if (project / "target" / relative).exists():
                shutil.copytree(project / "target" / relative, destination / relative)
        totals, coverage = ai_csv.raw_metrics(destination, target["fqcn"])
        seen = set()
        for path in (destination / "surefire-reports").glob("TEST-*.xml"):
            node = ET.parse(path).getroot()
            if int(node.get("tests", "0")) > int(node.get("skipped", "0")):
                seen.add(node.get("name"))
        expected = {(target["package"] + "." if target["package"] else "") + p.stem for p in tests}
        result = {"target_class": target["fqcn"], "command": command, "started_at_utc": started,
                  "finished_at_utc": client.utc(), "exit_code": exit_code, "quality_gate_executed": False,
                  "test_sha256": {p.name: context_builder.sha(p) for p in tests},
                  "target_coverage": coverage, **totals}
        if csv_path:
            result["csv_sha256"] = context_builder.sha(csv_path)
        result["passed"] = (exit_code == 0 and expected <= seen and totals["tests"] > 0
                            and totals["failures"] == totals["errors"] == totals["skipped"] == 0 and bool(coverage))
        if not coverage:
            result["coverage_note"] = "Target not observed/instrumentable; no coverage success is claimed"
        xml = project / "target/site/jacoco/jacoco.xml"
        if xml.exists():
            gaps = coverage_gaps.extract(xml, project / "src/main/java")
            gaps["report"] = "site/jacoco/jacoco.xml"
            source = target["source"].removeprefix("src/main/java/")
            gaps["gaps"] = [item for item in gaps["gaps"] if item["file"] == source]
            client.save(destination / "gaps.json", gaps)
        client.save(destination / "run.json", result)
        print(f"Tests={result['tests']}, failures={result['failures']}, errors={result['errors']}; passed={result['passed']}", flush=True)
        return result


def unit_candidate(project, context, text, name, destination, target, model, max_repairs,
                   keep_payloads=False, fixed=(), allow_no_additions=False):
    history, previous_code, feedback, kind = [], None, '', None
    for index in range(max_repairs + 1):
        attempt = destination / 'attempts' / f'{index + 1:02d}'
        attempt.mkdir(parents=True)
        prompt = text if index == 0 else render('AI-repair-test.md', {
            'ORIGINAL_PROMPT': text, 'CANDIDATE': previous_code or '',
            'FAILURE_KIND': kind, 'FAILURE_LOG': feedback[-18000:]})
        answer = client.generate(prompt, attempt / 'model', model, keep_payloads=keep_payloads)
        measured = {'target_class': target['fqcn'], 'passed': False, 'exit_code': None,
                    'tests': 0, 'failures': 0, 'errors': 0, 'skipped': 0, 'target_coverage': {}}
        code = answer.get('test_source', '')
        validated = False
        try:
            no_additions = answer.get('decision') == 'no_additions_needed'
            if no_additions:
                if not allow_no_additions or not fixed or code not in ('', None) or not isinstance(answer.get('analysis'), str):
                    raise ValueError('no_additions_needed requires a fully covered baseline, empty test_source and analysis')
                (attempt / 'analysis.md').write_text(answer['analysis'])
                (attempt / 'generated').mkdir()
                current = []
            else:
                if not isinstance(code, str):
                    raise ValueError('test_source must be a string')
                candidates.validate_unit(code)
                if previous_code and not candidates.assertions(previous_code) <= candidates.assertions(code):
                    kind = 'assertion_changed_needs_review'
                    raise ValueError('Repair changed or removed an assertion; automatic repair stopped')
                current = [java_answer(answer, name, attempt, target)]
            for path in fixed:
                copied = attempt / 'generated' / path.name
                shutil.copy2(path, copied)
                current.append(copied)
            validated = True
            measured = run_java(project, current, attempt / 'build', target,
                                expected_manifest=json.loads((destination / 'inputs/manifest.json').read_text()))
            measured['model_decision'] = 'no_additions_needed' if no_additions else 'add_tests'
            client.save(attempt / 'build/run.json', measured)
            feedback = (attempt / 'build/output.log').read_text()
            kind = candidates.repair_kind(measured, feedback)
        except ValueError as error:
            if validated:
                raise  # Source drift/report errors are not model response repairs.
            feedback = str(error)
            kind = kind if kind == 'assertion_changed_needs_review' else 'response_contract'
            (attempt / 'output.log').write_text(feedback + '\n')
        history.append({'attempt': index + 1, 'passed': measured['passed'], 'failure_kind': kind})
        client.save(destination / 'attempts.json', history)
        if measured['passed'] or kind not in ('compilation', 'mock_setup', 'response_contract') or index == max_repairs:
            for directory in ('model', 'generated'):
                if (attempt / directory).exists():
                    shutil.copytree(attempt / directory, destination / directory)
            for filename in ('analysis.md', 'output.log'):
                if (attempt / filename).exists():
                    shutil.copy2(attempt / filename, destination / filename)
            if (attempt / 'build').exists():
                shutil.copytree(attempt / 'build', destination, dirs_exist_ok=True)
            measured.update(failure_kind=kind, code_generation_attempts=index + 1)
            client.save(destination / 'run.json', measured)
            return measured
        previous_code = code
        print(f'Test setup repair {index + 1}/{max_repairs}: {kind}', flush=True)
    raise AssertionError('Unreachable repair loop')


def ai1(destination, target, model=None, prepare=False, requirements=None, schema=None, keep_payloads=False, max_repairs=2):
    fresh(destination, "AI-1", target)
    try:
        project, context = context_builder.snapshot(destination, target, requirements=requirements, schema=schema)
        name = target["name"] + "GeminiDraftTest"
        text = render("AI-1-generate-tests.md", context_builder.substitutions(project, context, name))
        if prepare or keep_payloads:
            (destination / "prompt.md").write_text(text)
        if prepare:
            return finish(destination, status="prepared_only", api_called=False)
        measured = unit_candidate(project, context, text, name, destination, target, model, max_repairs, keep_payloads)
        result = finish(destination, completed=measured['passed'], status='tested', new_model_generation=True)
        candidates.review_report(destination, measured, 'draft_passed_needs_review' if measured['passed'] else 'tests_failed')
        return result
    except Exception as error:
        finish(destination, status="failed", error_type=type(error).__name__)
        raise


def ai2(destination, previous, model=None, prepare=False, keep_payloads=False, max_repairs=2):
    before = json.loads((previous / "run.json").read_text())
    context = json.loads((previous / "inputs/context.json").read_text())
    target = context["target"]
    if not before.get("passed") or not json.loads((previous / "model/api.json").read_text()).get("completed"):
        raise ValueError("AI-2 requires a successful AI-1 model response and measured target coverage")
    draft = previous / "generated" / (target["name"] + "GeminiDraftTest.java")
    if before.get("test_sha256", {}).get(draft.name) != context_builder.sha(draft):
        raise ValueError("AI-1 draft changed after measurement")
    fresh(destination, "AI-2", target)
    try:
        project, context = context_builder.snapshot(destination, previous=previous)
        name = target["name"] + "GeminiAdditionalTest"
        values = context_builder.substitutions(project, context, name)
        values.update(DRAFT_TEST=draft.read_text(), TEST_RESULT=json.dumps(before, ensure_ascii=False),
                      GAPS_JSON=(previous / "gaps.json").read_text())
        text = render("AI-2-coverage.md", values)
        if prepare or keep_payloads:
            (destination / "prompt.md").write_text(text)
        if prepare:
            return finish(destination, status="prepared_only", api_called=False)
        after = unit_candidate(project, context, text, name, destination, target, model, max_repairs, keep_payloads,
                               fixed=[draft], allow_no_additions=candidates.fully_covered(before))
        assessment = candidates.compare(before, after)
        if after.get('model_decision') == 'no_additions_needed' and after.get('passed'):
            assessment = 'no_additions_proposed_needs_review'
        comparison = {"target_class": target["fqcn"], "before": before, "after": after,
                      "limitation": "Coverage/green tests do not certify business rules or assertions"}
        if "BRANCH" in before["target_coverage"] and "BRANCH" in after["target_coverage"]:
            comparison["branch_covered_delta"] = (after["target_coverage"]["BRANCH"]["covered"]
                                                   - before["target_coverage"]["BRANCH"]["covered"])
        client.save(destination / "comparison.json", comparison)
        result = finish(destination, completed=after['passed'] and assessment not in ('coverage_regressed', 'coverage_not_comparable'),
                        status='tested', new_model_generation=True, assessment=assessment, baseline_directory=str(previous.resolve()))
        candidates.review_report(destination, after, assessment, before)
        return result
    except Exception as error:
        finish(destination, status="failed", error_type=type(error).__name__)
        raise


def build_schema(destination, target, model=None, prepare=False, header=None, requirements=None, domain_schema=None, keep_payloads=False):
    fresh(destination, "AI-4-schema", target)
    try:
        project, context = context_builder.snapshot(destination, target, requirements=requirements, schema=domain_schema)
        name = target["name"] + "GeminiCsvTest"
        values = context_builder.substitutions(project, context, name)
        values["CSV_HEADER"] = json.dumps(header) if header is not None else "Not provided; derive it from the API and dependency state."
        text = render("AI-4-schema.md", values)
        if prepare or keep_payloads:
            (destination / "prompt.md").write_text(text)
        if prepare:
            return finish(destination, status="prepared_only", api_called=False, human_rows_sent_to_model=False)
        answer = client.generate(text, destination / "model", model, keep_payloads=keep_payloads)
        columns = ai_csv.validate_schema(answer, header)
        harness = java_answer(answer, name, destination, target)
        code = harness.read_text()
        if len(re.findall(r"@ParameterizedTest\b", code)) != 1 or "@CsvFileSource" not in code or '"/cases.csv"' not in code:
            raise ValueError("Schema harness must use one parameterized CSV test with /cases.csv")
        schema = {"target_class": target["fqcn"], "columns": columns,
                  "harness_file": harness.name, "harness_sha256": context_builder.sha(harness),
                  "human_rows_sent_to_model": False, "human_header_sent_to_model": header is not None}
        client.save(destination / "schema.json", schema)
        with (destination / "cases.template.csv").open("w", newline="") as stream:
            csv.writer(stream).writerow([column["name"] for column in columns])
        return finish(destination, completed=True, status="schema_generated_not_runtime_verified", human_rows_sent_to_model=False)
    except Exception as error:
        finish(destination, status="failed", error_type=type(error).__name__)
        raise


def freeze_data(destination, schema_from, csv_path, author, target=None):
    if schema_from:
        schema = json.loads((schema_from / "schema.json").read_text())
        count = len(ai_csv.read(csv_path, schema))
        fqcn = schema["target_class"]
        validation = "validated against existing CSV schema"
    else:
        with csv_path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            header, rows = reader.fieldnames, list(reader)
        if (not header or len(set(header)) != len(header) or not rows
                or not all(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", h) for h in header)
                or any(None in row or any(v is None for v in row.values()) for row in rows)):
            raise ValueError("Human CSV needs unique header identifiers and complete data rows")
        count, fqcn = len(rows), target["fqcn"]
        validation = "structure/hash only; semantic schema will be inferred later from src and header"
    if not author.strip():
        raise ValueError("Provide the actual human author")
    destination.mkdir(parents=True, exist_ok=False)
    shutil.copy2(csv_path, destination / "cases.csv")
    client.save(destination / "receipt.json", {"author": author, "target_class": fqcn,
        "sha256": context_builder.sha(csv_path), "frozen_at_utc": client.utc(), "case_count": count,
        "validation": validation,
        "attestation": "Author declares cases written before viewing AI data; schema/harness may be AI-assisted",
        "limitation": "Self-attestation and hash do not prove independent authorship"})


def ai4(destination, target, human, model=None, prepare=False, schema_from=None, requirements=None, domain_schema=None, keep_payloads=False):
    receipt = ai_csv.check_frozen(human, target["fqcn"])
    fresh(destination, "AI-4", target)
    try:
        if not schema_from:
            schema_from = destination / "schema-stage"
            built = build_schema(schema_from, target, model, prepare, ai_csv.header(human / "cases.csv"),
                                 requirements, domain_schema, keep_payloads)
            if prepare:
                return finish(destination, status="schema_prompt_prepared_only", api_called=False, human_rows_sent_to_model=False)
            if not built["completed"]:
                raise ValueError("Schema generation failed")
        schema = json.loads((schema_from / "schema.json").read_text())
        if schema["target_class"] != target["fqcn"]:
            raise ValueError("Schema belongs to another class")
        ai_csv.read(human / "cases.csv", schema)
        harness = schema_from / "generated" / schema["harness_file"]
        if harness.name != target["name"] + "GeminiCsvTest.java" or context_builder.sha(harness) != schema["harness_sha256"]:
            raise ValueError("Schema harness changed after generation")
        project, context = context_builder.snapshot(destination, target, previous=schema_from)
        values = context_builder.substitutions(project, context, harness.stem)
        values["CSV_SCHEMA"] = json.dumps(schema, ensure_ascii=False)
        text = render("AI-4-boundary-data.md", values)
        if prepare or keep_payloads:
            (destination / "prompt.md").write_text(text)
        if prepare:
            return finish(destination, status="prepared_only", api_called=False, human_rows_sent_to_model=False)
        answer = client.generate(text, destination / "model", model, keep_payloads=keep_payloads)
        if not isinstance(answer.get("csv"), str) or not isinstance(answer.get("analysis"), str):
            raise ValueError("AI-4 needs csv and analysis strings")
        generated = destination / "generated"
        generated.mkdir()
        ai_data = generated / "cases.csv"
        ai_data.write_text(answer["csv"])
        (destination / "analysis.md").write_text(answer["analysis"])
        ai_csv.read(ai_data, schema)
        if ai_csv.check_frozen(human, target["fqcn"])["sha256"] != receipt["sha256"]:
            raise ValueError("Human data changed during generation")
        saved_human = destination / "inputs/human"
        shutil.copytree(human, saved_human)
        shutil.copy2(harness, generated / harness.name)
        harness = generated / harness.name
        client.save(destination / "schema.json", schema)
        comparison = ai_csv.compare(saved_human / "cases.csv", ai_data, schema)
        client.save(destination / "comparison.json", comparison)
        expected = json.loads((destination / "inputs/manifest.json").read_text())
        before = run_java(project, [harness], destination / "human", target, saved_human / "cases.csv", expected)
        after = run_java(project, [harness], destination / "ai", target, ai_data, expected)
        client.save(destination / "execution-comparison.json", {"human": before, "ai": after})
        reconciled = ai_csv.reconcile(destination, target["fqcn"], saved_human / "cases.csv", ai_data, schema, comparison, harness)
        client.save(destination / "reconciliation.json", reconciled)
        (destination / "report.md").write_text(ai_csv.report(reconciled))
        return finish(destination, completed=before["passed"] and after["passed"] and reconciled["consistent"],
                      status="compared_executed_and_reconciled", human_rows_sent_to_model=False,
                      human_sha256=receipt["sha256"], new_model_generation=True)
    except Exception as error:
        finish(destination, status="failed", error_type=type(error).__name__)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("list-classes", "ai1", "ai2", "pipeline", "schema", "freeze", "ai4", "all"))
    parser.add_argument("--class", dest="class_name", help="Simple or fully qualified top-level Java class")
    parser.add_argument("--from-ai1", type=Path)
    parser.add_argument("--schema-from", type=Path, help="Saved AI-4 schema stage, not a database schema")
    parser.add_argument("--human-frozen", type=Path, help="Directory with human cases.csv and receipt.json")
    parser.add_argument("--requirements", type=Path, help="Optional independent business requirements document")
    parser.add_argument("--schema", type=Path, help="Optional SQL/JSON/domain schema document")
    parser.add_argument("--csv", type=Path, help="Human CSV for freeze; not sent to Gemini")
    parser.add_argument("--author")
    parser.add_argument("--attest-independent", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--model")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--keep-payloads", action="store_true", help="Debug only: retain full prompts and model payloads")
    parser.add_argument('--max-repairs', type=int, choices=(0, 1, 2), default=2,
                        help='At most 2 technical repairs; assertion failures are left for review')
    args = parser.parse_args()
    if args.stage == "list-classes":
        print(json.dumps(context_builder.discover(), ensure_ascii=False, indent=2))
        return 0
    if args.stage in ("ai1", "ai2", "pipeline", "all") and args.output:
        # Apply has to be able to delete the output safely after syncing reviewed tests.
        import ai_apply
        try:
            ai_apply.managed_directory(args.output)
        except ValueError as error:
            parser.error(str(error))
    if args.stage in ("ai1", "pipeline", "schema", "ai4", "all") and not args.class_name:
        parser.error("Provide --class; business class selection is no longer hard-coded")
    if args.stage == "ai2" and not args.from_ai1:
        parser.error("ai2 needs --from-ai1")
    if args.stage in ("ai4", "all") and not args.human_frozen:
        parser.error("AI-4 needs --human-frozen; never reuse another class's human data")
    if args.stage == "freeze" and not ((args.schema_from or args.class_name) and args.csv and args.author
                                        and args.attest_independent and args.output):
        parser.error("freeze needs --class (or --schema-from), --csv, --author, --attest-independent and durable --output")
    try:
        if args.stage != "freeze" and not args.prepare_only:
            client.configured(args.model)
        stamp = client.utc().replace(":", "").replace(".", "").replace("+0000", "Z")
        output = (args.output or ROOT / ".ai-work" / f"{stamp}-{args.stage}").resolve()
        if args.stage == "freeze":
            freeze_data(output, args.schema_from.resolve() if args.schema_from else None, args.csv.resolve(), args.author,
                        context_builder.select(args.class_name) if args.class_name else None)
            print(f"Human data frozen: {output}")
            return 0
        target = context_builder.select(args.class_name) if args.class_name else None
        if args.stage == "ai2" and target:
            baseline_target = json.loads((args.from_ai1 / "inputs/context.json").read_text())["target"]
            if baseline_target["fqcn"] != target["fqcn"]:
                raise ValueError("--class differs from the AI-1 baseline target")
        common = {"model": args.model, "prepare": args.prepare_only, "keep_payloads": args.keep_payloads}
        inputs = {"requirements": args.requirements, "schema": args.schema}
        print(f"Output: {output}", flush=True)
        repairs = {'max_repairs': args.max_repairs}
        if args.stage == 'pipeline':
            output.mkdir(parents=True, exist_ok=False)
            client.save(output / 'session.json', {'kind': 'ai12', 'stages': ['ai1', 'ai2']})
            first = ai1(output / 'ai1', target, **common, **inputs, **repairs)
            result = ai2(output / 'ai2', output / 'ai1', **common, **repairs) if first.get('completed') else first
            if not first.get('completed'):
                print('AI-2 not run: AI-1 is not a passing measured baseline.', flush=True)
        elif args.stage == "ai1":
            result = ai1(output, target, **common, **inputs, **repairs)
        elif args.stage == "ai2":
            result = ai2(output, args.from_ai1.resolve(), **common, **repairs)
        elif args.stage == "schema":
            result = build_schema(output, target, **common, requirements=args.requirements, domain_schema=args.schema)
        elif args.stage == "ai4":
            result = ai4(output, target, args.human_frozen.resolve(), **common,
                         schema_from=args.schema_from.resolve() if args.schema_from else None,
                         requirements=args.requirements, domain_schema=args.schema)
        else:
            ai_csv.check_frozen(args.human_frozen.resolve(), target["fqcn"])
            output.mkdir(parents=True, exist_ok=False)
            results = {}
            for stage in ("ai1", "ai2", "ai4"):
                if stage == "ai2" and (args.prepare_only or not results.get("ai1", {}).get("completed")):
                    results[stage] = {"completed": False, "status": "skipped_without_passing_baseline"}
                else:
                    try:
                        if stage == "ai1":
                            results[stage] = ai1(output / stage, target, **common, **inputs, **repairs)
                        elif stage == "ai2":
                            results[stage] = ai2(output / stage, output / "ai1", **common, **repairs)
                        else:
                            results[stage] = ai4(output / stage, target, args.human_frozen.resolve(), **common,
                                schema_from=args.schema_from.resolve() if args.schema_from else None,
                                requirements=args.requirements, domain_schema=args.schema)
                    except (ValueError, RuntimeError, OSError, KeyError, subprocess.SubprocessError) as error:
                        results[stage] = {"completed": False, "error_type": type(error).__name__}
                        print(f"{stage} stopped: {error}", file=sys.stderr)
                client.save(output / "summary.json", results)
            result = {"completed": all(item.get("completed") for item in results.values())}
        return 0 if args.prepare_only or result["completed"] else 1
    except (ValueError, RuntimeError, OSError, KeyError, subprocess.SubprocessError) as error:
        print(f"Stopped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
