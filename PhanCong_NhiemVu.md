# Tổng quan dự án và phân công nhiệm vụ

**Môn:** Kiểm thử phần mềm (FIT@HCMUS) · **Nhóm:** 09 · **Chủ đề seminar:** Unit Test · Code Coverage · CI/CD

> Tài liệu này dành cho cả nhóm đọc trước khi bắt tay làm. Phần 1–3 giải thích dự án làm gì và vì sao. Phần 4–5 là hiện trạng thật (đã có, chưa có). Phần 6 là phân công từng người. Phần 7–9 là quy tắc làm việc, rủi ro và checklist.
>
> **Ngày lập:** 28/10/2026, dựa trên nhánh `reportweek04` (commit `de9b88a`) và nhánh gọn `seminar-core`. Những chỗ ghi `___` là nhóm cần tự điền (ngày hạn, tên tài khoản...).

---

## 1. Đề bài và cách nhóm thực hiện

### Đề bài của nhóm
Chủ đề **Unit Test · Code Coverage · CI/CD**. Thầy yêu cầu:
1. Trình bày **khái niệm tổng quan về unit testing**.
2. Dùng **một ví dụ và một bộ test case** để giải thích **các loại coverage**.
3. **Demo ít nhất 2 công cụ**.
4. Trình bày **cách tích hợp vào CI/CD**.
5. Tìm **bài báo nghiên cứu hạng ≥ B, trong 5 năm gần đây**, về unit testing.

Sản phẩm nộp: slide (nền trắng, chữ đen), báo cáo, video demo, bài tập áp dụng, source code, bảng phân công kèm minh chứng. **Mốc:** Tuần 6 nộp chấm điểm (thiếu: −3đ), trình bày thử với GV trước tuần seminar (thiếu: −4đ), Tuần 12 nộp bản hiệu chỉnh.

### Nhóm thực hiện như thế nào
Dùng **một ứng dụng quản lý thư viện** làm ví dụ duy nhất, đi qua ba bước:

| Bước | Làm gì | Công cụ |
|---|---|---|
| 1. Unit test | Viết test cho tính phí trả sách trễ và mượn sách | JUnit, Mockito |
| 2. Coverage | Đo test phủ bao nhiêu code, test có kiểm đúng không | JaCoCo, PIT |
| 3. CI/CD | Tự động chạy test và chặn code thiếu test mỗi lần đẩy code | GitHub Actions (so với Jenkins) |

AI hỗ trợ ở cả ba bước (sinh test, đọc coverage, review code). Mỗi bước có demo từ cài đặt, cơ bản đến phức tạp, kèm điểm yếu của công cụ. Câu hỏi xuyên suốt: **"Test xanh và coverage 100% đã chắc code đúng chưa?"**

### Thầy nhắn thêm (cập nhật 28/10)
1. **Gửi slide / gặp thầy trước 3–4 ngày** so với hạn, vì còn xếp lịch và chỉnh sửa ra bản final.
2. **Phải có nhiều video demo**, không chỉ một: setup, khái niệm cơ bản trong tool, demo đơn giản, demo phức tạp, **demo trường hợp công cụ không xử lý được**, và có **data driven**. Nếu gộp một video thì phải **ghi timestamp rõ ràng**. Một video 2–3 phút cho cả nhóm sẽ bị đánh giá thấp.
3. **Thầy đọc từ slide**, nên slide ngoài lý thuyết phải **nhắc đến từng video và tóm tắt nội dung video**.
4. **Không tự implement lại paper.** Chọn paper **có source code công bố**, **chạy lại kết quả đã công bố**, rồi thử trên một số trường hợp test thực tế. Paper không có source code thì **chọn paper khác**. (Tự implement lại được dựa trên paper thì càng tốt.)
5. Moodle bảo trì nên chưa nộp thì cứ nộp, đã nộp mà chưa ưng thì nộp lại.

**Ảnh hưởng đến kế hoạch:** video là **bắt buộc** (việc H không còn "hỏi GV", bỏ quyết định tạm loại video khỏi checklist Tuần 6); việc E đổi thành "chọn paper có code, chạy lại, thử nghiệm"; slide phải có phần mô tả video.

