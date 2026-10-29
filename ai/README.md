# Chạy Gemini AI-1, AI-2, AI-3 và AI-4

Ngô Gia An (23120205). Hướng dẫn cho người tự chạy demo; không cần lưu/nộp evidence.
Source, prompt và script được giữ trong Git. Output sinh ra chỉ dùng local, được Git bỏ qua.

## Luồng hoạt động

```text
Bạn chọn class trong src/main/java
    ↓
Script đọc trực tiếp source + dependency/domain/schema liên quan
    ├── AI-1: sinh Java test → JUnit/JaCoCo → tối đa 2 vòng sửa lỗi kỹ thuật
    ├── AI-2: đọc test nháp + kết quả thật → bổ sung → chạy lại → review.md
    │         → người review → apply → full suite/gate → src/test → dọn output
    └── AI-4: CSV người viết đã có trước
              → Gemini suy ra schema/harness theo src và header
              → Gemini sinh CSV riêng, không xem dữ liệu người
              → chạy hai CSV → đối chiếu JUnit/JaCoCo → report.md
```

Gemini API không tự mở filesystem trên máy. Script đọc file rồi gửi nội dung cần thiết.
Không lưu bản copy source trong output. Khi chạy test, source được copy vào thư mục tạm
hệ thống để không trộn với test chuẩn; thư mục build tạm được dọn khi kết thúc.
Chỉ hash/context nhỏ được giữ để phát hiện source thay đổi giữa AI-1 và AI-2.
Output AI-1/AI-2 phải nằm trong thư mục con của `.ai-work/` (hoặc đường dẫn
`gemini-live` cũ) để apply có thể dọn đúng phạm vi sau khi sync test.

Không có mức phí, hạn mức hoặc schema nghiệp vụ mặc định trong runner/prompt.
Class/service mới được tự phát hiện. Có thể thêm `--requirements <file.md>` và
`--schema <schema.sql/json>` để đưa yêu cầu độc lập hoặc schema domain riêng.
Nếu chỉ có source, AI đang kiểm hành vi implementation; không tự chứng minh đúng nghiệp vụ.

## 1. Chuẩn bị môi trường và key một lần

Mở Terminal tại gốc repo; các lệnh sau dùng cùng Terminal:

```bash
cd "/Users/ngogiaan1103/Documents/ChatGPT/seminar-testing 2"
java -version
case-study/mvnw -v
```

Cần Java 25 và Python 3.10+. Maven Wrapper nằm sẵn trong repo. Nếu Java chưa đúng,
chọn JAVA_HOME theo README chính trước khi tiếp tục.

Mở `.env.gemini` ở gốc repo và điền key tại máy:

```dotenv
GEMINI_API_KEY=KEY_CUA_BAN
AI_MODEL=gemini-3.6-flash
```

Model trên là model bạn đã chạy thành công; có thể đổi sang model tài khoản có quyền.
Không gửi key vào chat. Script tự đọc file, không cần nhập lại hoặc `source`.
Trên máy mới, chỉ copy example nếu chưa có cấu hình:

```bash
if [ ! -f .env.gemini ]; then
  cp ai/gemini.env.example .env.gemini
fi
chmod 600 .env.gemini
python3 scripts/gemini_client.py status
```

Expected: `key_configured: true`; status không hiển thị key, không gọi API.
Biến môi trường nếu có được ưu tiên hơn file; `--model` ghi đè model cho riêng lệnh đó.

## 2. AI-4: phải tự thiết kế CSV trước

Làm bước này trước khi xem test/data AI của class cần đối chứng. CSV chứa **input và
expected output/exception**, không chỉ input. Tên/thứ tự cột do bạn thiết kế dựa trên API,
đặc tả và trạng thái dependency của class; runner không bắt mọi lớp dùng schema tính phí.

Ví dụ LoanService có thể cần cột tham số mượn, trạng thái sách/thành viên, số sách đang giữ,
nợ phí và kết quả mong đợi. Bạn tự chọn ca và tính expected; không nhờ AI viết bộ human.
Không cần gọi model để lấy schema trước: script có thể khóa CSV ngay khi bạn tự viết xong.

Lưu input bền vững ngoài output tạm, ví dụ `ai/human/loan-service/cases.csv`, rồi khóa offline:

