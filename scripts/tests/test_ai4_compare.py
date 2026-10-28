import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("ai4", Path(__file__).resolve().parents[1]/"ai4_compare.py")
ai4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai4)


class IndependentOracleTest(unittest.TestCase):
    # Synthetic fixtures exercise tooling only; never report these as human data.
    def test_empty_and_duplicate_oracles_are_rejected(self):
        with self.assertRaises(ValueError):
            ai4.read_cases(b"daysLate,tier,expected,expectedException\n")
        with self.assertRaises(ValueError):
            ai4.read_cases(b"daysLate,tier,expected,expectedException\n1,NORMAL,2000,\n1,NORMAL,2000,\n")

    def test_freeze_detects_tampering_and_comparison_keeps_disagreement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root/"human.csv"
            source.write_text("daysLate,tier,expected,expectedException\n1,NORMAL,2001,\n-1,VIP,,IllegalArgumentException\n")
            ai = root/"ai.csv"
            ai.write_text("daysLate,tier,expected\n1,NORMAL,2000\n2,VIP,0\n")
            frozen = root/"frozen"
            ai4.freeze(source, frozen, "Synthetic fixture")
            result = ai4.compare(frozen, ai)
            self.assertEqual(result["matching_outcomes"], 0)
            self.assertEqual(len(result["disagreements"]), 1)
            self.assertEqual(len(result["missing_from_ai"]), 1)
            self.assertEqual(len(result["extra_in_ai"]), 1)
            with self.assertRaises(FileExistsError):
                ai4.freeze(source, frozen, "Synthetic fixture")
            (frozen/"cases.csv").write_text("changed")
            with self.assertRaisesRegex(ValueError, "changed"):
                ai4.compare(frozen, ai)
