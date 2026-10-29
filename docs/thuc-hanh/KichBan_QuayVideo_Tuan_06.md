# Kịch bản video demo — Tuần 06

**Mục đích:** hướng dẫn quay demo Unit Test, Code Coverage và luồng ứng dụng. Đây là kịch bản quay, không phải video đã ghi. Chỉ đưa video vào gói nộp sau khi quay thật và kiểm tra file phát được.

## Video A — Unit Test (5–7 phút) — Người thực hiện: Nguyễn Bảo An (23120207)

**Yêu cầu sư phạm:** Đầy đủ 5 phân đoạn chuẩn theo yêu cầu của GV: Setup môi trường, Khái niệm cơ bản (UT-1), Data-driven & Biên (UT-2), Mockito nâng cao (UT-3), và Trường hợp công cụ không xử lý tốt / Anti-patterns.

| Phân đoạn | Timestamp | Nội dung chi tiết cần quay và thuyết minh | Lệnh / File minh chứng |
|---|---|---|---|
| **1. Setup môi trường** | `00:00 - 01:00` | - Giới thiệu Java 25 (`java --version`), cấu trúc project `case-study/`, Maven Wrapper (`./mvnw`).<br>- Mở `pom.xml`, chỉ ra `spring-boot-starter-test` quản lý JUnit Jupiter 6 và Mockito 5. | `java --version`<br>`case-study/pom.xml` |
| **2. Khái niệm & UT-1** | `01:00 - 02:15` | - Khái niệm Unit test, quy tắc AAA (Arrange-Act-Assert).<br>- Chạy `FineCalculatorTest` cơ bản.<br>- Mở Surefire XML report (`target/surefire-reports/TEST-*.xml`) để giải thích trạng thái Pass, Fail, Error và thời gian thực thi (nguyên tắc Fast của FIRST). | `./mvnw test -Dtest=FineCalculatorTest`<br>`target/surefire-reports/` |
| **3. Data-driven & Biên (UT-2)** | `02:15 - 03:45` | - Trình bày kỹ thuật Data-driven testing: tách mã test khỏi dữ liệu.<br>- Mở `fine-cases.csv` phân tích các mốc biên (0 ngày, ân hạn 2 ngày VIP, chạm trần 50.000 VND).<br>- Mở code `@ParameterizedTest` kết hợp `@CsvFileSource`.<br>- Chạy test và cho thấy 15 test con được sinh ra tự động từ bảng dữ liệu. | `fine-cases.csv`<br>`FineCalculatorTest.java` |
| **4. Mockito phức tạp (UT-3)** | `03:45 - 05:15` | - Khái niệm Test Double: Stub vs Mock/Spy.<br>- Trình bày `LoanServiceTest`: giải thích tại sao cô lập 3 Repository bằng Mockito mock để tập trung test logic mượn sách.<br>- Demo 1 ca nghiệp vụ lỗi (nợ phí / hết hạn mức): `verify` không lưu phiếu mượn.<br>- Demo ca mượn thành công: dùng `ArgumentCaptor` kiểm tra thông tin phiếu mượn và cập nhật trạng thái sách. | `LoanServiceTest.java`<br>`./mvnw test -Dtest=LoanServiceTest` |
| **5. Trường hợp công cụ gặp hạn chế / Anti-patterns** | `05:15 - 06:45` | - Mở file `MockitoAntiPatternTest.java` (đánh dấu `@Tag("antipattern")`).<br>- Minh họa **Train Wreck Mocking** (vi phạm định luật Demeter).<br>- Minh họa **Self-fulfilling Prophecy** (test chính mock thay vì test code thật).<br>- Minh họa lạm dụng mock pure logic & cảnh báo JVM khi inline mock static/final.<br>- Kết luận bài học thực tế cho kiểm thử đơn vị. | `MockitoAntiPatternTest.java`<br>`./mvnw test -Dtest=MockitoAntiPatternTest -Dtest.excludedTags=""` |

## Video B — Code Coverage và mutation testing (8–9 phút) — Người thực hiện: Trương Nhật Đạt (23120231)