### Gói nộp bài (deadline khoảng Tuần 07)
Cần hoàn thiện **khoảng 90% nội dung seminar** rồi nộp qua link của thầy. Không nộp hoặc làm sơ sài: có thể bị trừ 1–2đ.

**Giới hạn:** tối đa **20 file**, mỗi file **≤ 20 MB**, tổng **≤ 400 MB**. **Không nộp bằng Google Drive.** File lớn hơn 20 MB thì nén/chia nhỏ và ghi **`ZipTool`** trong tên file để thầy giải nén được.

| Mục phải nộp | Định dạng | Lấy từ đâu | Người làm |
|---|---|---|---|
| **Slide** (thầy đọc đầu tiên) | Markdown + PDF hoặc PowerPoint | `slides/` (xuất PDF), thêm phần tóm tắt từng video | Bảo An |
| **Báo cáo** | Markdown + PDF | `docs/thuc-hanh/BaoCao_ChiTiet.md`, xuất PDF | Bảo An (mỗi người viết phần mình) |
| **Link video demo** | Markdown (file liệt kê link + tóm tắt + timestamp) | Video đăng YouTube | Bảo An tổng hợp, mỗi người quay phần mình |
| **Scripts / source code** | Nén (ZipTool nếu >20 MB) | `case-study/`, `ai/`, `scripts/`, `.github/`, `Jenkinsfile` | Thế Vinh |
| **Seminar contribution** | **Google Sheet của thầy** (điền trực tiếp) | Mỗi người tự điền phần việc của mình | Cả nhóm |
| **Git commit log** | Markdown | Xuất **từ `git log` thật** của repo | Quang Vinh |
| **AI usage declaration** | Markdown + PDF | Khai báo trung thực AI dùng ở đâu, ai review | Bảo An, cả nhóm xác nhận |

**Lưu ý quan trọng:**
- **Git commit log và Seminar contribution phải khớp với Git thật.** Không dùng script sinh commit giả (script đó đã bị loại bỏ). Ai chưa có commit thì phải có commit/PR trước khi nộp.
- **AI usage declaration** ghi đúng thực tế: AI hỗ trợ viết code, test, tài liệu, bằng chứng; người nào đã chạy lại và review phần nào.
- Không đưa API key, mật khẩu, đường dẫn máy cá nhân vào file nộp. Kiểm kích thước từng file trước khi nộp.

---

## 2. Dự án của nhóm gồm những gì

### 2.1. Ý tưởng xuyên suốt
Dùng **một ứng dụng nhỏ quản lý thư viện** làm ví dụ duy nhất, đi qua ba tầng nối nhau:

```
Viết unit test  →  Đo test phủ được bao nhiêu code  →  Tự động hóa bằng CI/CD
 (JUnit, Mockito)        (JaCoCo, PIT)                     (GitHub Actions, Jenkins)
                         + AI hỗ trợ ở mọi tầng
```

Câu hỏi dẫn dắt cả bài: **"Test chạy xanh và coverage 100% có nghĩa là code đúng không?"** Câu trả lời của nhóm: không nhất thiết. Cần test có assertion tốt, đo bằng mutation, và tự động chặn bằng CI.

### 2.2. Ứng dụng làm nền (`case-study/`)
- **Công nghệ:** Java 25, Spring Boot 4.1.1, H2 trong bộ nhớ, Maven Wrapper (không cần cài Maven).
- `FineCalculator`: tính phí trả sách trễ. NORMAL không ân hạn, 2.000đ/ngày. VIP ân hạn 2 ngày, 1.000đ/ngày. Tối đa 50.000đ. Ngày âm hoặc hạng rỗng thì báo lỗi.
- `LoanService`: mượn sách. Từ chối khi sách không tồn tại, đang được mượn, thành viên không tồn tại, đã mượn đủ 3 sách, còn nợ phí.
- `LoanController`: `POST /api/loans` trả 201 (thành công) hoặc 409 kèm mã lỗi (ví dụ `BOOK_UNAVAILABLE`).
- Dữ liệu và mã chạy được trên mọi máy có JDK 25, không cần database ngoài.

