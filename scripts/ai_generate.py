#!/usr/bin/env python3
"""Real Gemini AI-1/AI-2/AI-4 demo for FineCalculator. No production/test source overwrite."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

import ai4_compare
import coverage_gaps
import gemini_client as client

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path("vn/edu/seminar/fine")
TARGET = "vn/edu/seminar/fine/FineCalculator"
DRAFT = "FineCalculatorGeminiDraftTest"
ADDITIONAL = "FineCalculatorGeminiAdditionalTest"
SPEC = (
    "FineCalculator.calculate(int daysLate, MemberTier tier) returns BigDecimal VND. "
    "NORMAL: grace=0 days, then 2000 VND per late day. VIP: grace=2 days, then "
    "1000 VND per day beyond grace. Within grace, including zero, the fee is zero. "
    "Both tiers have a 50000 VND cap. A null tier or negative days throws "
    "IllegalArgumentException. daysLate uses the full Java int range. "
    "The API has MemberTier.NORMAL and MemberTier.VIP; null is Java null."
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fresh(destination, stage):
    destination.mkdir(parents=True, exist_ok=False)
    client.save(destination / "stage.json", {"stage": stage, "started_at_utc": client.utc(),
                "completed": False, "environment": "local isolated Maven copy; not CI or paper reproduction",
                "operator": "invoking person/process; not independently verified", "human_review": "pending"})


def finish(destination, **fields):
    path = destination / "stage.json"
    data = json.loads(path.read_text())
    data.update(fields, finished_at_utc=client.utc())
    client.save(path, data)
    return data


def snapshot(destination, previous=None):
    project = destination / "inputs/project"
    if previous:
        source = previous / "inputs/project"
        manifest = json.loads((previous / "inputs/manifest.json").read_text())
        actual = {p.relative_to(source).as_posix(): digest(p) for p in source.rglob("*") if p.is_file()}
        if actual != manifest:
            raise ValueError("AI-1 source snapshot changed; refuse an invalid before/after comparison")
        shutil.copytree(source, project)
    else:
        source = ROOT / "case-study"
        project.mkdir(parents=True)
        for name in ("pom.xml", "mvnw"):
            shutil.copy2(source / name, project / name)
        shutil.copytree(source / ".mvn", project / ".mvn")
        main = project / "src/main/java" / PACKAGE
        main.mkdir(parents=True)
        for name in ("FineCalculator.java", "MemberTier.java"):
            shutil.copy2(source / "src/main/java" / PACKAGE / name, main / name)
        manifest = {p.relative_to(project).as_posix(): digest(p) for p in project.rglob("*") if p.is_file()}
    client.save(destination / "inputs/manifest.json", manifest)
    return project


def source_text(project):
    return "\n".join(f"File {name}:\n" + (project / "src/main/java" / PACKAGE / name).read_text()
                     for name in ("FineCalculator.java", "MemberTier.java"))


def prompt(name, **values):
    text = (ROOT / "ai/prompts" / name).read_text()
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    if re.search(r"\{\{[A-Z_]+\}\}", text):
        raise ValueError("Unfilled prompt placeholder")
    return text


def java_answer(answer, class_name, destination):
    code = answer.get("test_source")
    analysis = answer.get("analysis")
    if not isinstance(code, str) or not isinstance(analysis, str):
        raise ValueError("Expected test_source and analysis strings; raw response retained")
    if (not re.search(r"\bpackage\s+vn\.edu\.seminar\.fine\s*;", code)
            or not re.search(r"\bclass\s+" + re.escape(class_name) + r"\b", code)
            or "```" in code or re.search(r"@(?:Disabled\w*|Ignore|Tag)\b", code)):
        raise ValueError("Wrong package/class, disabled/tagged tests or Markdown in Java response")
    directory = destination / "generated"
    directory.mkdir()
    path = directory / f"{class_name}.java"
    path.write_text(code)
    (destination / "analysis.md").write_text(analysis)
    return path


def summarize(project):
    suites = []
    for path in sorted((project / "target/surefire-reports").glob("TEST-*.xml")):
        element = ET.parse(path).getroot()
        suites.append({"name": element.get("name"), **{k: int(element.get(k, "0"))
                       for k in ("tests", "failures", "errors", "skipped")}})
    result = {"suites": suites, **{k: sum(s[k] for s in suites)
              for k in ("tests", "failures", "errors", "skipped")}}
    report = project / "target/site/jacoco/jacoco.xml"
    if report.exists():
        target = ET.parse(report).getroot().find(f".//class[@name='{TARGET}']")
        if target is not None:
            result["fine_coverage"] = {c.get("type"): {"covered": int(c.get("covered")),
                "missed": int(c.get("missed"))} for c in target.findall("counter")}
    return result


def run_java(source, tests, destination, csv=None):
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="seminar-ai-java-") as temporary:
        project = Path(temporary) / "case-study"
        shutil.copytree(source, project)
        test_directory = project / "src/test/java" / PACKAGE
        test_directory.mkdir(parents=True)
        for path in tests:
            shutil.copy2(path, test_directory / path.name)
        command = ["./mvnw", "-B", "-ntp", "-Dtest.pattern=**/*Test.java", "-Dtest.excludedTags="]
        if csv:
            resources = project / "src/test/resources"
            resources.mkdir(parents=True)
            shutil.copy2(csv, resources / "cases.csv")
        command += ["clean", "test", "jacoco:report"]
        environment = {k: v for k, v in os.environ.items() if k not in ("GEMINI_API_KEY", "AI_MODEL")}
        started = client.utc()
        print(f"JUnit/JaCoCo: {destination.name}", flush=True)
        try:
            process = subprocess.run(command, cwd=project, env=environment,
                                     capture_output=True, text=True, timeout=300)
            code, output = process.returncode, process.stdout + process.stderr
        except subprocess.TimeoutExpired as error:
            def text(value):
                return value.decode(errors="replace") if isinstance(value, bytes) else (value or "")
            code, output = 124, text(error.stdout) + text(error.stderr) + "\nMaven timeout (300s).\n"
        key, _ = client.settings()
        if key:
            output = output.replace(key, "<redacted>")
        output = output.replace(str(project), "<project>").replace(str(Path.home()), "<home>")
        (destination / "output.log").write_text(output)
        for relative in ("surefire-reports", "site/jacoco"):
            if (project / "target" / relative).exists():
                shutil.copytree(project / "target" / relative, destination / relative)
        result = {"command": [part.replace(str(project), "<project>") for part in command],
                  "started_at_utc": started, "finished_at_utc": client.utc(), "exit_code": code,
                  "test_sha256": {path.name: digest(path) for path in tests},
                  "quality_gate_executed": False, **summarize(project)}
        if csv:
            result["csv_sha256"] = digest(csv)
        expected = {"vn.edu.seminar.fine." + path.stem for path in tests}
        seen = {s["name"] for s in result["suites"] if s["tests"] > s["skipped"]}
        result["passed"] = (code == 0 and expected <= seen and result["tests"] > 0
                            and result["failures"] == result["errors"] == 0 and "fine_coverage" in result)
        report = project / "target/site/jacoco/jacoco.xml"
        if report.exists():
            gaps = coverage_gaps.extract(report, project / "src/main/java")
            gaps["report"] = "site/jacoco/jacoco.xml"
            gaps["gaps"] = [g for g in gaps["gaps"] if g["file"] == str(PACKAGE / "FineCalculator.java")]
            client.save(destination / "gaps.json", gaps)
        client.save(destination / "run.json", result)
        print(f"Tests={result['tests']}, failures={result['failures']}, errors={result['errors']}; passed={result['passed']}", flush=True)
        return result


def ai1(destination, model=None, prepare=False):
    fresh(destination, "AI-1")
    try:
        project = snapshot(destination)
        text = prompt("AI-1-generate-tests.md", SPEC=SPEC, SOURCE=source_text(project), CLASS_NAME=DRAFT)
        (destination / "prompt.md").write_text(text)
        if prepare:
            return finish(destination, status="prepared_only", api_called=False)
        print("AI-1: generating a fresh Gemini draft...", flush=True)
        answer = client.generate(text, destination / "model", model)
        test = java_answer(answer, DRAFT, destination)
        result = run_java(project, [test], destination)
        return finish(destination, completed=result["passed"], status="tested", new_model_generation=True)
    except Exception as error:
        finish(destination, status="failed", error_type=type(error).__name__)
        raise


def ai2(destination, previous, model=None, prepare=False):
    before = json.loads((previous / "run.json").read_text())
    if not before.get("passed") or not json.loads((previous / "model/api.json").read_text()).get("completed"):
        raise ValueError("AI-2 needs a successful AI-1 model response and JUnit/JaCoCo run")
    draft = previous / "generated" / f"{DRAFT}.java"
    if before.get("test_sha256", {}).get(draft.name) != digest(draft):
        raise ValueError("AI-1 draft changed after measurement; rerun AI-1 rather than compare stale coverage")
    fresh(destination, "AI-2")
    try:
        project = snapshot(destination, previous)
        text = prompt("AI-2-coverage.md", SPEC=SPEC, SOURCE=source_text(project), CLASS_NAME=ADDITIONAL,
                      DRAFT_TEST=draft.read_text(), TEST_RESULT=json.dumps(before, ensure_ascii=False),
                      GAPS_JSON=(previous / "gaps.json").read_text())
        (destination / "prompt.md").write_text(text)
        if prepare:
            return finish(destination, status="prepared_only", api_called=False)
        print("AI-2: sending the measured draft and coverage gaps to Gemini...", flush=True)
        answer = client.generate(text, destination / "model", model)
        additional = java_answer(answer, ADDITIONAL, destination)
        shutil.copy2(draft, additional.parent / draft.name)
        after = run_java(project, [additional.parent / draft.name, additional], destination)
        comparison = {"before": before, "after": after,
                      "limitation": "Coverage/green tests do not prove assertions or business rules are correct."}
        if "fine_coverage" in after:
            comparison["branch_covered_delta"] = (after["fine_coverage"]["BRANCH"]["covered"]
                                                   - before["fine_coverage"]["BRANCH"]["covered"])
        client.save(destination / "comparison.json", comparison)
        return finish(destination, completed=after["passed"], status="tested", new_model_generation=True,
                      baseline=str(previous.relative_to(ROOT)) if previous.is_relative_to(ROOT) else previous.name)
    except Exception as error:
        finish(destination, status="failed", error_type=type(error).__name__)
        raise


def check_human():
    frozen = ROOT / "ai/human/frozen"
    receipt = json.loads((frozen / "receipt.json").read_text())
    if digest(frozen / "cases.csv") != receipt["sha256"]:
        raise ValueError("Frozen human CSV changed; refusing the comparison")
    ai4_compare.read_cases((frozen / "cases.csv").read_bytes())
    return frozen, receipt


def ai4(destination, model=None, prepare=False):
    frozen, receipt = check_human()  # Validate before paying for a request.
    fresh(destination, "AI-4")
    try:
        project = snapshot(destination)
        text = prompt("AI-4-boundary-data.md", SPEC=SPEC)
        (destination / "prompt.md").write_text(text)
        if prepare:
            return finish(destination, status="prepared_only", api_called=False,
                          human_sent_to_model=False, human_sha256=receipt["sha256"])
        print("AI-4: generating new data from specification only (no human CSV sent)...", flush=True)
        answer = client.generate(text, destination / "model", model)
        if not isinstance(answer.get("csv"), str) or not isinstance(answer.get("analysis"), str):
            raise ValueError("AI-4 response needs csv and analysis strings")
        generated = destination / "generated"
        generated.mkdir()
        csv = generated / "cases.csv"
        csv.write_text(answer["csv"])
        (destination / "analysis.md").write_text(answer["analysis"])
        ai4_compare.read_cases(csv.read_bytes(), ai=True)
        if not csv.read_text().splitlines()[0] == ",".join(ai4_compare.FIELDS):
            raise ValueError("New AI-4 CSV must include expectedException, even for valid cases")
        _, current_receipt = check_human()
        if current_receipt["sha256"] != receipt["sha256"]:
            raise ValueError("Human data changed during generation; comparison stopped")
        comparison = ai4_compare.compare(frozen, csv)
        client.save(destination / "comparison.json", comparison)
        human = destination / "inputs/human"
        shutil.copytree(frozen, human)
        harness = destination / "generated/FineCalculatorCsvTest.java"
        shutil.copy2(ROOT / "ai/harness/FineCalculatorCsvTest.java", harness)
        before = run_java(project, [harness], destination / "human", human / "cases.csv")
        after = run_java(project, [harness], destination / "ai", csv)
        client.save(destination / "execution-comparison.json", {"human": before, "ai": after,
                    "human_independence": "Self-declared in supplied notes, not proven by hash",
                    "agreement_is_not_model_accuracy": True})
        return finish(destination, completed=before["passed"] and after["passed"], status="compared_and_tested",
                      new_model_generation=True, human_sent_to_model=False, human_sha256=receipt["sha256"])
    except Exception as error:
        finish(destination, status="failed", error_type=type(error).__name__)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("ai1", "ai2", "ai4", "all"))
    parser.add_argument("--from-ai1", type=Path, help="AI-1 result directory, required for standalone ai2")
    parser.add_argument("--output", type=Path, help="New result directory; existing runs are never overwritten")
    parser.add_argument("--model", help="Override the saved Gemini model")
    parser.add_argument("--prepare-only", action="store_true", help="Save inputs/prompts, no API or Maven execution")
    args = parser.parse_args()
    if args.stage == "ai2" and not args.from_ai1:
        parser.error("ai2 requires --from-ai1 pointing to a successful AI-1 directory")
    try:
        if not args.prepare_only:
            client.configured(args.model)
        stamp = client.utc().replace(":", "").replace(".", "").replace("+0000", "Z")
        output = (args.output or ROOT / "evidence/tuan-06/gemini-live" / f"{stamp}-{args.stage}").resolve()
        print(f"Output: {output}", flush=True)
        if args.stage == "ai1":
            result = ai1(output, args.model, args.prepare_only)
        elif args.stage == "ai2":
            result = ai2(output, args.from_ai1.resolve(), args.model, args.prepare_only)
        elif args.stage == "ai4":
            result = ai4(output, args.model, args.prepare_only)
        else:
            output.mkdir(parents=True, exist_ok=False)
            results = {}
            # AI-4 remains independent of the AI-1/2 conversation and can run even if tests fail.
            for stage in ("ai1", "ai2", "ai4"):
                if stage == "ai2" and (args.prepare_only or not results.get("ai1", {}).get("completed")):
                    results[stage] = {"completed": False, "status": "skipped_without_passing_baseline"}
                    continue
                try:
                    if stage == "ai2":
                        results[stage] = ai2(output / stage, output / "ai1", args.model)
                    else:
                        results[stage] = globals()[stage](output / stage, args.model, args.prepare_only)
                except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as error:
                    results[stage] = {"completed": False, "error_type": type(error).__name__}
                    print(f"{stage} stopped: {error}", file=sys.stderr)
                client.save(output / "summary.json", results)
            result = {"completed": all(item.get("completed") for item in results.values())}
        return 0 if args.prepare_only or result["completed"] else 1
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError, KeyError) as error:
        print(f"Stopped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