**Yêu cầu sư phạm:** đủ các phân đoạn GV yêu cầu: Setup, Khái niệm cơ bản, Demo đơn giản, Demo phức tạp, Trường hợp công cụ không xử lý được. Lệnh đầy đủ ở `HuongDan_Demo.md` (CC-0 → CC-6). Nếu tách thành nhiều video, giữ nguyên tên phân đoạn để slide dẫn chiếu.

| Phân đoạn | Timestamp | Nội dung chi tiết cần quay và thuyết minh | Lệnh / File minh chứng |
|---|---|---|---|
| **1. Setup** | `00:00 - 01:00` | - Mở `pom.xml`: plugin JaCoCo (`prepare-agent`, `report`, `check` với BRANCH ≥ 90% cho `FineCalculator`) và PIT (`targetClasses` = `${pit.classes}`).<br>- Giải thích JaCoCo là Java agent gắn vào bytecode lúc chạy test, không sửa mã nguồn. | `case-study/pom.xml` |
| **2. Khái niệm cơ bản: các loại coverage** | `01:00 - 03:00` | - Mở `LoanPeriodPolicy.java`: chỉ ra 6 câu lệnh, 2 quyết định, 3 điều kiện con, 4 đường đi.<br>- Chạy cộng dồn T1 → T2 → T3; mỗi lần mở HTML JaCoCo, chỉ dòng xanh/vàng và số nhánh 3/6 → 5/6 → 6/6.<br>- Đọc bảng mục 3.1: statement đạt từ T1, decision từ T2, condition và MC/DC từ T3, path từ T4.<br>- Chạy bộ T2 + T3: condition đủ nhưng dòng `days += 7` đỏ, tức condition ≠ decision. | CC-0 trong `HuongDan_Demo.md`<br>`BaoCao_ChiTiet.md` mục 3.1, 3.3 |
| **3. Demo đơn giản: trước/sau (CC-1/CC-2)** | `03:00 - 04:00` | - Chạy `-Pbaseline`: `FineCalculator` 5/10 nhánh (50%).<br>- Chạy bộ đầy đủ: 10/10 nhánh.<br>- Chỉ cột Line và cột Branch khác nhau. | `-Pbaseline clean verify`<br>`clean verify` |
| **4. Demo phức tạp: gate và mutation (CC-3/CC-4) + công cụ thứ hai** | `04:00 - 06:00` | - Gate đỏ: baseline + bật gate → `Rule violated`, Maven exit 1; bộ đầy đủ → `All coverage checks have been met`.<br>- Test bẫy: 100% branch nhưng PIT chỉ diệt 3/11; bộ đầy đủ 10/11. Mở báo cáo PIT, đọc một mutant sống.<br>- OpenClover: cùng bộ {T1, T2}, OpenClover báo 4/4 (100%), JaCoCo báo 5/6 (83%). Giải thích hai công cụ định nghĩa "branch" khác nhau. | CC-3, CC-4, CC-0b<br>`BaoCao_ChiTiet.md` mục 5.2 |
| **5. Trường hợp công cụ không xử lý được** | `06:00 - 08:30` | - **Quyết định ẩn trong thư viện:** chạy `FineCalculatorNoCapTest`: JaCoCo 10/10, gate pass, PIT mặc định 10/11 giống hệt bộ tốt, nhưng không ca nào chạm trần 50.000. Bật `INLINE_CONSTS`: mutant `50000 → 50001` sống.<br>- **Mutant tương đương:** mở mutant dòng 15 (`<=` → `<`), giải thích vì sao không đầu vào nào phân biệt được.<br>- **PIT chậm:** so log `clean test` (39 test, 22 s) với PIT toàn project (85 s, 46 mutant).<br>- Kết luận: coverage cho biết code đã chạy; PIT cho biết test có bắt lỗi không; cả hai vẫn cần người đọc đặc tả. | CC-5, CC-6<br>`BaoCao_ChiTiet.md` mục 3.4 |

## Video D — CI/CD với GitHub Actions (8–9 phút) — Người thực hiện: Phạm Quang Vinh (23120202)

