# Quay lại AI-1 → AI-4 với LoanService — lệnh copy/paste

Chuẩn bị ngày 30/10/2026 cho Ngô Gia An (23120205). Dùng **Terminal zsh trên máy này**,
copy từng khối lệnh theo thứ tự và kiểm expected rồi mới sang khối kế tiếp.
Không copy dấu ba backtick. Giữ cùng Terminal đến cuối; mục 10 hướng dẫn khôi phục biến
nếu đóng Terminal giữa chừng. Các đoạn chờ API/CI có thể cắt khi dựng video và nói rõ đã cắt.

## Trạng thái Codex đã chuẩn bị

- Đang ở nhánh local **`codex/loan-ai-demo-20261030`**, tách từ `seminar-core` tại `814672a`.
- Đã gỡ đúng `LoanServiceGeminiDraftTest.java` và `LoanServiceGeminiAdditionalTest.java`.
  Giữ production Loan, `LoanServiceTest` và các fixture demo `LoanServiceAi*Test`.
  Nhánh `seminar-core` vẫn giữ bản cũ; Git lưu lịch sử để lấy lại.
- Baseline sau gỡ đã chạy `clean verify`: **39 tests, 0 failures/errors/skipped**, gate PASS.
  JaCoCo toàn project LINE **76/83**, BRANCH **24/24**; LoanService LINE **17/17**, BRANCH **6/6**.
  Vì test chuẩn đã phủ hết LoanService, không hứa coverage toàn suite tăng sau khi thêm test AI.
- Java 25.0.5, Maven Wrapper 3.9.16, Python 3.14.3; cấu hình local có Gemini key.
- Chưa push/tạo PR và chưa gọi Gemini mới. Lệnh push/tạo PR nằm ở mục 4 để bạn tự quay.
- CSV human Loan vẫn là mẫu trống, **bạn/người viết cần tự điền**. Không dùng CSV FineCalculator.

Luồng quay: **checkout → CSV human/khóa → baseline → tạo draft PR trước → AI-1 → AI-2
→ review/apply → push lên cùng PR/AI-3 → AI-4**. Draft PR ban đầu ghi nhận việc gỡ test;
sau push tiếp, GitHub review diff mới nhất so với `seminar-core`, không chỉ commit cuối.
Đây là lượt làm lại, không xóa được lịch sử PR #13 hay việc đã từng xem test AI trước đó.

## 1. Checkout và kiểm môi trường

### 1.1. Vào đúng repo/nhánh

```bash
cd "/Users/ngogiaan1103/Documents/ChatGPT/seminar-testing 2"
git switch codex/loan-ai-demo-20261030
git branch --show-current
git status --short
```

**Expected:** branch in `codex/loan-ai-demo-20261030`; status không có thay đổi ở lần đầu
sau checkpoint preparation. Nếu bạn đã tự điền CSV/notes thì các thay đổi đó là bình thường.
Không checkout về `seminar-core` trước AI-1/apply, vì hai file Gemini cũ sẽ xuất hiện lại.

### 1.2. Kiểm công cụ và key

```bash
java -version
case-study/mvnw -v
python3 --version
python3 scripts/gemini_client.py status
gh auth status
```

**Expected:** Java 25, Maven 3.9.16, Python >=3.10; status có `key_configured: true`, model
`gemini-3.6-flash`; `gh` đăng nhập GitHub. Lệnh status Gemini không gọi API, không chứng minh
quota còn. Không mở `.env.gemini` khi quay.

Nếu Java sai, chỉ chạy khối sửa môi trường sau rồi kiểm lại mục 1.2:

```bash
export JAVA_HOME="$(/usr/libexec/java_home -v 25)"
export PATH="$JAVA_HOME/bin:$PATH"
java -version
```

**Expected:** Java 25. Nếu `gh` thực sự chưa đăng nhập trong Terminal có mạng, chạy
`gh auth login --hostname github.com` trước khi quay; không đăng nhập/nhập token trên video.

### 1.3. Khởi tạo biến và output cho đúng một lượt

