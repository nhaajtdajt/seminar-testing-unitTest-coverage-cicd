# Kế hoạch Thực hiện Nhiệm vụ Unit Test (Ngô Gia An - 23120205)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hoàn thiện toàn bộ 6 hạng mục nhiệm vụ của thành viên Ngô Gia An (23120205) về mảng Unit Test: lý thuyết tổng quan, phân tích kỹ thuật (Data-driven/Checkpoints/Record-Playback), demo trường hợp JUnit/Mockito chống chỉ định/không xử lý tốt, khảo sát thực tế JUnit vs TestNG, bổ sung test case riêng biệt và kịch bản chi tiết quay video demo chuẩn yêu cầu giảng viên.

**Architecture:** 
- Tài liệu học thuật và báo cáo chuyên sâu cập nhật tại `docs/thuc-hanh/BaoCao_ChiTiet.md` và `docs/thuc-hanh/KichBan_QuayVideo_Tuan_06.md`.
- Mã nguồn kiểm thử minh họa (Demo chống chỉ định & Unit test riêng biệt) đặt trực tiếp trong package `vn.edu.seminar` thuộc `case-study/src/test/java/`.
- Cấu hình pom và surefire hỗ trợ chạy cả JUnit 5 và TestNG minh họa (nếu cần module riêng hoặc test sample) mà không làm gãy pipeline CI chính.

**Tech Stack:** Java 25, JUnit Jupiter 6, Mockito 5, AssertJ, Spring Boot Test 4.1.1, TestNG 7.x (khảo sát/đối chiếu).

**Spec:** `PhanCong_NhiemVu.md` (Mục 5: Phân công Ngô Gia An và Mục 4: Các yêu cầu còn thiếu A-J).

## Global Constraints
- Tất cả các test bổ sung và test demo phải chạy xanh hoặc được cô lập bằng tag/profile phù hợp, không được làm hỏng lệnh chuẩn `mvn clean verify` của case study.
- Giữ nguyên cấu trúc dự án, ngôn ngữ tiếng Việt mạch lạc, chuyên nghiệp, chính xác về mặt thuật ngữ kiểm thử phần mềm (ISTQB / Martin Fowler / Gerard Meszaros).
- Không bịa đặt số liệu hay paper, các ví dụ code phải tự biên dịch và chạy được trên JDK 25.

## Review Focus
1. Test anti-pattern/chống chỉ định: phải giải thích rõ nguyên nhân kiến trúc dẫn đến lỗi thay vì chỉ đổ lỗi cho Mockito.
2. Tagging trong Maven Surefire: Đảm bảo class test demo chống chỉ định có tag `@Tag("antipattern")` để tránh bị Surefire chạy ngầm trong pipeline chính (vì pom đã cấu hình `test.excludedTags=...,antipattern,...`).
3. Khảo sát TestNG: So sánh tối thiểu 4 tiêu chí rõ ràng, khách quan dựa trên tính năng thật.
4. Test bổ sung của Ngô Gia An: Phải kiểm thử logic thực tế có giá trị (edge case hoặc business rule của `FineCalculator` / `LoanService`).

---

### Task 1: Soạn thảo phần "Khái niệm tổng quan về Unit Testing" trong Báo cáo

**Files:**
- Modify: `docs/thuc-hanh/BaoCao_ChiTiet.md`

**Interfaces:**
- Consumes: Cấu trúc báo cáo hiện tại ở Mục 2.
- Produces: Nội dung chuyên sâu về Unit Testing (Định nghĩa Unit, AAA, FIRST, Test Pyramid, Phân loại Test Double theo Meszaros, Test Oracle).

- [ ] **Step 1: Viết nội dung lý thuyết Unit Testing vào Mục 2 của `BaoCao_ChiTiet.md`**
  - Bổ sung định nghĩa Unit rõ ràng theo chuẩn công nghiệp (hành vi cô lập).
  - Trình bày chi tiết AAA (Arrange - Act - Assert).
  - Phân tích nguyên tắc FIRST (Fast, Independent, Repeatable, Self-validating, Timely).
  - Vẽ sơ đồ Text/ASCII và giải thích Test Pyramid (Unit -> Service/Integration -> UI/E2E).
  - Định nghĩa và phân biệt 5 loại Test Double: Dummy, Stub, Fake, Mock, Spy (kèm ví dụ cụ thể trong case-study).
  - Khái niệm Test Oracle: vai trò xác định pass/fail tự động.

