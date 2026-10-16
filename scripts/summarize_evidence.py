#!/usr/bin/env python3
"""Generate measurements from selected, non-invalidated evidence; no estimated test results."""
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'evidence/tuan-05'

def main():
    runs = {}
    for name in ['baseline', 'gate-fail', 'jdk21', 'coverage-trap', 'ai-draft-recheck', 'ai-improved', 'ai-data', 'final']:
        folder = DEST / name
        entry = json.loads((folder/'run.json').read_text())
        suites = [ET.parse(p).getroot() for p in (folder/'surefire-reports').glob('TEST-*.xml')]
        entry['tests'] = {key:sum(int(s.attrib.get(key, 0)) for s in suites) for key in ['tests', 'failures', 'errors', 'skipped']}
        report = ET.parse(folder/'site/jacoco/jacoco.xml').getroot()
        clazz = next(c for c in report.findall('.//class') if c.attrib['name'] == 'vn/edu/seminar/fine/FineCalculator')
        entry['fine_calculator'] = {c.attrib['type']:{'covered':int(c.attrib['covered']), 'missed':int(c.attrib['missed'])} for c in clazz.findall('counter')}
        runs[name] = entry
    mutations = {}
    for name in ['pit-weak', 'pit-strong']:
        report = ET.parse(DEST/name/'pit-reports/mutations.xml').getroot()
        mutations[name] = dict(Counter(m.attrib['status'] for m in report))
    def rows(path):
        with path.open() as handle:
            return {tuple(row) for row in list(csv.reader(handle))[1:]}
    reference = rows(ROOT/'case-study/src/test/resources/fine-cases.csv')
    generated = rows(ROOT/'ai/data/AI-4-boundaries.csv')
    benchmarks = {}
    for mode in ['cache', 'jacoco']:
        path = DEST / f'benchmark-{mode}' / 'summary.json'
        benchmarks[mode] = json.loads(path.read_text()) if path.exists() else {
            'status': 'not_measured', 'reason': 'No measurements are present for the current configuration.'}
    output = {'generated_at_utc':datetime.now(timezone.utc).isoformat(), 'runs':runs, 'mutations':mutations,
        'ai_data':{'reference_count':len(reference), 'generated_count':len(generated), 'overlap':len(reference & generated), 'reference_only':sorted(reference-generated), 'generated_only':sorted(generated-reference), 'independent_human_reference':False},
        'benchmarks':benchmarks}
    (DEST/'summary.json').write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n")
    files = [p for folder in ['case-study/src', 'ai', 'scripts', '.github/workflows'] for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    files += [ROOT/'case-study/pom.xml', ROOT/'Jenkinsfile']
    (DEST/'source-sha256.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT)}\n' for p in sorted(files)))
    print('Generated summary.json from selected XML/JSON evidence; missing benchmarks marked not_measured.')

if __name__ == '__main__':
    main()