```bash
setopt PIPE_FAIL
export AI_BRANCH="codex/loan-ai-demo-20261030"
export GH_REPO="nhaajtdajt/seminar-testing-unitTest-coverage-cicd"
export AI_CLASS="LoanService"
export AI_HUMAN="ai/human/loan-service/frozen"
export GA_RUN=".ai-work/LoanService-video-$(date +%Y%m%d-%H%M%S)"
mkdir -p .ai-work
mkdir "$GA_RUN"
printf '%s\n' "$GA_RUN" > .ai-work/loan-video-current-run.txt
git rev-parse HEAD > "$GA_RUN/preparation-sha.txt"
printf 'Branch: %s\nOutput: %s\n' "$AI_BRANCH" "$GA_RUN"
```

**Expected:** output là thư mục `.ai-work/LoanService-video-<thời điểm>` mới, cùng branch ở trên.
Chạy khối này một lần cho lượt quay. `mkdir` báo đã tồn tại thì kiểm tra trước, không ghi đè
baseline cũ. `.ai-work/` bị Git bỏ qua. Không cần server/Docker/database cho luồng unit test này.

## 2. Hoàn thành và khóa CSV human trước output AI mới

### 2.1. Tạo file làm việc từ mẫu nếu chưa có

```bash
python3 - <<'PY'
from pathlib import Path
folder = Path('ai/human/loan-service')
target = folder / 'cases.csv'
if target.exists():
    print('Giữ nguyên cases.csv đã có; kiểm nội dung trước khi tiếp tục.')
else:
    with target.open('x') as stream:
        stream.write((folder / 'cases.template.csv').read_text())
    print('Đã tạo cases.csv chỉ có header; cần người viết tự điền dữ liệu.')
PY
open -t ai/human/loan-service/cases.csv
open -t ai/human/loan-service/cases-notes.md
```

**Expected:** mở CSV chín cột và notes; khi mới tạo, chưa có ca kiểm thử.
**Dừng nhập lệnh tại đây để tự điền, lưu hai file rồi mới tiếp tục.**
Xem [ý nghĩa từng cột](../../ai/human/loan-service/README.md). Không có số dòng cố định bắt buộc.

Tác giả phải ghi đúng nguồn. Nếu đã xem test/data AI Loan trước đây thì xóa file không làm
bộ mới trở thành độc lập; cần người chưa xem tự viết nếu muốn dùng luồng đối chứng độc lập.
Chỉ dùng `--attest-independent` dưới đây khi tác giả thực sự đáp ứng điều kiện này.
Nếu chưa có tác giả phù hợp, có thể quay AI-1/2/3 riêng nhưng phần AI-4 độc lập vẫn còn chờ.

### 2.2. Kiểm có dữ liệu, header và notes đầy đủ

```bash
python3 - <<'PY'
import csv
from pathlib import Path
folder = Path('ai/human/loan-service')
with (folder / 'cases.template.csv').open(newline='') as stream:
    header = next(csv.reader(stream))
with (folder / 'cases.csv').open(encoding='utf-8-sig', newline='') as stream:
    reader = csv.DictReader(stream)
    rows = list(reader)
    assert reader.fieldnames == header, 'Sai tên/thứ tự cột.'
assert rows, 'CSV mới có header; hãy tự điền dữ liệu.'
assert all(None not in r and all(v is not None and v != '' for v in r.values()) for r in rows), 'Có dòng thiếu/thừa cột hoặc ô trống.'
inputs = [tuple(r[k] for k in header[:7]) for r in rows]
assert len(set(inputs)) == len(inputs), 'Có tổ hợp input trùng.'
assert 'CHƯA ĐIỀN' not in (folder / 'cases-notes.md').read_text(), 'Chưa hoàn thành notes.'
print(f'CSV cấu trúc OK: {len(rows)} ca. Chưa xác nhận expected/độc lập thay tác giả.')
PY
```

**Expected:** `CSV cấu trúc OK: N ca`, với N là số dòng bạn thực sự viết.
Đây là kiểm cấu trúc; review expected và nguồn dữ liệu bằng người trước khi khóa.