### 2.3. Bộ công cụ sẽ trình bày
| Tầng | Công cụ thực hành | Công cụ đối chiếu (cần khảo sát) |
|---|---|---|
| Unit test | JUnit Jupiter 6, Mockito 5, AssertJ | TestNG, Spock, JUnit 4 |
| Coverage | JaCoCo (line, branch, gate), PIT (mutation) | Cobertura, OpenClover |
| CI/CD | GitHub Actions | Jenkins (Jenkinsfile đã viết), GitLab CI |
| AI | Gemini API, trợ lý AI trong IDE | Các mô hình khác (nêu trong phần nghiên cứu) |

### 2.4. Các kịch bản demo (mã số dùng xuyên suốt tài liệu)
| Mã | Nội dung | Mức |
|---|---|---|
| **UT-1** | Cài đặt, chạy test, đọc báo cáo | Cài đặt |
| **UT-2** | TDD + `@ParameterizedTest` đọc CSV (Data driven) | Cơ bản |
| **UT-3** | Mockito với 6 tình huống mượn sách | Phức tạp |
| **CC-1/2** | Đo coverage trước và sau khi thêm test (50% → 100% branch) | Cơ bản |
| **CC-3** | Coverage gate: thiếu test thì build đỏ | Phức tạp |
| **CC-4** | Test bẫy: 100% branch nhưng PIT chỉ diệt 3/11 mutant | Phức tạp |
| **CI-1** | Workflow tối thiểu chạy test | Cài đặt |
| **CI-2** | Cache, artifact, summary | Cơ bản |
| **CI-3** | Pipeline nhiều job test → gate → package, PR đỏ rồi xanh | Phức tạp |
| **AI-1..4** | Sinh test, đọc gap coverage, review diff, sinh dữ liệu biên | Áp dụng AI |

### 2.5. Dòng chảy bài trình bày (tóm tắt)
1. Mở đầu: vấn đề "coverage cao có an toàn không".
2. Tổng quan unit testing + demo UT-1/2/3.
3. Coverage: **một ví dụ, một bộ test, bảng các loại coverage** + CC-1..4.
4. CI/CD: khái niệm, pipeline, demo CI-1/2/3, so sánh Jenkins.
5. AI: AI-1..4 và nguyên tắc review.
6. Nghiên cứu: các bài báo hạng ≥B, điểm yếu công cụ, bài tập.

(Kịch bản từng phút sẽ viết sau khi các phần dưới đã xong.)

### 2.6. AI trong dự án làm gì

**Đề yêu cầu:** trình bày khả năng áp dụng AI vào chủ đề testing, có demo cụ thể, **tổng quát hóa và tái sử dụng được**. Cần phân biệt: (1) AI là **nội dung demo** (bắt buộc có); (2) AI là **công cụ làm bài** (được phép, nhưng phải review và nhận trách nhiệm, nên cần khai báo trung thực).

| Mã | AI làm gì | Kết quả đã có | Điểm yếu cần nói |
|---|---|---|---|
| **AI-1** | Sinh test nháp cho `FineCalculator` | 3 test, phủ 70% nhánh | Bỏ sót ca lỗi, nhánh VIP |
| **AI-2** | Đọc báo cáo coverage, chỉ ra nhánh chưa phủ, đề xuất test bổ sung | Thêm 3 test, phủ 100% nhánh | Phủ nhánh chưa chắc assertion tốt (cần PIT) |
| **AI-3** | Review `git diff`, nêu lỗi tiềm ẩn (gọi Gemini, dùng được trong CI) | 4/4 lỗi cài sẵn trong diff mẫu | Chỉ đo trên diff mẫu, chưa là đánh giá độc lập |
| **AI-4** | Sinh dữ liệu biên cho test data-driven | 13/15 ca trùng bộ tham chiếu | Thiếu 2 ca; bộ so sánh cũng có AI hỗ trợ, cần người tự viết đối chứng |

**Tái sử dụng được vì:** prompt nằm trong `ai/prompts/`, script (`coverage_gaps.py`, `ai_review.py`, `evaluate_review.py`) nhận đầu vào bất kỳ, quy trình chung là *AI sinh nháp → chạy test → đo coverage/mutation → người review → lặp*. **Còn thiếu:** thử cùng quy trình trên một lớp khác (ví dụ `LoanService`) để chứng minh tổng quát.

