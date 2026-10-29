# AI-4 — Sinh dữ liệu từ source và schema tương ứng

Class cần kiểm thử: {{TARGET_CLASS}}
Yêu cầu nghiệp vụ: {{REQUIREMENTS}}
Schema/domain: {{SCHEMA}}
Source production: {{SOURCE}}
Schema CSV đã được xác định cho class này: {{CSV_SCHEMA}}

Sinh dữ liệu mới theo schema, suy ra điều kiện, biên, expected và exception từ input trên.
Không dùng quy tắc hoặc giá trị nghiệp vụ mặc định. Không có CSV người viết, test tham chiếu
hoặc output AI-1/AI-2 trong request này. Không yêu cầu xem bộ đối chứng; bước so sánh chỉ
diễn ra sau khi bạn trả lời. Xét trạng thái dependency khi API cần mock.

Mỗi tổ hợp input xuất hiện một lần, expected cụ thể để harness kiểm được. Không thêm cột
hoặc comment. Tuân thủ thứ tự header, null token và kiểu dữ liệu trong schema.

Chỉ trả JSON object, không Markdown fence:
{"analysis": "Lý do chọn ca, cách suy ra expected và giả định", "csv": "CSV hoàn chỉnh gồm header"}

Không tự tuyên bố đã chạy test, coverage tăng hoặc bộ người viết sai.