```bash
python3 scripts/ai_generate.py freeze \
  --class LoanService --csv ai/human/loan-service/cases.csv \
  --author "Ngô Gia An - 23120205" --attest-independent \
  --output ai/human/loan-service/frozen
```

Lệnh này không gọi Gemini. Nó kiểm cấu trúc CSV, lưu bản nguyên vẹn và receipt/hash;
schema về ý nghĩa cột được suy ra sau từ source và header. Không dùng lại output frozen đã có.
Nếu đã xem test/data AI thì không tuyên bố bộ mới là đối chứng độc lập; nhờ người chưa xem
thiết kế hoặc ghi đúng nguồn tham khảo.

**FineCalculator:** bạn đã có CSV/notes và bản khóa ở `ai/human/frozen`; dùng luôn, không freeze lại.

## 3. Chọn class và thư mục local

```bash
python3 scripts/ai_generate.py list-classes
```

Không gọi API. Có thể dùng simple name nếu duy nhất, hoặc tên đầy đủ. Hỗ trợ top-level
Java types trong Maven module; dependency local được tìm theo type/import. Nên chọn
concrete class có hành vi; interface trừu tượng không tự tạo thành bài test nghiệp vụ.

Ví dụ chạy cả ba phần với CSV FineCalculator đã chuẩn bị:

```bash
AI_CLASS="FineCalculator"
AI_HUMAN="ai/human/frozen"
GA_RUN=".ai-work/${AI_CLASS}-$(date +%Y%m%d-%H%M%S)"
```

Với LoanService, đổi `AI_CLASS="LoanService"`, `AI_HUMAN="ai/human/loan-service/frozen"`
sau khi đã tự thiết kế/khóa đúng bộ CSV của LoanService. Không đưa CSV FineCalculator vào LoanService.

`.ai-work/` là output local mặc định, không phải evidence cần commit. Lệnh luôn dùng thư mục
mới để không ghi đè test/baseline đang xem. Không cần tự tạo `$GA_RUN` trước.

## 4. AI-1: sinh test nháp và tự chạy

```bash
python3 scripts/ai_generate.py ai1 \
  --class "$AI_CLASS" --output "$GA_RUN/ai1"
open "$GA_RUN/ai1"
```

Gemini nhận source class và dependency liên quan, suy ra constructor/API/mock state/biên,
trả code. Script tự lưu `generated/<Class>GeminiDraftTest.java`, rồi chạy JUnit và JaCoCo.
Bạn không cần copy-paste code hoặc sửa test chuẩn.

Runner kiểm tra hợp đồng test, chạy code và chỉ tự sửa lỗi kỹ thuật (compile/import/API,
cách khai báo Mockito stub) tối đa **2 vòng**. Dùng `--max-repairs 0`, `1` hoặc `2`
để chọn ngân sách. Mỗi vòng gọi model còn có retry API giới hạn riêng, không đồng
nghĩa một vòng chỉ có một HTTP request. Mọi vòng nằm trong `attempts/`, không tự ghi src.
Assertion fail, timeout hoặc source đổi sẽ dừng để review; vòng repair cũng bị dừng
nếu làm thay đổi/xóa assertion cũ. Đó là kiểm tra cú pháp bảo thủ, không chứng minh
expected đúng nghiệp vụ. Giới hạn API/setup/repair không thay cho người review.

Model mặc định là **gemini-3.6-flash**. Khi dịch vụ tạm lỗi, có thể tăng số lần retry
tuần tự (mặc định 3, cho phép 1–10) và chọn timeout mỗi request (mặc định 180 giây,
cho phép 10–180). Backoff tăng dần, tối đa 30 giây; không tự đổi model:

```bash
GEMINI_MAX_ATTEMPTS=8 GEMINI_API_TIMEOUT=90 \
  python3 scripts/ai_generate.py pipeline --class LoanService \
  --model gemini-3.6-flash --output "$GA_RUN"
```

Chọn `$GA_RUN` mới cho mỗi lượt. Các biến trên chỉ áp dụng cho lệnh đó; key vẫn được
đọc tự động từ `.env.gemini`. Retry API khác vòng sửa code; lỗi key/model/quyền không
được retry như lỗi dịch vụ tạm thời.

