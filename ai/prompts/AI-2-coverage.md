# AI-2 — Đề xuất test từ khoảng trống coverage

Đọc source và JSON trích từ JaCoCo. XML chỉ cho biết số nhánh bỏ sót trên dòng,
không xác định chính xác nhánh true/false. Đối chiếu source trước khi kết luận.

Source: {{SOURCE}}

Khoảng trống: {{GAPS_JSON}}

Với mỗi đề xuất, ghi file/dòng, quy tắc nghiệp vụ, đầu vào, kết quả mong đợi và lý do.
Sinh test JUnit chạy được; không xóa assertion hoặc giảm ngưỡng gate để tăng độ phủ.
Chỉ tuyên bố cải thiện sau khi đã chạy lại và đối chiếu báo cáo.
