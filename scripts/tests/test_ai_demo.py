import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("ai_demo", Path(__file__).resolve().parents[1]/"run_ai_demo.py")
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)


class FrozenDataExecutionTest(unittest.TestCase):
    def test_tampered_oracle_is_rejected_before_maven_or_evidence_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            frozen = root/"ai/human/frozen"
            frozen.mkdir(parents=True)
            (frozen/"cases.csv").write_text("changed after freeze")
            (frozen/"receipt.json").write_text(json.dumps({"sha256": "original hash"}))
            output = root/"evidence"
            with patch.object(demo, "ROOT", root), \
                 patch("sys.argv", ["run_ai_demo.py", "human", "--output", str(output)]), \
                 patch.object(demo.subprocess, "run") as maven, patch("sys.stderr", io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    demo.main()
            self.assertEqual(error.exception.code, 2)
            maven.assert_not_called()
            self.assertFalse(output.exists())
