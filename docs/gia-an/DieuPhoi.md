# Điều phối và kiểm tra trước nộp

Ngô Gia An (23120205), trưởng nhóm theo `PhanCong_NhiemVu.md` hiện tại. Tài liệu này là công cụ điều phối, không phải bằng chứng đã họp/nộp/gặp GV.

## Các mốc cần điền ngày thật

| Mốc | Quy tắc | Ngày thực tế | Bằng chứng |
|---|---|---|---|
| Hạn nộp seminar | Lấy từ thông báo GV | Chưa xác nhận | Link/thông báo GV |
| Gửi slide / gặp GV | Trước hạn nộp 3–4 ngày | Tính sau khi có hạn thật | Lịch hẹn hoặc phản hồi thật |
| Họp nhóm mỗi tuần | Mỗi người báo đã làm / đang làm / vướng | Chưa đặt lịch | Biên bản thật, tên người tham gia |
| Tập trình bày 1 | Chạy đủ tool/video | Chưa đặt lịch | Ghi nhận lỗi cần sửa |
| Tập trình bày 2 | Bấm giờ, kiểm Q&A | Chưa đặt lịch | Thời lượng đo thật |

## Theo dõi phần Gia An

- [x] AI-5 LoanService chạy thật và lưu evidence.
- [x] Chuẩn bị bộ công cụ AI-4 để người tự điền.
- [x] Kiểm nguồn paper, hạng venue và artifact.
- [x] Chạy lại phân tích dữ liệu CoverUp và thử dry-run source nhóm.
- [ ] Chạy sinh test mới của cả hai paper và lưu kết quả thực tế.
- [x] Đã nhận CSV/notes Gia An cung cấp; Codex khóa, commit rồi so và chạy Java: 23/23 người dùng, 13/13 AI. Độc lập theo tuyên bố trong notes; chờ Gia An tự review/chạy lại.
- [ ] Gia An đọc hiểu, chạy lại và xác nhận AI declaration.
- [ ] Thành viên khác review chéo và xác nhận phần của họ.
- [ ] Đủ URL video, timestamp thật và nội dung slide tương ứng.
- [ ] Gửi slide / gặp GV trước hạn 3–4 ngày.
- [ ] Điền Google Sheet contribution và xuất git log thật khi nộp.
- [ ] Kiểm gói: ≤20 file, mỗi file ≤20 MB, tổng ≤400 MB; tên ZipTool nếu cần chia/nén; không dùng Google Drive.

Ghi commit thật bằng `git log --date=iso-strict --format='%h | %aI | %an <%ae> | %s' seminar-core`. Bảng contribution phải mô tả đúng phần có AI hỗ trợ, không coi một tài khoản Git là bằng chứng cả nhóm đã thực hiện.

## Câu hỏi cần chuẩn bị cho phần AI/paper

| Câu hỏi | Ý cần trả lời |
|---|---|
| Vì sao AI test xanh vẫn thiếu? | Nháp LoanService 2 test chỉ 3/6 nhánh; mở gap và source |
| 100% branch có đủ? | Cần oracle/assertion, mutation; 9/9 chỉ trên tập mutant đã chạy |
| AI-4 đã có đối chứng chưa? | Đã khóa 23 ca Gia An cung cấp trước so sánh; ghi chú tuyên bố chỉ dựa đặc tả. Độc lập không được hash tự chứng minh |
| Hash chứng minh tác giả người? | Không; chỉ phát hiện dữ liệu thay đổi, vẫn cần xác nhận trung thực |
| Fixture sai có phải lỗi model thật? | Không; cài sẵn để minh họa, đã ghi nhãn |
| CoverUp có test Java không? | Tool gốc dùng Python; thử trên coverage_gaps.py, không dịch nghiệp vụ Java |
| 89,0% là kết quả nhóm tự sinh? | Là replay phân tích dữ liệu tác giả trên 163 module MT |
| ChatUniTest đã tái lập chưa? | Chưa; nêu đúng preflight/parse và kết quả thực tế, không gán AI-5 cho paper |
| Hạng của bài là gì? | FSE CORE2023 A* là venue; P2 demo track cần GV xác nhận |
| Ai tự review phần mới? | Chờ tên/ngày thật trong khai báo cá nhân, không điền thay |
