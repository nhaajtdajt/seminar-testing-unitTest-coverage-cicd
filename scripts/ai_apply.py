#!/usr/bin/env python3
"""Preview/apply reviewed AI-2 candidates, verify the full suite, then delete managed output."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import ai_candidates as candidates
import ai_context as context
import ai_csv
import gemini_client as client

ROOT = Path(__file__).resolve().parents[1]


def managed_directory(raw):
    raw = Path(raw).absolute()
    for part in (raw, *raw.parents):
        if part.is_symlink():
            raise ValueError('Managed output must not pass through symlinks')
        if part == ROOT.absolute():
            break
    path = raw.resolve()
    bases = [ROOT / '.ai-work', ROOT / 'evidence/tuan-06/gemini-live']
    if not any(path != base.resolve() and path.is_relative_to(base.resolve()) for base in bases):
        raise ValueError('Use an output subdirectory inside .ai-work (or legacy gemini-live) so apply can safely delete it')
    if path.exists() and any(p.is_symlink() for p in path.rglob('*')):
        raise ValueError('Refusing an output tree containing symlinks')
    return path


def read(path):
    return json.loads(path.read_text())


def plan(directory):
    directory = managed_directory(directory)
    review = candidates.checked_review(directory)
    stage, result = read(directory / 'stage.json'), read(directory / 'run.json')
    if stage.get('stage') != 'AI-2' or not stage.get('completed') or not result.get('passed'):
        raise ValueError('Apply requires completed, passing AI-2 output')
    if review['assessment'] in ('tests_failed', 'coverage_regressed', 'coverage_not_comparable'):
        raise ValueError('Candidate comparison is not acceptable; inspect review.md')
    previous = managed_directory(stage['baseline_directory'])
    if previous == directory or previous.is_relative_to(directory) or directory.is_relative_to(previous):
        raise ValueError('AI-1 and AI-2 outputs must be separate non-overlapping directories')
    candidates.checked_review(previous)
    if not read(previous / 'stage.json').get('completed') or not read(previous / 'run.json').get('passed'):
        raise ValueError('AI-1 baseline is not passing')
    for folder in (directory, previous):
        if not read(folder / 'model/api.json').get('completed'):
            raise ValueError('Model generation did not complete')
    ctx = read(directory / 'inputs/context.json')
    target = ctx['target']
    if read(previous / 'inputs/context.json')['target'] != target or context.select(target['fqcn']) != target:
        raise ValueError('Target differs from the measured baseline or current source')
    expected = read(directory / 'inputs/manifest.json')
    if expected != read(previous / 'inputs/manifest.json'):
        raise ValueError('AI-1/AI-2 source fingerprints differ')
    project = ROOT / 'case-study'
    context.check_project(project, expected)
    package = target['package']
    if package and not re.fullmatch(r'[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*', package):
        raise ValueError('Invalid package')
    target_dir = project / 'src/test/java' / Path(*package.split('.'))
    if not target_dir.resolve().is_relative_to(project.resolve()):
        raise ValueError('Test destination escapes project')
    for part in (target_dir, *target_dir.parents):
        if part.is_symlink():
            raise ValueError('Test destination must not pass through symlinks')
        if part == project:
            break
    copies = []
    for name in review['candidate_files']:
        if name not in (target['name'] + 'GeminiDraftTest.java', target['name'] + 'GeminiAdditionalTest.java'):
            raise ValueError('Unexpected test filename')
        source, destination = directory / 'generated' / name, target_dir / name
        if destination.exists() or destination.is_symlink():
            raise ValueError(f'Refusing to overwrite existing test: {name}')
        code = source.read_text()
        candidates.validate_unit(code)
        stripped = context.LITERALS.sub(' ', code)
        actual_package = re.search(r'\bpackage\s+([\w.]+)\s*;', stripped)
        if ((actual_package.group(1) if actual_package else '') != package
                or not re.search(r'\bclass\s+' + re.escape(source.stem) + r'\b', stripped)):
            raise ValueError('Candidate package/class does not match destination')
        if result.get('test_sha256', {}).get(name) != context.sha(source):
            raise ValueError('Candidate bytes differ from the measured test')
        copies.append((source, destination))
    draft = target['name'] + 'GeminiDraftTest.java'
    if not copies or not (directory / 'generated' / draft).is_file():
        raise ValueError('AI-2 must retain the draft')
    if context.sha(directory / 'generated' / draft) != context.sha(previous / 'generated' / draft):
        raise ValueError('AI-2 modified the fixed draft')
    cleanup = [previous, directory]
    session = directory.parent
    marker = session / 'session.json'
    if previous.parent == session and marker.is_file():
        owned = read(marker)
        if (owned == {'kind': 'ai12', 'stages': ['ai1', 'ai2']}
                and previous.name == 'ai1' and directory.name == 'ai2'
                and {p.name for p in session.iterdir()} <= {'session.json', 'ai1', 'ai2'}):
            cleanup = [managed_directory(session)]
    return {'directory': directory, 'previous': previous, 'target': target,
            'copies': copies, 'cleanup': cleanup, 'assessment': review['assessment']}


def integration_inputs():
    project = ROOT / 'case-study'
    paths = [project / 'pom.xml', project / 'mvnw']
    for directory in (project / '.mvn', project / 'src', ROOT / 'ai/data'):
        for path in directory.rglob('*'):
            if path.is_symlink():
                raise ValueError('Integration inputs must not contain symlinks')
            if path.is_file():
                paths.append(path)
    return {p.relative_to(ROOT).as_posix(): context.sha(p) for p in paths}


def verify(plan_data):
    destination = plan_data['directory'] / 'integration'
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir()
    with tempfile.TemporaryDirectory(prefix='seminar-ai-apply-') as temporary:
        workspace = Path(temporary)
        project = workspace / 'case-study'
        project.mkdir()
        for name in ('pom.xml', 'mvnw'):
            shutil.copy2(ROOT / 'case-study' / name, project / name)
        for name in ('.mvn', 'src'):
            shutil.copytree(ROOT / 'case-study' / name, project / name)
        if (ROOT / 'ai/data').is_dir():
            shutil.copytree(ROOT / 'ai/data', workspace / 'ai/data')
        for source, actual in plan_data['copies']:
            target = project / actual.relative_to(ROOT / 'case-study')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        command = ['./mvnw', '-B', '-ntp', 'clean', 'verify']
        environment = {k:v for k,v in os.environ.items() if k not in ('GEMINI_API_KEY','AI_MODEL')}
        try:
            process = subprocess.run(command, cwd=project, env=environment, capture_output=True, text=True, timeout=300)
            code, log = process.returncode, process.stdout + process.stderr
        except subprocess.TimeoutExpired:
            code, log = 124, 'Full suite verification timed out after 300s.'
        key, _ = client.settings()
        if key:
            log = log.replace(key, '<redacted>')
        log = log.replace(str(workspace), '<integration-work>').replace(str(Path.home()), '<home>')
        (destination / 'output.log').write_text(log)
        for relative in ('surefire-reports', 'site/jacoco'):
            if (project / 'target' / relative).exists():
                shutil.copytree(project / 'target' / relative, destination / relative)
        totals, coverage = ai_csv.raw_metrics(destination, plan_data['target']['fqcn'])
        result = {'exit_code':code, 'command':command, 'quality_gate_executed':True,
                  'target_coverage':coverage, **totals}
        result['passed'] = code == 0 and totals['tests'] > 0 and not any(totals[k] for k in ('failures','errors','skipped'))
        # The candidates must actually execute in the full suite, not just compile or be excluded by tags/patterns.
        import xml.etree.ElementTree as ET
        seen = {ET.parse(p).getroot().get('name') for p in (destination/'surefire-reports').glob('TEST-*.xml')
                if int(ET.parse(p).getroot().get('tests','0')) > int(ET.parse(p).getroot().get('skipped','0'))}
        package = plan_data['target']['package']
        expected = {(package + '.' if package else '') + source.stem for source, _ in plan_data['copies']}
        result['passed'] = result['passed'] and expected <= seen and bool(coverage)
        client.save(destination / 'run.json', result)
        return result


def apply(directory, reviewed=False, reviewer=None, execute=False):
    data = plan(directory)
    summary = {'assessment':data['assessment'], 'files':[str(p.relative_to(ROOT)) for _,p in data['copies']],
               'delete_after_success':[str(p.relative_to(ROOT)) for p in data['cleanup']]}
    if not execute:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print('Preview only. Read review.md and test sources; then use --apply --reviewed --reviewer NAME.')
        return summary
    if not reviewed or not reviewer or not reviewer.strip():
        raise ValueError('Explicit --reviewed and the actual --reviewer are required before syncing/deleting output')
    lock = ROOT / '.ai-work/apply.lock'
    lock.parent.mkdir(exist_ok=True)
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    created = []
    try:
        before = integration_inputs()
        measured = verify(data)
        if not measured['passed']:
            raise ValueError('Full suite/gate did not pass; no tests synced and output retained. Read ai2/integration/output.log')
        if integration_inputs() != before:
            raise ValueError('Source/tests/data changed during integration verification; nothing synced')
        data = plan(directory)  # Recheck hashes, conflicts and cleanup bounds immediately before writes.
        try:
            for source, destination in data['copies']:
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open('xb') as stream:
                    created.append(destination)
                    stream.write(source.read_bytes())
        except BaseException:
            for path in created:
                path.unlink()
            raise
        try:
            for path in data['cleanup']:
                managed_directory(path)
                shutil.rmtree(path)
        except (OSError, ValueError) as error:
            summary.update(applied=True, reviewer=reviewer.strip(), integration=measured, output_deleted=False)
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            raise ValueError('Tests were synced successfully, but output cleanup failed; do not apply again. Inspect permissions/clean remaining output.') from error
        summary.update(applied=True, reviewer=reviewer.strip(), integration=measured, output_deleted=True)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print('Synced reviewed tests; managed AI output deleted. Commit/push and open a PR to run CI/AI-3.')
        return summary
    finally:
        os.close(descriptor)
        lock.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--from-ai2', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--reviewed', action='store_true')
    parser.add_argument('--reviewer')
    args = parser.parse_args()
    try:
        apply(args.from_ai2, args.reviewed, args.reviewer, args.apply)
        return 0
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        print(f'Apply stopped: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
