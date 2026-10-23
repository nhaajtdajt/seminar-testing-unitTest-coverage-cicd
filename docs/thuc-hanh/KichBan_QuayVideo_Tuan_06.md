# Kịch bản video demo — Tuần 06

**Mục đích:** hướng dẫn quay demo Unit Test, Code Coverage và luồng ứng dụng. Đây là kịch bản quay, không phải video đã ghi. Chỉ đưa video vào gói nộp sau khi quay thật và kiểm tra file phát được.

## Video A — Unit Test (5–7 phút)

1. Giới thiệu Java 25, project `case-study/` và yêu cầu chạy lại.
2. Chạy test `FineCalculatorTest`; mở Surefire XML để giải thích pass/fail/error.
3. Mở `fine-cases.csv`, giải thích dữ liệu biên và `@CsvFileSource`.
4. Chạy `LoanServiceTest`; chỉ ra một nhánh nghiệp vụ lỗi, một nhánh thành công, verify không ghi dữ liệu khi lỗi.
5. Chỉ ra `LoanFlowTest` dùng H2 thật trong phạm vi integration test và nêu giới hạn của mock.

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