Xem `analysis.md`, file Java mới, `run.json` và `output.log`. Expected kỹ thuật:
`run.json.passed: true`, có test thực sự chạy, không failures/errors và có counter target.
Số test và coverage phụ thuộc kết quả thật, không có số cố định phải đạt trong demo.
`review.md` là bản tóm tắt để đọc, `review.json` khóa hash test và kết quả đo.

## 5. AI-2: bổ sung từ đúng test/coverage vừa chạy

Chỉ chạy khi AI-1 pass:

```bash
python3 scripts/ai_generate.py ai2 \
  --from-ai1 "$GA_RUN/ai1" --output "$GA_RUN/ai2"
open "$GA_RUN/ai2"
```

AI-2 tự lấy target, đọc source hiện tại và kiểm hash với baseline. Nếu production/build
input đã đổi hoặc test nháp bị sửa sau khi đo, script dừng để không dùng coverage cũ.
Không cần bản source copy trong output; không cần truyền lại dữ liệu bằng tay.

Output có `generated/<Class>GeminiAdditionalTest.java`, bản nháp giữ nguyên và
`comparison.json` so before/after. Test nháp và bổ sung được chạy chung trong thư mục tạm.
Nếu AI-1 đã đạt 100% branch, AI-2 có thể thêm ca/assertion hữu ích mà coverage không tăng.
Nếu toàn bộ counter target đã đầy đủ và không tìm được bổ sung có ích, AI-2 được trả
`no_additions_needed`; lúc đó output chỉ giữ bản nháp đã chạy lại, không cố sinh test trùng.

Đọc `ai2/review.md`: `coverage_increased`, `no_coverage_gain_needs_review`,
`no_additions_proposed_needs_review`, `coverage_regressed` hoặc `tests_failed`.
Test pass và cải thiện coverage là hai kết luận riêng. Coverage giảm/không so sánh
được sẽ không được apply. Không tăng coverage vẫn cần bạn đánh giá ca mới/assertion.

### Chạy AI-1 → AI-2 bằng một lệnh

Nếu chỉ làm phần sinh test, không cần CSV/AI-4:

```bash
AI_CLASS="LoanService"
GA_RUN=".ai-work/${AI_CLASS}-$(date +%Y%m%d-%H%M%S)"
python3 scripts/ai_generate.py pipeline --class "$AI_CLASS" \
  --model gemini-3.6-flash --output "$GA_RUN"
open "$GA_RUN/ai2/review.md"
```

AI-2 chỉ chạy sau khi AI-1 pass. Nếu AI-1 dừng sau khi đo, đọc `ai1/review.md`, `attempts.json`
và output của lượt tương ứng. Nếu API lỗi trước khi có code, có thể chưa có review.md;
xem `stage.json` và `attempts/<số-vòng>/model/api.json`. Không tự coi AI-2 đã hoàn thành. Có thể thêm
`--requirements`, `--schema`, `--max-repairs` như khi chạy từng bước.

### Review → apply → xóa output → PR

1. Đọc `ai2/review.md`, `analysis.md`, các file Java trong `ai2/generated` và report thật.
   Kiểm expected, assertion, mock state, ca trùng và giới hạn source-only.
2. Xem trước file sẽ sync và thư mục output sẽ xóa:

```bash
python3 scripts/ai_apply.py --from-ai2 "$GA_RUN/ai2"
```

Preview không gọi API/Maven, không ghi source hoặc xóa output. Nếu đồng ý sau khi
đã đọc, chạy apply với tên người thực sự review (không điền thay người khác):

```bash
python3 scripts/ai_apply.py --from-ai2 "$GA_RUN/ai2" \
  --apply --reviewed --reviewer "Ngô Gia An - 23120205"
```

Apply không gọi Gemini. Script kiểm hash source/test/report, từ chối ghi đè test có sẵn,
chạy **full suite chuẩn + test ứng viên + coverage gate** trong bản sao tạm, kiểm ứng viên
có thực sự được chạy. Sau khi pass, nó tạo file mới ở package tương ứng trong
`case-study/src/test/java/`. Source/test/data đổi trong lúc verify thì dừng, không sync.
Nếu ghi file giữa chừng lỗi, các file mới vừa ghi được rollback; test cũ giữ nguyên.

