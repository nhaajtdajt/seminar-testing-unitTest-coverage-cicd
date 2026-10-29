# AI-4 — Sinh dữ liệu biên

Đặc tả duy nhất dùng để thiết kế dữ liệu: {{SPEC}}

Sinh dữ liệu biên độc lập từ đặc tả. Không được xem hoặc yêu cầu CSV người viết,
test tham chiếu, bộ AI cũ hoặc kết quả AI-1/AI-2. Bước đối chiếu được chương trình
thực hiện SAU khi nhận xong bộ dữ liệu mới này; không điều chỉnh bộ sinh theo đối chứng.

Xét trước/đúng/sau grace period; trước/đúng/sau mức trần; 0, ngày âm,
Integer.MAX_VALUE, Integer.MIN_VALUE và hạng null. Không tự thay đổi đặc tả.

CSV phải có đúng header: daysLate,tier,expected,expectedException
- daysLate là số nguyên Java int.
- tier là NORMAL, VIP hoặc NULL (NULL biểu diễn Java null).
- Ca hợp lệ: expected là số tiền không âm, expectedException để trống.
- Ca lỗi: expected để trống, expectedException là IllegalArgumentException.
- Mỗi cặp daysLate,tier xuất hiện một lần; có cả ca hợp lệ lẫn ca lỗi.
- Kết thúc mỗi dòng bằng newline. Không ghi comment trong CSV.

Chỉ trả JSON object, không Markdown fence:
{"analysis": "Lý do chọn các ca và phép tính expected", "csv": "Nội dung CSV hoàn chỉnh"}

Không tự tuyên bố dữ liệu đã pass hoặc bộ người viết sai; chưa có lượt chạy/đối chiếu.
