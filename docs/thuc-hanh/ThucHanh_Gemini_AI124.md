# Thực hành Gemini: AI-1, AI-2 và AI-4 trên FineCalculator

**Phụ trách:** Ngô Gia An (23120205). **Chuẩn bị:** 29/10/2026.

Script và prompt đã được chuẩn bị; lượt kiểm tra công cụ dùng fixture offline, không gọi
Gemini hoặc chạy Maven thật. Bạn tự thực hiện các lệnh live bên dưới. Không dùng số liệu
cũ của Codex hoặc số liệu giả lập kiểm công cụ làm kết quả mới của Gemini.

Kiểm tra khi chuẩn bị: 21 test Python pass, Python syntax pass và harness CSV biên dịch
được với javac/JUnit 6. Đây là kiểm tra công cụ, chưa phải lượt sinh/chạy test Gemini.

## 1. Phạm vi và luồng

| Bước | Gemini nhận | Script lưu/chạy |
|---|---|---|
| AI-1 | Đặc tả, source FineCalculator/MemberTier, prompt | Response gốc, file test Java mới, JUnit và JaCoCo |
| AI-2 | Cùng source, test nháp đã pass, kết quả JUnit và gap JaCoCo thật | Phân tích, file bổ sung, giữ nguyên bản nháp, chạy lại hai lớp và so trước/sau |
| AI-4 | Chỉ đặc tả và schema CSV; không gửi dữ liệu người viết hoặc test cũ | CSV Gemini mới, so bản người viết đã khóa, chạy hai CSV bằng cùng một harness JUnit |

Runner hiện hỗ trợ **FineCalculator**. LoanService và AI-3/CI là phạm vi khác.
Script tự tạo file Java trong thư mục kết quả rồi chạy trong bản sao Maven tạm.
Không ghi đè `case-study/src/test`, production code hoặc CSV chuẩn/người viết.
Các file sinh mới vẫn cần người đọc assertion và review trước khi đưa vào bộ chuẩn.

## 2. Cấu hình một lần

Tại gốc repo:

```bash
cd "/Users/ngogiaan1103/Documents/ChatGPT/seminar-testing 2"
java -version
case-study/mvnw -v
```

**Expected:** JDK 25. Nếu cần, chọn JAVA_HOME như README trước khi tiếp tục.

File `.env.gemini` ở gốc repo đã được tạo với key để trống. Mở bằng editor, điền:

```dotenv
GEMINI_API_KEY=KEY_CUA_BAN
AI_MODEL=gemini-3.8-flash
```

Thay `KEY_CUA_BAN` bằng key thật tại máy, không gửi vào chat. Đây là file cấu hình local
được script tự đọc, không cần `source` hoặc nhập lại khi chạy. Giá trị trong môi trường
`GEMINI_API_KEY`/`AI_MODEL`, nếu có, được ưu tiên hơn file; `--model` ưu tiên cao nhất cho model.

`.gitignore` đã bỏ qua `.env.*`, file thật có quyền 600. Nếu làm trên máy mới:

```bash
cp ai/gemini.env.example .env.gemini
chmod 600 .env.gemini
```

Chỉ copy khi chưa có file cấu hình, tránh ghi đè key cũ. Cũng có thể chạy
`python3 scripts/gemini_client.py setup` để nhập key ẩn một lần.

Kiểm tra cấu hình mà không hiển thị key hoặc gọi API:

```bash
python3 scripts/gemini_client.py status
git check-ignore .env.gemini
```

