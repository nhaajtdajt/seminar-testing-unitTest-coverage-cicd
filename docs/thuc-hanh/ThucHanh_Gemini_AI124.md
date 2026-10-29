# Thực hành Gemini: chọn class, đọc source/schema, sinh test và đối chiếu báo cáo

**Phụ trách:** Ngô Gia An (23120205). **Cập nhật:** 29/10/2026.

Script đã được chuẩn bị và kiểm tra bằng fixture offline. Codex không gọi Gemini hoặc
chạy Maven live thay bạn. Các số đo trong test công cụ là giả lập, không phải kết quả Gemini.

## 1. Luồng tổng quát, không có quy tắc nghiệp vụ mặc định

```text
--class → tìm class/package từ src/main/java
       → source class + dependency/domain production + DDL/schema liên quan
       → yêu cầu nghiệp vụ độc lập nếu người dùng cung cấp
       → Gemini suy ra API, mock state, input/biên/expected
          ├── AI-1: sinh test nháp → JUnit/JaCoCo
          ├── AI-2: đọc test nháp + kết quả/gap → bổ sung → đo lại
          └── AI-4: suy ra schema CSV và harness theo class
                   → sinh CSV AI mới, không xem dữ liệu người viết
                   → so hai CSV → chạy cùng harness
                   → đọc lại Surefire/JaCoCo/hash → report.md
```

Runner không chứa mức phí, số ngày ân hạn, hạn mức mượn sách hoặc schema CSV nghiệp vụ
cố định. Các giá trị đó chỉ xuất hiện trong source/tài liệu đầu vào hoặc output model.
Service mới trong cùng Maven module được tự phát hiện, không cần sửa registry/prompt.

Nếu chỉ đưa source, đây là kiểm hành vi implementation, chưa chứng minh implementation
đúng nghiệp vụ. Dùng `--requirements` khi có đặc tả độc lập; `--schema` khi có SQL/JSON/domain
schema riêng. Prompt ghi rõ phần thiếu yêu cầu và yêu cầu AI nêu giả định.

Source class và closure dependency local qua type reference/import được đưa làm ngữ cảnh,
không đưa test hoặc CSV tham chiếu. Toàn bộ production Java vẫn được copy để biên dịch
đủ dependency. DDL CREATE/ALTER TABLE được lấy từ SQL resources khi có; dữ liệu seed
và application.properties không được dùng làm đặc tả. JPA entities/DTO nằm trong source.
Ngữ cảnh Java quá 200 KB bị từ chối thay vì bị cắt âm thầm; chia module trước khi thử.

## 2. Cấu hình key một lần

```bash
cd "/Users/ngogiaan1103/Documents/ChatGPT/seminar-testing 2"
java -version
case-study/mvnw -v
```

Expected: JDK 25. Chọn JAVA_HOME như README nếu cần. Mở `.env.gemini` ở gốc repo:

```dotenv
GEMINI_API_KEY=KEY_CUA_BAN
AI_MODEL=gemini-3.8-flash
```