**Gắn với paper (mục E):** các nghiên cứu về LLM sinh test cho thấy test sinh ra thường đạt coverage khá nhưng có test sai hoặc flaky; kết quả AI-1 của nhóm là bằng chứng thực nghiệm tương ứng.

**Khai báo dùng AI:** nhóm cần một trang ghi rõ AI viết phần nào, ai review, ai chạy lại. Không đưa API key vào repo, slide hay video.

---

## 3. Chúng ta sẽ làm gì thêm so với hiện tại

Những mục này **chưa có** hoặc **còn yếu**, và là nơi thầy sẽ nhìn kỹ:

| # | Việc | Vì sao quan trọng |
|---|---|---|
| A | **Bảng các loại coverage trên một ví dụ và một bộ test** (statement, branch, condition, MC/DC, path, method...) | Là yêu cầu trực tiếp của thầy; hiện tài liệu mới có line và branch |
| B | **Khái niệm tổng quan unit testing** đầy đủ hơn (định nghĩa unit, test pyramid, test double, oracle...) | Yêu cầu trực tiếp của thầy; hiện mới 1–2 đoạn |
| C | **Chạy CI thật trên GitHub** (PR đỏ → xanh, required checks) | Hiện chỉ có file workflow, chưa có lần chạy nào |
| D | **Khảo sát công cụ và so sánh nhiều tiêu chí** | Đề yêu cầu; hiện chỉ có 1 bảng 4 dòng, chưa thử công cụ đối chiếu |
| E | **Bài báo hạng ≥B trong 5 năm, có source code công bố:** chạy lại kết quả của paper và thử trên test thực tế của nhóm (không tự implement lại); gắn vào slide | Yêu cầu của thầy; chưa có |
| F | **Record & Playback / Checkpoints** (diễn giải tương đương, trình bày rõ) | Đề yêu cầu đủ 3 phần; hiện chỉ Data driven có |
| G | **Điểm yếu của công cụ** (mock static/final, mock quá sâu, JaCoCo với lambda, mutant tương đương, cache hỏng...) | Đề yêu cầu chỉ rõ |
| H | **Nhiều video demo** (setup, khái niệm cơ bản, đơn giản, phức tạp, trường hợp công cụ không xử lý được, data driven) đăng YouTube; slide tóm tắt từng video; nếu gộp thì ghi timestamp | Thầy xác nhận bắt buộc, một video 2–3 phút sẽ bị đánh giá thấp |
| I | **Từng thành viên tự chạy, review và commit bằng tài khoản riêng** | Yêu cầu "chính chủ" và bằng chứng đóng góp |
| J | **Trình bày thử với GV** | Không làm bị trừ 4đ |

---

## 4. Những gì đã làm được (hiện trạng thật)

> Đa số mã, test, script, tài liệu và bằng chứng dưới đây được tạo với **AI hỗ trợ trong một số phiên làm việc** (chủ yếu qua tài khoản của Phạm Quang Vinh và `bingsu`). Vì vậy, **mỗi thành viên vẫn phải tự chạy lại, đọc hiểu và xác nhận phần của mình** trước khi nhận là của mình (xem mục 7).

### 4.1. Mã nguồn và test (nhánh `master`, `seminar-core`)
- Ứng dụng quản lý thư viện chạy được, build bằng `case-study/mvnw`.
- **33 test pass** trên JDK 25: 17 cho `FineCalculator` (CSV 15 dòng + 2 ca lỗi), 6 cho `LoanService`, 5 cho tầng web, 2 integration, 3 persistence.
- JaCoCo: toàn project branch 18/18, line khoảng 90,8%; `FineCalculator` 10/10 nhánh.
- Cấu hình PIT và JaCoCo gate (ngưỡng 90% branch cho `FineCalculator`).

### 4.2. Các thí nghiệm đã đo (bằng chứng trong `evidence/`)
| Thí nghiệm | Kết quả |
|---|---|
| Baseline 1 test | 5/10 nhánh (50%) |
| Bộ đầy đủ | 10/10 nhánh (100%) |
| Gate 90% với bộ thiếu test | Maven exit 1 (đỏ đúng như kỳ vọng) |
| Test bẫy (không assert tiền) | 100% branch nhưng PIT diệt 3/11; bộ mạnh diệt 10/11 |
| TDD replay | 4 vòng đỏ → xanh (chạy lại để minh họa, không phải lịch sử commit thật) |
| HTTP smoke | 5/5 tình huống đúng mã trạng thái |
| Benchmark JaCoCo | Trung vị 9,7s (không JaCoCo) và 12,8s (có JaCoCo), 3 lượt/cấu hình |
| Benchmark cache Maven | Lạnh ~48s, ấm ~12,5s (3 cặp), mạng thay đổi nên chỉ mang tính tham khảo |

