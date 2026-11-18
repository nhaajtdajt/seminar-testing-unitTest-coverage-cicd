# DANH SÁCH LIÊN KẾT VIDEO DEMO SEMINAR — NHÓM 09
**Môn:** Kiểm thử phần mềm (FIT@HCMUS) · **Lớp:** CQ2023/31  
**Chủ đề Seminar:** Unit Test · Code Coverage · CI/CD  
**Nhóm:** 09

---

## 1. Bảng Tổng Hợp 5 Video Demo

| Video | Tên nội dung | Người thực hiện | Thời lượng | Link YouTube |
|---|---|---|---|---|
| **Video A** | Unit Test với JUnit 5 & Mockito | Nguyễn Bảo An (23120207) | 06:45 | [https://youtu.be/5CaBhsgvM-Q](https://youtu.be/5CaBhsgvM-Q) |
| **Video B** | Code Coverage & PIT Mutation Testing | Trương Nhật Đạt (23120231) | 08:35 | [https://youtu.be/DbqXRK-PThA](https://youtu.be/DbqXRK-PThA) |
| **Video C** | Case Study Ứng Dụng & 7 Kịch Bản HTTP | Nguyễn Lê Thế Vinh (23120190) | 04:30 | [https://youtu.be/Wco_4852snM](https://youtu.be/Wco_4852snM) |
| **Video D** | CI/CD Pipeline với GitHub Actions | Phạm Quang Vinh (23120202) | 08:45 | [https://youtu.be/vakw7UD_SvU](https://youtu.be/vakw7UD_SvU) |
| **Video E** | Ứng dụng AI & Tái hiện Thực nghiệm Paper | Ngô Gia An (23120205) | 09:15 | [https://youtu.be/fLtNeE-MSw4](https://youtu.be/fLtNeE-MSw4) |

---

## 2. Chi Tiết Timestamps & Nội Dung Từng Video

### Video A — Unit Test với JUnit 5 & Mockito
* **Người thực hiện:** Nguyễn Bảo An (23120207)
* **Liên kết YouTube:** [https://youtu.be/5CaBhsgvM-Q](https://youtu.be/5CaBhsgvM-Q)
* **Timestamps:**
  - `00:00`: Setup môi trường Java 25, Maven Wrapper, cấu trúc `pom.xml`.
  - `01:00`: Khái niệm Unit test, quy tắc AAA (Arrange - Act - Assert), chạy test cơ bản và phân tích báo cáo Surefire XML.
  - `02:15`: Data-driven testing với `@ParameterizedTest` và `@CsvFileSource`, kiểm thử giá trị biên (0 ngày, ân hạn 2 ngày VIP, trần 50.000đ).
  - `03:45`: Mockito nâng cao cô lập 3 Repository, Checkpoint `verify(..., never()).save()` và `ArgumentCaptor`.
  - `05:15`: Anti-patterns và hạn chế: Train Wreck Mocking (vi phạm Law of Demeter) và Self-fulfilling Prophecy.
  - `06:30`: Tổng kết và chuyển tiếp sang Video B.

---

### Video B — Code Coverage & PIT Mutation Testing
* **Người thực hiện:** Trương Nhật Đạt (23120231)
* **Liên kết YouTube:** [https://youtu.be/DbqXRK-PThA](https://youtu.be/DbqXRK-PThA)
* **Timestamps:**
  - `00:00`: Setup plugin JaCoCo agent và PIT trong `pom.xml`.
  - `01:00`: Minh họa 6 loại coverage trên `LoanPeriodPolicy` (Statement, Decision, MC/DC).
  - `03:00`: Demo trước/sau: So sánh Baseline 50% vs Bộ đầy đủ 100% Branch Coverage.
  - `04:00`: Demo phức tạp: Gate fail văng Exit 1; test bẫy 100% branch nhưng PIT chỉ diệt 3/11 mutant.
  - `06:00`: Điểm yếu công cụ: Quyết định ẩn trong `Math.min()`, mutant tương đương và chi phí thời gian PIT.

---

### Video C — Chạy Ứng Dụng & 7 Kịch Bản HTTP Smoke Test
* **Người thực hiện:** Nguyễn Lê Thế Vinh (23120190)
* **Liên kết YouTube:** [https://youtu.be/Wco_4852snM](https://youtu.be/Wco_4852snM)
* **Timestamps:**
  - `00:00`: Khởi chạy file JAR thực tế trên OpenJDK 25, kiểm tra dữ liệu mẫu H2 in-memory.
  - `01:00`: Chạy script `demo_case_study.sh` duyệt qua 7 request HTTP curl (201 Created, 409 UNAVAILABLE, 404 NOT_FOUND, 409 UNPAID_FINE).
  - `03:30`: Chạy `LoanFlowEdgeCaseTest` đối chiếu 100% kết quả HTTP thực tế với test tự động.

---

### Video D — CI/CD Pipeline với GitHub Actions
* **Người thực hiện:** Phạm Quang Vinh (23120202)
* **Liên kết YouTube:** [https://youtu.be/vakw7UD_SvU](https://youtu.be/vakw7UD_SvU)
* **Timestamps:**
  - `00:00`: Cấu hình workflow `.github/workflows/ci.yml`, runners `ubuntu-latest`, Temurin JDK 25.
  - `01:00`: Khái niệm CI/CD, cơ chế liên kết `needs` giữa 3 job (`test` -> `coverage-gate` -> `package`).
  - `02:15`: Demo đơn giản: Run xanh hoàn chỉnh, đọc log, tải artifact JAR và Surefire report.
  - `04:00`: Demo phức tạp: PR #2 đỏ do thiếu coverage bị chặn, branch protection required check BLOCKED nút merge.
  - `06:30`: Mổ xẻ sự cố thực tế: Cache miss khi sửa `pom.xml`, runner jitter trên GitHub cloud.

---

### Video E — Ứng Dụng AI & Tái Hiện Thực Nghiệm Paper
* **Người thực hiện:** Ngô Gia An (23120205)
* **Liên kết YouTube:** [https://youtu.be/fLtNeE-MSw4](https://youtu.be/fLtNeE-MSw4)
* **Timestamps:**
  - `00:00`: Setup môi trường, cấu hình Gemini Client, phân biệt tương tác Codex vs Gemini API.
  - `01:30`: Demo AI-1 sinh test nháp và AI-2 phân tích gap coverage bổ sung test.
  - `03:45`: Bot AI review diff tự động trên PR; demo ca test có oracle sai để minh họa giới hạn của LLM.
  - `05:30`: Demo đối chứng độc lập AI-4: Bộ dữ liệu biên do con người lập vs Gemini sinh.
  - `07:15`: Tái hiện thực nghiệm bài báo CoverUp (FSE'25) và so sánh với công cụ Pynguin (EMSE'23).