Điền key tại máy, không gửi vào chat. Script tự đọc file ở mỗi lần chạy, không cần nhập lại
hoặc `source`. File được Git bỏ qua và đã đặt quyền 600. Model mặc định theo
[Google models](https://ai.google.dev/gemini-api/docs/models); đổi nếu key không có quyền.
Client dùng [generateContent](https://ai.google.dev/api/generate-content).

Trên máy mới, chỉ khi chưa có file cấu hình:

```bash
cp ai/gemini.env.example .env.gemini
chmod 600 .env.gemini
```

Kiểm tra mà không hiển thị key hoặc gọi API:

```bash
python3 scripts/gemini_client.py status
git check-ignore .env.gemini
```

Expected: `key_configured: true`, Git in `.env.gemini`. Status không kiểm quyền/quota.
Environment variables được ưu tiên hơn file; `--model` ưu tiên cao nhất cho model.

## 3. Chọn class và tự chạy AI-1/AI-2

```bash
python3 scripts/ai_generate.py list-classes
```

Lệnh chỉ đọc source, không gọi API. Dùng simple name nếu duy nhất hoặc tên đầy đủ để
tránh trùng. Danh sách là top-level Java types; nested DTO được đưa trong source class
bao ngoài. Chọn concrete class có hành vi cần kiểm, không coi interface trừu tượng là
nghiệp vụ đã được test. Class không có nhánh có thể không có chỉ số BRANCH.

Ví dụ với LoanService; đổi `--class` cho feature/class mới:

```bash
GA_RUN="evidence/tuan-06/gemini-live/loan-$(date +%Y%m%d-%H%M%S)"

python3 scripts/ai_generate.py ai1 \
  --class vn.edu.seminar.loan.LoanService --output "$GA_RUN/ai1"
```

Tùy chọn: thêm `--requirements <file-yeu-cau.md>` và `--schema <file-schema.sql/json>`
bằng đường dẫn có thật. Không cần sửa prompt theo tên service hoặc chép source vào chat.

Script lưu source/POM, gọi Gemini, tự tạo `generated/LoanServiceGeminiDraftTest.java`,
chạy test/JaCoCo trong bản sao tạm. Không ghi đè production, test chuẩn hoặc CSV của nhóm.

Mở output và đọc trước khi tiếp tục:

```bash
open "$GA_RUN/ai1"
```

| Output | Cần xem |
|---|---|
| `inputs/context.json`, `inputs/manifest.json` | Target, yêu cầu/schema, hash source/POM |
| `prompt.md`, `model/` | Input và response thật, model/usage/finish reason |
| `generated/*Test.java`, `analysis.md` | Code mới, tình huống và assertion |
| `run.json`, `output.log`, `surefire-reports/` | Test có chạy/pass thật không |
| `site/jacoco/`, `gaps.json` | Counter/gap của class được chọn |
| `stage.json` | Hoàn thành kỹ thuật, vẫn chờ người review |

Không ấn định số test/coverage. API trả lời không có nghĩa test biên dịch/pass. Không chạy
AI-2 nếu AI-1 không pass hoặc không có đo coverage của target hợp lệ.

```bash
python3 scripts/ai_generate.py ai2 \
  --from-ai1 "$GA_RUN/ai1" --output "$GA_RUN/ai2"
open "$GA_RUN/ai2"
```

AI-2 tự lấy đúng target, source snapshot, yêu cầu/schema và test đã đo ở AI-1.
Không cần truyền lại `--class` hoặc copy report. Bản nháp giữ nguyên; file mới là
`generated/LoanServiceGeminiAdditionalTest.java`; `comparison.json` chứa before/after.
Nếu AI-1 đã phủ đủ nhánh, AI-2 có thể bổ sung assertion/biên mà coverage không tăng.
Sửa source snapshot hoặc bản nháp sau khi đo sẽ làm script từ chối kết quả cũ.
Nếu source/dependency production đã thay đổi, tạo baseline/schema mới cho feature mới;
không dùng kết quả của phiên bản cũ để đánh giá source hiện tại.

JUnit dùng `clean test jacoco:report`, không chạy quality gate ở phase verify. Class thiếu
counter/không được quan sát không được coi là coverage thành công; đọc `coverage_note`.
Đây là unit test trực tiếp: không chứng minh HTTP validation, wiring hoặc ORM/database
thật. Các kiểm thử integration của nhóm vẫn có vai trò riêng.

## 4. AI-4 với CSV người viết đã có: FineCalculator

Không sửa/freeze lại bản người viết đã khóa:

```bash
GA_FINE="evidence/tuan-06/gemini-live/fine-data-$(date +%Y%m%d-%H%M%S)"
python3 scripts/ai_generate.py ai4 --class FineCalculator \
  --human-frozen ai/human/frozen --output "$GA_FINE"
open "$GA_FINE/report.md"
```

Script thực hiện theo thứ tự:

1. Kiểm hash CSV người viết; chỉ đưa **header**, không đưa dòng dữ liệu, vào bước schema.
2. Gemini đọc source/domain và suy ra schema CSV + harness tương ứng với header đó.
3. Request riêng sinh CSV AI mới theo source và schema, không đưa CSV người viết/AI cũ.
4. So input/expected của hai CSV; chạy riêng bằng chính xác cùng harness/source.
5. Đọc lại CSV, XML Surefire, XML JaCoCo và hash để đối chiếu với summary.
6. Xuất `report.md`, `reconciliation.json`, `comparison.json` và kết quả thực thi.

AI-4 có hai lần generation logic nếu chưa có schema: schema/harness rồi dữ liệu. Mỗi
request có thể retry tối đa ba lần với lỗi tạm thời. Schema/harness do Gemini sinh cần
người review; không nhận là framework đã tự chứng minh assertion đúng.

## 5. AI-4 cho service mới: suy ra schema trước, người tự viết dữ liệu sau

Không dùng CSV tính phí cho service khác. Lấy schema tự động từ source service:

```bash
GA_DATA="evidence/tuan-06/gemini-live/loan-data-$(date +%Y%m%d-%H%M%S)"
python3 scripts/ai_generate.py schema --class LoanService \
  --output "$GA_DATA/schema"
open "$GA_DATA/schema"
```

Output: `schema.json`, `generated/LoanServiceGeminiCsvTest.java`, `analysis.md`,
`cases.template.csv` chỉ có header. Chưa sinh ca dữ liệu; chưa xác nhận harness đã chạy.
Review cách ánh xạ tham số, trạng thái mock và expected; báo lỗi nếu schema không diễn tả
được yêu cầu. Không tự sửa harness/schema đã hash rồi dùng kết quả cũ để nhận là hợp lệ.

Copy template ra file riêng và **tự viết input + expected dựa trên yêu cầu**, trước khi xem
data AI. Không nhờ AI điền bộ được gọi là human:

```bash
cp "$GA_DATA/schema/cases.template.csv" "$GA_DATA/human.csv"
```

Sau khi tự điền, khóa dữ liệu bằng khai báo đúng thực tế:

```bash
python3 scripts/ai_generate.py freeze \
  --schema-from "$GA_DATA/schema" --csv "$GA_DATA/human.csv" \
  --author "Ngô Gia An - 23120205" --attest-independent \
  --output "$GA_DATA/human-frozen"
```

Freeze chỉ kiểm schema, lưu nguyên CSV và receipt/hash; không gọi Gemini. Không dùng flag
khai báo độc lập nếu đã xem data AI/test tham chiếu. Schema/harness AI hỗ trợ được ghi rõ.

```bash
python3 scripts/ai_generate.py ai4 --class LoanService \
  --schema-from "$GA_DATA/schema" --human-frozen "$GA_DATA/human-frozen" \
  --output "$GA_DATA/ai4"
open "$GA_DATA/ai4/report.md"
```

Thay class là dùng cùng luồng cho service/feature mới; không phải lập trình lại comparator
hoặc nhét giới hạn nghiệp vụ vào prompt. Không có dữ liệu người thì chưa hoàn thành phần
đối chứng độc lập; script không tự tạo bộ human để lấp chỗ thiếu.

## 6. Đọc báo cáo AI-4 ở bước cuối

| Output | Ý nghĩa |
|---|---|
| `schema-stage/` hoặc thư mục `--schema-from` | Source/schema/harness thực tế đã dùng |
| `generated/cases.csv`, `model/` | CSV AI mới và response gốc |
| `inputs/human/` | Bản sao dữ liệu người đã khóa |
| `comparison.json` | Input chung, expected khớp/mâu thuẫn, ca chỉ có mỗi bên |
| `human/`, `ai/` | JUnit/Surefire/JaCoCo của mỗi bộ qua cùng harness |
| `execution-comparison.json` | Hai summary runtime |
| `reconciliation.json` | Đọc lại raw report: count, counter, CSV hash và harness hash có khớp không |
| `report.md` | Bảng số ca, pass/fail/skipped, line/branch, trùng/thiếu/thêm và kiểm tra nhất quán |

Nếu summary nói 20 test mà XML chỉ có 18, hoặc số test không bằng số dòng CSV, báo cáo
đối chiếu FAIL; không coi thí nghiệm hoàn tất. Counter không có/không có nhánh ghi N/A.
Đồng thuận không phải accuracy. Nếu expected mâu thuẫn, đối chiếu yêu cầu/Java/analysis;
không sửa hai bộ cho giống nhau. Tính độc lập người viết dựa trên khai báo, không do hash.

Với expected là tên kiểu Java, schema có thể khai báo `normalization` gồm `kind: java_type`
và alias từ tên ngắn sang đúng tên đầy đủ. Comparator chỉ áp dụng ở cột expected được khai báo,
không tự bỏ package của mọi chuỗi hoặc gộp hai class khác package. Báo cáo tách khác cách
biểu diễn với mâu thuẫn ngữ nghĩa. Alias phải được đối chiếu source/import/harness khi review.

Nếu cần tính lại báo cáo từ kết quả đã chạy, không gọi API/Maven:

```bash
python3 scripts/reconcile_ai4.py --run "$GA_FINE" \
  --output "$GA_FINE/reviews/recheck-$(date +%Y%m%d-%H%M%S)" --update-reports
```

Lệnh lưu bản báo cáo trước trong `previous/`, ghi lại revision, chỉ cập nhật comparison,
reconciliation và report. CSV, response, schema model gốc, Java và XML không bị sửa.
Nếu đã có bản schema so sánh được review, lệnh tự dùng lại qua `report-revision.json`.
Lần sửa đầu có thể truyền `--comparison-schema <schema-reviewed.json>` và `--notes <review.md>`;
schema review chỉ được đổi quy tắc chuẩn hóa, không đổi input/type/role/header để che lỗi.

## 7. Chạy cả ba hoặc chuẩn bị offline

Ví dụ dữ liệu người của FineCalculator đã sẵn:

```bash
python3 scripts/ai_generate.py all --class FineCalculator \
  --human-frozen ai/human/frozen
```

AI-2 bỏ qua nếu AI-1 không pass; AI-4 vẫn được thử độc lập. Không dùng output cũ thay thế
lượt lỗi. Chọn `--output` mới nếu tự đặt tên; không ghi đè các lượt trước.

Chỉ đọc source và chuẩn bị prompt, không gọi API hoặc Maven:

```bash
python3 scripts/ai_generate.py ai1 --class LoanService --prepare-only
python3 scripts/ai_generate.py schema --class LoanService --prepare-only
```

AI-2 cần baseline có kết quả thật. Các output prepare không phải evidence sinh test.
Key/model sai, quota hoặc response cắt ngắn: xem `model/api.json`, `response.json`.
Compile/assertion fail: xem `output.log` và Surefire; không sửa nghiệp vụ để ép test pass.

Runner không tự commit/push/merge, không sửa source/test chuẩn. Java mới tự lưu trong
thư mục kết quả và chạy ở bản sao tạm; sau khi đọc/review bạn mới đưa vào bộ chuẩn.
Cấu hình `.env.gemini` không được chép vào snapshot/report/Git. Chưa có generation live
do Codex thực hiện cho luồng tổng quát này.