Sau khi sync thành công, **xóa toàn bộ output AI-1/AI-2 của phiên**. Với lệnh `pipeline`,
cả `$GA_RUN` được xóa nếu chỉ chứa hai stage và metadata phiên. Nếu cùng thư mục còn
AI-4 hoặc dữ liệu khác, chỉ dọn hai stage; giữ AI-4, CSV human gốc, `.env.gemini` và
evidence paper. Không cần chạy cleaner thêm cho lượt đã apply. Lượt apply lỗi giữ output;
nếu chỉ cleanup lỗi sau khi đã sync, script báo rõ trạng thái đó, không apply lần nữa.

Nếu sửa file ứng viên/report sau khi đo, apply từ chối để tránh dùng số đo cũ.
Hãy giữ lượt này để kiểm tra và sinh/đo một lượt mới trước khi apply. Tên file test đã
tồn tại cũng bị từ chối; script không tự ghi đè test bạn đã chỉnh hoặc commit.

Sau apply, dùng Git như bình thường. Tạo nhánh riêng **trước khi apply**; ví dụ từ
checkout sạch trên nhánh tích hợp (không chạy lệnh đổi nhánh khi đang có thay đổi riêng):

```bash
git switch -c "codex/ai-tests-$(date +%Y%m%d-%H%M%S)"
```

Sau khi apply, kiểm tra diff, chỉ add các file mới của class bạn chọn. Ví dụ LoanService:

```bash
git diff --stat
git status --short
git add case-study/src/test/java/vn/edu/seminar/loan/LoanServiceGemini*Test.java
git commit -m "test(loan): add reviewed Gemini unit tests"
git push -u origin HEAD
gh pr create --base seminar-core --title "test(loan): add reviewed Gemini tests" \
  --body "Test sinh bằng Gemini, đã review và chạy full suite/gate qua ai_apply. Xem CI để kiểm tra kết quả PR."
```

Nếu AI-2 không bổ sung file, chỉ có `GeminiDraftTest.java` để add. Script không tự
commit/push/tạo PR. PR mới sẽ chạy test/coverage/package và AI-3 như mục 10;
output local đã được dọn, Git chỉ nhận các file test đã chọn cùng thay đổi bạn chủ động add.

## 6. AI-4: sinh CSV AI riêng và đối chiếu báo cáo

```bash
python3 scripts/ai_generate.py ai4 --class "$AI_CLASS" \
  --human-frozen "$AI_HUMAN" --output "$GA_RUN/ai4"
open "$GA_RUN/ai4/report.md"
```

Script kiểm hash bộ human, chỉ gửi **header**, source/domain và yêu cầu cho bước schema.
Gemini tự suy ra kiểu/cột/expected và sinh harness theo class. Request riêng sinh CSV AI mới,
không có dòng dữ liệu human hoặc test AI-1/AI-2. Sau đó script:

1. So input/expected của hai bộ theo schema tương ứng.
2. Chạy từng CSV qua cùng harness, cùng phiên bản source.
3. Đối chiếu lại CSV, Surefire XML, JaCoCo XML và hash.
4. Xuất bảng tổng hợp `report.md` ngay tại output local.

Xem số ca, pass/fail/skipped, line/branch, input chung, ca thiếu/thêm và expected khác nhau.
Schema có thể khai báo alias Java tường minh để tên exception ngắn và đầy đủ không bị báo
mâu thuẫn giả; không tự gộp hai type khác package. Báo cáo tách khác biểu diễn với khác expected.

Nguồn chi tiết nếu cần xem tại chỗ: `schema.json`, `generated/cases.csv`, `comparison.json`,
`human/`, `ai/`, `reconciliation.json`. Không cần commit/export các file đó.
Test xanh/coverage cao không bảo đảm mọi ca biên đầy đủ; đây là giới hạn để giải thích trong demo.

## 7. Chạy cả ba bằng một lệnh

Sau khi hiểu từng bước và đã có CSV human đúng class:

```bash
python3 scripts/ai_generate.py all \
  --class "$AI_CLASS" --human-frozen "$AI_HUMAN"
```

