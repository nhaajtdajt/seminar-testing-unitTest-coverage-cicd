"""Candidate checks and review reports; passing coverage never certifies business correctness."""
from collections import Counter
import json
from pathlib import Path
import re

import ai_context as context
import gemini_client as client


def assertions(code):
    # Keep literals, discard comments/formatting, and preserve complete assertion chains.
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|[\w$]+|[^\s]', code)
    tokens = [t for t in tokens if not t.startswith(('//', '/*'))]
    found, index = [], 0
    while index < len(tokens):
        if re.fullmatch(r'assert\w*|fail', tokens[index]) and tokens[index:index+2][-1] == '(':
            end, depth = index, 0
            while end < len(tokens):
                token = tokens[end]
                if token in ('(', '{', '['):
                    depth += 1
                elif token in (')', '}', ']'):
                    depth -= 1
                if token == ';' and depth == 0:
                    found.append(tuple(tokens[index:end]))
                    break
                end += 1
            index = end
        index += 1
    return Counter(found)


def validate_unit(code):
    stripped = context.LITERALS.sub(' ', code)
    if not re.search(r'@(?:org\.junit\.jupiter\.api\.)?Test\b', stripped):
        raise ValueError('Unit candidate must contain an ordinary @Test')
    if re.search(r'\b(?:assume\w*|assumingThat)\s*\(|@(?:[\w$]+\.)*(?:Disabled\w*|Ignore|Tag)\b', stripped):
        raise ValueError('Disabled, tagged or assumption-based candidates are not accepted')
    if not assertions(code):
        raise ValueError('Candidate has no recognizable assertion; review contract required')
    if re.search(r'\bassertTrue\s*\(\s*true\s*\)|\bassertFalse\s*\(\s*false\s*\)', stripped):
        raise ValueError('Trivial constant assertion')


def repair_kind(result, log):
    if result.get('passed'):
        return None
    if result.get('exit_code') == 124:
        return 'timeout_needs_review'
    if result.get('failures', 0):
        return 'assertion_failure_needs_review'
    if 'COMPILATION ERROR' in log:
        return 'compilation'
    if any(name in log for name in ('UnnecessaryStubbingException', 'UnfinishedStubbingException',
                                    'InvalidUseOfMatchersException', 'MissingMethodInvocationException')):
        return 'mock_setup'
    return 'execution_failure_needs_review'


def compare(before, after):
    if not after.get('passed'):
        return 'tests_failed'
    gains, losses = [], []
    for kind in ('LINE', 'BRANCH'):
        first = before.get('target_coverage', {}).get(kind)
        last = after.get('target_coverage', {}).get(kind)
        if first and last:
            if first['covered'] + first['missed'] != last['covered'] + last['missed']:
                return 'coverage_not_comparable'
            gains.append(last['covered'] > first['covered'])
            losses.append(last['covered'] < first['covered'])
    if any(losses):
        return 'coverage_regressed'
    if any(gains):
        return 'coverage_increased'
    return 'no_coverage_gain_needs_review' if gains else 'coverage_not_comparable'


def fully_covered(result):
    counters = result.get('target_coverage', {})
    return bool(counters) and all(counter['missed'] == 0 for counter in counters.values())


def review_report(destination, result, assessment, before=None):
    files = sorted((destination / 'generated').glob('*.java'))
    names = [p.name for p in files]
    lines = ['# Review test ứng viên', '', f"Class: `{result['target_class']}`", '',
             f"Trạng thái kỹ thuật: **{assessment}**.",
             f"JUnit: tests={result.get('tests', 0)}, failures={result.get('failures', 0)}, "
             f"errors={result.get('errors', 0)}, skipped={result.get('skipped', 0)}.", '',
             '| Coverage target | Trước | Sau |', '|---|---|---|']
    for kind in ('LINE', 'BRANCH'):
        def value(run):
            counter = (run or {}).get('target_coverage', {}).get(kind)
            if not counter or counter['covered'] + counter['missed'] == 0:
                return 'N/A'
            return f"{counter['covered']}/{counter['covered'] + counter['missed']}"
        lines.append(f'| {kind} | {value(before)} | {value(result)} |')
    lines += ['', '## File cần đọc', ''] + [f'- [generated/{name}](generated/{name})' for name in names]
    lines += ['', 'Đọc `analysis.md`, expected, assertion, mock state và ca trùng. ',
              'No coverage gain không chứng minh test vô ích, nhưng chưa chứng minh cải thiện coverage. ',
              'Test xanh/coverage cao không xác nhận đúng nghiệp vụ. Quality gate của suite chuẩn sẽ chạy khi apply.',
              '', 'Output chưa được chép vào src/test. Sau review, dùng ai_apply.py với --reviewed và tên reviewer thật.',
              'Apply thành công sẽ xóa output AI-1/AI-2 của phiên; apply lỗi giữ output để xử lý.',
              'Nếu sửa file sau khi đo, phải sinh/đo lại; apply từ chối bản đã thay đổi sau báo cáo.']
    (destination / 'review.md').write_text('\n'.join(lines) + '\n')
    sealed = [destination / name for name in ('run.json', 'stage.json', 'inputs/context.json',
              'inputs/manifest.json', 'model/api.json', 'analysis.md', 'review.md')]
    sealed += files
    client.save(destination / 'review.json', {'version': 1, 'assessment': assessment,
                'candidate_files': names, 'review_required': True,
                'sha256': {p.relative_to(destination).as_posix(): context.sha(p) for p in sealed if p.is_file()}})


def checked_review(directory):
    document = json.loads((directory / 'review.json').read_text())
    if document.get('version') != 1 or not document.get('sha256'):
        raise ValueError('Missing candidate review seal; regenerate AI-1/AI-2')
    for name, expected in document['sha256'].items():
        path = directory / name
        if Path(name).is_absolute() or '..' in Path(name).parts or path.is_symlink() or context.sha(path) != expected:
            raise ValueError('Candidate or measured report changed after measurement; regenerate before apply')
    actual = sorted(p.name for p in (directory / 'generated').glob('*.java'))
    if actual != sorted(document['candidate_files']):
        raise ValueError('Candidate file set changed after measurement')
    required = {'run.json','stage.json','inputs/context.json','inputs/manifest.json','model/api.json','analysis.md','review.md'}
    required |= {'generated/' + name for name in actual}
    if not required <= document['sha256'].keys():
        raise ValueError('Incomplete review seal')
    return document
