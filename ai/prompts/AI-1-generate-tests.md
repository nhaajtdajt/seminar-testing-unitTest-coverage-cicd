# AI-1 — Sinh test từ source

Sinh bản nháp unit test từ đặc tả và source được cung cấp, không dùng bộ test/CSV tham chiếu.
Liệt kê các tình huống và giả định trước khi viết test. Không cố ý bỏ ca để làm coverage thấp.
Xét dữ liệu hợp lệ, đầu vào lỗi, mốc biên, grace period và mức trần nếu có trong đặc tả.
Không tự thêm API hoặc quy tắc nghiệp vụ. Mỗi test phải assert giá trị/exception cụ thể.

Đặc tả: {{SPEC}}

```java
{{SOURCE}}
```

Hợp đồng đầu ra có thể chạy:
- Java 25, JUnit Jupiter 6 và AssertJ đã có trong Maven; dùng @Test thông thường.
- Một lớp tên {{CLASS_NAME}}, package vn.edu.seminar.fine.
- Không mock logic thuần, không đọc/ghi file, không CSV, không gọi mạng/process.
- Không kế thừa lớp test khác, không @Tag, @Disabled, assumption hoặc test rỗng.
- So sánh BigDecimal bằng isEqualByComparingTo; không sửa production code.
- Không tự tuyên bố test đã pass hoặc đoán coverage khi chưa chạy.

Chỉ trả JSON object, không Markdown fence:
{"analysis": "Các tình huống, lý do và giả định", "test_source": "Toàn bộ file Java"}
