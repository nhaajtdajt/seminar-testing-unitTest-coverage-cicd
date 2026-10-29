"""Synthetic offline checks only: no Gemini request or Maven process is executed."""
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import ai_generate as demo
import gemini_client as client


def java(name):
    return f"package vn.edu.seminar.fine; class {name} {{}}"


def model_response(text, finish="STOP"):
    return io.BytesIO(json.dumps({"candidates": [{"finishReason": finish,
        "content": {"parts": [{"text": json.dumps(text)}]}}]}).encode())


def fake_maven(command, cwd, **kwargs):
    """Write fixture reports into the *temporary* project, without running Java."""
    project = Path(cwd)
    report = project / "target/surefire-reports"
    report.mkdir(parents=True)
    for path in (project / "src/test/java").rglob("*.java"):
        (report / f"TEST-{path.stem}.xml").write_text(
            f'<testsuite name="vn.edu.seminar.fine.{path.stem}" tests="1" failures="0" errors="0" skipped="0"/>')
    xml = project / "target/site/jacoco/jacoco.xml"
    xml.parent.mkdir(parents=True)
    xml.write_text('<report><package name="vn/edu/seminar/fine"><class name="vn/edu/seminar/fine/FineCalculator">'
                   '<counter type="BRANCH" covered="10" missed="0"/></class>'
                   '<sourcefile name="FineCalculator.java"><line nr="1" mi="0" ci="1" mb="0" cb="2"/></sourcefile>'
                   '</package></report>')
    return subprocess.CompletedProcess(command, 0, "synthetic Maven fixture", "")


