# Bài tập seminar — Tuần 06

Tài liệu này đi kèm các phần Unit Test và Code Coverage. Làm bài theo thứ tự: mô tả hành vi cần kiểm → viết/sửa test → chạy đúng profile → đọc báo cáo → giải thích kết quả. Các bài yêu cầu đổi nghiệp vụ thực hiện trên bản sao của repository.

## Bài 1 — Unit Test: thêm hạng thành viên

**Mục tiêu:** thực hành phân tích điều kiện biên và data-driven test.

Thêm hạng `STUDENT` theo chính sách giả định cho bài tập: được miễn phí 1 ngày, sau đó tính 500 VND/ngày, mức trần 20.000 VND. Không thay đổi chính sách `NORMAL` hoặc `VIP` trong case study chính.

1. Viết bảng đầu vào/đầu ra cho 0, 1, 2 ngày; ngày chạm và vượt trần; số ngày âm; hạng `null`.
2. Viết test trước khi sửa calculator. Dùng assertion số tiền chính xác và kiểm tra ngoại lệ cho dữ liệu không hợp lệ.
3. Nếu dùng CSV, thêm cột cho hạng, số ngày và số tiền mong đợi; giải thích mỗi dòng là một invocation.
4. Chạy test mục tiêu, sau đó chạy `clean verify` trên bản sao. Kiểm tra test không làm thay đổi kết quả của `NORMAL`/`VIP`.

### Đáp án gợi ý

| Hạng | Ngày trễ | Phí mong đợi |
|---|---:|---:|
| STUDENT | 0 | 0 VND |
| STUDENT | 1 | 0 VND |
| STUDENT | 2 | 500 VND |
| STUDENT | 40 | 19.500 VND |
| STUDENT | 41 | 20.000 VND |
| STUDENT | 42 | 20.000 VND |

Ngày âm và hạng `null` phải bị từ chối theo cùng hợp đồng kiểm tra đầu vào hiện có. Nếu nhóm muốn chính sách khác cho `STUDENT`, ghi rõ đó là thay đổi đề xuất và cập nhật toàn bộ expected values trước khi chạy.

## Bài 2 — Coverage không đồng nghĩa với assertion tốt

**Mục tiêu:** phân biệt line/branch coverage với khả năng bắt lỗi.

1. Tạo một test calculator thực thi nhánh phí dương nhưng bỏ assertion số tiền.
2. Chạy `-Pcoverage-trap clean verify`; lưu HTML/XML JaCoCo vào một thư mục riêng.
3. Chạy PIT cho cùng lớp và lưu mutation report.
4. So sánh hai báo cáo: coverage có thể giữ nguyên trong khi mutant thay đổi phép tính vẫn sống.
5. Thêm assertion tiền chính xác; chạy lại PIT và giải thích mutant bị diệt hoặc tương đương.

Không chép đè các báo cáo chuẩn trong `evidence/tuan-05/`. Có thể dùng thư mục tạm hoặc bản sao repo cho kết quả bài tập.

### Đáp án gợi ý

JaCoCo đo phần mã/nhánh đã được thực thi; nó không xác nhận assertion đã kiểm đúng giá trị nghiệp vụ. PIT biến đổi mã để xem test có phát hiện thay đổi đó không. Kết luận cần dựa trên mutation cụ thể, source và test; mutant sống không tự động chứng minh test sai nếu mutant tương đương.

## Bài 3 — Đọc coverage gate trong pipeline

**Mục tiêu:** giải thích điều kiện chặn build mà không hạ ngưỡng để làm xanh giả.

1. Chạy profile baseline để lấy báo cáo ban đầu.
2. Chạy bộ test đầy đủ với gate đang cấu hình.
3. Ghi exit code, tỷ lệ branch của `FineCalculator`, ngưỡng và test chịu trách nhiệm cho nhánh còn thiếu.
4. Trên bản sao, bỏ một test biên rồi xác nhận gate thất bại; khôi phục test và xác nhận gate thành công.
5. Vẽ luồng `test → coverage check → package` và chỉ ra job nào bị chặn khi check lỗi.

### Đáp án gợi ý

Gate phải giữ nguyên ngưỡng đã chốt. Khi gate thất bại, truy ngược nhánh thiếu và bổ sung test/logic theo đặc tả; không giảm ngưỡng chỉ để pipeline xanh. Bằng chứng local không được mô tả như một lần chạy GitHub Actions/Jenkins.

## Bài 4 — Phân biệt unit, web và integration test

**Mục tiêu:** chọn đúng mức kiểm thử cho một lỗi.

Với từng thay đổi sau, nêu test phù hợp nhất và một giới hạn còn lại: (a) sai công thức phí, (b) JSON thiếu `bookId`, (c) repository không lưu phiếu mượn, (d) API trả sai mã HTTP.

### Đáp án gợi ý

| Thay đổi | Mức kiểm thử phù hợp | Giới hạn cần nói rõ |
|---|---|---|
| Công thức phí | Unit test `FineCalculator` | Không chứng minh API hay persistence nối đúng |
| JSON request | Web/controller test | MockMvc không xác nhận server chạy trên máy thật |
| Lưu phiếu | Repository hoặc integration test H2 | H2 in-memory không đại diện cấu hình CSDL triển khai |
| Mã HTTP | Controller/HTTP smoke | Smoke trên máy không phải kiểm thử tải hay môi trường production |

## Checklist nộp bài

- [ ] Ghi lệnh, JDK, thời điểm và exit code.
- [ ] Lưu log cùng báo cáo HTML/XML; không chỉ chụp số phần trăm.
- [ ] Gắn test với requirement/nhánh cụ thể.
- [ ] Nêu rõ kết quả local, dịch vụ từ xa và giới hạn môi trường.
- [ ] Không ghi nhận bài tập gợi ý như kết quả đã thực hiện nếu chưa chạy.
