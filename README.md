# Seminar: Unit Test · Code Coverage · CI/CD

> Nhánh `seminar-core`: bản gọn chỉ giữ phần quan trọng (mã nguồn, test, CI, AI, slide, báo cáo chi tiết, bài tập và bằng chứng đã chọn lọc). Báo cáo tuần cũ, HTML sinh tự động và các lượt chạy lặp đã bỏ; xem lịch sử ở các nhánh `reportweek04` và `noplan01`.

Case study quản lý thư viện, dùng chung từ unit test đến coverage và pipeline.

- [Phân công nhiệm vụ hiện tại](PhanCong_NhiemVu.md) · [Bảng công việc](docs/thuc-hanh/BangCongViec.md).
- [Hướng dẫn chạy và kịch bản demo](docs/thuc-hanh/HuongDan_Demo.md).
- [Bài làm thử từ ứng dụng đến paper, kèm expected](docs/thuc-hanh/ThucHanh_App_Paper.md).
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

Ứng dụng chạy ở cổng **8081** vì cổng 8080 mặc định hay bị chiếm (ví dụ một dịch vụ khác trên máy). Muốn dùng cổng khác thì đổi `--server.port` và cổng trong lệnh `curl` bên dưới.

```bash
curl -i http://localhost:8081/api/loans \
  -H 'Content-Type: application/json' \
  -d '{"bookId":1,"memberId":1}'
```

Lần đầu trả 201; mượn lại sách 1 trả 409. Tắt và khởi động lại để đặt lại dữ liệu. Ứng dụng dùng H2 in-memory (Spring Data JPA, dữ liệu mẫu trong `data.sql`); dữ liệu không được lưu bền khi tắt ứng dụng.

## Trạng thái và giới hạn tái hiện

Mã nguồn, test, demo coverage/mutation/TDD và tài liệu seminar được triển khai với AI hỗ trợ. Đã tích hợp core mới: workflow CI tự chạy trên PR và push master/seminar-core; bằng chứng GitHub đỏ/xanh và required checks theo snapshot nằm ở [github-actions](evidence/tuan-06/github-actions/README.md). Lượt local sau tích hợp ngày 29/10 đạt 39/39 test và gate pass. Trạng thái còn chờ ở bảng công việc; không suy ra cấu hình live từ snapshot hoặc sửa tác giả lịch sử.

Phần còn thiếu và trạng thái từng hạng mục: xem [Bảng công việc](docs/thuc-hanh/BangCongViec.md). Repo đã dọn các file build/cache và bằng chứng của cấu hình cũ (Java 21 + Spring Boot 3.5). Chạy Maven sẽ tạo lại `case-study/target/`. Các tài liệu đề xuất cũ (`nop-lan-1/`, `docs/00-…`, `docs/superpowers/`) nằm ở nhánh `noplan01`. Đề bài gốc của thầy: [require.md](require.md).

Cấu hình và hướng dẫn tại `case-study/`, `docs/thuc-hanh/` mô tả bản thực hành hiện tại. Lượt xác minh source, HTTP và Gemini API cho gói tuần này nằm trong `evidence/tuan-06/`. Video là yêu cầu seminar theo `PhanCong_NhiemVu.md`; kịch bản/ảnh chỉ là chuẩn bị, không thay video đã quay. Phần slide/HTML riêng của Gia An được hoãn đến cuối.


## AI và paper — Ngô Gia An (23120205)

- Nội dung AI ở [báo cáo mục 6](docs/thuc-hanh/BaoCao_ChiTiet.md); paper ở mục 9 và [research/README.md](research/README.md).
- Lệnh chạy theo cùng format nhóm tại [hướng dẫn mục 9](docs/thuc-hanh/HuongDan_Demo.md). AI LoanService dùng `run_ai_demo.py draft/improved/mistake/mutation`; AI-4 dùng `human/data`. Chọn output mới và chạy tuần tự.
- [AI-4](evidence/tuan-06/ai-4/README.md): đã khóa CSV/notes 23 ca Gia An cung cấp trước so; 23/23 người dùng và 13/13 AI pass. Độc lập theo notes, Codex chạy lệnh.
- [AI Loan](evidence/tuan-06/ai-loan/README.md): 2 → 10 test, branch 50% → 100%, PIT 9/9. [Paper evidence](evidence/tuan-06/papers/README.md): mới reanalysis/dry-run/parse, chưa generation.
- Bằng chứng dùng chung `evidence/tuan-06/<chu-de>/<luot>/`: `run.json`, `output.log`, `site/jacoco/`, `pit-reports/`. Không để docs/evidence theo thư mục tên cá nhân.
- [Video E](docs/thuc-hanh/KichBan_QuayVideo_Tuan_06.md) mới có artifact GA-01..07; chưa quay, chưa URL/timestamp. [Bảng công việc](docs/thuc-hanh/BangCongViec.md) theo dõi phần còn chờ.
- Theo yêu cầu ngày 29/10, phần slide/HTML của Gia An làm sau cùng. Giữ nguyên slide/source renderer từ core, đã gỡ các PDF/Markdown slide tự xuất trước đó; không còn bản xuất riêng để nộp nhầm.
