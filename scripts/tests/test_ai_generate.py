"""Synthetic offline checks only: model/network and Maven are mocked."""
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ai_generate as demo
import ai_context as context
import ai_csv
import gemini_client as client


def java(target, name, csv=False):
    annotations = '@ParameterizedTest @CsvFileSource(resources="/cases.csv")' if csv else ""
    return f"package {target['package']}; class {name} {{ {annotations} void example() {{}} }}"


def model_response(value, finish="STOP"):
    return io.BytesIO(json.dumps({"candidates": [{"finishReason": finish,
                     "content": {"parts": [{"text": json.dumps(value)}]}}]}).encode())


def fake_maven(command, cwd, **kwargs):
    project = Path(cwd)
    report = project / "target/surefire-reports"
    report.mkdir(parents=True)
    nodes = []
    for path in (project / "src/test/java").rglob("*.java"):
        package = demo.re.search(r"package\s+([\w.]+);", path.read_text()).group(1)
        data = project / "src/test/resources/cases.csv"
        count = len(data.read_text().splitlines()) - 1 if data.exists() else 1
        (report / f"TEST-{path.stem}.xml").write_text(
            f'<testsuite name="{package}.{path.stem}" tests="{count}" failures="0" errors="0" skipped="0"/>')
        name = path.stem.split("Gemini")[0]
        nodes.append(f'<package name="{package.replace(".", "/")}"><class name="{package.replace(".", "/")}/{name}">'
                     '<counter type="BRANCH" covered="2" missed="0"/></class>'
                     f'<sourcefile name="{name}.java"/></package>')
    xml = project / "target/site/jacoco/jacoco.xml"
    xml.parent.mkdir(parents=True)
    # Multiple suites may measure the same target; retain one class counter.
    xml.write_text('<report>' + ''.join(dict.fromkeys(nodes)) + '</report>')
    return subprocess.CompletedProcess(command, 0, "synthetic Maven fixture", "")


def fixture_schema():
    return {"columns": [
        {"name": "daysLate", "type": "integer", "role": "input"},
        {"name": "tier", "type": "string", "role": "input", "nullable": True, "null_tokens": ["NULL"]},
        {"name": "expected", "type": "decimal", "role": "expected", "nullable": True, "null_tokens": [""]},
        {"name": "expectedException", "type": "string", "role": "expected", "nullable": True, "null_tokens": [""]}]}