### 2.3. Nhập đúng tên tác giả và freeze

```bash
read "HUMAN_AUTHOR?Tên người thực sự tự viết CSV: "
python3 scripts/ai_generate.py freeze \
  --class "$AI_CLASS" --csv ai/human/loan-service/cases.csv \
  --author "$HUMAN_AUTHOR" --attest-independent \
  --output "$AI_HUMAN"
```

**Expected:** `Human data frozen: .../ai/human/loan-service/frozen`; có `cases.csv` và
`receipt.json`. Đây là lệnh offline. Nếu `frozen/` đã có, không freeze đè; chỉ xác minh mục 2.4
nếu đó chính là bộ muốn dùng. Không tự sửa receipt/hash hoặc xác nhận thay tác giả.

### 2.4. Xác minh hash và commit bộ human trước so sánh

```bash
python3 - <<'PY'
import json, os, sys
from pathlib import Path
sys.path.insert(0, 'scripts')
import ai_csv
receipt = ai_csv.check_frozen(Path(os.environ['AI_HUMAN']), 'vn.edu.seminar.loan.LoanService')
print(json.dumps(receipt, ensure_ascii=False, indent=2))
PY
git add -- ai/human/loan-service/cases.csv ai/human/loan-service/cases-notes.md ai/human/loan-service/frozen
git diff --cached --stat
git commit -m "test(loan): freeze human CSV before the new AI demo"
```

**Expected:** receipt đúng tác giả, class `vn.edu.seminar.loan.LoanService`, số ca và SHA-256;
commit chỉ chứa dữ liệu/notes/receipt Loan đã chọn. Nếu không có thay đổi để commit, kiểm
`git log -1` và receipt; không tạo commit giả. Hash không chứng minh quá trình viết độc lập.

## 3. Quay baseline chưa có test Gemini mới

### 3.1. Kiểm hai file cũ đã gỡ

```bash
python3 - <<'PY'
from pathlib import Path
folder = Path('case-study/src/test/java/vn/edu/seminar/loan')
for name in ('LoanServiceGeminiDraftTest.java', 'LoanServiceGeminiAdditionalTest.java'):
    assert not (folder / name).exists(), f'{name} đã có; không chạy apply trùng.'
assert (folder / 'LoanServiceTest.java').exists()
assert Path('case-study/src/main/java/vn/edu/seminar/loan/LoanService.java').exists()
print('OK: hai test Gemini chưa có; service và test chuẩn còn nguyên.')
PY
```

**Expected:** dòng `OK` như trên. Không cần gỡ các fixture `LoanServiceAi*Test`;
profile chuẩn đã loại chúng và runner AI chỉ build test vừa sinh trong thư mục tạm.

### 3.2. Chạy baseline thật

```bash
case-study/mvnw -B -ntp -f case-study/pom.xml clean verify | tee "$GA_RUN/baseline.log"
```

**Expected trên baseline đã chuẩn bị:** `Tests run: 39, Failures: 0, Errors: 0, Skipped: 0`,
`All coverage checks have been met`, `BUILD SUCCESS`. Chỉ tiếp tục khi pass.
Nếu bạn thay source/test sau preparation thì dùng số đo thực tế.

### 3.3. Mở source và coverage

```bash
open -t case-study/src/main/java/vn/edu/seminar/loan/LoanService.java
open case-study/target/site/jacoco/vn.edu.seminar.loan/LoanService.java.html
```

**Expected:** source `borrow` và JaCoCo LoanService, hiện LINE 17/17, BRANCH 6/6.
Lời dẫn: “Đây là suite chuẩn 39 test. Bước tiếp theo đo riêng test AI sinh ra,
không cộng coverage của suite chuẩn vào kết quả AI-1.” Gate chuẩn hiện kiểm nhánh
FineCalculator >=90%, không phải một gate 90% riêng cho LoanService.

## 4. Tạo draft PR trước khi chạy AI-1

### 4.1. Push nhánh preparation

```bash
git status --short
git push -u origin "$AI_BRANCH"
```