class GenerationWorkflowTests(unittest.TestCase):
    def test_private_config_accepts_dotenv_quotes_and_env_override(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = Path(temporary) / ".env.gemini"
            config.write_text('GEMINI_API_KEY="local-dummy-key"\nAI_MODEL=\'local-model\'\n')
            with patch.object(client, "CONFIG", config), patch.dict(client.os.environ, {}, clear=True):
                self.assertEqual(client.settings(), ("local-dummy-key", "local-model"))
                with patch.dict(client.os.environ, {"GEMINI_API_KEY": "env-dummy-key", "AI_MODEL": "env-model"}):
                    self.assertEqual(client.settings(), ("env-dummy-key", "env-model"))

    def test_incomplete_response_retained_but_never_accepted(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            with patch.object(client, "configured", return_value=("dummy-key", "test-model")), \
                    patch.object(client.urllib.request, "urlopen", return_value=model_response({}, "MAX_TOKENS")):
                with self.assertRaises(ValueError):
                    client.generate("prompt", output)
            self.assertFalse(json.loads((output / "api.json").read_text())["completed"])
            self.assertTrue((output / "response.json").exists())
            self.assertNotIn("dummy-key", (output / "request.json").read_text())

    def test_http_503_retries_then_preserves_real_attempt_count(self):
        error = client.urllib.error.HTTPError("https://example.invalid", 503, "Unavailable", {}, io.BytesIO(b""))
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            with patch.object(client, "configured", return_value=("dummy-key", "test-model")), \
                    patch.object(client.urllib.request, "urlopen", side_effect=[error, model_response({"ok": True})]), \
                    patch.object(client.time, "sleep"):
                self.assertEqual(client.generate("prompt", output), {"ok": True})
            self.assertEqual(json.loads((output / "api.json").read_text())["attempts"], 2)
        error.close()

    def test_prepare_only_does_not_call_model_or_maven(self):
        with tempfile.TemporaryDirectory() as temporary:
            with patch.object(client, "generate") as api, patch.object(demo, "run_java") as java_run:
                result = demo.ai1(Path(temporary) / "ai1", prepare=True)
            api.assert_not_called()
            java_run.assert_not_called()
            self.assertFalse(result["api_called"])
            project = Path(temporary) / "ai1/inputs/project"
            self.assertFalse((project / "src/test").exists())
            self.assertFalse((project / ".env.gemini").exists())

    def test_ai4_prompt_never_contains_human_rows_or_old_ai_output(self):
        original = (demo.ROOT / "ai/human/frozen/cases.csv").read_bytes()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "ai4"
            with patch.object(client, "generate") as api, patch.object(demo, "run_java") as java_run:
                result = demo.ai4(output, prepare=True)
            api.assert_not_called()
            java_run.assert_not_called()
            self.assertFalse(result["human_sent_to_model"])
            self.assertNotIn(original.decode(), (output / "prompt.md").read_text())
        self.assertEqual(original, (demo.ROOT / "ai/human/frozen/cases.csv").read_bytes())

    def test_generated_paths_cannot_be_redirected_or_disabled(self):
        with tempfile.TemporaryDirectory() as temporary:
            for code in ["package other; class FineCalculatorGeminiDraftTest {}",
                         java(demo.DRAFT).replace("class", "@Disabled class"), "```java\n" + java(demo.DRAFT)]:
                with self.subTest(code=code), self.assertRaises(ValueError):
                    demo.java_answer({"test_source": code, "analysis": "fixture"}, demo.DRAFT, Path(temporary))

    def test_empty_generated_test_is_not_success_just_because_maven_exited_zero(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "result"
            output.mkdir()
            project = demo.snapshot(output)
            test = Path(temporary) / f"{demo.DRAFT}.java"
            test.write_text(java(demo.DRAFT))
            with patch.object(demo.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")):
                result = demo.run_java(project, [test], output)
            self.assertFalse(result["passed"])
            self.assertEqual(result["tests"], 0)

    def test_ai1_ai2_share_snapshot_keep_draft_and_allow_zero_coverage_delta(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prompts = []
            def generated(text, destination, model):
                prompts.append(text)
                client.save(destination / "api.json", {"completed": True, "provider": "synthetic fixture"})
                return {"analysis": "synthetic fixture", "test_source": java(demo.DRAFT if len(prompts) == 1 else demo.ADDITIONAL)}
            with patch.object(client, "generate", side_effect=generated), patch.object(demo.subprocess, "run", side_effect=fake_maven):
                self.assertTrue(demo.ai1(root / "ai1")["completed"])
                self.assertTrue(demo.ai2(root / "ai2", root / "ai1")["completed"])
            comparison = json.loads((root / "ai2/comparison.json").read_text())
            self.assertEqual(comparison["branch_covered_delta"], 0)
            self.assertIn(java(demo.DRAFT), prompts[1])
            self.assertEqual((root / "ai1/generated" / f"{demo.DRAFT}.java").read_bytes(),
                             (root / "ai2/generated" / f"{demo.DRAFT}.java").read_bytes())
            self.assertEqual(json.loads((root / "ai2/run.json").read_text())["tests"], 2)

    def test_ai2_rejects_draft_edited_after_coverage_measurement(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            baseline = root / "ai1"
            client.save(baseline / "run.json", {"passed": True, "test_sha256": {f"{demo.DRAFT}.java": "wrong-hash"}})
            client.save(baseline / "model/api.json", {"completed": True})
            path = baseline / "generated" / f"{demo.DRAFT}.java"
            path.parent.mkdir()
            path.write_text(java(demo.DRAFT))
            with patch.object(client, "generate") as api, self.assertRaisesRegex(ValueError, "changed after measurement"):
                demo.ai2(root / "ai2", baseline)
            api.assert_not_called()

    def test_ai4_compares_new_csv_and_executes_identical_harness_for_both(self):
        csv = "daysLate,tier,expected,expectedException\n1,NORMAL,2000,\n-1,VIP,,IllegalArgumentException\n"
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "ai4"
            with patch.object(client, "generate", return_value={"analysis": "synthetic fixture", "csv": csv}), \
                    patch.object(demo.subprocess, "run", side_effect=fake_maven):
                result = demo.ai4(output)
            self.assertTrue(result["completed"])
            self.assertFalse(result["human_sent_to_model"])
            comparison = json.loads((output / "comparison.json").read_text())
            self.assertEqual(comparison["human_cases"], 23)
            self.assertEqual(comparison["ai_cases"], 2)
            human = json.loads((output / "human/run.json").read_text())
            ai = json.loads((output / "ai/run.json").read_text())
            self.assertEqual(human["test_sha256"], ai["test_sha256"])
            self.assertNotEqual(human["csv_sha256"], ai["csv_sha256"])


if __name__ == "__main__":
    unittest.main()
