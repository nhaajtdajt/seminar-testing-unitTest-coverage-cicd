# Ghi chú bộ CSV LoanService

- Người viết 10 ca gốc: Gia An, theo thông tin người dùng cung cấp.
- Thời điểm viết bản gốc theo khai báo: 30/10/2026 14:00–14:30 (GMT+7).
- Nguồn ghi trong bản gốc: “Đặc tả chuẩn nghiệp vụ mượn sách thư viện (LoanService business logic)”.
- Bản gốc khai báo chưa xem test/data AI và tự chọn phân vùng/biên. Đây là khai báo của người viết, không được hash tự chứng minh.
- Bản hiện tại: Codex chỉnh theo source ngày 30/10/2026, theo yêu cầu “sửa lại theo src giúp tôi đi”. Bản này có AI hỗ trợ, kiểm hành vi implementation; không tuyên bố là đối chứng độc lập.
- Ai chỉnh và đóng gói frozen: Codex, thay mặt người dùng.

## Quy tắc đối chiếu từ source hiện tại

Source: `case-study/src/main/java/vn/edu/seminar/loan/LoanService.java` và `LoanException.java`.

- Thứ tự kiểm tra: sách tồn tại → sách available → thành viên tồn tại → hạn mức → nợ phí.
- Đang mượn >= 3 sách: `LIMIT_REACHED`.
- Nợ phí > 0: `UNPAID_FINE`, nếu chưa bị chặn bởi điều kiện trước đó.
- Thành công khi các điều kiện trên không chặn; phiếu mượn được lưu và sách chuyển unavailable.
- Miền dữ liệu: số sách đang mượn không âm; số tiền dùng dấu chấm thập phân.

## Các chỉnh sửa so với CSV người viết ban đầu

- bookId 1004: activeLoans 5 → 3; expectedCode TOO_MANY_LOANS → LIMIT_REACHED.
- bookId 1007: activeLoans 4 → 2, giữ expected SUCCESS để kiểm sát dưới hạn mức hiện tại.
- bookId 1010: activeLoans 5 → 3; expectedCode TOO_MANY_LOANS → LIMIT_REACHED, kiểm thứ tự lỗi khi đồng thời có nợ.
- Bảy ca còn lại giữ nguyên; giữ tổng số 10 ca.

AI-4 so CSV này với CSV Gemini sinh riêng qua cùng harness. Vì bộ này đã được chỉnh theo implementation, kết quả chỉ phản ánh khác biệt dữ liệu và hành vi đã chạy; không tự xác minh source đúng một đặc tả độc lập.