**Expected:** status sạch; Git báo nhánh được push và theo dõi `origin/codex/loan-ai-demo-20261030`.
Push này đưa checkpoint gỡ test, hướng dẫn và bộ human lên nhánh demo, chưa đổi `seminar-core`.
Nếu có file khác chưa commit, kiểm tra trước; không dùng `git add .` để gom mọi thứ.

### 4.2. Chuẩn bị nội dung và tạo PR

```bash
cat > "$GA_RUN/pr-body-initial.md" <<'BODY'
Làm lại demo Gemini trên LoanService: gỡ hai test Gemini cũ ở nhánh demo để quay lại quá trình sinh, review và apply. Giữ service và test chuẩn của nhóm.

Baseline sau gỡ: 39 tests pass, coverage gate pass. CSV human Loan được khóa trước khi sinh output AI mới; nguồn và tác giả ghi trong notes/receipt. Sau AI-1/AI-2 sẽ apply test đã review rồi push tiếp lên cùng PR để xem CI và Gemini AI-3.

PR demo ở trạng thái draft, chưa đề nghị merge. Kết quả baseline không phải kết quả của test AI mới.
BODY
gh pr create --repo "$GH_REPO" --draft \
  --base seminar-core --head "$AI_BRANCH" \
  --title "test(loan): replay Gemini AI-1 to AI-4 demo" \
  --body-file "$GA_RUN/pr-body-initial.md"
```

**Expected:** trả URL một **draft PR mới**, base `seminar-core`, head là nhánh demo;
không phải PR #13. Đây là PR cho lượt làm lại, ban đầu sẽ thấy hai file Gemini bị xóa.
Workflow có trigger `pull_request` nên draft PR cũng chạy CI/AI-3. Nếu báo PR đã tồn tại,
không tạo thêm; dùng mục 4.3 lấy PR hiện có.

### 4.3. Lưu số PR và mở trình duyệt

```bash
export AI_PR="$(gh pr view "$AI_BRANCH" --repo "$GH_REPO" --json number --jq .number)"
printf '%s\n' "$AI_PR" > "$GA_RUN/pr-number.txt"
gh pr view "$AI_PR" --repo "$GH_REPO" --json number,url,isDraft,baseRefName,headRefName
gh pr view "$AI_PR" --repo "$GH_REPO" --web
```

**Expected:** số PR mới, `isDraft: true`, đúng base/head, browser mở PR đó. Không lấy số
PR cố định từ tài liệu. Lời dẫn: “Tôi tạo PR trước; sau khi apply sẽ cập nhật cùng PR này.”

### 4.4. Chờ lượt CI baseline xong trước khi cập nhật tiếp

```bash
gh pr checks "$AI_PR" --repo "$GH_REPO" --watch --interval 10
```

**Expected:** lần lượt có `AI tooling offline checks`, `test (JDK 25)`, `coverage-gate`,
`package`, `Gemini diff review (advisory)`, `AI review and CI summary`.
JUnit/gate/package dự kiến pass từ baseline đã kiểm. Gemini phụ thuộc Secret/model/quota
trên GitHub; check xanh một mình chưa chứng minh API đã review hoàn chỉnh, cần đọc comment.
Nếu mới mở PR chưa có check, đợi chúng xuất hiện trong tab Checks rồi chạy lại lệnh.
Lỗi API hoặc check đỏ: xem log/comment, không mặc định nguyên nhân là coverage.

## 5. AI-1 — sinh test Loan mới và tự đo

### 5.1. Gọi Gemini

```bash
python3 scripts/ai_generate.py ai1 \
  --class "$AI_CLASS" --model gemini-3.6-flash \
  --output "$GA_RUN/ai1"
```

**Expected nếu API/code thành công:** in output path, `JUnit/JaCoCo`, `Tests=N`,
`failures=0`, `errors=0`, `passed=True`; có test Java và báo cáo thật. Có thể có tối đa
hai vòng repair kỹ thuật. Số test/coverage không cố định; không hứa 7 test như lượt cũ.

### 5.2. Kiểm trạng thái rồi xem review

