"""Cleanup is confined to disposable output and preserves real source and human CSV."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import clean_ai
import ai_context
import ai_generate
import gemini_client


class LocalAiWorkspaceTests(unittest.TestCase):
    def test_cleanup_preview_then_apply_preserves_csv_key_and_real_src(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = {
                '.ai-work/run/ai1/generated/NewTest.java': 'generated',
                '.ai-work/run/ai1/model/request.json': 'source payload',
                'evidence/tuan-06/gemini-live/old/inputs/project/pom.xml': 'pom',
                'evidence/tuan-06/gemini-live/old/inputs/project/mvnw': 'wrapper',
                'evidence/tuan-06/gemini-live/old/inputs/project/src/main/java/Original.java': 'copy',
                '.ai-work/run/ai4/generated/cases.csv': 'ai CSV',
                '.ai-work/run/ai4/inputs/human/cases.csv': 'human copy',
                'ai/human/frozen/cases.csv': 'human original',
                'case-study/src/main/java/Original.java': 'real source',
                '.env.gemini': 'private config',
                '.ai-work/run/ai4/report.md': 'local report',
            }
            for relative, content in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            with patch.object(clean_ai, 'ROOT', root):
                count = clean_ai.clean(clean_ai.allowed_roots())
                self.assertEqual(count, 5)
                self.assertTrue((root / '.ai-work/run/ai1/generated/NewTest.java').exists())
                clean_ai.clean(clean_ai.allowed_roots(), apply=True)
            for relative in ['.env.gemini', 'case-study/src/main/java/Original.java', 'ai/human/frozen/cases.csv',
                             '.ai-work/run/ai4/generated/cases.csv', '.ai-work/run/ai4/inputs/human/cases.csv',
                             '.ai-work/run/ai4/report.md']:
                self.assertEqual((root / relative).read_text(), files[relative])
            self.assertFalse((root / '.ai-work/run/ai1/generated/NewTest.java').exists())
            self.assertFalse((root / 'evidence/tuan-06/gemini-live/old/inputs/project').exists())

    def test_cleanup_rejects_real_src_and_symlink_escape(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(clean_ai, 'ROOT', root):
                with self.assertRaises(ValueError):
                    clean_ai.plan([root / 'case-study'])
                (root / '.ai-work').mkdir()
                (root / '.ai-work/escape').symlink_to(root / 'case-study', target_is_directory=True)
                with self.assertRaises(ValueError):
                    clean_ai.plan([root / '.ai-work'])

    def test_build_copy_is_temporary_and_excludes_tests_target_and_env(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'case-study'
            for relative in ['pom.xml', 'mvnw', '.mvn/wrapper/properties', 'src/main/java/NewService.java',
                             'src/test/java/ExistingTest.java', 'target/old.jar', '.env.gemini']:
                path = source / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('fixture')
            destination = root / 'temporary-build'
            ai_context.copy_project(source, destination, ai_context.manifest(source))
            self.assertTrue((destination / 'src/main/java/NewService.java').exists())
            for relative in ['src/test', 'target', '.env.gemini']:
                self.assertFalse((destination / relative).exists())

    def test_human_csv_can_be_frozen_before_any_model_schema_exists(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            csv = root / 'human.csv'
            csv.write_text('state,expected\nready,accepted\n')
            with patch.object(gemini_client, 'generate') as api:
                ai_generate.freeze_data(root / 'frozen', None, csv, 'Synthetic fixture', {'fqcn': 'sample.NewService'})
            api.assert_not_called()
            self.assertEqual(csv.read_bytes(), (root / 'frozen/cases.csv').read_bytes())


if __name__ == '__main__':
    unittest.main()
