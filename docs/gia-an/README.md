# Phần việc Ngô Gia An — 23120205

Căn cứ duy nhất về phạm vi: `PhanCong_NhiemVu.md`, mục **Ngô Gia An: AI, paper và trình bày (kiêm trưởng nhóm)** trên nhánh `seminar-core`. Triển khai với Codex hỗ trợ ngày 28/10/2026. Các commit dùng Git identity đã cấu hình; không đổi tác giả lịch sử và chưa push.

## Tóm gọn việc của bạn

1. Chọn 2–3 paper năm 2021–2026, kiểm hạng ≥B và source công khai; dùng code tác giả chạy lại rồi thử trên source/test nhóm.
2. Cho người tự viết dữ liệu biên AI-4 trước khi xem dữ liệu AI; mở rộng quy trình AI sang LoanService.
3. Khai báo đúng phần AI viết và phần người đã review/chạy lại.
4. Ghép nội dung slide/báo cáo; slide nền trắng chữ đen và nhắc/tóm tắt từng video.
5. Quay AI và paper sau khi artifact sẵn sàng; điều phối review, gặp GV trước hạn 3–4 ngày và nộp bài.

## Đã triển khai và kiểm chứng

| Yêu cầu | Artifact | Kết quả / giới hạn |
|---|---|---|
| AI-4 độc lập | [Dữ liệu và quy trình](../../ai/human/README.md), `scripts/ai4_compare.py`, Java human-data runner | Đã khóa 23 ca + ghi chú Gia An cung cấp; so 11 ca chung khớp; Java 23/23 pass, FineCalculator branch 10/10. Độc lập theo ghi chú; Codex chạy lệnh. [Kết quả](AI4_KetQua.md) |
| Lớp khác | [AI-5 review](../../ai/results/AI-5-loan-review.md), prompt và ba suite LoanService | Nháp 2 test, 3/6 branch → bổ sung 10 test, 6/6 branch; PIT 9/9; fixture sai đỏ đúng 1 assertion |
| Paper có code/hạng | [Danh mục và thử nghiệm](../../research/README.md) | CoverUp 2025, ChatUniTest 2024; FSE CORE2023 A*, ChatUniTest thuộc demo track |
| Tái hiện paper | `evidence/gia-an/papers/` | CoverUp replay **phân tích** 163 module đạt 89,0% vs 76,8%; dry-run trên source nhóm. ChatUniTest chưa có thí nghiệm generation; không nhận replay phân tích là chạy lại toàn bộ paper |
| Khai báo AI | [File Gia An](../../ai-usage-declaration/01_NgoGiaAn.md) | Điền đóng góp của Codex và bằng chứng; phần tự review/ký của bạn để chờ xác nhận |
| Slide/báo cáo | `slides/slides.json`, `slides/index.html`, `slides/slides.md`, báo cáo chi tiết mục Gia An | Có nội dung AI-4/5, hai paper, video và trạng thái; xem PDF xuất kèm nếu cần đọc/quay offline |
| Video | [Danh mục artifact](Video_Artifacts.md) | GA-01..07; các video khác ghi đúng người phụ trách; **chưa quay, chưa có YouTube/timestamp** |

## Bạn cần tự làm tiếp

- Đọc lại CSV/ghi chú và [kết quả AI-4](AI4_KetQua.md), tự chạy lại để xác nhận; dữ liệu đã khóa/commit/so sánh, không còn chờ tạo CSV.
- Đọc source/test mới, chạy các lệnh trong `Video_Artifacts.md`, ghi phần hiểu/sửa của mình và ký AI declaration khi thực sự xác nhận.
- Hoàn thiện generation thực nghiệm paper với model/môi trường thật, lưu cả lỗi và output; xác nhận GV chấp nhận demo track của ChatUniTest.
- Cung cấp ngày hạn thật trong [điều phối](DieuPhoi.md), tổ chức review và lịch gặp GV. Chưa có email, cuộc họp hoặc nộp bài nào được thực hiện thay bạn.
- Sau đó quay video theo artifact đã chuẩn bị; hướng dẫn quay chi tiết làm ở lượt sau.

Hoàn thành phần code/artifact không đồng nghĩa cả nhiệm vụ thành viên đã xong: các mục cần người, model và dịch vụ thật ở trên vẫn mở. Những thay đổi trên nhánh này đã được chia commit theo nội dung; chưa tạo issue/PR vì yêu cầu hiện tại là implement trực tiếp trên `seminar-core`.
