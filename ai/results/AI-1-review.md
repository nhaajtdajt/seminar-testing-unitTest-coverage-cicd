# Review bản test AI-1

Nguồn sinh: Codex trong phiên làm việc hiện tại. Đây là demo AI hỗ trợ tương tác; không phải kết quả gọi API tự động, cũng chưa phải bản do thành viên nhóm xác nhận.

Bản đầu: `case-study/src/test/java/vn/edu/seminar/fine/FineCalculatorAiDraftTest.java` có 3 test: NORMAL trễ 1 ngày, VIP đúng 2 ngày gia hạn, NORMAL vượt trần. Chúng dùng logic thật và kiểm giá trị tiền bằng `isEqualByComparingTo`.

Đối chiếu source phát hiện thiếu: null; ngày âm; NORMAL 0 ngày; VIP vượt gia hạn; trước/đúng/sau mức trần theo từng hạng; số ngày cực lớn. Bổ sung bằng `FineCalculatorTest.java` và `fine-cases.csv`. Không ghi nhận test sai nếu cả ba test ban đầu thực sự pass; sự thiếu trường hợp kiểm thử được báo cáo riêng.

Checklist đọc source: có assertion cụ thể; không mock lớp tính phí; không dùng API giả; so tiền không phụ thuộc scale; dữ liệu biên phải khớp đặc tả. Số test pass và coverage trước/sau lấy từ log/XML đã chạy trong `evidence/tuan-05`, không suy từ việc đọc mã.

Nhóm cần tự review lại và điền người xác nhận trước khi nộp.