Output tự nằm trong `.ai-work/<timestamp>-all/`. AI-2 bỏ qua nếu AI-1 không pass;
AI-4 vẫn được thử riêng. Đây là các lệnh live, dùng API quota. Không tự sửa nghiệp vụ hoặc
dùng kết quả cũ để làm lượt lỗi thành xanh. API có retry giới hạn cho lỗi tạm thời.

## 8. Đọc lỗi và bật debug khi cần

- API 503/timeout: lỗi dịch vụ tạm thời; thử lượt mới sau hoặc đổi model được phép.
- API 400/401/403/404/429: xem model/key/quyền/quota trong `model/api.json`.
- Java compile/assertion fail: xem `output.log`, file test mới và Surefire.
- Source đổi: chạy AI-1/schema mới, không sửa hash để ép dùng kết quả cũ.
- Class không có nhánh: BRANCH có thể N/A; không tự coi là thiếu test.
- Cửa sổ Terminal hiện `bquote>`: Ctrl+C; chỉ copy lệnh, không copy dấu ba backtick.

Mặc định không giữ full prompt/request/response chứa source. Khi thật sự cần debug,
thêm `--keep-payloads` vào lệnh; chúng vẫn nằm trong thư mục bị Git bỏ qua.
`--prepare-only` chủ động lưu prompt để bạn xem nhưng không gọi API hoặc Maven.

## 9. Clean sau khi xem xong demo

Xem trước danh sách và dung lượng:

```bash
python3 scripts/clean_ai.py
```

Dọn thật:

```bash
python3 scripts/clean_ai.py --apply
```

Hoặc chỉ dọn phiên đang xem:

```bash
python3 scripts/clean_ai.py --root "$GA_RUN" --apply
```

Cleaner chỉ hoạt động trong `.ai-work/` và output cũ `evidence/tuan-06/gemini-live/`.
Nó dọn Java sinh ra, bản copy `inputs/project` cũ và prompt/response debug chứa source.
Giữ nguyên source thật, `.env.gemini`, CSV human gốc, CSV output, receipt và báo cáo local.
Không clean giữa AI-1 và AI-2, hoặc trước khi AI-4 chạy xong: baseline/harness Java còn cần.
Đã clean thì tạo phiên mới để sinh/chạy lại khi demo lần sau.

Cả hai thư mục output đã được `.gitignore` bỏ qua, kể cả quên clean rồi `git add .`.
Không force-add chúng. Cleaner là dọn thủ công khi chưa/không apply; lệnh apply thành
công tự xóa output AI-1/AI-2. Runner/cleaner/apply không tự commit, push, merge hoặc triển khai server.

## 10. AI-3 tự động trong CI và comment PR

Sau khi đã commit/push phần tích hợp trên `seminar-core`, PR trong cùng repository
tự chạy workflow **Seminar CI** (`.github/workflows/ci.yml`):

```text
PR opened / synchronize / reopened
    ├── test (JDK 25) → coverage-gate → package (JAR)
    └── ai-review: Gemini đọc diff source/test/POM
                         ↓ đợi các job kết thúc, kể cả failure/skipped
                    ai-comment: cập nhật một comment trên PR
```

Bạn không cần gọi AI-3 local. AI-1/2/4 vẫn là các công cụ riêng ở những phần trước;
AI-3 không tự gọi chúng, sinh/sửa test hoặc merge PR. Gemini review chất lượng diff,
không quyết định JUnit pass/fail. JUnit/JaCoCo và Maven quyết định test/coverage gate.
Comment ghép **kết quả CI đo được** với **nhận xét Gemini chạy song song**; Gemini
không nhận các báo cáo sinh ra sau lượt review đó. Coverage job đỏ không luôn có nghĩa
thiếu coverage: cần xem log để phân biệt lỗi build/test/môi trường với vi phạm ngưỡng.

### Cấu hình GitHub một lần

Trong GitHub → repository → **Settings → Secrets and variables → Actions**:

- **Secrets**: thêm `GEMINI_API_KEY` (cùng key bạn đang dùng local).
- **Variables**: `AI_MODEL=gemini-3.6-flash`, hoặc model tài khoản có quyền.
- **Variables tùy chọn**: `GEMINI_MAX_ATTEMPTS` từ 1–10 (CI mặc định 6),
  `GEMINI_API_TIMEOUT` từ 10–180 giây (CI mặc định 90). Retry tuần tự có backoff;
  hết quota ngày thì dừng ngay, rate limit ngắn chờ theo RetryInfo nếu trong ngân sách.
