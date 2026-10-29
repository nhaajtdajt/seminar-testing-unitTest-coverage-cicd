# AI-4 — Suy ra schema dữ liệu và harness từ source

Class cần kiểm thử: {{TARGET_CLASS}}
Yêu cầu nghiệp vụ: {{REQUIREMENTS}}
Schema/domain: {{SCHEMA}}
Source production: {{SOURCE}}
Header cần tương thích (chỉ tên cột, không có dòng dữ liệu): {{CSV_HEADER}}

Thiết kế schema CSV cho trạng thái/input và expected của class này. Input có thể gồm
tham số phương thức và trạng thái dependency mock. Suy ra kiểu và quy tắc từ source;
không có schema nghiệp vụ mặc định. Nếu header đã có, giữ đúng tên/thứ tự; nếu chưa có,
tự thiết kế header phù hợp. Không sinh dòng data hoặc ca mẫu ở bước này.

Sinh harness dùng chung cho CSV người và AI:
- Java 25, JUnit Jupiter 6, AssertJ, Mockito khi cần; package {{PACKAGE}}, class {{CLASS_NAME}}.
- Đúng một @ParameterizedTest và @CsvFileSource(resources="/cases.csv", numLinesToSkip=1).
- Mỗi cột nhận bằng String rồi parse theo schema, xử lý blank/null token và quoting CSV.
- Mỗi dòng kiểm expected output/exception và interaction phù hợp; không tính expected bằng
  chính thuật toán đang test. Chỉ mock dependency, không mock đối tượng được kiểm.
- Không @Disabled, @Tag, assumption, test rỗng, kế thừa test, mạng/process hoặc Spring context.
- Không ghi đè production hoặc dùng test tham chiếu.

Chỉ trả JSON:
{
  "analysis": "Ánh xạ cột vào API/mock state, expected, null và giả định",
  "columns": [{"name": "tên cột", "type": "string|integer|decimal|boolean", "role": "input|expected", "nullable": false, "null_tokens": []}],
  "test_source": "Toàn bộ harness Java"
}
Phải có input và expected. Tên cột là identifier, không trùng. Schema/harness cần người review;
không tự tuyên bố đã kiểm đúng yêu cầu hoặc đã chạy test.