```bash
python3 - <<'PY'
import json, os
from pathlib import Path
folder = Path(os.environ['GA_RUN']) / 'ai1'
stage = json.loads((folder / 'stage.json').read_text())
run = json.loads((folder / 'run.json').read_text())
assert stage['completed'] and run['passed'], 'AI-1 chưa pass; đọc logs trước AI-2.'
print('AI-1 PASS:', run['tests'], 'tests; coverage:', run['target_coverage'])
PY
cat "$GA_RUN/ai1/review.md"
open -t "$GA_RUN/ai1/generated/LoanServiceGeminiDraftTest.java"
open "$GA_RUN/ai1/site/jacoco/vn.edu.seminar.loan/LoanService.java.html"
```

**Expected:** AI-1 PASS, review có số đo, editor mở test mới và browser mở coverage
**chỉ của test AI-1**. Chỉ vào một assertion và nhánh tương ứng. Source/test chuẩn chưa bị ghi.
Nếu API fail trước sinh code có thể chưa có `run.json`/`review.md`; xem mục 11, không tiếp AI-2.

## 6. AI-2 — đọc đúng test/coverage AI-1 và bổ sung

### 6.1. Gọi bước bổ sung

```bash
python3 scripts/ai_generate.py ai2 \
  --from-ai1 "$GA_RUN/ai1" --model gemini-3.6-flash \
  --output "$GA_RUN/ai2"
```

**Expected nếu thành công:** dùng baseline AI-1 vừa đo; giữ nguyên draft; chạy draft cùng
phần bổ sung. Nếu baseline đã đủ mọi counter, model có thể trả `no_additions_needed`.
Không bắt buộc có file Additional và không bắt buộc coverage tăng.

### 6.2. Đọc kết quả và code trước apply

```bash
python3 - <<'PY'
import json, os
from pathlib import Path
folder = Path(os.environ['GA_RUN']) / 'ai2'
stage = json.loads((folder / 'stage.json').read_text())
run = json.loads((folder / 'run.json').read_text())
assert stage['completed'] and run['passed'], 'AI-2 chưa đủ điều kiện apply; kiểm logs.'
print('AI-2 PASS:', run['tests'], 'tests; assessment:', stage['assessment'])
print('Files:', sorted(p.name for p in (folder / 'generated').glob('*.java')))
PY
cat "$GA_RUN/ai2/review.md"
cat "$GA_RUN/ai2/analysis.md"
cat "$GA_RUN/ai2/comparison.json"
open "$GA_RUN/ai2/generated"
```

**Expected:** PASS; assessment có thể `coverage_increased`, `no_coverage_gain_needs_review`
hoặc `no_additions_proposed_needs_review`. Người review phải mở Java đọc expected,
assertion, stub và interaction. Coverage regressed/not comparable/tests failed thì dừng.
Lời dẫn: “Pass và tăng coverage là hai kết luận riêng; tôi review assertion trước khi apply.”

## 7. Review → apply → commit/push lên cùng PR

### 7.1. Preview file sẽ sync và output sẽ dọn

```bash
python3 scripts/ai_apply.py --from-ai2 "$GA_RUN/ai2"
```

**Expected:** JSON liệt kê DraftTest và AdditionalTest nếu có, đường dẫn đích trong
`case-study/src/test/java/vn/edu/seminar/loan/`; cuối có `Preview only`.
Không còn lỗi trùng hai file đã gỡ. Chưa ghi source/xóa output ở bước preview.

### 7.2. Apply sau khi bạn thực sự review

```bash
python3 scripts/ai_apply.py --from-ai2 "$GA_RUN/ai2" \
  --apply --reviewed --reviewer "Ngô Gia An - 23120205" \
  | tee "$GA_RUN/apply-result.log"
```

**Expected:** full suite + ứng viên + gate pass; JSON có `applied: true`,
`integration.passed: true`, `output_deleted: true`; cuối báo `Synced reviewed tests`.
Tổng test thường là **39 + số test ứng viên thực sự chạy**, không ép bằng 49.
Hai thư mục `ai1/`, `ai2/` bị xóa sau sync; log apply/baseline và file PR trong `$GA_RUN`
được giữ. Vì vậy quay review/coverage AI-1/2 trước khi chạy lệnh này.