- `AI_REVIEW_REF` mặc định `seminar-core`: nhánh tin cậy chứa automation đã push.
  Chỉ đổi khi nhóm đã chuyển automation sang nhánh khác được kiểm soát.

`.env.gemini` local không tự xuất hiện trên GitHub runner. Không commit file key.
`GITHUB_TOKEN` được GitHub tự cấp; job comment có `pull-requests: write`.
Nếu tổ chức chặn quyền ghi, người quản trị cần cho phép workflow dùng quyền này.
Không cần token cá nhân cho workflow. Giữ các required checks hiện có; AI là nhận xét
tham khảo, không thêm điều kiện vào job đóng gói.
Các thiết lập retry mới chỉ có hiệu lực khi nhánh automation tin cậy `AI_REVIEW_REF`
đã chứa phiên bản `gemini_client.py` hỗ trợ chúng; mặc định hiện trỏ `seminar-core`.

AI jobs checkout automation ở nhánh tin cậy, đọc diff PR bằng Git, không chạy code PR
với Gemini key/quyền comment. PR từ fork vẫn chạy test/coverage nhưng bỏ qua AI jobs
để không cấp secret cho nguồn ngoài. Chỉ các file đổi trong `case-study/src/` và
`case-study/pom.xml` được gửi; service mới trong cây source này tự được nhận diện.
Trong `src/` có cả `main/` và `test/`: AI-3 đọc thay đổi nghiệp vụ để nhận xét test
có bỏ sót nhánh mới hay không, không chỉ đọc diff thư mục test. Test AI-1/AI-2 ở
output local chưa commit vào PR không nằm trong diff này.
Diff quá 80 KB sẽ báo không review được, không cắt bớt rồi kết luận không có lỗi.

### Chạy thử và expected

1. Tạo nhánh tính năng, thay đổi source/test, commit và push; mở PR vào nhánh tích hợp.
2. Vào tab **Checks**: thấy lane test/gate/package và **Gemini diff review (advisory)**
   chạy độc lập. Mở job để biết API có hoàn thành hay không.
3. Đợi **AI review and CI summary**: bot tạo comment chứa SHA, link Actions,
   trạng thái ba job, tổng JUnit và line/branch từ JaCoCo nếu report có sẵn,
   cùng finding Gemini và vị trí file/dòng. Có bảng coverage từng class production đổi
   trong PR khi JaCoCo có dữ liệu của class đó.
4. Push commit mới lên cùng PR: bot cập nhật comment của nó. Lượt chạy cũ không
   ghi đè comment khi head PR đã đổi. Người review vẫn tự đánh giá finding.

Test lỗi → coverage/package có thể `skipped`, nhưng comment vẫn xuất hiện.
Coverage lỗi → package `skipped`, comment giữ trạng thái đỏ và số đo nếu có.
Gemini 503/quota/lỗi JSON → comment báo chưa có AI review hoàn chỉnh, vẫn hiển thị CI.
PR chỉ sửa docs/automation ngoài cây case study → không gọi Gemini, comment ghi rõ.
Lượt bị hủy chủ động không đăng comment. Xem artifact `ai-review` khi cần chẩn đoán;
nó chỉ chứa kết quả/context/hash API metadata, không lưu full source/prompt/key,
được tự xóa sau 1 ngày trên Actions và không được commit vào Git.

Workflow **AI fixture review (manual)** trong `ai-review.yml` chỉ dành cho diff mẫu
khi chạy tay, không comment PR; không cần bật thêm trigger PR ở workflow này.

Kiểm tra automation offline (không gọi API, không đăng comment):

```bash
python3 -m unittest discover -s scripts/tests -v
```

### Mẫu đã kiểm thử: PR #12, coverage đỏ → sửa test → CI xanh

