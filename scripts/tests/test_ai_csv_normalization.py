"""Expected-type aliases must not hide real business or cross-package differences."""
from copy import deepcopy
from pathlib import Path
import sys
import tempfile
import unittest
import subprocess

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ai_csv


class ExpectedTypeNormalizationTests(unittest.TestCase):
    def test_offline_report_cli_starts_without_api_configuration(self):
        command = [sys.executable, str(Path(__file__).resolve().parents[1] / "reconcile_ai4.py"), "--help"]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--comparison-schema", result.stdout)

    def setUp(self):
        self.schema = {"columns": [
            {"name": "scenario", "type": "string", "role": "input"},
            {"name": "resultType", "type": "string", "role": "expected", "normalization": {
                "kind": "java_type", "aliases": {"Problem": "example.Problem"}}}]}

    def compare(self, left, right, schema=None):
        with tempfile.TemporaryDirectory() as temporary:
            a, b = Path(temporary) / "human.csv", Path(temporary) / "ai.csv"
            a.write_text("scenario,resultType\ncase," + left + "\n")
            b.write_text("scenario,resultType\ncase," + right + "\n")
            original = (a.read_bytes(), b.read_bytes())
            result = ai_csv.compare(a, b, schema or self.schema)
            self.assertEqual(original, (a.read_bytes(), b.read_bytes()))
            return result

    def test_alias_matches_with_representation_difference_retained(self):
        result = self.compare("Problem", "example.Problem")
        self.assertEqual(result["matching_outcomes"], 1)
        self.assertFalse(result["disagreements"])
        self.assertEqual(len(result["representation_differences"]), 1)

    def test_same_simple_name_from_different_packages_stays_a_disagreement(self):
        result = self.compare("example.Problem", "other.Problem")
        self.assertEqual(result["matching_outcomes"], 0)
        self.assertEqual(len(result["disagreements"]), 1)

    def test_ordinary_strings_are_never_implicitly_normalized(self):
        schema = deepcopy(self.schema)
        schema["columns"][1].pop("normalization")
        result = self.compare("Problem", "example.Problem", schema)
        self.assertEqual(len(result["disagreements"]), 1)

    def test_arbitrary_renaming_and_qualified_package_alias_are_rejected(self):
        for aliases in ({"Different": "example.Problem"}, {"other.Problem": "example.Problem"}):
            schema = deepcopy(self.schema)
            schema["columns"][1]["normalization"]["aliases"] = aliases
            with self.subTest(aliases=aliases), self.assertRaises(ValueError):
                ai_csv.validate_schema(schema)

    def test_input_identity_cannot_be_changed_by_expected_normalization(self):
        schema = deepcopy(self.schema)
        schema["columns"][0]["normalization"] = schema["columns"][1]["normalization"]
        with self.assertRaises(ValueError):
            ai_csv.validate_schema(schema)


if __name__ == "__main__":
    unittest.main()
