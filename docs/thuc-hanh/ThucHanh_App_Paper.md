# Thực hành: chạy ứng dụng thư viện và thử tool của paper

**Người thực hành:** Ngô Gia An (23120205). **Ngày chuẩn bị:** 29/10/2026. Chạy lần lượt A rồi B; mỗi bước có kết quả mong đợi và ý nghĩa. Phần này là bài làm thử, không đánh dấu bạn đã tự chạy/xác nhận trước khi thực sự thực hiện.

**Đã kiểm tra khi chuẩn bị:** Java 25/Maven Wrapper; bốn HTTP response 201/409/409/404 trên app local; baseline Python một test; CoverUp dry-run với route Gemini. **Chưa gọi Gemini sinh test thật** vì key do bạn nhập ở máy. Kết quả generation không cố định và chưa được hứa trước.

## A. Hiểu ứng dụng thư viện qua HTTP và test

### A1. Mở Terminal A tại gốc repo

```bash
cd "/Users/ngogiaan1103/Documents/ChatGPT/seminar-testing 2"
java -version
case-study/mvnw -v
```

**Expected:** Java major version 25; Maven Wrapper in thông tin Maven/Java và kết thúc bình thường. Nếu Java không phải 25, chỉnh JAVA_HOME theo README trước khi tiếp tục.

### A2. Build và chạy bộ kiểm thử chuẩn

```bash
case-study/mvnw -B -ntp -f case-study/pom.xml clean verify
```

**Expected trên phiên bản hiện tại:** 39 tests, failures/errors/skipped đều 0; `All coverage checks have been met`; `BUILD SUCCESS`. Có JAR `case-study/target/library-case-study-0.1.0.jar` và report `case-study/target/site/jacoco/index.html`.

**Ý nghĩa:** Java đã chạy các bộ test chuẩn và JaCoCo gate trước khi tạo bản ứng dụng. Lệnh này không gọi Gemini. Mở report JaCoCo để xem số đo nếu muốn; đây là report runtime trong target, không phải chỉnh slide/HTML trình bày.

### A3. Khởi động ứng dụng trong Terminal A

```bash
java -jar case-study/target/library-case-study-0.1.0.jar \
  --server.address=127.0.0.1 --server.port=8081
```

**Expected:** log có `Tomcat started on port 8081` và `Started LibraryApplication`. Terminal tiếp tục giữ tiến trình app là bình thường. Nếu báo port bận, dùng 8082 và thay cổng trong tất cả curl bên dưới.

Mở `case-study/src/main/resources/data.sql`: sách 1/3 còn sẵn, sách 2 đã được mượn; thành viên 1 không nợ, thành viên 2 nợ 5.000. Dữ liệu H2 trong bộ nhớ được nạp lại sau mỗi lần khởi động.

### A4. Mở Terminal B, mượn sách lần đầu

```bash
curl -i http://127.0.0.1:8081/api/loans \
  -H 'Content-Type: application/json' \
  -d '{"bookId":1,"memberId":1}'
```

**Expected:** HTTP **201**; JSON có `id`, `bookId: 1`, `memberId: 1`, `borrowedAt`. ID/thời gian thay đổi mỗi lần, không so chính xác hai giá trị này với mẫu.

**Ý nghĩa:** controller nhận request → service kiểm điều kiện → repository lưu phiếu và đánh dấu sách 1 không còn sẵn. Có thể mở `LoanService.borrow()` để đối chiếu từng bước.

### A5. Gửi lại đúng request vừa rồi, giữ nguyên tiến trình app

```bash
curl -i http://127.0.0.1:8081/api/loans \
  -H 'Content-Type: application/json' \
  -d '{"bookId":1,"memberId":1}'
```

**Expected:** HTTP **409**, body `{"code":"BOOK_UNAVAILABLE"}`.

**Ý nghĩa:** trạng thái sách được lưu sau request trước; cùng request nhưng trạng thái ứng dụng đã đổi. Nếu ngay A4 đã 409 thì có thể bạn đã mượn sách trong tiến trình này trước đó; restart app để bắt đầu lại bộ dữ liệu mẫu.

### A6. Thử thành viên đang nợ phí

```bash
curl -i http://127.0.0.1:8081/api/loans \
  -H 'Content-Type: application/json' \
  -d '{"bookId":3,"memberId":2}'
```

