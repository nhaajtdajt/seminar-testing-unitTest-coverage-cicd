# Seminar: Unit Test · Code Coverage · CI/CD

> Nhánh `reportweek04`: tài liệu và bằng chứng của Tuần thực hành 04, tách từ `master` (chỉ chứa code). Mã nguồn và cách build nằm ở `master`; nhánh này chứa thêm báo cáo, slide, bằng chứng chạy và công cụ dựng tài liệu.

Case study quản lý thư viện, dùng chung từ unit test đến coverage và pipeline.

- Báo cáo Tuần thực hành 04: [Markdown](bao-cao-tuan/BaoCao_Tuan_04.md) · [HTML](bao-cao-tuan/BaoCao_Tuan_04.html).
- [Kế hoạch và phân công hàng tuần](KeHoach_BaoCao_HangTuan.md).
- [Hướng dẫn chạy và kịch bản demo](docs/thuc-hanh/HuongDan_Demo.md).
- [Bản thảo báo cáo chi tiết](docs/thuc-hanh/BaoCao_ChiTiet.md).
- [Minh chứng chạy thật tại máy](evidence/tuan-05/README.md).
- Bản nháp slide: mở `slides/index.html` bằng trình duyệt; phím ←/→ chuyển trang, Ctrl+P in.
- Source LaTeX: `report/main.tex` (dùng XeLaTeX).
- Gói đề xuất nộp lần 1, đặc tả thiết kế gốc và đề bài: nhánh [`noplan01`](../../tree/noplan01).

## Chạy nhanh

Yêu cầu JDK 25, Python 3.10+ cho script. Maven không cần cài: `case-study/mvnw` tự tải Maven 3.9.16. Cấu hình theo thiết kế gốc: Java 25, Spring Boot 4.1.1, JUnit Jupiter 6.0.3, Mockito 5.23.0, AssertJ 3.27.7, H2 2.4.240, JaCoCo 0.8.15, PIT 1.30.0.

Trên máy hiện tại, shell mặc định vẫn dùng Java 21; JDK 25 được cài riêng. Chọn JDK 25 cho phiên terminal trước khi build/chạy (máy khác thay bằng đường dẫn cài đặt của mình):

```bash
export JAVA_HOME=/home/pham-quang-vinh/.local/jdks/ubuntu-openjdk25/usr/lib/jvm/java-25-openjdk-amd64
export PATH="$JAVA_HOME/bin:$PATH"
case-study/mvnw -v
```

```bash
case-study/mvnw -B -ntp -f case-study/pom.xml clean verify
java -jar case-study/target/library-case-study-0.1.0.jar --server.port=8081
```

Ứng dụng chạy ở cổng **8081** vì cổng 8080 mặc định hay bị chiếm (ví dụ Jenkins cài sẵn trên máy này). Muốn dùng cổng khác thì đổi `--server.port` và cổng trong lệnh `curl` bên dưới.

```bash
curl -i http://localhost:8081/api/loans \
  -H 'Content-Type: application/json' \
  -d '{"bookId":1,"memberId":1}'
```

Lần đầu trả 201; mượn lại sách 1 trả 409. Tắt và khởi động lại để đặt lại dữ liệu. Ứng dụng dùng H2 in-memory (Spring Data JPA, dữ liệu mẫu trong `data.sql`); dữ liệu không được lưu bền khi tắt ứng dụng.

## Trạng thái ở Tuần thực hành 04, có phần làm trước Tuần 05

Mã nguồn, test, các demo coverage/mutation/TDD tại máy và bản thảo tài liệu đã được triển khai với AI hỗ trợ, bao gồm phần làm trước của kế hoạch Tuần 05. Workflow GitHub Actions và Jenkinsfile đã được viết. Việc chạy trên GitHub/Jenkins, bật quy tắc chặn merge, gọi API AI tự động và xác nhận đóng góp của 5 thành viên được liệt kê theo trạng thái thực tế trong báo cáo Tuần thực hành 04.

Đối chiếu chi tiết phần còn thiếu: [mục 8 của báo cáo Tuần thực hành 04](bao-cao-tuan/BaoCao_Tuan_04.md#8-phần-đã-làm-trước-và-phần-còn-lại-của-kế-hoạch-tuần-05). Repo đã dọn các file build/cache và bằng chứng của cấu hình cũ (Java 21 + Spring Boot 3.5); lịch dọn nằm trong `evidence/tuan-05/cleanup.json`. Chạy Maven sẽ tạo lại `case-study/target/`. Các tài liệu đề xuất cũ (`nop-lan-1/`, `docs/00-…`, `docs/superpowers/`, `require.md`) nằm ở nhánh `noplan01`.

Cấu hình và hướng dẫn tại `case-study/`, `docs/thuc-hanh/` mô tả bản thực hành hiện tại.