Nếu lệnh fail, không commit như đã thành công: xem output và `ai2/integration/output.log`
nếu còn. Nếu báo synced nhưng cleanup lỗi, không apply lần nữa; kiểm các file đã được sync.

### 7.3. Xem và commit đúng các file test mới

```bash
git status --short
git diff --stat
git diff -- case-study/src/test/java/vn/edu/seminar/loan/LoanServiceGeminiDraftTest.java case-study/src/test/java/vn/edu/seminar/loan/LoanServiceGeminiAdditionalTest.java
python3 - <<'PY'
import subprocess
from pathlib import Path
folder = Path('case-study/src/test/java/vn/edu/seminar/loan')
paths = [str(folder / name) for name in ('LoanServiceGeminiDraftTest.java', 'LoanServiceGeminiAdditionalTest.java') if (folder / name).is_file()]
assert paths, 'Không có file ứng viên đã apply.'
subprocess.run(['git', 'add', '--', *paths], check=True)
PY
git diff --cached --stat
git diff --cached -- case-study/src/test/java/vn/edu/seminar/loan/LoanServiceGeminiDraftTest.java case-study/src/test/java/vn/edu/seminar/loan/LoanServiceGeminiAdditionalTest.java
git commit -m "test(loan): apply reviewed Gemini tests from the recorded demo"
git push origin "$AI_BRANCH"
```

**Expected:** trước stage, file mới có thể là `??`, nên `git diff` chưa hiện nội dung;
sau stage thấy đầy đủ diff. Commit chỉ nhận file Gemini thực sự có, không lỗi glob khi
AI-2 không tạo Additional. Push cập nhật **cùng PR**, không cần `gh pr create` lần hai.
Nhánh vẫn chưa được merge.

### 7.4. Cập nhật mô tả PR theo kết quả vừa apply

```bash
python3 - <<'PY'
import json, os
from pathlib import Path
run = Path(os.environ['GA_RUN'])
text = (run / 'apply-result.log').read_text()
result, _ = json.JSONDecoder().raw_decode(text.lstrip())
assert result.get('applied') and result['integration']['passed']
count = result['integration']['tests']
files = '\n'.join('- ' + name for name in result['files'])
body = f'''Làm lại demo Gemini trên LoanService: sinh test từ source, bổ sung từ coverage, review và apply vào src/test. Nhánh giữ checkpoint gỡ test cũ trước lượt quay; production và test chuẩn được giữ nguyên.

Các file đã apply:
{files}

Validation local khi apply: {count} tests, 0 failures/errors/skipped, full suite và coverage gate pass. Kết quả chi tiết của PR nằm trong Checks và comment AI-3 cho head mới nhất. Coverage toàn suite không nhất thiết tăng vì suite chuẩn đã phủ LoanService.

CSV human Loan được khóa trước output AI mới; nguồn/tác giả nằm trong notes và receipt. AI-4 chạy local qua cùng harness, xem kết quả thực tế trong video. PR demo ở trạng thái draft, chưa đề nghị merge.
'''
(run / 'pr-body-final.md').write_text(body)
print('Đã tạo mô tả từ kết quả apply thực tế:', count, 'tests.')
PY
gh pr edit "$AI_PR" --repo "$GH_REPO" --body-file "$GA_RUN/pr-body-final.md"
```

**Expected:** mô tả PR có số test thực tế, không dùng số test từ lượt demo cũ.
Nội dung không tuyên bố AI-4 đã pass trước khi chạy.

## 8. AI-3 — quay CI và comment của PR mới

### 8.1. Mở và chờ Checks cho head vừa push

```bash
git rev-parse HEAD
gh pr view "$AI_PR" --repo "$GH_REPO" --json url,headRefOid,isDraft
gh pr view "$AI_PR" --repo "$GH_REPO" --web
gh pr checks "$AI_PR" --repo "$GH_REPO" --watch --interval 10
```