**Expected:** `key_configured: true`, model đã chọn; Git in `.env.gemini`.
Status không kiểm quyền/quota của key. Model mặc định được chọn theo
[danh sách Google](https://ai.google.dev/gemini-api/docs/models); đổi AI_MODEL nếu key không có quyền dùng model đó.
Client dùng [Gemini generateContent](https://ai.google.dev/api/generate-content).

## 3. AI-1: sinh và chạy test nháp thật

Giữ cùng Terminal để biến thư mục tồn tại:

```bash
GA_RUN="evidence/tuan-06/gemini-live/demo-$(date +%Y%m%d-%H%M%S)"
python3 scripts/ai_generate.py ai1 --output "$GA_RUN/ai1"
```

Đây là lệnh **gọi API thật**, sử dụng quota của bạn. Script tự:

1. Lưu bản source/POM đầu vào, không lấy test/CSV có sẵn.
2. Gửi prompt AI-1 và nhận JSON chứa `analysis`, `test_source`.
3. Lưu `generated/FineCalculatorGeminiDraftTest.java`.
4. Chạy JUnit và JaCoCo trong thư mục tạm chỉ chứa source/test của thí nghiệm.
5. Giữ log, report, hash và kết quả; dọn thư mục build tạm.

Mở kết quả:

```bash
open "$GA_RUN/ai1"
```

| File | Bạn cần xem |
|---|---|
| `prompt.md` | Model đã được cung cấp gì |
| `model/response.json`, `model/parsed-response.json` | Response mới, không phải fixture/Codex cũ |
| `model/api.json` | Model, số lần request, finish reason, usage và `completed` |
| `generated/FineCalculatorGeminiDraftTest.java` | Từng input, lời gọi hàm và assertion |
| `output.log`, `surefire-reports/`, `run.json` | Compile/test thực tế, số pass/fail/skipped |
| `site/jacoco/index.html`, `gaps.json` | Coverage của FineCalculator và chỗ thiếu |
| `stage.json` | Trạng thái bước, chưa được con người xác nhận review |

**Expected về quy trình:** `stage.json.completed` và `run.json.passed` là true khi
test có thực sự chạy, pass và có report. Không ấn định trước số test hay coverage.
Nếu compile/assertion fail, lưu nguyên lỗi; không coi API trả lời là test thành công.

Lệnh Maven dùng `clean test jacoco:report`: **không chạy quality gate ở phase verify**.
Đây là phép đo bộ test nháp, không thay đổi gate hoặc cấu hình CI của nhóm.

## 4. AI-2: tự đọc bản nháp và coverage, sinh file bổ sung

Chỉ tiếp tục khi AI-1 đã pass và có JaCoCo:

```bash
python3 scripts/ai_generate.py ai2 \
  --from-ai1 "$GA_RUN/ai1" --output "$GA_RUN/ai2"
open "$GA_RUN/ai2"
```

Script lấy snapshot source/POM của lượt AI-1, kiểm hash bản nháp so với bản đã đo,
đưa test/kết quả/gap cho Gemini. Bạn không copy code hoặc report bằng tay.

**Output chính:**

- `analysis.md`: thiếu gì, expected và lý do bổ sung.
- `generated/FineCalculatorGeminiAdditionalTest.java`: test mới.
- `generated/FineCalculatorGeminiDraftTest.java`: bản nháp giữ nguyên.
- `run.json`, log, Surefire và JaCoCo: kết quả chạy cả hai lớp.
- `comparison.json`: before/after, số nhánh được phủ tăng/giảm thực tế.

Nếu AI-1 đã phủ hết nhánh, AI-2 vẫn có thể bổ sung assertion/ca biên; delta bằng 0
không tự động là lỗi. Đọc chất lượng test, không ép model tạo mức tăng giả.
Nếu sửa bản nháp hoặc snapshot sau khi đo, script từ chối dùng coverage cũ.

## 5. AI-4: sinh CSV mới rồi đối chứng với CSV bạn đã viết

Không sửa hoặc freeze lại `ai/human/frozen/`:

```bash
python3 scripts/ai_generate.py ai4 --output "$GA_RUN/ai4"
open "$GA_RUN/ai4"
```

AI-4 độc lập với thành công/thất bại của AI-1/AI-2; có thể chạy riêng trước hai bước đó.
Mỗi request dùng ngữ cảnh mới. Prompt không có CSV người viết, bộ AI cũ hoặc output AI-1/2.

Script kiểm hash bản người viết, gọi Gemini sinh CSV mới có cả expected amount/exception,
sau đó mới so dữ liệu và chạy Java. Cả hai bộ dùng chính xác cùng
`ai/harness/FineCalculatorCsvTest.java` trên cùng source.

| File/thư mục | Ý nghĩa |
|---|---|
| `model/`, `analysis.md` | Request/response và lý do chọn ca mới |
| `generated/cases.csv` | CSV mới do Gemini trả về, không ghi đè `ai/data/AI-4-boundaries.csv` |
| `inputs/human/` | Bản sao CSV/receipt đã khóa, không sửa bản gốc |
| `comparison.json` | Input chung, expected khớp/mâu thuẫn, ca chỉ có ở mỗi bên |
| `human/run.json`, `human/site/jacoco/` | Chạy CSV người viết qua Java |
| `ai/run.json`, `ai/site/jacoco/` | Chạy CSV Gemini mới qua cùng harness |
| `execution-comparison.json` | Hai kết quả test/coverage thực tế |

Bộ người viết hiện có 23 ca. Không ấn định số ca hoặc coverage của CSV Gemini mới.
Tỷ lệ trùng input không phải accuracy. Nếu cùng input khác expected, đối chiếu đặc tả
và lượt Java để xác định nguyên nhân; không tự sửa một bộ cho giống bộ còn lại.
Tính độc lập của bộ người viết dựa trên notes đã cung cấp, không được hash chứng minh.

## 6. Một lệnh chạy cả ba phần (sau khi đã hiểu từng bước)

Chọn thư mục mới, không dùng lại thư mục đã có:

```bash
python3 scripts/ai_generate.py all
```

Output mặc định ở `evidence/tuan-06/gemini-live/<timestamp>-all/`, gồm `ai1`, `ai2`, `ai4`
và `summary.json`. Nếu AI-1 không pass, AI-2 bị bỏ qua; AI-4 vẫn được thử riêng.
Exit 0 chỉ khi ba bước hoàn tất; lỗi/response/test đều được giữ, không tự dùng output cũ thay thế.

Mỗi bước gọi Gemini tối đa ba request khi gặp lỗi mạng/HTTP tạm thời; không có vòng tự
sửa test vô hạn. Các test fail cần được đọc và xử lý trong lượt mới, giữ nguyên lượt lỗi.

## 7. Chuẩn bị offline và đọc lỗi

Không cần key nếu chỉ muốn xem prompt/input; không gọi API hoặc Maven:

```bash
python3 scripts/ai_generate.py all --prepare-only
```

AI-2 được ghi là bỏ qua trong lượt prepare vì chưa có test/coverage thật của AI-1.
Các kết quả prepare không phải evidence sinh test bằng model.

| Vấn đề | Xử lý |
|---|---|
| Chưa có key | Điền `.env.gemini`, kiểm `status`; không gửi key vào chat |
| HTTP 400/401/403/404 | Kiểm key, model, quyền truy cập và cấu hình trong `model/api.json` |
| HTTP 429/503 hoặc timeout | Xem quota/trạng thái dịch vụ, giữ lượt lỗi và thử lượt mới |
| Response bị cắt/không đúng JSON | Xem `response.json` và finish reason, không coi là generation hoàn chỉnh |
| Java không compile/test fail | Đọc `output.log`, Surefire và code mới; không đổi nghiệp vụ để ép pass |
| Output directory đã tồn tại | Chọn tên mới để không ghi đè bằng chứng |
| AI-4 CSV sai schema/duplicate | Xem CSV/response gốc; giữ lỗi, không âm thầm chỉnh dữ liệu |

Không có thao tác tự commit/push/merge trong runner. Khi test đã được review, người dùng
mới quyết định đưa file Java vào source chính bằng commit riêng. Cấu hình Gemini không
được chép vào snapshot, report hoặc Git; log Maven được loại key và đường dẫn home.
