# Demo LoanService — bản ngắn để copy/paste

Chạy theo thứ tự trong **cùng Terminal**. Máy đã chuẩn bị môi trường; hai test Gemini cũ
đã gỡ trên nhánh demo. Baseline: **39 test pass, coverage gate pass**.

## Chuẩn bị một lần trước khi quay

```bash
cd "/Users/ngogiaan1103/Documents/ChatGPT/seminar-testing 2"
git switch codex/loan-ai-demo-20261030
export GA_RUN=".ai-work/Loan-video-$(date +%Y%m%d-%H%M%S)"
```

**Expected:** đúng nhánh demo, output mới ở `$GA_RUN`. Không đổi Terminal/biến giữa các bước.

Bạn chuẩn bị CSV tại `ai/human/loan-service/cases.csv` theo
[mẫu và ý nghĩa cột](../../ai/human/loan-service/README.md). Khóa bộ CSV trước output AI mới:

```bash
python3 scripts/ai_generate.py freeze --class LoanService --csv ai/human/loan-service/cases.csv --author "Ngô Gia An - 23120205" --attest-independent --output ai/human/loan-service/frozen
```

**Expected:** `Human data frozen: .../ai/human/loan-service/frozen`, có `cases.csv` và
`receipt.json`. Chỉ xác nhận độc lập khi đúng thực tế, điền đúng tên tác giả nếu người khác
viết. Nếu đã có bộ frozen đúng, bỏ qua lệnh này. Không freeze đè hoặc dùng bộ FineCalculator.

## AI-1 — một lệnh sinh test và tự chạy đo coverage

```bash
python3 scripts/ai_generate.py ai1 --class LoanService --output "$GA_RUN/ai1"
```

**Tự làm:** đọc source LoanService + dependency → Gemini sinh unit test → chạy JUnit/JaCoCo.

**Expected khi thành công:** Terminal có `Tests=N, failures=0, errors=0; passed=True`.
Không có số N cố định. Các file để quay:

| File trong `$GA_RUN/ai1/` | Nội dung |
|---|---|
| `generated/LoanServiceGeminiDraftTest.java` | Unit test vừa sinh |
| `review.md` | Số test và line/branch coverage |
| `site/jacoco/vn.edu.seminar.loan/LoanService.java.html` | Coverage tô màu trên source |

Mở để quay bằng hai lệnh này:

```bash
open "$GA_RUN/ai1/generated"
open "$GA_RUN/ai1/site/jacoco/vn.edu.seminar.loan/LoanService.java.html"
```

Đây là coverage **riêng test AI-1**, chưa cộng suite chuẩn.

## AI-2 — một lệnh đọc coverage, bổ sung test và đo lại

```bash
python3 scripts/ai_generate.py ai2 --from-ai1 "$GA_RUN/ai1" --output "$GA_RUN/ai2"
```

**Tự làm:** đọc test/coverage/gap AI-1 → Gemini bổ sung test theo nhánh còn thiếu → chạy
lại cả draft và test bổ sung → so coverage trước/sau. Chỉ chạy sau khi AI-1 pass.

**Expected khi thành công:** `passed=True`; `review.md` có bảng coverage trước/sau.
Đây là một lượt bổ sung có đo lại, không phải vòng lặp bảo đảm đạt ngưỡng bất kỳ.
Nếu AI-1 đã đủ coverage, AI-2 có thể bổ sung assertion hoặc trả `no_additions_needed`.

Mở kết quả để quay:

```bash
cat "$GA_RUN/ai2/review.md"
open "$GA_RUN/ai2/generated"
```

**Unit test:** trong `ai2/generated/`, gồm DraftTest và AdditionalTest **nếu có**.
Review expected/assertion/mock trước bước apply. Không sửa file ứng viên đã đo rồi apply.

## AI-3 — apply rồi tạo PR, CI tự review

Sau khi đã xem test và quay đủ output AI-1/2, chạy lần lượt bốn lệnh dưới đây:

```bash
python3 scripts/ai_apply.py --from-ai2 "$GA_RUN/ai2" --apply --reviewed --reviewer "Ngô Gia An - 23120205"
git add -- 'case-study/src/test/java/vn/edu/seminar/loan/LoanServiceGemini*Test.java' && git commit -m "test(loan): add reviewed Gemini demo tests"
git push -u origin HEAD
gh pr create --draft --base seminar-core --head codex/loan-ai-demo-20261030 --title "test(loan): demo Gemini AI tests" --body "Demo sinh test LoanService bằng Gemini, bổ sung từ coverage và review trước apply. Full suite và coverage gate được kiểm khi apply. PR demo, chưa đề nghị merge."
```

