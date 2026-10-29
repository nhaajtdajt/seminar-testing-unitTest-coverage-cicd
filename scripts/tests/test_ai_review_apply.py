"""Offline failure-path contracts; real Gemini/Maven/PR validation is performed separately."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ai_apply
import ai_candidates
import ai_context
import ai_generate
import gemini_client
from test_ai_generate import java, fake_maven

REAL_ROOT = ai_generate.ROOT


class CandidatePipelineTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        shutil.copytree(REAL_ROOT / 'case-study', self.root / 'case-study',
                        ignore=shutil.ignore_patterns('target'))
        shutil.copytree(REAL_ROOT / 'ai/data', self.root / 'ai/data')
        self.session = self.root / '.ai-work/demo'
        self.session.mkdir(parents=True)
        gemini_client.save(self.session / 'session.json', {'kind':'ai12', 'stages':['ai1','ai2']})
        for module in (ai_apply, ai_context):
            patcher = patch.object(module, 'ROOT', self.root)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.target = ai_context.select('FineCalculator')
        self.calls = 0

    def response(self, text, destination, model=None, **kwargs):
        self.calls += 1
        gemini_client.save(destination / 'api.json', {'completed':True, 'provider':'synthetic offline fixture'})
        name = self.target['name'] + ('GeminiDraftTest' if self.calls == 1 else 'GeminiAdditionalTest')
        return {'analysis':'Synthetic offline fixture, no real API', 'test_source':java(self.target, name)}

    def pipeline(self):
        with patch.object(gemini_client, 'generate', side_effect=self.response), \
                patch.object(ai_generate.subprocess, 'run', side_effect=fake_maven):
            self.assertTrue(ai_generate.ai1(self.session/'ai1', self.target)['completed'])
            self.assertTrue(ai_generate.ai2(self.session/'ai2', self.session/'ai1')['completed'])

    def test_compile_failure_repairs_once_preserving_assertions(self):
        calls, prompts = [], []
        def response(text, destination, model=None, **kwargs):
            prompts.append(text)
            gemini_client.save(destination / 'api.json', {'completed':True})
            return {'analysis':'fixture','test_source':java(self.target, self.target['name']+'GeminiDraftTest')}
        def maven(command, cwd, **kwargs):
            calls.append(command)
            if len(calls) == 1:
                import subprocess
                return subprocess.CompletedProcess(command, 1, '[ERROR] COMPILATION ERROR: cannot find symbol', '')
            return fake_maven(command, cwd, **kwargs)
        with patch.object(gemini_client, 'generate', side_effect=response), patch.object(ai_generate.subprocess, 'run', side_effect=maven):
            result = ai_generate.ai1(self.session/'ai1', self.target)
        self.assertTrue(result['completed'])
        self.assertEqual(len(prompts), 2)
        self.assertIn('COMPILATION ERROR', prompts[1])
        history=json.loads((self.session/'ai1/attempts.json').read_text())
        self.assertEqual([row['passed'] for row in history], [False,True])

    def test_assertion_failure_stops_without_repair(self):
        def failed(*args, **kwargs):
            output=Path(args[2])
            output.mkdir()
            (output/'output.log').write_text('AssertionFailedError: expected 10 but was 20')
            result={'target_class':self.target['fqcn'],'passed':False,'exit_code':1,
                    'tests':1,'failures':1,'errors':0,'skipped':0,'target_coverage':{}}
            gemini_client.save(output/'run.json',result)
            return result
        with patch.object(gemini_client, 'generate', side_effect=self.response) as api, \
                patch.object(ai_generate, 'run_java', side_effect=failed):
            result=ai_generate.ai1(self.session/'ai1',self.target)
        self.assertFalse(result['completed'])
        self.assertEqual(api.call_count,1)

    def test_repair_cannot_change_expected(self):
        calls=[]
        def response(text, destination, model=None, **kwargs):
            calls.append(text)
            gemini_client.save(destination/'api.json',{'completed':True})
            code=java(self.target,self.target['name']+'GeminiDraftTest')
            if len(calls)==2:
                code=code.replace('isEqualTo(1)','isEqualTo(2)')
            return {'analysis':'fixture','test_source':code}
        import subprocess
        with patch.object(gemini_client,'generate',side_effect=response), \
                patch.object(ai_generate.subprocess,'run',return_value=subprocess.CompletedProcess([],1,'COMPILATION ERROR','')) as maven:
            result=ai_generate.ai1(self.session/'ai1',self.target)
        self.assertFalse(result['completed'])
        self.assertEqual(len(calls),2)
        self.assertEqual(maven.call_count,1)
        self.assertEqual(json.loads((self.session/'ai1/run.json').read_text())['failure_kind'],'assertion_changed_needs_review')

    def test_repairs_are_bounded(self):
        def response(text, destination, model=None, **kwargs):
            gemini_client.save(destination/'api.json',{'completed':True})
            return {'analysis':'fixture','test_source':java(self.target,self.target['name']+'GeminiDraftTest')}
        import subprocess
        with patch.object(gemini_client,'generate',side_effect=response) as api, \
                patch.object(ai_generate.subprocess,'run',return_value=subprocess.CompletedProcess([],1,'COMPILATION ERROR','')):
            self.assertFalse(ai_generate.ai1(self.session/'ai1',self.target,max_repairs=2)['completed'])
        self.assertEqual(api.call_count,3)

    def test_ai2_can_decline_duplicate_additions_when_fully_covered(self):
        def response(text, destination, model=None, **kwargs):
            if self.calls:
                gemini_client.save(destination/'api.json',{'completed':True})
                return {'decision':'no_additions_needed','analysis':'fixture full coverage; no new scenario','test_source':''}
            return self.response(text,destination,model,**kwargs)
        with patch.object(gemini_client,'generate',side_effect=response), patch.object(ai_generate.subprocess,'run',side_effect=fake_maven):
            ai_generate.ai1(self.session/'ai1',self.target)
            result=ai_generate.ai2(self.session/'ai2',self.session/'ai1')
        self.assertTrue(result['completed'])
        self.assertEqual(result['assessment'],'no_additions_proposed_needs_review')
        self.assertEqual(len(ai_apply.plan(self.session/'ai2')['copies']),1)

    def test_preview_and_missing_review_do_not_write_or_delete(self):
        self.pipeline()
        with patch.object(ai_apply,'verify') as verify:
            ai_apply.apply(self.session/'ai2')
            with self.assertRaises(ValueError):
                ai_apply.apply(self.session/'ai2', execute=True)
            verify.assert_not_called()
        self.assertTrue(self.session.exists())
        self.assertFalse((self.root/'case-study/src/test/java/vn/edu/seminar/fine/FineCalculatorGeminiDraftTest.java').exists())

    def test_apply_syncs_only_new_files_then_deletes_whole_owned_session(self):
        self.pipeline()
        originals={p: p.read_bytes() for p in (self.root/'case-study/src').rglob('*') if p.is_file()}
        human=self.root/'ai/human/frozen/cases.csv'
        human.parent.mkdir(parents=True)
        human.write_text('original human CSV')
        with patch.object(ai_apply.subprocess,'run',side_effect=fake_maven):
            result=ai_apply.apply(self.session/'ai2',True,'Offline fixture reviewer',True)
        self.assertTrue(result['output_deleted'])
        self.assertFalse(self.session.exists())
        self.assertEqual(human.read_text(),'original human CSV')
        for path,content in originals.items():
            self.assertEqual(path.read_bytes(),content)
        self.assertEqual(len(result['files']),2)
        for name in result['files']:
            self.assertTrue((self.root/name).is_file())

    def test_existing_test_is_never_overwritten(self):
        self.pipeline()
        destination=ai_apply.plan(self.session/'ai2')['copies'][0][1]
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_text('existing user test')
        with patch.object(ai_apply,'verify') as verify, self.assertRaises(ValueError):
            ai_apply.apply(self.session/'ai2',True,'fixture',True)
        verify.assert_not_called()
        self.assertEqual(destination.read_text(),'existing user test')
        self.assertTrue(self.session.exists())

    def test_failed_full_suite_preserves_output_and_does_not_sync(self):
        self.pipeline()
        copies=ai_apply.plan(self.session/'ai2')['copies']
        with patch.object(ai_apply,'verify',return_value={'passed':False}), self.assertRaises(ValueError):
            ai_apply.apply(self.session/'ai2',True,'fixture',True)
        self.assertTrue(self.session.exists())
        self.assertTrue(all(not path.exists() for _,path in copies))
        self.assertFalse((self.root/'.ai-work/apply.lock').exists())

    def test_partial_write_failure_rolls_back_only_our_new_files(self):
        self.pipeline()
        copies=ai_apply.plan(self.session/'ai2')['copies']
        original_open=Path.open
        def opened(path, mode='r', *args, **kwargs):
            if path==copies[1][1] and mode=='xb':
                raise OSError('synthetic write failure on second candidate')
            return original_open(path,mode,*args,**kwargs)
        with patch.object(ai_apply,'verify',return_value={'passed':True}), \
                patch.object(Path,'open',autospec=True,side_effect=opened), self.assertRaises(OSError):
            ai_apply.apply(self.session/'ai2',True,'fixture',True)
        self.assertTrue(self.session.exists())
        self.assertTrue(all(not p.exists() for _,p in copies))

    def test_source_drift_after_generation_does_not_trigger_more_model_calls(self):
        def changed(text,destination,model=None,**kwargs):
            answer=self.response(text,destination,model,**kwargs)
            source=self.root/'case-study'/self.target['source']
            source.write_text(source.read_text()+'\n// source changed during API request\n')
            return answer
        with patch.object(gemini_client,'generate',side_effect=changed) as api, self.assertRaises(ValueError):
            ai_generate.ai1(self.session/'ai1',self.target)
        self.assertEqual(api.call_count,1)

    def test_test_changes_during_full_suite_abort_sync(self):
        self.pipeline()
        copies=ai_apply.plan(self.session/'ai2')['copies']
        def modified(data):
            old=next((self.root/'case-study/src/test').rglob('*.java'))
            old.write_text(old.read_text()+'\n// changed during verification\n')
            return {'passed':True}
        with patch.object(ai_apply,'verify',side_effect=modified), self.assertRaises(ValueError):
            ai_apply.apply(self.session/'ai2',True,'fixture',True)
        self.assertTrue(self.session.exists())
        self.assertTrue(all(not path.exists() for _,path in copies))

    def test_modified_candidate_or_report_is_rejected_before_integration(self):
        self.pipeline()
        candidate=next((self.session/'ai2/generated').glob('*.java'))
        original=candidate.read_text()
        candidate.write_text(original+'\n// edited after measurement\n')
        with self.assertRaises(ValueError):
            ai_apply.plan(self.session/'ai2')
        candidate.write_text(original)
        (self.session/'ai2/run.json').write_text('{}')
        with self.assertRaises(ValueError):
            ai_apply.plan(self.session/'ai2')

    def test_cleanup_preserves_ai4_sibling(self):
        self.pipeline()
        csv=self.session/'ai4/generated/cases.csv'
        csv.parent.mkdir(parents=True)
        csv.write_text('AI-4 output, not part of AI-1/2 cleanup')
        with patch.object(ai_apply.subprocess,'run',side_effect=fake_maven):
            ai_apply.apply(self.session/'ai2',True,'fixture',True)
        self.assertTrue(csv.is_file())
        self.assertFalse((self.session/'ai1').exists())
        self.assertFalse((self.session/'ai2').exists())

    def test_cleanup_rejects_repository_root_and_symlink(self):
        with self.assertRaises(ValueError):
            ai_apply.managed_directory(self.root)
        with self.assertRaises(ValueError):
            ai_apply.managed_directory(self.root/'.ai-work')
        linked=self.root/'.ai-work/linked'
        linked.symlink_to(self.root/'case-study',target_is_directory=True)
        with self.assertRaises(ValueError):
            ai_apply.managed_directory(linked/'anything')

    def test_comparison_distinguishes_gain_stagnation_and_regression(self):
        before={'passed':True,'target_coverage':{'BRANCH':{'covered':2,'missed':2}}}
        after=copy.deepcopy(before)
        self.assertEqual(ai_candidates.compare(before,after),'no_coverage_gain_needs_review')
        after['target_coverage']['BRANCH']={'covered':3,'missed':1}
        self.assertEqual(ai_candidates.compare(before,after),'coverage_increased')
        after['target_coverage']['BRANCH']={'covered':1,'missed':3}
        self.assertEqual(ai_candidates.compare(before,after),'coverage_regressed')


if __name__=='__main__':
    unittest.main()