### 4.3. CI/CD
- `.github/workflows/ci.yml`: 3 job nối nhau (test → coverage-gate → package), cache Maven, upload artifact, summary.
- `.github/workflows/ai-review.yml`: job review diff bằng AI.
- `Jenkinsfile` mô tả cùng pipeline, chỉ để so sánh.
- Đã kiểm cú pháp bằng actionlint.
- **Chưa chạy trên GitHub/Jenkins.** Trigger tự động đang tắt, chỉ chạy tay.

### 4.4. AI
| Demo | Kết quả |
|---|---|
| AI-1 sinh test | 3 test, phủ 70% nhánh |
| AI-2 đọc gap coverage | Thêm 3 test, phủ 100% nhánh |
| AI-3 review diff (Gemini thật) | Tìm 4/4 lỗi cài sẵn trong fixture, 0 báo thừa; **chỉ đo trên fixture mẫu, không phải đánh giá độc lập** |
| AI-4 dữ liệu biên | 13/15 ca trùng với bộ tham chiếu; thiếu 2 ca |

### 4.5. Tài liệu
23 slide (`slides/`), báo cáo chi tiết (8 mục), hướng dẫn demo, 4 bài tập kèm đáp án gợi ý, kịch bản quay video, bảng công việc, kế hoạch hàng tuần.


---

## 5. Những gì còn thiếu (tóm tắt)
- Chưa có bảng các loại coverage trên một bộ test (mục A) và phần khái niệm unit testing đầy đủ (mục B).
- Chưa chạy CI thật (C), chưa có bộ video (H), chưa có paper chạy lại được (E), chưa có khảo sát công cụ đối chiếu (D).
- Record & Playback / Checkpoints chưa được trình bày (F).
- Phân công chưa có minh chứng đối chiếu được cho 3 trong 5 thành viên (I).

---

## 6. Phân công từng người

Mỗi việc = 1 issue = 1 nhánh = 1 PR, commit bằng tài khoản của chính mình. Cách làm chi tiết do từng người tự nghiên cứu. Hạn: `___` (nhóm thống nhất khi họp). Mỗi người **quay video demo phần của mình** (xem mục "Thầy nhắn thêm").

### Ngô Gia An (23120205): Unit Test
**Đã có để đọc và chạy lại:** test `FineCalculator`, `LoanServiceTest`, hướng dẫn UT-1/2/3, slide 4–10.
**Cần làm:**
1. Viết phần **khái niệm tổng quan về unit testing**: unit là gì, AAA, FIRST, test pyramid, stub/mock/fake/spy.
2. Trình bày **Data driven** (CSV), **Checkpoints** (assertion/verify) và **Record & Playback** theo cách nhóm diễn giải tương đương, nêu rõ lý do.
3. Làm demo **trường hợp JUnit/Mockito không xử lý tốt** (mock quá sâu, test tự xác nhận, mock static/final).
4. **Khảo sát và so sánh JUnit với TestNG** (≥4 tiêu chí), chạy thử TestNG.
5. Tự viết **thêm 1–2 test** của riêng mình.
6. Quay video: **setup, cơ bản, phức tạp, trường hợp không xử lý được, data driven** cho Unit Test.

### Trương Nhật Đạt (23120231): Code Coverage
**Đã có để đọc và chạy lại:** JaCoCo, PIT, gate, CC-1/2/3, test bẫy, slide 11–14.
**Cần làm:**
1. **Việc ưu tiên số 1:** một ví dụ và một bộ test để giải thích các loại coverage (statement, branch, condition, MC/DC, path, method), kèm **bảng: mỗi test làm loại coverage nào tăng**.
2. Nói rõ **JaCoCo đo được loại nào, không đo được loại nào**.
3. Chạy thử **một công cụ coverage thứ hai** (OpenClover hoặc Cobertura) và so sánh với JaCoCo (≥4 tiêu chí).
4. Làm demo **trường hợp JaCoCo/PIT không xử lý tốt** (100% coverage nhưng test yếu, mutant tương đương, PIT chậm).
5. Quay video: **setup, cơ bản, phức tạp, trường hợp không xử lý được** cho Coverage.