**Expected:** PR head SHA khớp commit local mới; draft vẫn true. Đợi check của SHA mới,
không nhận check baseline xanh là kết quả của test vừa push. Trong browser kiểm commit ở
Checks đã đổi; nếu CLI chưa thấy check mới, đợi chúng xuất hiện rồi chạy lại watch.
JUnit/gate/package dự kiến pass; API review có thể gặp quota/lỗi dịch vụ cần đọc riêng.

### 8.2. Đọc comment AI-3

```bash
gh api "repos/$GH_REPO/issues/$AI_PR/comments?per_page=100" \
  --jq '.[] | select(.user.login == "github-actions[bot]" and (.body | contains("<!-- seminar-gemini-ai3 -->"))) | {url: .html_url, body: .body}'
```

**Expected:** comment bot có SHA mới, link Actions, bảng test/gate/package, số đo CI và
nhận xét Gemini hoặc thông báo chưa review được. Khi không có finding, nói “Gemini không
nêu finding trên diff này”, không kết luận mọi test đều đúng. Nếu API lỗi, không gọi đó là
review hoàn chỉnh chỉ vì job/comment đã chạy. Mở comment trên browser để quay dễ đọc.

Lời dẫn: “AI-3 đọc diff PR song song với CI; JUnit/JaCoCo đo test và coverage. Comment
kết hợp hai nguồn, AI không quyết định pass/fail và không tự merge.” Không cần gọi
`ai_review.py --live` local cho đoạn này. Không dùng lại PR #13 như kết quả của lượt mới.

## 9. AI-4 — Loan human so với Loan AI

### 9.1. Sinh CSV AI riêng và chạy hai bộ

```bash
python3 scripts/ai_generate.py ai4 \
  --class "$AI_CLASS" --human-frozen "$AI_HUMAN" \
  --model gemini-3.6-flash --output "$GA_RUN/ai4"
```

**Expected nếu thành công:** schema/harness được sinh từ source và header human; request
sinh dữ liệu AI không có dòng CSV human hoặc test AI-1/2. Chạy hai lượt Java qua cùng
harness/source. Output có `report.md`, `comparison.json`, `reconciliation.json`,
`human/run.json`, `ai/run.json`. Bước này có hai lượt generation schema/data riêng,
không có repair harness tự động như AI-1/2; lỗi compile/assertion cần review.

### 9.2. Kiểm trạng thái và mở báo cáo

```bash
python3 - <<'PY'
import json, os
from pathlib import Path
folder = Path(os.environ['GA_RUN']) / 'ai4'
stage = json.loads((folder / 'stage.json').read_text())
result = json.loads((folder / 'reconciliation.json').read_text())
assert stage['completed'] and result['consistent'], 'AI-4 chưa pass; đọc report/logs.'
print('AI-4 PASS; human rows sent to model:', stage['human_rows_sent_to_model'])
for name, run in result['executions'].items():
    print(name, 'tests:', run['tests'], 'failures:', run['failures'], 'errors:', run['errors'], 'coverage:', run['coverage'])
PY
cat "$GA_RUN/ai4/report.md"
open -t "$GA_RUN/ai4/schema.json"
open -t "$GA_RUN/ai4/generated/LoanServiceGeminiCsvTest.java"
open -t "$GA_RUN/ai4/generated/cases.csv"
open "$GA_RUN/ai4/human/site/jacoco/vn.edu.seminar.loan/LoanService.java.html"
open "$GA_RUN/ai4/ai/site/jacoco/vn.edu.seminar.loan/LoanService.java.html"
```

**Expected:** `human rows sent to model: False`; số test mỗi bên khớp CSV, không failures/
errors/skipped khi pass; reconciliation nhất quán. Số ca/nhánh/expected chung phụ thuộc
bộ thực tế, không lấy số 23/13 hoặc 100%/80% của FineCalculator cho Loan.

Review schema/harness: parse đúng cột, kiểm `LoanException.code()`, phiếu được lưu,
clock cố định và trạng thái sách. Cùng harness không chứng minh harness đúng. Chỉ rõ
ca thiếu/thêm, expected mâu thuẫn nếu có; đối chiếu yêu cầu, không tự nhận người hay AI đúng.
Coverage CSV này đo riêng LoanService và không chạy gate chuẩn.