**Expected theo thứ tự — chỉ chạy lệnh kế khi lệnh trước thành công:**

1. Apply chạy full suite/gate; có `applied: true`, `integration.passed: true`,
   `output_deleted: true`. Test mới nằm trong `case-study/src/test/java/vn/edu/seminar/loan/`.
   Tổng test là baseline cộng ứng viên thực sự chạy. **Output AI-1/2 bị dọn sau apply**.
2. Git tạo commit test. Git pathspec đã được quote, vẫn chạy khi không có AdditionalTest.
3. Push thành công lên nhánh demo.
4. In URL **draft PR mới**. Mở URL đó → tab **Checks** và comment **Gemini AI-3 review**.

**Apply tạo output ở đâu, xóa ở đâu?**

| Sau khi review rồi apply thành công | Đường dẫn |
|---|---|
| Tạo test nháp trong source thật | `case-study/src/test/java/vn/edu/seminar/loan/LoanServiceGeminiDraftTest.java` |
| Tạo test bổ sung nếu AI-2 có sinh | `case-study/src/test/java/vn/edu/seminar/loan/LoanServiceGeminiAdditionalTest.java` |
| In kết quả full suite/gate và sync | Terminal, JSON có `integration`, `applied`, `output_deleted` |
| Xóa toàn bộ output AI-1 | `$GA_RUN/ai1/`, gồm Java nháp, review, log và JaCoCo |
| Xóa toàn bộ output AI-2 | `$GA_RUN/ai2/`, gồm Java ứng viên, review, so sánh và báo cáo integration |

Với các lệnh từng bước ở đây, apply chỉ dọn hai thư mục stage đó; giữ `$GA_RUN` để chạy
AI-4 tiếp. Không xóa test vừa chép vào `src/test`, CSV human, output AI-4 hay `.env.gemini`.
Nếu full suite/gate fail, không sync test và giữ output để kiểm lỗi. Nếu sync xong nhưng
dọn output bị lỗi, script báo riêng; không apply lại lần hai.

**Trên GitHub để quay:** test → coverage-gate → package; Gemini review chạy song song,
comment tổng hợp số test/coverage CI và nhận xét AI. Chờ cả comment hoàn tất.
Nếu API thành công thì comment có review Gemini; nếu quota/Secret/model lỗi thì đọc trạng thái
thực tế, không nhận là review hoàn chỉnh. AI không nêu finding cũng là kết quả có thể xảy ra.

Nếu PR đã tồn tại, không tạo lần hai: push tiếp sẽ cập nhật cùng PR. Đây là lượt làm lại
nên diff PR là so với test đã có ở `seminar-core`; không xóa lịch sử lượt cũ.
Không có lệnh merge trong demo.

## AI-4 — CSV đã chuẩn bị, một lệnh chạy toàn bộ

```bash
python3 scripts/ai_generate.py ai4 --class LoanService --human-frozen ai/human/loan-service/frozen --output "$GA_RUN/ai4"
```

**Tự làm:** kiểm bộ human đã khóa → sinh schema/harness từ source và header → sinh CSV AI
riêng → chạy hai CSV qua cùng harness → đối chiếu JUnit/JaCoCo/hash → xuất báo cáo.

Mở báo cáo và dữ liệu để quay:

```bash
cat "$GA_RUN/ai4/report.md"
open "$GA_RUN/ai4/generated"
```

**Expected khi thành công:** `report.md` có bảng **Người viết / AI** với số ca, tests,
failures/errors/skipped, LINE/BRANCH LoanService; input chung, expected khớp/mâu thuẫn,
ca thiếu/thêm. Hai lượt Java PASS; đối chiếu CSV/Surefire/JaCoCo/hash PASS.
Số test mỗi bên bằng số dòng CSV của bên đó; số lượng/coverage cụ thể phụ thuộc dữ liệu thật.

**File để quay:** `ai4/report.md`, `ai4/generated/cases.csv` (CSV AI),
`ai4/generated/LoanServiceGeminiCsvTest.java` (harness). Human gốc vẫn ở
`ai/human/loan-service/frozen/cases.csv`. Chỉ header human được gửi vào bước schema,
không gửi dòng dữ liệu human. Schema/harness cũng cần review, cùng pass chưa chứng minh oracle đúng.

Nếu một bước fail, dừng ở bước đó và đọc `stage.json`, `output.log`/`model/api.json` của
bước tương ứng; API lỗi sớm có thể chưa sinh report. Không dùng kết quả lượt trước làm lượt mới.