### Phạm Quang Vinh (23120202): CI/CD
**Đã có để đọc và chạy lại:** `ci.yml`, `ai-review.yml`, `Jenkinsfile`, benchmark.
**Cần làm:**
1. **Việc ưu tiên số 1:** bật lại trigger, **chạy CI thật trên GitHub**, tạo **PR đỏ rồi xanh**, bật **required checks** để không merge được khi đỏ.
2. Tạo **GitHub Issues/Projects** theo bảng phân công này; mời thành viên vào repo; hướng dẫn mọi người tạo nhánh và PR.
3. **So sánh GitHub Actions với Jenkins** (≥4 tiêu chí), chạy thử Jenkinsfile.
4. Làm demo **trường hợp CI gặp vấn đề** (cache hỏng, lộ secret giả, job chậm, test flaky).
5. Quay video: **setup, cơ bản, phức tạp (PR đỏ→xanh), trường hợp không xử lý được** cho CI/CD.

### Nguyễn Lê Thế Vinh (23120190): Case study
**Đã có để đọc và chạy lại:** ứng dụng, test web/integration, HTTP smoke, README.
**Cần làm:**
1. **Chạy lại từ máy sạch** (cài JDK 25, clone, `mvnw clean verify`, gọi `curl`), ghi lỗi gặp và sửa README.
2. **Thêm một hàm có điều kiện ghép** (`a && b`) vào case study kèm test, để Đạt minh họa condition coverage và MC/DC.
3. Viết **sơ đồ/mô tả nghiệp vụ** ngắn, dễ hiểu cho slide mở đầu.
4. Tự viết **thêm 1–2 test** của riêng mình (web hoặc persistence).
5. Chuẩn bị **dữ liệu và môi trường demo**, chạy thử nhiều lần.
6. Quay video: **giới thiệu và chạy case study**, demo integration.

### Nguyễn Bảo An (23120207): AI, paper và trình bày (kiêm trưởng nhóm)
**Đã có để đọc và chạy lại:** `ai/`, AI-1..4, slide 19–23, báo cáo chi tiết, bài tập.
**Cần làm:**
1. **Chọn 2–3 paper** hạng ≥B (2021–2026) về unit testing **có source code công bố**; **kiểm hạng thật** (CORE/Scimago).
2. Với mỗi paper: **chạy lại kết quả công bố**, rồi **thử trên test của nhóm**; chia cho từng người chạy từng bài, không tự cài đặt lại.
3. Làm **AI-4 đối chứng độc lập** (một người tự viết dữ liệu biên trước, rồi so với bản AI) và thử quy trình AI trên **một lớp khác** (`LoanService`).
4. Viết **trang khai báo dùng AI** (AI viết phần nào, ai review).
5. **Hợp nhất slide và báo cáo**: slide có lý thuyết, **nhắc và tóm tắt từng video**, nền trắng chữ đen.
6. Quay video: **demo AI (setup, cơ bản, phức tạp, trường hợp AI sai)** và video **phần paper**.
7. **Điều phối chung**: họp hàng tuần, theo dõi `BangCongViec.md`, **gửi slide/gặp thầy trước hạn 3–4 ngày**, nộp bài.

## 7. Việc chung của cả nhóm
1. **Họp ngắn đầu tuần** (15 phút): mỗi người báo *đã làm / đang làm / vướng*; Bảo An ghi lại.
2. **Mỗi người quay video demo phần công cụ của mình** (Bảo An điều phối) và nói được ý chính của paper nhóm chọn trong 2 phút.
3. **Review chéo:** mỗi PR cần ít nhất 1 người khác đọc và nhận xét.
4. **Tập thử trình bày** ít nhất 2 lần, một lần bấm giờ; **nộp trước và trình bày thử với GV**.
5. **Chuẩn bị 10 câu hỏi khó** và người trả lời cho từng câu.
6. **Hỏi GV** hệ xếp hạng "rank ≥ B" là CORE hay hệ khác. **Gửi slide / gặp thầy trước hạn 3–4 ngày.**