- [ ] **Step 2: Kiểm tra định dạng markdown và tính mạch lạc**
  Đảm bảo không phá vỡ liên kết các mục khác trong báo cáo.

---

### Task 2: Trình bày Data-driven, Checkpoints & Record-Playback trong Unit Test

**Files:**
- Modify: `docs/thuc-hanh/BaoCao_ChiTiet.md`

**Interfaces:**
- Consumes: Case study `fine-cases.csv` và `FineCalculatorTest`.
- Produces: Mục giải trình 3 kỹ thuật kiểm thử theo yêu cầu của GV trong ngữ cảnh Unit Test.

- [ ] **Step 1: Soạn thảo phân tích 3 kỹ thuật vào `BaoCao_ChiTiet.md`**
  - **Data-driven Testing:** Tách biệt logic test và ma trận dữ liệu. Minh chứng bằng `@ParameterizedTest` và file `fine-cases.csv`.
  - **Checkpoints:** Điểm kiểm chứng trạng thái và hành vi. So sánh `assert` (state verification) vs `Mockito.verify` (behavior verification).
  - **Record & Playback:** Phân tích bản chất ban đầu (sinh test UI), cách áp dụng tương đương ở cấp Unit/Component (HTTP record/replay như WireMock, Golden Master testing / Snapshot testing) và lý do tại sao ở tầng Unit Test thuần túy, việc code tay test case rõ ràng, dễ bảo trì lại được ưu tiên hơn Record & Playback.

- [ ] **Step 2: Rà soát tính nhất quán với case study**
  Đảm bảo các ví dụ viện dẫn khớp chính xác với source code hiện có.

---

### Task 3: Xây dựng Demo trường hợp JUnit / Mockito không xử lý tốt (hoặc chống chỉ định)

**Files:**
- Create: `case-study/src/test/java/vn/edu/seminar/antipattern/MockitoAntiPatternTest.java`
- Modify: `docs/thuc-hanh/BaoCao_ChiTiet.md` (mục Điểm yếu công cụ)

**Interfaces:**
- Consumes: Spring Boot Test, Mockito.
- Produces: Class kiểm thử được gắn `@Tag("antipattern")` minh họa 3 lỗi điển hình:
  1. *Mock quá sâu (Train Wreck / vi phạm Law of Demeter)*: `when(a.getB().getC().doSomething())`.
  2. *Test tự xác nhận (Self-fulfilling prophecy)*: assert lại chính giá trị stub mà không kiểm tra logic thực sự.
  3. *Lạm dụng mock static / private / final*: tác động hiệu năng và cảnh báo về bad design (tight coupling).

- [ ] **Step 1: Tạo file test `MockitoAntiPatternTest.java`**
  Viết code minh họa 3 trường hợp kèm chú thích rõ ràng tại sao đó là anti-pattern và giải pháp khắc phục. Đánh dấu class bằng `@Tag("antipattern")`.

- [ ] **Step 2: Chạy test độc lập để xác minh mã biên dịch và chạy đúng ý đồ**
  Run: `cd case-study && ./mvnw test -Dtest=MockitoAntiPatternTest -Dtest.excludedTags=""`
  Expected: Các test case chạy thành công, log ra các cảnh báo/kết quả tương ứng.

- [ ] **Step 3: Chạy toàn bộ test suite để đảm bảo không gãy pipeline chuẩn**
  Run: `cd case-study && ./mvnw test`
  Expected: BUILD SUCCESS (nhờ exclusion `antipattern`).

- [ ] **Step 4: Cập nhật lý giải và phân tích các trường hợp này vào báo cáo `BaoCao_ChiTiet.md`**

---

### Task 4: Khảo sát và so sánh JUnit với TestNG

**Files:**
- Modify: `docs/thuc-hanh/BaoCao_ChiTiet.md` (Mục 5: Khảo sát công cụ)
- Create: `case-study/src/test/java/vn/edu/seminar/survey/TestNgComparisonNotes.md` (hoặc tích hợp trực tiếp bảng so sánh vào báo cáo)

**Interfaces:**
- Consumes: Tài liệu kỹ thuật JUnit 5 và TestNG 7.x.
- Produces: Bảng so sánh đa tiêu chí (≥ 4 tiêu chí) kèm đánh giá khi nào nên chọn cái nào.