[PR nháp #12](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/12)
dùng test riêng `Ai3PipelineSmokeTest`; không sửa production code hoặc test chuẩn của
thành viên khác, không merge file thử vào `seminar-core`. Đã xác nhận ngày 29/10/2026:

| Lượt | JUnit / coverage / package | Gemini và comment |
|---|---|---|
| [Commit e6745e0 — coverage đỏ](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40859123302) | 1 test pass; FineCalculator BRANCH 50% < gate 90%; coverage job failure, package skipped | Gọi API thật; phát hiện `NO_ASSERTION`; bot vẫn comment |
| [Commit 5a3b4ba — CI xanh](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40859373081) | 40 tests pass; JaCoCo toàn project LINE 76/83 (91,6%), BRANCH 24/24 (100%); package success | Gọi API thật; không nêu finding; cập nhật cùng comment theo head mới |

[Comment của bot](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/12#issuecomment-6494438628)
hiển thị lượt mới nhất. Xem lượt đỏ qua link Actions và commit tương ứng;
artifact chỉ giữ 1 ngày nên có thể đã hết hạn khi xem lại. Số test/coverage trong bảng
là kết quả của phiên này, có thể khác khi source và bộ test chuẩn thay đổi.

### Tự chạy lại mẫu trên một PR mới

Các lệnh dưới đây **tạo PR và gọi Gemini thật qua CI**, dùng quota của key trên GitHub.
Chạy từng bước, đợi kết quả rồi mới chuyển bước. Không cần chạy AI-1/AI-2 hoặc CSV AI-4.

**Bước 1 — Chuẩn bị nhánh demo.** GitHub Secret/model ở phần trên đã được cấu hình
trên repository của nhóm; không cần nhập lại key. Kiểm tra đăng nhập và working tree:

```bash
gh auth status
git status --short
```

Expected: `gh` đã đăng nhập, `git status --short` không in file đang sửa.
Nếu đang có thay đổi riêng, hoàn tất/cất chúng trước khi đổi nhánh; không reset để xóa.
Sau đó, trong cùng cửa sổ Terminal:

```bash
git switch seminar-core
git pull --ff-only origin seminar-core
AI3_BRANCH="codex/ai3-demo-$(date +%Y%m%d-%H%M%S)"
git switch -c "$AI3_BRANCH"
```

**Bước 2 — Tạo test thiếu assertion và giới hạn lượt chạy.** Đoạn chuẩn bị này dừng
nếu file mẫu hoặc `maven.config` đã tồn tại, tránh ghi đè cấu hình riêng:

```bash
python3 - <<'PY'
from pathlib import Path

test = Path("case-study/src/test/java/vn/edu/seminar/ai/Ai3PipelineSmokeTest.java")
config = Path("case-study/.mvn/maven.config")
if any(path.exists() or path.is_symlink() for path in (test, config)):
    raise SystemExit("Dừng: file mẫu/config đã tồn tại; kiểm tra trước khi tiếp tục.")
test.parent.mkdir(parents=True, exist_ok=True)
config.parent.mkdir(parents=True, exist_ok=True)
with test.open("x") as stream:
    stream.write("""package vn.edu.seminar.ai;

import org.junit.jupiter.api.Test;
import vn.edu.seminar.fine.FineCalculator;
import vn.edu.seminar.fine.MemberTier;

class Ai3PipelineSmokeTest {
    @Test
    void calculatesNormalMemberFine() {
        new FineCalculator().calculate(1, MemberTier.NORMAL);
    }
}
""")
with config.open("x") as stream:
    stream.write("-Dtest=Ai3PipelineSmokeTest\n")
print("Đã tạo hai file demo mới. Có thể commit bước tiếp theo.")
PY
```

`maven.config` khiến Maven chỉ chạy test mẫu, vì vậy nhiều nhánh FineCalculator chưa
được chạy và gate sẽ đỏ. Không hạ ngưỡng JaCoCo. Test thiếu assertion vẫn có thể pass
vì không kiểm tra kết quả; đây là lỗi cố ý để Gemini nhận xét trên PR nháp.

**Bước 3 — Commit, push và tạo PR nháp.** Chỉ tiếp tục khi bước 2 báo tạo thành công:

```bash
git add case-study/src/test/java/vn/edu/seminar/ai/Ai3PipelineSmokeTest.java case-study/.mvn/maven.config
git commit -m "test(ai): demo review with low coverage and missing assertion"
git push -u origin "$AI3_BRANCH"
gh pr create --draft --base seminar-core --head "$AI3_BRANCH" \
  --title "test(ai): demo Gemini review with red and green CI" \
  --body "PR nháp demo AI-3. Cố ý chỉ chạy một test thiếu assertion để coverage gate đỏ; sau đó sẽ sửa test và khôi phục bộ test chuẩn. Không merge PR này."
AI3_PR="$(gh pr view --json number --jq .number)"
gh pr view "$AI3_PR" --web
```

Trong **Checks**, đợi **AI review and CI summary** hoàn tất. Expected:

- `test (JDK 25)`: success; `coverage-gate`: failure; `package`: skipped.
- Gemini có thể nêu `NO_ASSERTION` ở lời gọi `calculate`. Nội dung AI không cố định;
  nếu bỏ sót, ghi nhận đó là giới hạn của model, không sửa output cho khớp mẫu.
- Bot vẫn comment trạng thái đỏ, số test/coverage đo thật và nhận xét Gemini nếu API
  thành công. Coverage toàn project trong comment khác coverage riêng FineCalculator;
  gate đang kiểm class được khai báo trong `pom.xml`.

Đọc log coverage để xác nhận đúng lỗi **Coverage checks have not been met**,
không kết luận thiếu coverage nếu job thực ra lỗi compile hoặc môi trường.
Đọc job Gemini để phân biệt API hoàn thành với thiếu Secret/503/quota.
Nếu không có comment hoặc không có review API hoàn chỉnh, xử lý lỗi trước bước 4.

**Bước 4 — Sửa assertion và trả lại bộ test đầy đủ.** Mở file vừa tạo, thay nội dung bằng:

```java
package vn.edu.seminar.ai;

import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import vn.edu.seminar.fine.FineCalculator;
import vn.edu.seminar.fine.MemberTier;
import static org.assertj.core.api.Assertions.assertThat;

class Ai3PipelineSmokeTest {
    @Test
    void calculatesNormalMemberFine() {
        assertThat(new FineCalculator().calculate(1, MemberTier.NORMAL))
                .isEqualByComparingTo(new BigDecimal("2000"));
    }
}
```

Expected `2000` là phí một ngày trễ NORMAL theo source/đặc tả của mẫu hiện tại;
nếu nghiệp vụ thay đổi, đọc lại trước khi dùng. Xóa đúng cấu hình demo mới tạo,
commit hai thay đổi và push lên **cùng nhánh/cùng PR**:

```bash
git rm case-study/.mvn/maven.config
git add case-study/src/test/java/vn/edu/seminar/ai/Ai3PipelineSmokeTest.java
git commit -m "test(ai): add assertion and restore the full test suite"
git push
gh pr view "$AI3_PR" --web
```

**Bước 5 — Kiểm tra kết quả xanh và comment cập nhật.** Đợi các job kết thúc.
Với source/bộ test chuẩn ở phiên đã chạy, cả test, coverage, package, Gemini và comment
đều success; có 40 tests, BRANCH toàn project 100%. Lượt của bạn dùng số đo thật,
không lấy bảng mẫu làm output bắt buộc. Nếu bộ test chuẩn đang lỗi, kiểm tra log tương ứng.
Workflow hiện còn có job **AI tooling offline checks** kiểm các script AI bằng Python;
job này không gọi Gemini và không thay thế JUnit/coverage của ứng dụng.

Trong comment, kiểm tra SHA đã đổi sang commit bước 4, link Actions trỏ đúng lượt mới,
kết quả CI được cập nhật và không xuất hiện comment bot thứ hai. Gemini không còn
nêu lỗi thiếu assertion là kết quả đã quan sát ở PR #12; vẫn đọc finding thực tế của lượt mới.

**Bước 6 — Kết thúc demo.** Giữ PR nháp để trình bày hoặc đóng sau khi xem xong;
không merge cấu hình/lỗi thử vào nhánh chung. Quay về nhánh làm việc:

```bash
git switch seminar-core
git status --short --branch
```

Các file thử chỉ nằm trên nhánh demo; `seminar-core` không có chúng. Không cần tạo
`gemini-live` hoặc commit evidence. Nếu mở Terminal khác, tìm lại PR bằng
`gh pr list --base seminar-core`, rồi dùng số PR đó thay cho biến `AI3_PR`.
