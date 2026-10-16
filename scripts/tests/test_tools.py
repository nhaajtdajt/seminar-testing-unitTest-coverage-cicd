import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import io

ROOT = Path(__file__).resolve().parents[2]

def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

coverage = module('coverage_gaps')
review = module('ai_review')
evaluate = module('evaluate_review')

class EvidenceToolsTest(unittest.TestCase):
    def test_line_with_only_missed_instructions_is_not_silently_lost(self):
        with tempfile.TemporaryDirectory() as temporary:
            xml = Path(temporary) / 'jacoco.xml'
            xml.write_text('<report><package name="demo"><sourcefile name="X.java"><line nr="2" mi="4" ci="0" mb="0" cb="0"/><line nr="3" mi="0" ci="3" mb="1" cb="1"/><line nr="4" mi="0" ci="3" mb="0" cb="2"/></sourcefile></package></report>')
            result = coverage.extract(xml)
            self.assertEqual([g['line'] for g in result['gaps']], [2, 3])
            self.assertEqual(result['gaps'][1]['missed_branches'], 1)

    def test_prepare_mode_never_calls_api_or_claims_it_did(self):
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary) / 'out'
            with patch('sys.argv', ['ai_review.py', '--diff', str(ROOT/'ai/fixtures/review.diff'), '--output', str(out)]), patch.object(review.urllib.request, 'urlopen') as api:
                self.assertEqual(review.main(), 0)
                api.assert_not_called()
            self.assertFalse(json.loads((out/'metadata.json').read_text())['api_called'])
            self.assertFalse((out/'review.json').exists())

    def test_blocked_or_truncated_api_response_cannot_be_saved_as_success(self):
        raw = json.dumps({'candidates': [{'finishReason': 'MAX_TOKENS', 'content': {'parts': [{'text': '{"findings":[]}'}]}}]}).encode()
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary) / 'out'
            with patch('sys.argv', ['ai_review.py', '--diff', str(ROOT/'ai/fixtures/review.diff'), '--output', str(out), '--live']), patch.dict('os.environ', {'GEMINI_API_KEY': 'dummy-unit-test-key', 'AI_MODEL': 'test-model'}), patch.object(review.urllib.request, 'urlopen', return_value=io.BytesIO(raw)):
                self.assertEqual(review.main(), 1)
            self.assertFalse((out/'review.json').exists())

    def test_bad_finding_shape_is_rejected(self):
        with self.assertRaises(ValueError):
            review.validate_review({'findings': [{'file':'X.java', 'line':0, 'rule':'OTHER', 'message':'x'}]})

    def test_duplicate_findings_do_not_inflate_true_positives(self):
        item = {'file':'A.java', 'line':10, 'rule':'NO_ASSERTION'}
        result = evaluate.evaluate({'findings':[item]}, {'findings':[item, item]})
        self.assertEqual(result['true_positive'], 1)
        self.assertEqual(result['false_positive'], 1)

if __name__ == '__main__':
    unittest.main()