**Expected:** HTTP **409**, `{"code":"UNPAID_FINE"}`. Dùng sách 3 vì sách này còn sẵn; nếu dùng sách 1 đã mượn, service sẽ chặn ở BOOK_UNAVAILABLE trước khi xét nợ.

### A7. Thử sách không tồn tại

```bash
curl -i http://127.0.0.1:8081/api/loans \
  -H 'Content-Type: application/json' \
  -d '{"bookId":99,"memberId":1}'
```

**Expected:** HTTP **404**, `{"code":"BOOK_NOT_FOUND"}`. Đọc `LoanExceptionHandler` để thấy cách mã lỗi nghiệp vụ được đổi thành HTTP status.

### A8. Dừng app và xem hai bộ CSV được chạy ra sao

Quay lại Terminal A, nhấn **Ctrl+C**. App dừng; dữ liệu H2 trong bộ nhớ không được giữ cho lần khởi động sau. Dừng app trước khi chạy các lệnh Maven có clean tiếp theo.

Trong Terminal B:

```bash
cd "/Users/ngogiaan1103/Documents/ChatGPT/seminar-testing 2"
GA_APP_PRACTICE="$(mktemp -d /tmp/ga-app-practice.XXXXXX)"
python3 scripts/run_ai_demo.py human --output "$GA_APP_PRACTICE/human"
python3 scripts/run_ai_demo.py data --output "$GA_APP_PRACTICE/ai"
python3 scripts/ai4_compare.py compare ai/human/frozen ai/data/AI-4-boundaries.csv \
  --output "$GA_APP_PRACTICE/comparison.json"
```

| Lệnh | Expected | Ý nghĩa |
|---|---|---|
| human | 23 test pass; `fine_coverage.BRANCH`: covered 10, missed 0 | Java tính thật rồi so với 23 kỳ vọng bạn cung cấp |
| data | 13 test pass; covered 8, missed 2 | Cùng lớp Java nhưng dùng riêng CSV AI có sẵn |
| compare | matching_inputs = 11; matching_outcomes = 11; disagreements rỗng | So hai danh sách đầu vào/kỳ vọng, không chạy Java |

Hai profile CSV skip coverage gate để quan sát riêng từng bộ. Bạn không cần freeze lại dữ liệu. Mở `FineCalculator`, `FineCalculatorHumanDataTest`, CSV gốc và `cases-notes.md` để nối đầu vào → kỳ vọng → lời gọi Java → assertion. Chưa có Gemini tham gia các lệnh A1–A8.

**Hoàn thành phần A khi:** bạn giải thích được vì sao cùng request lần đầu 201/lần hai 409; vì sao dùng sách 3 cho ca nợ; và khác nhau giữa so hai CSV với chạy CSV qua Java.

## B. Thử CoverUp với Gemini — tool của paper thực sự làm gì?

CoverUp là công cụ Python, nên bài này dùng script Python thật của nhóm `scripts/coverage_gaps.py`. Công cụ này đọc JaCoCo XML để trích gap; ta sẽ nhờ CoverUp sinh pytest để kiểm chính script đó. Đây là thử tool paper trên source nhóm; không phải sinh JUnit cho ứng dụng Java. ChatUniTest là hướng thử Java riêng, làm sau.

Luồng bạn quan sát:

```text
Một smoke test đang có → đo coverage thấp
                         ↓
            CoverUp chọn source còn thiếu
                         ↓
                 gọi Gemini sinh pytest
                         ↓
             chạy test mới, đo coverage lại
```

Dùng Gemini là đổi model so với cấu hình GPT-4o trong thực nghiệm CoverUp đã lưu. Kết quả phải ghi là **thử nghiệm với Gemini trên source nhóm**, không gọi là tái lập đúng toàn bộ kết quả paper.

### B1. Kiểm môi trường đã được chuẩn bị trên máy này

```bash
cd "/Users/ngogiaan1103/Documents/ChatGPT/seminar-testing 2"
/tmp/seminar-coverup-venv/bin/python --version
/tmp/seminar-coverup-venv/bin/python -m coverup --version
```

