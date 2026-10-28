# Kịch bản video demo — Tuần 06

**Mục đích:** hướng dẫn quay demo Unit Test, Code Coverage và luồng ứng dụng. Đây là kịch bản quay, không phải video đã ghi. Chỉ đưa video vào gói nộp sau khi quay thật và kiểm tra file phát được.

## Video A — Unit Test (5–7 phút) — Người thực hiện: Ngô Gia An (23120205)

**Yêu cầu sư phạm:** Đầy đủ 5 phân đoạn chuẩn theo yêu cầu của GV: Setup môi trường, Khái niệm cơ bản (UT-1), Data-driven & Biên (UT-2), Mockito nâng cao (UT-3), và Trường hợp công cụ không xử lý tốt / Anti-patterns.

| Phân đoạn | Timestamp | Nội dung chi tiết cần quay và thuyết minh | Lệnh / File minh chứng |
|---|---|---|---|
| **1. Setup môi trường** | `00:00 - 01:00` | - Giới thiệu Java 25 (`java --version`), cấu trúc project `case-study/`, Maven Wrapper (`./mvnw`).<br>- Mở `pom.xml`, chỉ ra `spring-boot-starter-test` quản lý JUnit Jupiter 6 và Mockito 5. | `java --version`<br>`case-study/pom.xml` |
| **2. Khái niệm & UT-1** | `01:00 - 02:15` | - Khái niệm Unit test, quy tắc AAA (Arrange-Act-Assert).<br>- Chạy `FineCalculatorTest` cơ bản.<br>- Mở Surefire XML report (`target/surefire-reports/TEST-*.xml`) để giải thích trạng thái Pass, Fail, Error và thời gian thực thi (nguyên tắc Fast của FIRST). | `./mvnw test -Dtest=FineCalculatorTest`<br>`target/surefire-reports/` |
| **3. Data-driven & Biên (UT-2)** | `02:15 - 03:45` | - Trình bày kỹ thuật Data-driven testing: tách mã test khỏi dữ liệu.<br>- Mở `fine-cases.csv` phân tích các mốc biên (0 ngày, ân hạn 2 ngày VIP, chạm trần 50.000 VND).<br>- Mở code `@ParameterizedTest` kết hợp `@CsvFileSource`.<br>- Chạy test và cho thấy 15 test con được sinh ra tự động từ bảng dữ liệu. | `fine-cases.csv`<br>`FineCalculatorTest.java` |
| **4. Mockito phức tạp (UT-3)** | `03:45 - 05:15` | - Khái niệm Test Double: Stub vs Mock/Spy.<br>- Trình bày `LoanServiceTest`: giải thích tại sao cô lập 3 Repository bằng Mockito mock để tập trung test logic mượn sách.<br>- Demo 1 ca nghiệp vụ lỗi (nợ phí / hết hạn mức): `verify` không lưu phiếu mượn.<br>- Demo ca mượn thành công: dùng `ArgumentCaptor` kiểm tra thông tin phiếu mượn và cập nhật trạng thái sách. | `LoanServiceTest.java`<br>`./mvnw test -Dtest=LoanServiceTest` |
| **5. Trường hợp công cụ gặp hạn chế / Anti-patterns** | `05:15 - 06:45` | - Mở file `MockitoAntiPatternTest.java` (đánh dấu `@Tag("antipattern")`).<br>- Minh họa **Train Wreck Mocking** (vi phạm định luật Demeter).<br>- Minh họa **Self-fulfilling Prophecy** (test chính mock thay vì test code thật).<br>- Minh họa lạm dụng mock pure logic & cảnh báo JVM khi inline mock static/final.<br>- Kết luận bài học thực tế cho kiểm thử đơn vị. | `MockitoAntiPatternTest.java`<br>`./mvnw test -Dtest=MockitoAntiPatternTest -Dtest.excludedTags=""` |

## Video B — Coverage và mutation testing (5–7 phút)

1. Chạy profile baseline và mở `target/site/jacoco/index.html`.
2. Giải thích line coverage và branch coverage trên `FineCalculator`.
3. Chạy bộ đầy đủ, mở gate result và chỉ ra điều kiện pass.
4. Mở PIT weak/strong; giải thích killed/survived mutant bằng source và assertion liên quan.
5. Kết luận ngắn: coverage là tín hiệu thực thi; PIT bổ sung góc nhìn về sức phát hiện lỗi.

## Video C — Ứng dụng / HTTP (3–5 phút)

1. Khởi chạy JAR và chỉ ra dữ liệu mẫu H2 được nạp khi ứng dụng khởi động.
2. Gửi request mượn hợp lệ; giải thích response 201.
3. Gửi lại cùng sách; giải thích 409 `BOOK_UNAVAILABLE`.
4. Thử một request sai và một tình huống dữ liệu mẫu không đủ quyền mượn.
5. Nhắc rằng dữ liệu là H2 in-memory và reset khi khởi động lại.

## Checklist quay và bàn giao

- [ ] Quay màn hình ứng dụng/repository đã làm sạch thông báo cá nhân; dùng tiếng nói hoặc phụ đề giải thích.
- [ ] Hiển thị tên thao tác và kết quả đầu ra đủ lâu để đọc.
- [ ] Lưu MP4/MOV thật dưới `evidence/tuan-06/video/`.
- [ ] Phát thử từ đầu đến cuối; kiểm tra âm thanh, chữ, mã HTTP và đường dẫn.
- [ ] Ghi thời lượng, dung lượng, người quay và SHA-256 vào `evidence/tuan-06/video/README.md`.
- [ ] Nếu chưa quay, để trạng thái “chưa có file video”; không dùng storyboard hoặc ảnh làm bằng chứng video.
