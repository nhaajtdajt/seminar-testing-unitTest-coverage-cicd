#!/usr/bin/env python3
"""Prepare a Week 04 snapshot, AI disclosure and actual Git history for submission."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile
from render_reports import render

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def export_chat(source, destination):
    messages = []
    for line in source.open():
        entry = json.loads(line)
        value = entry.get('payload', {})
        if entry.get('type') != 'response_item' or value.get('type') != 'message':
            continue
        role = value.get('role')
        if role not in ('user', 'assistant') or value.get('phase') not in (None, 'commentary', 'final', 'final_answer'):
            continue
        text = '\n'.join(block.get('text', '') for block in value.get('content', []) if isinstance(block, dict)).strip()
        if not text or text.startswith('<environment_context>'):
            continue
        # The exported conversation contains visible messages, not tool output or private instructions.
        text = re.sub(r'(?:AIza[0-9A-Za-z_-]{25,}|gh[pousr]_[0-9A-Za-z]{20,}|sk-[0-9A-Za-z_-]{24,})', '[REDACTED]', text)
        messages.append((entry.get('timestamp', 'Không có timestamp'), role, text))
    if not messages:
        raise RuntimeError('No visible user/assistant messages found in the supplied chat log')
    body = '# Chat log sử dụng AI — Tuần thực hành 04\n\n'
    body += 'Bản xuất các tin nhắn người dùng và phản hồi hiển thị của trợ lý có trong phiên Codex truy xuất được. Timestamp dùng UTC như dữ liệu gốc. Các câu trả lời cũ phản ánh trạng thái tại thời điểm trao đổi; báo cáo Tuần 04 và log chạy mới là trạng thái cập nhật. Không có log từ model khác mà nhóm đã dùng để chỉnh Java 25.\n\n'
    body += f'**Số tin nhắn xuất:** {len(messages)}. **Tin nhắn đầu/cuối:** {messages[0][0]} / {messages[-1][0]}.\n\n'
    for number, (timestamp, role, text) in enumerate(messages, 1):
        fence = '`' * max(3, 1 + max((len(run) for run in re.findall(r'`+', text)), default=0))
        body += f'## {number}. {timestamp} — {"Người dùng" if role == "user" else "Codex"}\n\n{fence}text\n{text}\n{fence}\n\n'
    destination.write_text(body)
    return len(messages)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--group-id', default='Group09', help='Course GroupID; default Group09')
    parser.add_argument('--chat-log', type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'Group(?:\d+|XX)', args.group_id):
        parser.error('GroupID must look like Group02')
    members = json.loads((ROOT / 'bao-cao-tuan/thanh-vien.json').read_text())['members']
    rows = '\n'.join(f"| {m['student_id']} | {m['full_name']} | {m['responsibility'].replace('điều phối video', 'ảnh minh chứng')} |" for m in members)
    now = datetime.now(timezone.utc).isoformat()
    group = args.group_id + (' (mã tạm, cần thay bằng mã nhóm thực tế)' if args.group_id == 'GroupXX' else '')
    commits = []
    for line in git('log', '--all', '--format=%H%x1f%an%x1f%ae%x1f%aI%x1f%cn%x1f%ce%x1f%cI%x1f%s').splitlines():
        sha, author, email, authored, committer, committer_email, committed, subject = line.split('\x1f', 7)
        commits.append(dict(sha=sha, author=author, email=email, authored=authored, committer=committer, committer_email=committer_email, committed=committed, subject=subject))
    dest_parent = ROOT / 'bai-nop'
    dest_parent.mkdir(exist_ok=True)
    name = args.group_id + '-04'
    destination = dest_parent / name
    archive = destination.with_suffix('.zip')
    with tempfile.TemporaryDirectory(prefix='.prepare-week04-', dir=dest_parent) as temp:
        staging = Path(temp) / name
        staging.mkdir()
        chat = Path(temp) / 'chat.md'
        chat_count = export_chat(args.chat_log, chat)
        ai = f'''# AI Usage Declaration — Tuần thực hành 04

**Nhóm:** {group}. **Ngày tổng hợp:** {now} (UTC).

Nhóm em có sử dụng AI để chuẩn bị seminar Unit Test · Code Coverage · CI/CD trong Tuần 04, bao gồm phần công việc làm trước kế hoạch Tuần 05.

## 1. Công cụ đã sử dụng

| Công cụ | Quá trình sử dụng | Giới hạn khai báo |
|---|---|---|
| OpenAI Codex | Phân tích repo, lập kế hoạch, hỗ trợ code/test, cấu hình CI, chạy kiểm tra và benchmark, soạn báo cáo và chuẩn bị ảnh minh chứng | Chat log truy xuất được gồm {chat_count} tin nhắn, đính kèm tại mục 5. Không xác định chính xác model từng lượt chỉ từ hội thoại. |
| Model khác theo thông tin người dùng | Điều chỉnh dự án sang Java 25 | Chưa được cung cấp tên model/công cụ và chat log; nhóm cần bổ sung phần khai báo này. |

Gemini API trong demo AI-3 mới được chuẩn bị client/prompt/workflow; chưa gọi API thật vì chưa có cấu hình key.

## 2. Quá trình sử dụng AI trong tuần

1. Nhóm cung cấp yêu cầu seminar, nhờ AI phân tích file và đề xuất phân công cho 5 thành viên.
2. AI hỗ trợ case study thư viện, JUnit/Mockito, JaCoCo, PIT, TDD replay và cấu hình CI. Đầu ra được đối chiếu bằng log chạy, XML/HTML và metadata lưu trong repository làm việc.
3. Sau khi dự án chuyển sang Java 25, kiểm tra lại môi trường và kết quả. Bản báo cáo dùng số liệu của cấu hình Java 25 hiện tại.
4. AI-1 tạo bản nháp 3 test, phủ 70% branch FineCalculator. AI-2 hỗ trợ đọc gap và bổ sung thành 6 test, đạt 100% branch cho lớp này.
5. AI-4 hỗ trợ 13 ca CSV đã chạy pass, trùng 13/15 ca tham chiếu. Hai bộ đều có AI hỗ trợ nên chưa phải đánh giá độc lập giữa con người và AI.
6. Chạy đủ 3 cặp benchmark cache Maven và 3 cặp JaCoCo. Các lượt tải lỗi được giữ riêng trong repository, không đưa vào trung vị.
7. AI hỗ trợ tổng hợp báo cáo Tuần 04, điền thành viên, chụp ảnh API và đóng gói đúng các mục nộp tuần. Gói này không kèm video.

## 3. Phân công rà soát

| MSSV | Họ tên | Phần phụ trách |
|---|---|---|
{rows}

Phân công do nhóm cung cấp, không tự xác nhận tác giả commit hay đóng góp cá nhân đã hoàn thành. Các thành viên cần rà soát nội dung trước khi nộp.

## 4. Kiểm tra đầu ra và giới hạn

- Bộ chuẩn có 33 lượt test pass. Coverage FineCalculator từ 50% lên 100% branch; không suy rộng 100% toàn ứng dụng.
- Coverage gate 90%: bộ baseline fail, bộ đầy đủ pass. Test yếu và test đầy đủ cùng phủ 100% branch nhưng diệt 3/11 và 10/11 mutant.
- Chưa có run GitHub Actions/Jenkins hoặc review AI-3 qua API thật; không ghi cấu hình thành kết quả thực thi trên dịch vụ.
- Source và tài liệu mới chưa được commit/push tại thời điểm kiểm tra. Git log kèm theo phản ánh lịch sử thật.
- Chat log bên dưới chỉ gồm phiên Codex truy xuất được. Phiên model khác chỉnh Java 25 chưa có log để đính kèm.

## 5. Chat log với AI

'''
        # Keep the original message text in fenced blocks; this avoids links to old workspace files.
        transcript = chat.read_text().split('\n', 1)[1]
        (staging / 'AI Usage Declaration.md').write_text(ai + transcript)

        mapping = '\n'.join(f"| {m['git_author'] or 'Chưa cung cấp / chưa xuất hiện trong log'} | {m['student_id']} | {m['full_name']} | {sum(c['author'] == m['git_author'] for c in commits)} |" for m in members)
        log = f'''# Git Commit Log Total — Tuần thực hành 04

## Đối chiếu Git username/tên tác giả với thành viên

| Git username/tên tác giả xuất hiện trong log | MSSV | Họ tên | Commit đối chiếu |
|---|---|---|---:|
{mapping}

`23120231` là author name thật trong Git, đối chiếu với MSSV của Trương Nhật Đạt. Git author name có thể khác GitHub login. Chưa có Git username của 4 thành viên còn lại; không tự suy ra tài khoản từ họ tên.

**Nhóm:** {group}. **Thời điểm xuất:** {now} (UTC).

**Phạm vi:** Toàn bộ lịch sử local qua `git log --all`, từ đầu project tới thời điểm xuất; không fetch lịch sử mới trong bước đóng gói. **Nhánh:** `{git('branch', '--show-current')}`. **HEAD:** `{git('rev-parse', 'HEAD')}`. **Tổng cộng:** {len(commits)} commit.

## 1. Danh sách commit tổng cộng từ đầu project

'''
        for number, c in enumerate(commits, 1):
            log += f"### {number}. {c['sha']}\n\n- Author: {c['author']} <{c['email']}>\n- Author date: {c['authored']}\n- Committer: {c['committer']} <{c['committer_email']}>\n- Commit date: {c['committed']}\n- Nội dung: {c['subject']}\n\n"
        log += '## 2. Danh sách commit của từng thành viên\n\n'
        for m in members:
            selected = [c for c in commits if c['author'] == m['git_author']]
            log += f"### {m['full_name']} — {m['student_id']}\n\n**Git username/tên tác giả:** {m['git_author'] or 'Chưa được cung cấp; chưa xuất hiện trong lịch sử hiện tại'}. **Số commit đối chiếu:** {len(selected)}.\n\n"
            if selected:
                log += '| Commit | Author date | Nội dung |\n|---|---|---|\n'
                for c in selected:
                    subject = c['subject'].replace('|', '\\|')
                    log += f"| `{c['sha']}` | {c['authored']} | {subject} |\n"
                log += '\n'
            else:
                log += 'Chưa có commit thuộc danh tính thành viên này trong lịch sử hiện có. Không dùng số commit để suy ra toàn bộ đóng góp ngoài Git.\n\n'
        log += '## 3. Phần chưa nằm trong lịch sử commit\n\nSource, test, workflow, báo cáo và minh chứng mới vẫn ở working tree tại lúc kiểm tra. Không cộng những file chưa commit thành commit của thành viên và không tạo lịch sử giả. Nhóm cần xuất lại log sau khi có commit mới bằng tài khoản thật.\n'
        (staging / 'Git Commit Log Total.md').write_text(log)

        cache = json.loads((ROOT / 'evidence/tuan-05/benchmark-cache/summary.json').read_text())
        jacoco = json.loads((ROOT / 'evidence/tuan-05/benchmark-jacoco/summary.json').read_text())
        assert cache['complete'] and cache['completed_pairs'] == 3
        assert len(jacoco['measurements']) == 6 and all(e['exit_code'] == 0 for e in jacoco['measurements'])
        http = json.loads((ROOT / 'evidence/tuan-04-demo/results.json').read_text())['cases']
        assert [e['actual_status'] for e in http] == [201, 409, 404, 400, 409]
        def seconds(value):
            return f'{value:.3f}'.replace('.', ',')
        pairs = ''
        for trial in range(1, 4):
            pair = {e['mode']: e for e in cache['measurements'] if e['trial'] == trial}
            pairs += f"| {trial} | {seconds(pair['cold']['seconds'])} | {seconds(pair['warm']['seconds'])} | {pair['cold']['started_at_utc'][11:19]} |\n"
        report = f'''# Báo cáo Tuần thực hành 04 — Unit Test · Code Coverage · CI/CD

**Nhóm:** {group}. **Tuần báo cáo:** Thực hành 04 theo xác nhận của nhóm. **Ngày tổng hợp:** 16/10/2026.

**Người phụ trách tổng hợp:** Phạm Quang Vinh (23120202). Một phần công việc dự kiến cho Tuần 05 đã được thực hiện sớm và được ghi nhận trong Tuần 04.

## 1. Thành viên và phân công

| MSSV | Họ tên | Phụ trách |
|---|---|---|
{rows}

Đây là phân công phụ trách rà soát và bàn giao. Nhóm cần xác nhận đóng góp thực tế của từng người; sản phẩm có AI hỗ trợ không tự chứng minh công sức cá nhân.

## 2. Mục tiêu và kết quả trong tuần

| Hạng mục | Kết quả thực tế |
|---|---|
| Case study thư viện | Java 25, Spring Boot 4.1.1, H2 in-memory qua Spring Data JPA; tính phí, mượn sách và REST API. |
| Unit Test | Bộ chuẩn 33 lượt test, 0 failure, 0 error: 17 tính phí, 6 nghiệp vụ mượn, 5 tầng web, 2 integration và 3 persistence. Bộ chuẩn cũng đã pass trên Java 21. |
| Coverage FineCalculator | Baseline 5/10 nhánh (50%); bộ đầy đủ 10/10 nhánh (100%), 100% line. Không kết luận 100% toàn ứng dụng. |
| Coverage gate | Yêu cầu ít nhất 90% branch cho FineCalculator; bộ baseline fail, bộ đầy đủ pass. |
| Chất lượng test và mutation | Bộ yếu và đầy đủ cùng phủ 100% branch; PIT diệt lần lượt 3/11 và 10/11 mutant. Mutant còn sống thay <= thành < tại ngưỡng gia hạn nhưng vẫn trả 0 theo đặc tả hiện tại. |
| TDD | Tái hiện 4 vòng đỏ/xanh trong bản sao riêng. Replay không thay cho commit lịch sử của nhóm. |
| HTTP API | 5 tình huống trên ứng dụng thật trả đúng status: 201, 409, 404, 400 và 409. |
| CI/CD | Có workflow test → gate → package, JDK 25, cache/artifact và Jenkinsfile. Workflow qua actionlint; chưa có run GitHub/Jenkins thật. |
| AI-1/AI-2 | Bản đầu 3 test đạt 70% branch; sau bổ sung thành 6 test đạt 100% branch FineCalculator. |
| AI-3/AI-4 | AI-3 mới chuẩn bị client/prompt, chưa gọi API thật; AI-4 có 13 ca CSV pass, trùng 13/15 ca tham chiếu, chưa có bộ con người độc lập. |

Số test là số lượt thực thi, gồm các dòng parameterized. Không cộng hai lượt chạy Java 21/25 thành 66 ca khác nhau. Các kết quả trên được đối chiếu với log/XML/JSON lưu trong repository làm việc; bộ nộp tuần này trình bày số liệu trong báo cáo và ảnh ứng dụng.

## 3. Benchmark tại máy

| Thí nghiệm | Số cặp hợp lệ | Trung vị (giây) |
|---|---|---|
| Maven repo lạnh / ấm | 3/3 | {seconds(cache['medians_seconds']['cold'])} / {seconds(cache['medians_seconds']['warm'])} |
| JaCoCo tắt / bật | 3/3 | {seconds(jacoco['medians_seconds']['off'])} / {seconds(jacoco['medians_seconds']['on'])} |

| Cặp cache | Lạnh (giây) | Ấm (giây) | Bắt đầu lạnh (UTC, 16/10/2026) |
|---|---|---|---|
{pairs}
Cặp 3 được bổ sung muộn hơn, ưu tiên IPv4, connect timeout 15 giây, request timeout 120 giây và giới hạn 1.800 giây/lệnh. Lượt lạnh bắt đầu từ kho dependency trống, lượt ấm dùng lại đúng kho vừa tải. Hai lượt bổ sung đều pass 33 test và coverage gate. Các lượt tải lỗi không tính vào số liệu hoàn thành.

Đây là số đo tại máy, chịu ảnh hưởng mạng, tải máy và thứ tự chạy. Lượt lạnh cặp 3 mất khoảng 8 phút, nên cần đọc từng lượt cùng trung vị. Không coi đây là số đo restore cache hoặc tốc độ GitHub Actions/Jenkins.

## 4. Screenshot ứng dụng

![API mượn sách: 5/5 tình huống trả đúng kết quả](screenshots/01-api-5-tinh-huong.png)

Ứng dụng cung cấp REST API. Ảnh được chụp từ trang kiểm tra gửi request thật tới ứng dụng Java 25, không giả lập response; trang kiểm tra phục vụ minh chứng, không phải giao diện sản phẩm riêng. Thời điểm gửi 5 request: 15:16:37–15:16:45 UTC ngày 16/10/2026.

| Tình huống | Đầu vào bookId/memberId | HTTP thực tế | Kết quả |
|---|---|---|---|
| Mượn thành công | 1 / 1 | 201 | Đạt |
| Sách đã được mượn | 1 / 1 | 409, BOOK_UNAVAILABLE | Đạt |
| Không có sách | 99 / 1 | 404, BOOK_NOT_FOUND | Đạt |
| ID sách âm | -1 / 1 | 400 | Đạt |
| Thành viên còn phí chưa trả | 3 / 2 | 409, UNPAID_FINE | Đạt |

## 5. Khó khăn và phần chưa hoàn tất

- Tài khoản GitHub đã kiểm tra có quyền READ: chưa push source mới, chạy workflow/PR đỏ–xanh hoặc bật required checks. Jenkins chưa có lượt chạy thực tế.
- Chưa có cấu hình key để gọi AI-3 qua API; chưa có dữ liệu con người độc lập cho đánh giá AI-4.
- Lịch sử hiện có 4 commit mang author 23120231, đối chiếu với Trương Nhật Đạt. Tên Git của 4 thành viên còn lại chưa được cung cấp. Chi tiết nằm trong Git Commit Log Total.
- Mã nhóm thực tế, xác nhận đóng góp và góp ý giảng viên còn cần nhóm bổ sung. Không ghi lùi ngày hoặc gán công việc đã hoàn thành cho các tuần trước khi chưa có minh chứng.

## 6. Kế hoạch tuần thực hành 05

| Thành viên | Việc tiếp theo |
|---|---|
| Phạm Quang Vinh | Tổng hợp đóng góp, dùng tài khoản có quyền để commit và chạy CI/PR đỏ–xanh, thu kết quả required checks. |
| Nguyễn Bảo An | Rà soát assertion và dữ liệu biên, tự chạy và duyệt Unit Test. |
| Trương Nhật Đạt | Đối chiếu JaCoCo/PIT, giải thích mutant còn sống, kiểm coverage gate trên CI. |
| Nguyễn Lê Thế Vinh | Kiểm lại nghiệp vụ, dữ liệu H2 và luồng API theo hướng dẫn trong repository. |
| Ngô Gia An | Rà soát kết quả AI, bổ sung khai báo của model khác nếu có log, hoàn thiện báo cáo và ảnh minh chứng. |
'''
        (staging / 'BaoCao_Tuan_04.md').write_text(report)
        (staging / 'screenshots').mkdir()
        shutil.copy2(ROOT / 'evidence/tuan-04-demo/screenshots/01-api-5-tinh-huong.png', staging / 'screenshots/01-api-5-tinh-huong.png')
        for file in staging.glob('*.md'):
            render(file)
        expected = {'AI Usage Declaration.md', 'AI Usage Declaration.html', 'Git Commit Log Total.md', 'Git Commit Log Total.html', 'BaoCao_Tuan_04.md', 'BaoCao_Tuan_04.html', 'screenshots/01-api-5-tinh-huong.png'}
        assert {str(p.relative_to(staging)) for p in staging.rglob('*') if p.is_file()} == expected
        staged_zip = Path(temp) / (name + '.zip')
        with zipfile.ZipFile(staged_zip, 'w', zipfile.ZIP_DEFLATED) as output:
            for filename in sorted(expected):
                output.write(staging / filename, filename)
        with zipfile.ZipFile(staged_zip) as output:
            assert output.testzip() is None
        # Replace only the generated submission snapshot, keeping a reversible backup outside the repo.
        with tempfile.TemporaryDirectory(prefix='seminar-submission-backup-') as backup:
            previous = Path(backup) / name
            previous_zip = Path(backup) / (name + '.zip')
            if destination.exists():
                if not (destination / 'AI Usage Declaration.md').is_file():
                    raise RuntimeError('Refusing to replace an unrecognized directory')
                shutil.move(str(destination), previous)
            if archive.exists():
                shutil.move(str(archive), previous_zip)
            try:
                shutil.move(str(staging), destination)
                shutil.move(str(staged_zip), archive)
            except BaseException:
                if destination.exists(): shutil.rmtree(destination)
                archive.unlink(missing_ok=True)
                if previous.exists(): shutil.move(str(previous), destination)
                if previous_zip.exists(): shutil.move(str(previous_zip), archive)
                raise
    print(f'Created {destination}\nCreated {archive}\nExactly 7 files: 3 Markdown/HTML pairs and 1 app screenshot. ZIP bytes: {archive.stat().st_size}')


if __name__ == '__main__':
    main()