**Expected:** Python 3.12.x, CoverUp 0.6.0. Môi trường nằm ở thư mục tạm, không nằm trong repo. Nếu thư mục này đã bị hệ thống dọn, tạo lại venv Python 3.12 và cài `research/requirements-coverup.lock.txt` trước khi tiếp tục. Lock hiện pin pytest 8.3.5 để tương thích SlipCover; dry-run đã kiểm tra sau khi pin.

### B2. Tạo bản sao source và test ban đầu

```bash
GA_PAPER_RUN="$(mktemp -d /tmp/ga-coverup-practice.XXXXXX)"
mkdir -p "$GA_PAPER_RUN/scripts" "$GA_PAPER_RUN/tests"
cp scripts/coverage_gaps.py "$GA_PAPER_RUN/scripts/"
cp evidence/tuan-06/papers/coverup-group-dry-retry/inputs/test_smoke.py \
  "$GA_PAPER_RUN/tests/"
cd "$GA_PAPER_RUN"
```

**Expected:** thư mục học có `scripts/coverage_gaps.py` và `tests/test_smoke.py`. Giữ cùng Terminal B ở phần B để các biến thư mục còn hiệu lực. Tool chỉ thao tác trên bản sao này; source/test của ứng dụng chính chưa được thay đổi.

### B3. Chạy test và đo baseline trước khi gọi AI

```bash
/tmp/seminar-coverup-venv/bin/python -m slipcover \
  --branch --source scripts --json --out before.json -m pytest -q
```

**Expected trong baseline đã kiểm:** `1 passed`. `before.json` ghi 11 dòng được phủ/28 dòng chưa phủ, 2 nhánh được phủ/14 nhánh chưa phủ. Tỷ lệ kết hợp line+branch là khoảng **23,6%**; đây không phải branch coverage 23,6%.

Smoke test chỉ thử report rỗng, nên nhiều xử lý XML/nhánh còn chưa được kiểm. Cảnh báo pytest rằng module slipcover đã được import trước có thể xuất hiện; đọc cùng dòng kết quả test. Nếu có error hoặc cảnh báo không kích hoạt được branch coverage, dừng để xử lý môi trường thay vì dùng số đo đó.

### B4. Nhập Gemini key trong Terminal, không đưa key vào chat/file Git

Với zsh trên macOS:

```bash
read -s "GEMINI_API_KEY?Nhập Gemini API key (sẽ ẩn): "
export GEMINI_API_KEY
printf '\n'
export GA_COVERUP_MODEL='gemini/gemini-3.8-flash'
```

