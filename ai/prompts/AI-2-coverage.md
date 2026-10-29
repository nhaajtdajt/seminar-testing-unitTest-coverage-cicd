# AI-2 — Đề xuất test từ khoảng trống coverage

Đọc source và JSON trích từ JaCoCo. XML chỉ cho biết số nhánh bỏ sót trên dòng,
không xác định chính xác nhánh true/false. Đối chiếu source trước khi kết luận.

Đặc tả: {{SPEC}}

Source: {{SOURCE}}

Test nháp đã được chạy (phải giữ nguyên):
{{DRAFT_TEST}}

Kết quả JUnit/coverage thật của bản nháp:
{{TEST_RESULT}}

Khoảng trống: {{GAPS_JSON}}

Với mỗi đề xuất, ghi file/dòng, quy tắc nghiệp vụ, đầu vào, kết quả mong đợi và lý do.
Sinh test bổ sung JUnit chạy được; không xóa assertion hoặc giảm ngưỡng gate.
Nếu coverage đã đầy đủ, nói rõ và xem xét biên/assertion chưa kiểm; không hứa tăng coverage.
Test bổ sung phải có ích, không chỉ lặp lại cùng input/assertion của bản nháp.

Hợp đồng đầu ra:
- Java 25, JUnit Jupiter 6 + AssertJ; @Test thông thường.
- Một lớp mới tên {{CLASS_NAME}}, package vn.edu.seminar.fine; không kế thừa lớp nháp.
- Không sửa bản nháp/production, không @Tag, @Disabled, assumption hoặc test rỗng.
- Không CSV, file, mạng/process; dùng isEqualByComparingTo cho BigDecimal.
- Chỉ trả JSON, không Markdown fence:
{"analysis": "Bằng chứng, tình huống bổ sung, expected và lý do", "test_source": "Toàn bộ file Java"}

Chỉ xác nhận cải thiện sau khi người dùng chạy lại và so báo cáo thực tế.
