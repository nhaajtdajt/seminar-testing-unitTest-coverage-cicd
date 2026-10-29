"""Offline contract tests: failure paths must still produce truthful PR comments."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ci_ai_review as ci


class CiAiReviewTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.event = {"repository": {"full_name": "team/seminar"}, "pull_request": {
            "number": 12, "base": {"sha": "a" * 40},
            "head": {"sha": "b" * 40, "repo": {"full_name": "team/seminar"}}}}
        self.context = ci.pull_context(self.event)
        self.context["changed_files"] = ["case-study/src/main/java/demo/Service.java"]
        self.finding = {"rule": "NO_ASSERTION", "file": self.context["changed_files"][0],
                        "line": 7, "message": "Add an assertion"}
        self.statuses = {"test": "success", "coverage-gate": "success", "package": "success"}
        self.current_pr = {"head": {"sha": self.context["head"]}, "state": "open"}

    def artifact(self, status="reviewed", findings=None):
        destination = self.directory / "ai-review"
        ci.client.save(destination / "context.json", self.context)
        ci.client.save(destination / "result.json", {
            "status": status, "api_completed": status == "reviewed", "model": "test-model"})
        if status == "reviewed":
            ci.client.save(destination / "review.json", {"findings": findings or []})

    def body(self):
        return ci.comment_body(self.context, self.directory, self.statuses, "https://example.test/run")

    def test_fork_is_rejected_before_any_api_call(self):
        self.event["pull_request"]["head"]["repo"]["full_name"] = "outsider/seminar"
        with patch.object(ci.client, "generate") as api:
            with self.assertRaises(ValueError):
                ci.review(self.event, self.directory)
            api.assert_not_called()

    def test_no_application_change_does_not_call_gemini(self):
        with patch.object(ci, "read_diff", return_value=("", [])), patch.object(ci.client, "generate") as api:
            self.assertEqual(ci.review(self.event, self.directory), 0)
            api.assert_not_called()
        self.assertEqual(json.loads((self.directory / "result.json").read_text())["status"], "no_app_changes")

    def test_missing_secret_is_not_a_successful_ai_review(self):
        with patch.object(ci, "read_diff", return_value=("diff", self.context["changed_files"])), \
                patch.dict("os.environ", {}, clear=True), patch.object(ci.client, "generate") as api:
            self.assertEqual(ci.review(self.event, self.directory), 0)
            api.assert_not_called()
        self.assertFalse(json.loads((self.directory / "result.json").read_text())["api_completed"])

    def test_live_response_is_validated_and_saved_without_source_payloads(self):
        def generated(prompt, destination):
            self.assertIn("Their results are not available yet", prompt)
            ci.client.save(destination / "api.json", {"model": "test-model", "attempts": 1})
            return {"findings": [self.finding]}
        with patch.object(ci, "read_diff", return_value=("diff", self.context["changed_files"])), \
                patch.dict("os.environ", {"GEMINI_API_KEY": "fake", "AI_MODEL": "test-model"}), \
                patch.object(ci.client, "generate", side_effect=generated):
            self.assertEqual(ci.review(self.event, self.directory), 0)
        self.assertTrue(json.loads((self.directory / "result.json").read_text())["api_completed"])
        self.assertFalse((self.directory / "model/prompt.md").exists())

    def test_api_failure_still_leaves_status_for_final_comment(self):
        with patch.object(ci, "read_diff", return_value=("diff", self.context["changed_files"])), \
                patch.dict("os.environ", {"GEMINI_API_KEY": "fake", "AI_MODEL": "test-model"}), \
                patch.object(ci.client, "generate", side_effect=RuntimeError("HTTP 503")):
            self.assertEqual(ci.review(self.event, self.directory / "ai-review"), 1)
        self.assertIn("Chưa có review Gemini hoàn chỉnh", self.body())

    def test_findings_outside_reviewed_files_are_rejected(self):
        finding = dict(self.finding, file="README.md")
        with patch.object(ci, "read_diff", return_value=("diff", self.context["changed_files"])), \
                patch.dict("os.environ", {"GEMINI_API_KEY": "fake", "AI_MODEL": "test-model"}), \
                patch.object(ci.client, "generate", return_value={"findings": [finding]}):
            self.assertEqual(ci.review(self.event, self.directory), 1)
        self.assertFalse((self.directory / "review.json").exists())

    def test_failed_gate_includes_measured_coverage_and_findings(self):
        self.artifact(findings=[self.finding])
        self.statuses.update({"coverage-gate": "failure", "package": "skipped"})
        reports = self.directory / "tests-jdk-25"
        reports.mkdir()
        (reports / "TEST-demo.xml").write_text('<testsuite tests="4" failures="0" errors="0" skipped="1"/>')
        coverage = self.directory / "coverage"
        coverage.mkdir()
        counters = '<counter type="LINE" covered="8" missed="2"/><counter type="BRANCH" covered="2" missed="2"/>'
        (coverage / "jacoco.xml").write_text('<report><package name="demo"><class name="demo/Service">'
            + counters + '</class></package>' + counters + '</report>')
        body = self.body()
        self.assertIn("| coverage-gate | failure |", body)
        self.assertIn("Coverage job đỏ", body)
        self.assertIn("JUnit: 4 tests", body)
        self.assertIn("2/4 (50.0%)", body)
        self.assertIn("NO\\_ASSERTION", body)
        self.assertIn("demo/Service", body)

    def test_failed_tests_and_skipped_coverage_are_not_reported_as_pass(self):
        self.artifact()
        self.statuses.update({"test": "failure", "coverage-gate": "skipped", "package": "skipped"})
        body = self.body()
        self.assertIn("| test | failure |", body)
        self.assertIn("Coverage gate bị bỏ qua", body)
        self.assertIn("không tự suy ra coverage đạt", body)

    def test_missing_ai_artifact_does_not_block_ci_summary(self):
        self.assertIn("| test | success |", self.body())
        self.assertIn("Chưa có review Gemini hoàn chỉnh", self.body())

    def test_mismatched_artifact_is_rejected(self):
        self.artifact()
        self.context["head"] = "c" * 40
        with self.assertRaises(ValueError):
            self.body()

    def test_sanitizes_model_mentions_and_markup(self):
        self.artifact(findings=[dict(self.finding, message="@someone <img src=x>\n## [click](bad)")])
        body = self.body()
        self.assertNotIn("@someone", body)
        self.assertNotIn("<img", body)
        self.assertNotIn("\n## [click]", body)

    def test_corrupt_xml_keeps_ci_statuses_visible(self):
        reports = self.directory / "tests-jdk-25"
        reports.mkdir()
        (reports / "TEST-broken.xml").write_text("<unclosed")
        self.assertIn("| test | success |", self.body())
        self.assertIn("Không đọc được report", self.body())

    def test_updates_existing_bot_comment_but_not_human_marker(self):
        comments = [{"id": 1, "user": {"login": "person"}, "body": ci.MARKER},
                    {"id": 2, "user": {"login": "github-actions[bot]"}, "body": ci.MARKER}]
        with patch.object(ci, "github", side_effect=[self.current_pr, comments, self.current_pr, {}]) as api:
            self.assertEqual(ci.publish(self.context, "body"), "posted")
            self.assertEqual(api.call_args.args[:2], ("PATCH", "/repos/team/seminar/issues/comments/2"))

    def test_human_comment_cannot_be_overwritten(self):
        comments = [{"id": 1, "user": {"login": "person"}, "body": ci.MARKER}]
        with patch.object(ci, "github", side_effect=[self.current_pr, comments, self.current_pr, {}]) as api:
            ci.publish(self.context, "body")
            self.assertEqual(api.call_args.args[0], "POST")

    def test_stale_commit_does_not_post(self):
        changed = copy.deepcopy(self.current_pr)
        changed["head"]["sha"] = "c" * 40
        with patch.object(ci, "github", return_value=changed) as api:
            self.assertEqual(ci.publish(self.context, "body"), "stale")
            self.assertEqual(api.call_count, 1)

    def test_close_or_push_during_comment_lookup_does_not_post(self):
        closed = dict(self.current_pr, state="closed")
        with patch.object(ci, "github", side_effect=[self.current_pr, [], closed]) as api:
            self.assertEqual(ci.publish(self.context, "body"), "stale")
            self.assertEqual(api.call_count, 3)


if __name__ == "__main__":
    unittest.main()