- [ ] **Step 1: Viết bảng so sánh chuyên sâu JUnit 5 vs TestNG**
  - Tiêu chí 1: Data-driven testing (`@DataProvider` vs `@ParameterizedTest`, `@CsvSource`, `@MethodSource`).
  - Tiêu chí 2: Quản lý vòng đời & phân nhóm test (`@Test(groups = ...)` vs `@Tag`, dependencies giữa các test `dependsOnMethods`).
  - Tiêu chí 3: Chạy song song (Parallel execution) & cấu hình XML suite.
  - Tiêu chí 4: Hệ sinh thái, độ phổ biến và tích hợp với Spring Boot.

- [ ] **Step 2: Viết đoạn đánh giá thực nghiệm và kết luận lựa chọn công cụ**
  Lý giải tại sao case study chọn JUnit 5 Jupiter làm mặc định cho hệ sinh thái Spring Boot.

---

### Task 5: Tự viết thêm 1–2 test mới của Ngô Gia An vào Case Study

**Files:**
- Modify: `case-study/src/test/java/vn/edu/seminar/fine/FineCalculatorTest.java`
- Modify: `case-study/src/test/java/vn/edu/seminar/loan/LoanServiceTest.java`

**Interfaces:**
- Consumes: `FineCalculator.calculateLateFee`, `LoanService.borrow`.
- Produces: Các test case mới có ý nghĩa kiểm thử cao (ví dụ: kiểm thử idempotency hoặc boundary edge case mà bộ test cũ chưa thể hiện rõ).

- [ ] **Step 1: Thêm test case vào `FineCalculatorTest.java`**
  Thêm test kiểm tra giá trị ngày trễ cực biên hoặc kiểm tra tính trần tối đa khi đổi hạng hội viên (ví dụ: VIP trễ đúng 52 ngày thì đạt trần 50.000đ).

- [ ] **Step 2: Thêm test case vào `LoanServiceTest.java`**
  Thêm test kiểm tra hành vi độc lập khi hội viên có nợ phí cũ đúng 0đ thì vẫn được phép mượn sách.

- [ ] **Step 3: Chạy test xác nhận pass 100%**
  Run: `cd case-study && ./mvnw test -Dtest=FineCalculatorTest,LoanServiceTest`
  Expected: PASS

- [ ] **Step 4: Chạy toàn bộ verify & JaCoCo coverage**
  Run: `cd case-study && ./mvnw clean verify`
  Expected: BUILD SUCCESS, Jacoco pass 100% branch.

---

### Task 6: Soạn Kịch bản chi tiết và Checklist quay Video Demo Unit Test

**Files:**
- Modify: `docs/thuc-hanh/KichBan_QuayVideo_Tuan_06.md`

**Interfaces:**
- Consumes: Toàn bộ kết quả và mã nguồn của các Task 1-5.
- Produces: Kịch bản phân đoạn video Unit Test chi tiết (Setup, Khái niệm cơ bản, Demo đơn giản, Demo phức tạp, Data-driven, Trường hợp không xử lý được/antipattern) kèm timestamp gợi ý.

- [ ] **Step 1: Cập nhật kịch bản Video Unit Test (Video A)**
  - Phân đoạn 1 (0:00 - 1:00): Setup môi trường, cấu hình `pom.xml` (JUnit 5, Spring Boot Test).
  - Phân đoạn 2 (1:00 - 2:30): Khái niệm cơ bản & Demo đơn giản (UT-1) - AAA, chạy `FineCalculatorTest` đơn, đọc test runner.
  - Phân đoạn 3 (2:30 - 4:00): Data-driven testing (UT-2) - `@ParameterizedTest`, đọc CSV, kiểm thử giá trị biên.
  - Phân đoạn 4 (4:00 - 5:30): Mockito phức tạp (UT-3) - Stub vs Verify trên 3 repository của `LoanService`.
  - Phân đoạn 5 (5:30 - 7:00): Trường hợp công cụ gặp hạn chế / Anti-pattern (`MockitoAntiPatternTest`) - Train Wreck, Mock Self-fulfilling, bài học rút ra.

- [ ] **Step 2: Cập nhật bảng phân công và tiến độ trong `BangCongViec.md`**
  Đánh dấu trạng thái tiến độ các mục tương ứng của Ngô Gia An.
