# AI-1 — Sinh test từ source

Đọc đặc tả và mã nguồn, liệt kê từng nhánh trước khi viết test JUnit Jupiter + AssertJ.
Mỗi test phải kiểm giá trị hoặc ngoại lệ cụ thể; không mock lớp chỉ có logic thuần.
Bao gồm dữ liệu hợp lệ, dữ liệu sai, giá trị biên và trường hợp tiền chạm/vượt mức trần.
Không tự thêm API không có trong mã nguồn. Phân biệt giả định với quy tắc đã được cung cấp.

Đặc tả: {{SPEC}}

```java
{{SOURCE}}
```

Đầu ra: danh sách nhánh, file test, dữ liệu CSV, các giả định cần con người xác nhận.
Sau khi sinh, người sử dụng chạy test, đọc từng assertion và lưu coverage trước/sau.