**Yêu cầu sư phạm:** đủ các phân đoạn GV yêu cầu: Setup, Khái niệm cơ bản, Demo đơn giản, Demo phức tạp, Trường hợp công cụ không xử lý tốt. Mọi cảnh quay trên GitHub thật; link run nằm ở `evidence/tuan-06/github-actions/`.

| Phân đoạn | Timestamp | Nội dung chi tiết cần quay và thuyết minh | Lệnh / File minh chứng |
|---|---|---|---|
| **1. Setup** | `00:00 - 01:00` | - Mở `.github/workflows/ci.yml`: trigger `pull_request`, `push` (master, seminar-core), `workflow_dispatch`.<br>- Chỉ `runs-on: ubuntu-latest`, `setup-java` JDK 25 (temurin), `permissions: contents: read`.<br>- Nói rõ nhóm chỉ dùng GitHub Actions, không dựng Jenkins. | `.github/workflows/ci.yml` |
| **2. Khái niệm cơ bản** | `01:00 - 02:15` | - CI là gì, khác Continuous Delivery và Deployment; nhóm dừng ở bước tạo JAR.<br>- Vẽ pipeline `test → coverage-gate → package`, giải thích `needs`.<br>- Mở `pom.xml`: `jacoco:check`, BRANCH ≥ 0,90 cho `FineCalculator`. | `case-study/pom.xml`<br>báo cáo mục 4.1 |
| **3. Demo đơn giản (CI-1/CI-2)** | `02:15 - 04:00` | - Tab Actions, mở [run xanh 40722865221](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40722865221): 3 job xanh.<br>- Mở log `mvnw clean test`, mở step summary, tải artifact `tests-jdk-25`, `coverage`, `library-app`.<br>- Chỉ dòng `Cache saved` / `Cache restored` trong log `setup-java`. | `evidence/tuan-06/github-actions/README.md` |
| **4. Demo phức tạp (CI-3): PR đỏ rồi xanh** | `04:00 - 06:30` | - Mở [PR #2](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/2): xóa `FineCalculatorTest`.<br>- [Run đỏ 40723239123](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40723239123): `test` xanh, `coverage-gate` đỏ với `Rule violated ... 0.00 ... 0.90`, `package` skipped.<br>- Khôi phục test, [run xanh 40723623913](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40723623913).<br>- Mở [PR #6](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/6): nút Merge bị chặn, trạng thái BLOCKED nhờ required checks trên `master`. | `evidence/tuan-06/github-actions/README.md` |
| **5. Trường hợp công cụ không xử lý tốt** | `06:30 - 08:30` | - **Cache bị vô hiệu:** [PR #9](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/9) chỉ thêm một dòng comment vào `pom.xml`, log ghi `maven cache is not found`; nêu trung thực chênh lệch thời gian nhỏ hơn dao động.<br>- **Test chạy hai lần** (`clean test` rồi `clean verify`).<br>- **Thời gian runner dao động** (29–70 s cùng bước).<br>- **Required check làm PR kẹt** khi workflow trên master chưa có trigger ([PR #4](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/4)).<br>- **Gate chỉ kiểm cái được cấu hình**: test bẫy 100% branch vẫn pass gate. | `evidence/tuan-06/github-actions/ci-weaknesses.md` |
| **6. Kết** | `08:30 - 09:00` | - Tóm tắt: CI chặn code thiếu test nhưng không đo chất lượng assertion; cần PIT và review.<br>- Nhắc video liên quan: A (Unit Test), B (Coverage). | slide CI/CD |

## Video C — Ứng dụng / HTTP (3–5 phút)

1. Khởi chạy JAR và chỉ ra dữ liệu mẫu H2 được nạp khi ứng dụng khởi động.
2. Gửi request mượn hợp lệ; giải thích response 201.
3. Gửi lại cùng sách; giải thích 409 `BOOK_UNAVAILABLE`.
4. Thử một request sai và một tình huống dữ liệu mẫu không đủ quyền mượn.
5. Nhắc rằng dữ liệu là H2 in-memory và reset khi khởi động lại.

**Người thực hiện:** Nguyễn Lê Thế Vinh (23120190). Chạy `PAUSE=1 scripts/demo_case_study.sh` để đi lần lượt 7 request (201, 409 `BOOK_UNAVAILABLE`, 404 `BOOK_NOT_FOUND`, 404 `MEMBER_NOT_FOUND`, 400, 409 `UNPAID_FINE`, 201), dừng chờ Enter giữa các bước. Mở đầu video bằng sơ đồ luồng trong `MoTa_NghiepVu_CaseStudy.md`; cuối video chạy `LoanFlowEdgeCaseTest` để cho thấy cùng tình huống được test tự động. **Chưa quay.**

## Video E — AI và paper — Người thực hiện: Ngô Gia An (23120205)

**Trạng thái:** mới chuẩn bị artifact, chưa quay/đăng YouTube. Timestamp thực tế điền sau khi quay; chưa ấn định thời lượng. Slide/HTML phần Gia An hoãn đến cuối; chưa đưa nội dung mới vào slide chung.

| Phân đoạn | Timestamp | Nội dung cần minh họa | Lệnh / File minh chứng |
|---|---|---|---|
| **GA-01: Setup** | Chưa quay | Java 25, Maven Wrapper, script collector; phân biệt Codex tương tác và Gemini API | `run_ai_demo.py full`; evidence source verify |
| **GA-02: Nháp và gap** | Chưa quay | LoanService nháp 2 test pass nhưng chỉ 3/6 branch; đọc gap/source | `run_ai_demo.py draft`; `evidence/tuan-06/ai-loan/draft/` |
| **GA-03: Phức tạp** | Chưa quay | Bổ sung 10 test, 6/6 branch; assertion/captor và PIT 9/9 | `run_ai_demo.py improved`, `mutation`; `ai-loan/improved/`, `pit-strong/` |
| **GA-04: Oracle sai** | Chưa quay | Fixture kỳ vọng mượn được khi giữ 3 sách; đúng một assertion fail | `run_ai_demo.py mistake`; fixture cài sẵn, không gọi là lỗi model thật |
| **GA-05: Data driven / AI-4** | Chưa quay | Notes/CSV người dùng → hash và commit khóa → đối chiếu → Java; 23/23 vs 13/13 pass, branch 100% vs 80% | `HuongDan_Demo.md` mục 9.3; `evidence/tuan-06/ai-4/README.md` |
| **GA-06: CoverUp** | Chưa quay | Nguồn/rank, script tác giả trên 163 module, 89,0% vs 76,8%; dry-run không sinh test | `research/README.md`; `evidence/tuan-06/papers/` |
| **GA-07: ChatUniTest** | Chưa quay | Generation–validation–repair; parse case study 20 class/28 method; generation và tái lập gốc còn chờ | `research/chatunitest/`; `evidence/tuan-06/papers/` |

Mọi lệnh đầy đủ ở `HuongDan_Demo.md` mục 9; mỗi lượt lưu output mới trước khi chạy clean tiếp theo. Không dùng số liệu cũ để nói là vừa chạy. Chỉ quay như một thí nghiệm thành công khi có kết quả thật; phần generation paper còn chờ model/môi trường. URL YouTube và timestamp GA-01..07 chưa có, ghi sau khi thực sự quay/xem lại. Hướng dẫn thao tác quay chi tiết làm ở bước sau.

## Checklist quay và bàn giao

- [ ] Quay màn hình ứng dụng/repository đã làm sạch thông báo cá nhân; dùng tiếng nói hoặc phụ đề giải thích.
- [ ] Hiển thị tên thao tác và kết quả đầu ra đủ lâu để đọc.
- [ ] Lưu MP4/MOV thật dưới `evidence/tuan-06/video/`.
- [ ] Phát thử từ đầu đến cuối; kiểm tra âm thanh, chữ, mã HTTP và đường dẫn.
- [ ] Ghi thời lượng, dung lượng, người quay và SHA-256 vào `evidence/tuan-06/video/README.md`.
- [ ] Nếu chưa quay, để trạng thái “chưa có file video”; không dùng storyboard hoặc ảnh làm bằng chứng video.