Key được nhập ở prompt ẩn. Không dùng lệnh echo để in giá trị. Route `gemini/` và biến GEMINI_API_KEY là cách LiteLLM gọi Gemini API; không phải Vertex AI. Model được chọn phải là model key của bạn có quyền truy cập. Nguồn: [LiteLLM Gemini](https://docs.litellm.ai/docs/providers/gemini), [Google models](https://ai.google.dev/gemini-api/docs/models).

### B5. Chạy dry-run để hiểu phần chuẩn bị

```bash
/tmp/seminar-coverup-venv/bin/python -m coverup \
  --model "$GA_COVERUP_MODEL" --dry-run \
  --tests-dir tests --package-dir scripts --no-checkpoint \
  --max-attempts 1 --max-concurrency 1 \
  --log-file coverup-dry.log scripts/coverage_gaps.py
```

**Expected đã kiểm offline:** tool đo khoảng 23,6%, xử lý 2 đoạn source; cuối lượt vẫn khoảng 23,6%, chưa có test sinh mới. Dòng “Prompting ...” vẫn được tool in ở dry-run; không dùng riêng dòng này để khẳng định đã gọi Gemini. Source tool kiểm tra cấu hình/key rồi bỏ qua lời gọi model ở chế độ này.

### B6. Sinh test thật — đây mới là bước gọi Gemini

```bash
/tmp/seminar-coverup-venv/bin/python -m coverup \
  --model "$GA_COVERUP_MODEL" \
  --tests-dir tests --package-dir scripts \
  --checkpoint coverup-checkpoint.json \
  --max-attempts 1 --max-concurrency 1 --max-backoff 4 --repeat-tests 1 \
  --log-file coverup-live.log scripts/coverage_gaps.py
```

**Expected về quy trình:** đo baseline → gửi source/gap cho Gemini → nhận pytest → chạy/đánh giá test → đo lại coverage. Chỉ một segment hoạt động cùng lúc và một vòng thử/segment, nhưng tool call/retry bên trong vẫn có thể tạo nhiều request; đây không phải giới hạn tổng chi phí. Bước này dùng API quota của bạn.

**Kết quả không cố định:**

- Nếu có test tốt: xuất hiện file test mới trong `tests/`, bộ test vẫn pass và coverage có thể tăng.
- Nếu test fail hoặc không tăng coverage: xem chỉ số F/U và log; không bảo đảm mọi lượt đều sinh được test tốt hoặc đạt 100%.
- Nếu có lỗi 401/403: kiểm key/quyền. 404: kiểm model. 429 hoặc retry lặp: nhấn Ctrl+C, kiểm quota/rate limit trước khi thử lại.

Đừng coi exit 0 hoặc “API trả lời” là bằng chứng có test mới tốt. Cần kiểm file test, kết quả pytest và coverage trước/sau. Nếu chia sẻ log để hỗ trợ, không gửi key và loại bỏ giá trị key nếu xuất hiện trong lỗi.

### B7. Xem kết quả và kiểm lại test mới

```bash
find tests -type f -name '*.py'
/tmp/seminar-coverup-venv/bin/python -m pytest -q
/tmp/seminar-coverup-venv/bin/python -m slipcover \
  --branch --source scripts --json --out after.json -m pytest -q
```

Mở một file mới trong `tests/`: tìm đầu vào, lời gọi `extract(...)` hoặc CLI và assertion. Hỏi: test có kiểm đúng dữ liệu trả về hay chỉ gọi hàm? Nếu nó tạo XML giả để kiểm parser, XML đó có đại diện đúng quy tắc không?

So số đo:

```bash
/tmp/seminar-coverup-venv/bin/python - <<'PY'
import json
for name in ['before.json', 'after.json']:
    s = json.load(open(name))['summary']
    print(name, {
        'line': f"{s['covered_lines']}/{s['covered_lines'] + s['missing_lines']}",
        'branch': f"{s['covered_branches']}/{s['covered_branches'] + s['missing_branches']}",
        'combined_percent': s['percent_covered'],
    })
PY
```

**Expected:** có hai bản số đo thực tế để đối chiếu. Nếu after cao hơn và test pass, tool đã bổ sung một số hành vi được thực thi. Nếu không tăng, ghi đúng kết quả và đọc log; không sửa số liệu. Đây là SlipCover trên Python, khác JaCoCo trên Java nên không so trực tiếp với 100%/80% của AI-4.

### B8. Kết thúc và bàn giao lần thử

```bash
unset GEMINI_API_KEY
```

Giữ thư mục `$GA_PAPER_RUN` gồm `before.json`, `after.json`, `coverup-live.log`, checkpoint và test mới. Ghi lại model đã dùng, thời điểm, số test trước/sau, pass/fail và coverage. Không tự chép test sinh vào source chính trước khi đọc/review. Thư mục /tmp có thể bị dọn, nên khi đã review cần lưu các artifact cần thiết vào evidence theo format chung, loại bỏ key/đường dẫn cá nhân.

**Hoàn thành lần thử B khi:** bạn chỉ được source đầu vào, test ban đầu, lời gọi model, test mới hoặc lý do thất bại, và số đo trước/sau. Đây là một lần áp dụng tool của paper trên source nhóm; vẫn chưa hoàn thành yêu cầu tái lập đầy đủ benchmark gốc của hai paper.

## Nếu muốn xem bước phân tích dữ liệu công bố của CoverUp

Repo tác giả và môi trường phân tích cũng đã được tải trên máy này. Từ gốc repo:

```bash
GA_REPLAY="$(mktemp -d /tmp/ga-paper-replay.XXXXXX)"
python3 scripts/paper_experiments.py coverup-reanalyse /tmp/seminar-coverup-eval \
  --python /tmp/seminar-paper-venv/bin/python --output "$GA_REPLAY/result"
```

**Expected:** script tác giả phân tích 163 module MT; overall line+branch CoverUp 89,0%, MuTAP gpt4o_zero 76,8%. Đây là dữ liệu tác giả đã công bố và phép tính chạy lại, không phải Gemini vừa sinh lại các test của 163 module. Hướng dẫn lấy source/revision nếu /tmp bị dọn nằm ở [research/README.md](../../research/README.md).
