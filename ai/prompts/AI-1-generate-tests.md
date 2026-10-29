# AI-1 — Sinh test từ source

Class cần kiểm thử: {{TARGET_CLASS}}
Yêu cầu nghiệp vụ (nếu có): {{REQUIREMENTS}}
Schema/domain: {{SCHEMA}}
Source class và dependency production: {{SOURCE}}

Suy ra API, constructor, dependency, điều kiện, kiểu dữ liệu và giá trị biên từ input trên.
Không có quy tắc hoặc giá trị nghiệp vụ mặc định. Nêu giả định và khác biệt giữa
kiểm hành vi implementation với kiểm yêu cầu độc lập. Không đọc test/CSV tham chiếu.
Nếu class có dependency, dùng Mockito stub theo đường đi cần kiểm; không stub dư.
Với clock/random ID, kiểm ổn định theo API thật, không đoán ID hoặc thời gian hiện tại.
Không cố ý bỏ ca để làm coverage thấp. Mỗi test phải kiểm hành vi cụ thể.

Hợp đồng đầu ra có thể chạy:
- Java 25, JUnit Jupiter 6 và AssertJ đã có trong Maven; dùng @Test thông thường.
- Một lớp tên {{CLASS_NAME}}, package {{PACKAGE}} (nếu package trống thì không khai báo package).
- Không mock chính class được kiểm. Không CSV, file, mạng/process, database/server thật.
- Không Spring context; controller/repository được kiểm ở mức unit với dependency mock.
- Nêu rõ unit test trực tiếp không kiểm được HTTP validation, ORM mapping hoặc wiring thật.
- Không kế thừa lớp test khác, không @Tag, @Disabled, assumption hoặc test rỗng.
- So sánh BigDecimal bằng isEqualByComparingTo; không sửa production code.
- Không tự tuyên bố test đã pass hoặc đoán coverage khi chưa chạy.

Chỉ trả JSON object, không Markdown fence:
{"analysis": "Các tình huống, lý do và giả định", "test_source": "Toàn bộ file Java"}