class GenerationWorkflowTests(unittest.TestCase):
    def test_config_quotes_and_environment_override(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = Path(temporary) / ".env.gemini"
            config.write_text('GEMINI_API_KEY="local-dummy-key"\nAI_MODEL=\'local-model\'\n')
            with patch.object(client, "CONFIG", config), patch.dict(client.os.environ, {}, clear=True):
                self.assertEqual(client.settings(), ("local-dummy-key", "local-model"))
                with patch.dict(client.os.environ, {"GEMINI_API_KEY": "env-dummy-key"}):
                    self.assertEqual(client.settings()[0], "env-dummy-key")

    def test_incomplete_response_is_retained_not_accepted(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            with patch.object(client, "configured", return_value=("dummy-key", "test-model")), \
                    patch.object(client.urllib.request, "urlopen", return_value=model_response({}, "MAX_TOKENS")):
                with self.assertRaises(ValueError):
                    client.generate("prompt", output)
            self.assertFalse(json.loads((output / "api.json").read_text())["completed"])
            self.assertTrue((output / "response.json").exists())
            self.assertNotIn("dummy-key", (output / "request.json").read_text())

    def test_http_503_retries_and_preserves_attempt_count(self):
        error = client.urllib.error.HTTPError("https://example.invalid", 503, "Unavailable", {}, io.BytesIO(b""))
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            with patch.object(client, "configured", return_value=("dummy-key", "test-model")), \
                    patch.object(client.urllib.request, "urlopen", side_effect=[error, model_response({"ok": True})]), \
                    patch.object(client.time, "sleep"):
                self.assertEqual(client.generate("prompt", output), {"ok": True})
            self.assertEqual(json.loads((output / "api.json").read_text())["attempts"], 2)
        error.close()

    def test_new_class_discovered_without_registry_or_business_prompt(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "case-study"
            source = project / "src/main/java/newfeature/DiscountService.java"
            source.parent.mkdir(parents=True)
            source.write_text('package newfeature; // class FalseName {}\npublic class DiscountService { '
                              'String s="class FalseLiteral {}"; class Nested {} int apply(int n) { return n * 17; }}')
            discovered = context.discover(project)
            self.assertEqual([d["fqcn"] for d in discovered], ["newfeature.DiscountService"])
            with patch.object(context, "discover", return_value=discovered):
                self.assertEqual(context.select("DiscountService")["package"], "newfeature")

    def test_prepare_for_services_controller_and_policy_uses_source_not_old_tests(self):
        with tempfile.TemporaryDirectory() as temporary:
            with patch.object(client, "generate") as api, patch.object(demo, "run_java") as execute:
                for name in ("LoanService", "LoanController", "LoanPeriodPolicy"):
                    output = Path(temporary) / name
                    target = context.select(name)
                    result = demo.ai1(output, target, prepare=True)
                    text = (output / "prompt.md").read_text()
                    self.assertIn(target["fqcn"], text)
                    self.assertIn(target["name"] + "GeminiDraftTest", text)
                    self.assertNotIn("LoanServiceAiDraftTest", text)
                    self.assertNotIn("File src/main/java/vn/edu/seminar/fine/FineCalculator.java", text)
                    self.assertFalse((output / "inputs/project/src/test").exists())
                    self.assertFalse((output / "inputs/project/.env.gemini").exists())
                    self.assertFalse(result["api_called"])
            api.assert_not_called()
            execute.assert_not_called()

    def test_ambiguous_simple_name_is_rejected(self):
        with patch.object(context, "discover", return_value=[{"name": "Service", "fqcn": "a.Service", "source": "a"},
                                                           {"name": "Service", "fqcn": "b.Service", "source": "b"}]):
            with self.assertRaises(ValueError):
                context.select("Service")

    def test_local_dependency_closure_includes_imported_enum_and_repository_types(self):
        project = demo.ROOT / "case-study"
        service = context.related_sources(project, context.select("LoanService"))
        self.assertTrue(any(p.endswith("BookRepository.java") for p in service))
        self.assertTrue(any(p.endswith("LoanException.java") for p in service))
        self.assertFalse(any(p.endswith("FineCalculator.java") for p in service))
        policy = context.related_sources(project, context.select("LoanPeriodPolicy"))
        self.assertTrue(any(p.endswith("MemberTier.java") for p in policy))

    def test_generated_java_cannot_redirect_package_or_disable_tests(self):
        target = context.select("LoanService")
        with tempfile.TemporaryDirectory() as temporary:
            for code in [java(target, "WrongTest"), java(target, "ChosenTest").replace("class", "@Disabled class"),
                         java(target, "ChosenTest").replace(target["package"], "other")]:
                with self.subTest(code=code), self.assertRaises(ValueError):
                    demo.java_answer({"test_source": code, "analysis": "fixture"}, "ChosenTest", Path(temporary), target)

    def test_ai2_retains_target_snapshot_and_draft_with_zero_coverage_delta(self):
        target = context.select("LoanService")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prompts = []
            def generated(text, output, model):
                prompts.append(text)
                client.save(output / "api.json", {"completed": True, "provider": "synthetic fixture"})
                name = target["name"] + ("GeminiDraftTest" if len(prompts) == 1 else "GeminiAdditionalTest")
                return {"analysis": "synthetic fixture", "test_source": java(target, name)}
            with patch.object(client, "generate", side_effect=generated), patch.object(demo.subprocess, "run", side_effect=fake_maven):
                self.assertTrue(demo.ai1(root / "ai1", target)["completed"])
                self.assertTrue(demo.ai2(root / "ai2", root / "ai1")["completed"])
            comparison = json.loads((root / "ai2/comparison.json").read_text())
            self.assertEqual(comparison["target_class"], target["fqcn"])
            self.assertEqual(comparison["branch_covered_delta"], 0)
            name = target["name"] + "GeminiDraftTest.java"
            self.assertEqual((root / "ai1/generated" / name).read_bytes(), (root / "ai2/generated" / name).read_bytes())
            self.assertIn("countActiveByMemberId", prompts[1])

    def test_schema_and_data_do_not_send_human_rows_and_reports_are_reconciled(self):
        target = context.select("FineCalculator")
        human = demo.ROOT / "ai/human/frozen"
        original = (human / "cases.csv").read_bytes()
        prompts = []
        data = "daysLate,tier,expected,expectedException\n1,NORMAL,2000,\n-1,VIP,,IllegalArgumentException\n"
        def generated(text, output, model):
            prompts.append(text)
            self.assertNotIn(original.decode(), text)
            if len(prompts) == 1:
                return {**fixture_schema(), "analysis": "synthetic fixture", "test_source": java(target, "FineCalculatorGeminiCsvTest", True)}
            return {"analysis": "synthetic fixture", "csv": data}
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "ai4"
            with patch.object(client, "generate", side_effect=generated), patch.object(demo.subprocess, "run", side_effect=fake_maven):
                result = demo.ai4(output, target, human)
            self.assertTrue(result["completed"])
            reconciliation = json.loads((output / "reconciliation.json").read_text())
            self.assertTrue(reconciliation["consistent"])
            self.assertEqual(reconciliation["executions"]["human"]["tests"], 23)
            self.assertEqual(reconciliation["executions"]["ai"]["tests"], 2)
            self.assertIn("Đối chiếu CSV/Surefire/JaCoCo/hash: PASS", (output / "report.md").read_text())
            # Tampering with the summary must be caught by the final raw-report reconciliation.
            run_path = output / "ai/run.json"
            run = json.loads(run_path.read_text())
            run["tests"] = 999
            client.save(run_path, run)
            schema = json.loads((output / "schema.json").read_text())
            comparison = json.loads((output / "comparison.json").read_text())
            checked = ai_csv.reconcile(output, target["fqcn"], output / "inputs/human/cases.csv",
                output / "generated/cases.csv", schema, comparison, output / "generated/FineCalculatorGeminiCsvTest.java")
            self.assertFalse(checked["consistent"])
        self.assertEqual(original, (human / "cases.csv").read_bytes())

    def test_ai2_rejects_test_or_source_changed_after_baseline(self):
        target = context.select("LoanService")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            def generated(text, output, model):
                client.save(output / "api.json", {"completed": True})
                return {"analysis": "fixture", "test_source": java(target, target["name"] + "GeminiDraftTest")}
            with patch.object(client, "generate", side_effect=generated), patch.object(demo.subprocess, "run", side_effect=fake_maven):
                demo.ai1(root / "ai1", target)
            test = root / "ai1/generated/LoanServiceGeminiDraftTest.java"
            original = test.read_text()
            test.write_text(original + "// edited")
            with patch.object(client, "generate") as api, self.assertRaisesRegex(ValueError, "changed after measurement"):
                demo.ai2(root / "ai2-test-changed", root / "ai1")
            api.assert_not_called()
            test.write_text(original)
            source = root / "ai1/inputs/project" / target["source"]
            source.write_text(source.read_text() + "// edited")
            with patch.object(client, "generate") as api, self.assertRaisesRegex(ValueError, "snapshot changed"):
                demo.ai2(root / "ai2-source-changed", root / "ai1")
            api.assert_not_called()

    def test_arbitrary_schema_compares_decimal_values_without_domain_constants(self):
        schema = {"columns": [{"name": "customer", "type": "string", "role": "input"},
                              {"name": "balance", "type": "decimal", "role": "expected"}]}
        with tempfile.TemporaryDirectory() as temporary:
            human, ai = Path(temporary) / "human.csv", Path(temporary) / "ai.csv"
            human.write_text("customer,balance\nalice,12.00\n")
            ai.write_text("customer,balance\nalice,12\nbob,7\n")
            result = ai_csv.compare(human, ai, schema)
            self.assertEqual(result["matching_outcomes"], 1)
            self.assertEqual(len(result["extra_in_ai"]), 1)

    def test_schema_cannot_change_existing_header_or_omit_expected_fields(self):
        with self.assertRaises(ValueError):
            ai_csv.validate_schema(fixture_schema(), ["unrelated"])
        with self.assertRaises(ValueError):
            ai_csv.validate_schema({"columns": [{"name": "x", "type": "string", "role": "input"}]})

    def test_report_without_branches_shows_na_instead_of_dividing_by_zero(self):
        row = {"tests": 1, "failures": 0, "errors": 0, "skipped": 0, "coverage": {}}
        value = {"target_class": "sample.Record", "executions": {"human": row, "ai": row}, "checks": [],
                 "consistent": True, "comparison": {"human_cases": 1, "ai_cases": 1,
                   "matching_inputs": 1, "matching_outcomes": 1, "disagreements": [],
                   "missing_from_ai": [], "extra_in_ai": []}}
        self.assertIn("| BRANCH | N/A | N/A |", ai_csv.report(value))


if __name__ == "__main__":
    unittest.main()
