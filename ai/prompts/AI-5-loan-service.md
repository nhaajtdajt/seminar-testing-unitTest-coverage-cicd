# AI-5: tái sử dụng quy trình trên LoanService

Nguồn sinh test: Codex tương tác ngày 28/10/2026. Không gọi Gemini cho lượt này.

## Bản nháp

Đọc `LoanService`, các record và repository tương ứng. Sinh unit test JUnit Jupiter + Mockito cho mượn thành công và sách không tồn tại. Dùng Clock.fixed, kiểm kết quả cụ thể và trạng thái sách. Không đọc test tham chiếu để tuyên bố một baseline độc lập.

## Bổ sung

Đầu vào: source cùng báo cáo JaCoCo của bản nháp, trích gap bằng `scripts/coverage_gaps.py`. Liệt kê nhánh chưa chạy; bổ sung sách unavailable, member missing, số sách ở 2/3/4, nợ nhỏ nhất dương. Kiểm chính xác mã lỗi, không ghi repository khi bị từ chối; capture phiếu lưu và kiểm ID sách, thành viên, thời điểm. Giữ nháp để so sánh. Coverage không tự đánh giá chất lượng assertion; dùng PIT riêng cho lớp LoanService.

## Giới hạn

Codex có thể nhìn thấy test/source trong cùng phiên, vì vậy đây là minh họa khả năng tái sử dụng workflow, không phải benchmark độc lập. `LoanServiceAiMistakeTest` là fixture cố ý cài kỳ vọng sai để tập phát hiện oracle sai, không phải lỗi quan sát được từ một lời gọi API. Không sửa nghiệp vụ để làm fixture sai chuyển xanh.
