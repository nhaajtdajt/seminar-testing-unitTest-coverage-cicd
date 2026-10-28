# Seminar: Unit Test · Code Coverage · CI/CD

> Nhánh `seminar-core`: bản gọn chỉ giữ phần quan trọng (mã nguồn, test, CI, AI, slide, báo cáo chi tiết, bài tập và bằng chứng đã chọn lọc). Báo cáo tuần cũ, HTML sinh tự động và các lượt chạy lặp đã bỏ; xem lịch sử ở các nhánh `reportweek04` và `noplan01`.

Case study quản lý thư viện, dùng chung từ unit test đến coverage và pipeline.

- [Phân công nhiệm vụ hiện tại](PhanCong_NhiemVu.md) · [Bảng công việc](docs/thuc-hanh/BangCongViec.md).
- [Hướng dẫn chạy và kịch bản demo](docs/thuc-hanh/HuongDan_Demo.md).
- [Báo cáo chi tiết](docs/thuc-hanh/BaoCao_ChiTiet.md).
- [Bài tập áp dụng](docs/thuc-hanh/BaiTap_Tuan_06.md) · [Kịch bản quay video](docs/thuc-hanh/KichBan_QuayVideo_Tuan_06.md) (kịch bản, chưa có video).
- Minh chứng: [Tuần 06 (mới nhất)](evidence/tuan-06/README.md) · [Các lượt chạy chính](evidence/tuan-05/README.md).
- Slide: mở `slides/index.html` bằng trình duyệt (←/→ chuyển trang, Ctrl+P in); nguồn `slides/slides.json`, dựng bằng `scripts/render_slides.py`.
- LaTeX: `report/main.tex` (XeLaTeX).
- Đề bài và gói đề xuất ban đầu: nhánh [`noplan01`](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/tree/noplan01).

## Chạy nhanh

Yêu cầu JDK 25, Python 3.10+ cho script. Maven không cần cài: `case-study/mvnw` tự tải Maven 3.9.16. Cấu hình theo thiết kế gốc: Java 25, Spring Boot 4.1.1, JUnit Jupiter 6.0.3, Mockito 5.23.0, AssertJ 3.27.7, H2 2.4.240, JaCoCo 0.8.15, PIT 1.30.0.

Chọn JDK 25 cho phiên terminal trước khi build/chạy. Đường dẫn bên dưới chỉ là ví dụ; thay bằng đường dẫn cài đặt JDK 25 trên máy đang dùng:

```bash
# Homebrew Apple Silicon; JDK 25 can be installed but not registered with java_home.
export JAVA_HOME=/opt/homebrew/opt/openjdk@25
export PATH="$JAVA_HOME/bin:$PATH"
java -version
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

## Trạng thái và giới hạn tái hiện

Mã nguồn, test, demo coverage/mutation/TDD và tài liệu seminar đã được triển khai với AI hỗ trợ. Workflow GitHub Actions và Jenkinsfile đã được viết. Trạng thái hiện tại và các giới hạn được ghi trong báo cáo Tuần 05; lịch sử Git không bị sửa để nhận công của tuần khác.

Phần còn thiếu và trạng thái từng hạng mục: xem [Bảng công việc](docs/thuc-hanh/BangCongViec.md). Repo đã dọn các file build/cache và bằng chứng của cấu hình cũ (Java 21 + Spring Boot 3.5). Chạy Maven sẽ tạo lại `case-study/target/`. Các tài liệu đề xuất cũ (`nop-lan-1/`, `docs/00-…`, `docs/superpowers/`, `require.md`) nằm ở nhánh `noplan01`.

Cấu hình và hướng dẫn tại `case-study/`, `docs/thuc-hanh/` mô tả bản thực hành hiện tại. Lượt xác minh source, HTTP và Gemini API cho gói tuần này nằm trong `evidence/tuan-06/`. Theo phạm vi nộp mới nhất, video, kịch bản và ảnh demo không thuộc checklist Tuần 05; các tệp đã có được giữ làm tài liệu tùy chọn.


## Phần Ngô Gia An (23120205), cập nhật 28/10/2026

- [Phạm vi và kết quả](docs/gia-an/README.md), [artifact video](docs/gia-an/Video_Artifacts.md), [paper](research/README.md).
- AI LoanService: `python3 scripts/run_ai_demo.py draft --output /tmp/ga-draft`, đổi `draft` thành `improved`, `mistake`, `mutation` hoặc `full` cho từng lượt. Mỗi output phải mới; chạy tuần tự.
- [AI-4 đối chứng người viết](ai/human/README.md): đã nhận và khóa 23 ca + ghi chú Gia An cung cấp; cả 23 ca pass. Xem [kết quả AI-4](docs/gia-an/AI4_KetQua.md); độc lập theo ghi chú, Codex chạy lệnh.
- [Evidence mới](evidence/gia-an/README.md): 39 test chuẩn; nháp/bổ sung 2→10 test, branch 50→100%, PIT 9/9. Paper mới đạt replay phân tích/dry-run/parse, chưa generation.
- Slide nguồn `slides/slides.json` sinh HTML/Markdown bằng `python3 scripts/render_slides.py`; bản PDF nằm ở `output/pdf/`. Export bằng `scripts/render_artifacts.mjs` với Node + marked + playwright và Chrome (chi tiết trong source script).
- Chưa quay video, chưa có URL YouTube/timestamp; chưa xác nhận review cá nhân, gặp GV hoặc nộp bài.