---

## 8. Quy trình làm việc (để có minh chứng đóng góp)

1. **Mỗi việc = 1 issue = 1 nhánh = 1 PR.** Tên nhánh gợi ý: `feat/coverage-table`, `docs/papers`, `ci/real-run`.
2. **Commit bằng tài khoản GitHub của chính mình**, thông điệp rõ ràng (`feat:`, `docs:`, `test:`, `ci:`).
3. **Không chỉnh sửa lịch sử hay tạo commit giả danh, ghi lùi ngày.** Minh chứng phải đối chiếu được với Git và GitHub.
4. **Dùng AI được, nhưng phải:**
   - đọc hiểu từng dòng trước khi commit;
   - chạy lại và xem kết quả thật;
   - ghi trong PR: *dùng AI làm gì, tự sửa gì*;
   - không nhận là của mình phần mình không giải thích được.
5. **Không đưa vào repo:** API key, mật khẩu, đường dẫn máy cá nhân trong log mới, file zip lớn.
6. **Nhánh `master` chỉ chứa code đã qua PR**; tài liệu và bằng chứng vào nhánh làm việc của nhóm.
7. **Cập nhật `BangCongViec.md`** khi hoàn thành việc (trạng thái + link PR).

---

## 9. Rủi ro cần để ý
| Rủi ro | Cách giảm |
|---|---|
| Thiếu phần thầy yêu cầu (A, B, E) sát hạn nộp | Làm A, B, E trước; C, D sau |
| Chỉ 2 người có commit; ba người còn lại không có minh chứng | Mỗi người có ít nhất 1 PR riêng trước khi nộp |
| Demo CI hỏng khi trình bày | Chạy sẵn, giữ PR đỏ/xanh, có video và ảnh dự phòng |
| Mạng yếu làm Maven tải chậm | Chạy `mvnw` một lần trước để có cache |
| Nội dung do AI sai hoặc bịa (nhất là paper, hạng, số liệu) | Kiểm trên trang gốc (DBLP, CORE, trang hội nghị) |
| Thiếu video hoặc video quá ngắn | Video bắt buộc: lập danh sách video (setup, cơ bản, đơn giản, phức tạp, không xử lý được, data driven), mỗi người quay phần công cụ của mình |
| Paper không có source code | Bỏ, chọn paper khác; chạy lại kết quả công bố, không tự implement |
| Slide quá dài hoặc quá ngắn | Mỗi phần có người chịu trách nhiệm số trang và thời lượng |

---

## 10. Checklist cuối trước khi nộp

- [ ] Có bảng các loại coverage trên một ví dụ và một bộ test (A)
- [ ] Có phần khái niệm unit testing đầy đủ (B)
- [ ] CI chạy thật trên GitHub, có PR đỏ → xanh, required checks (C)
- [ ] Có khảo sát và so sánh công cụ đã thử (D)
- [ ] Có paper hạng ≥B đã kiểm hạng, **có source code**, đã chạy lại kết quả và thử trên test của nhóm (E)
- [ ] Trình bày Record & Playback / Data driven / Checkpoints (F)
- [ ] Có điểm yếu công cụ có demo (G)
- [ ] Đủ bộ video (setup, cơ bản, đơn giản, phức tạp, không xử lý được, data driven), đã đăng YouTube, slide tóm tắt từng video, có timestamp nếu gộp (H)
- [ ] Mỗi thành viên có commit/PR bằng tài khoản riêng (I)
- [ ] Đã trình bày thử với GV (J)
- [ ] Slide nền trắng, chữ đen, chữ to; tất cả liên kết hoạt động
- [ ] Không có API key hoặc dữ liệu cá nhân trong repo
- [ ] Gói nộp: ≤20 file, mỗi file ≤20 MB, tổng ≤400 MB, không dùng Google Drive, file nén ghi `ZipTool`
- [ ] Đủ 7 mục: slide, báo cáo, link video, source, seminar contribution (Google Sheet), git commit log, AI usage declaration
- [ ] Mỗi người giải thích được phần mình mà không cần nhìn tài liệu