## 10. Nếu đóng Terminal giữa chừng

Chỉ chạy khối này để khôi phục **phiên đã tạo**; không chạy lại mục 1.3 tạo lượt khác:

```bash
cd "/Users/ngogiaan1103/Documents/ChatGPT/seminar-testing 2"
git switch codex/loan-ai-demo-20261030
setopt PIPE_FAIL
export AI_BRANCH="codex/loan-ai-demo-20261030"
export GH_REPO="nhaajtdajt/seminar-testing-unitTest-coverage-cicd"
export AI_CLASS="LoanService"
export AI_HUMAN="ai/human/loan-service/frozen"
export GA_RUN="$(cat .ai-work/loan-video-current-run.txt)"
if [ -f "$GA_RUN/pr-number.txt" ]; then
  export AI_PR="$(cat "$GA_RUN/pr-number.txt")"
fi
printf 'Output: %s\n' "$GA_RUN"
```

**Expected:** đúng thư mục lượt cũ. Tiếp tục bước đang dở dựa vào `stage.json`; không chạy
ai1/ai2/ai4 đè folder có sẵn. Nếu đã apply thành công thì ai1/ai2 đã bị dọn, dùng file test
trong `src/test` và log apply, không cố gọi AI-2 lại với baseline đã xóa.

## 11. Lỗi thường gặp và kết thúc video

| Tình huống | Cách xử lý |
|---|---|
| API 503/timeout/quota | Đọc `stage.json`, `attempts/*/model/api.json` hoặc `model/api.json`; giữ đúng trạng thái thất bại. Retry lượt mới, không tái dùng file cũ làm kết quả mới |
| AI-1/2 compile hoặc Mockito setup lỗi | Runner repair kỹ thuật tối đa hai vòng; xem `attempts.json`/`output.log` |
| Assertion fail | Dừng review oracle và source; không sửa expected chỉ để test xanh |
| Apply báo trùng file | Kiểm nhánh và hai file đích. Đã apply thì không apply lần hai; source cũ xuất hiện thì chưa ở đúng baseline |
| Apply source/hash drift | Source/build/test đã đổi; đo lại lượt mới, không sửa hash |
| AI-4 thiếu report | Kiểm `schema-stage/`, `stage.json`, output Java; không mở file chưa sinh |
| PR xanh nhưng thiếu review Gemini | Đọc comment/log quota/Secret/model; chưa được nhận là AI-3 hoàn chỉnh |
| PR còn báo xóa AdditionalTest | AI-2 có thể không sinh bổ sung; đó là diff thực tế so với base, cần review và giữ PR draft nếu chỉ demo |

Sau khi đã quay xong, xem trạng thái:

```bash
git status --short --branch
gh pr view "$AI_PR" --repo "$GH_REPO" --json url,state,isDraft
```

**Expected:** vẫn nhánh demo, PR OPEN và draft. Không có lệnh merge trong kịch bản.
Có thể quay lại `seminar-core` sau khi đã commit/cất các thay đổi muốn giữ:

```bash
git switch seminar-core
```

**Expected:** trở về bản tích hợp; test Gemini cũ hiện lại là đúng vì thuộc nhánh đó.
Không dùng `reset --hard` hay `clean -fd` để bắt đầu lại.

Chỉ dọn payload/Java output sau khi đã xem/ghi hình xong:

```bash
python3 scripts/clean_ai.py --root "$GA_RUN"
```

**Expected:** `PREVIEW`, chưa xóa gì. Nếu danh sách đúng và muốn dọn:

```bash
python3 scripts/clean_ai.py --root "$GA_RUN" --apply
```

**Expected:** dọn Java/payload local của phiên, giữ CSV/receipt/report và source thật.
Không clean trước khi hoàn thành AI-4. Ghi URL và timestamp thực tế khi video đã quay;
preparation và PR không thay cho video hoàn chỉnh.
