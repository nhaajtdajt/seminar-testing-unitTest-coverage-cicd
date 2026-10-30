# Nguyễn Lê Thế Vinh (23120190): Case study

> Tự điền bằng lời của bạn. Thay mọi `___`. Chỉ ghi điều bạn thực sự đã làm.

## 1. Phần việc của tôi
- Việc được giao: Case study: chạy lại từ máy sạch và sửa README, viết thêm test web/persistence, mô tả nghiệp vụ cho slide, chuẩn bị môi trường demo, quay Video C.
- Link PR / commit của tôi: PR [#16](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/16) · các commit chính: `1d920a6` (test), `dea7828` (mô tả nghiệp vụ), `2262f09` (script demo), `9a1412b` (README), `f3db1d2` (tiến độ/AI usage), `4f193f5` (kịch bản Video C).

## 2. Tôi đã dùng AI như thế nào
| # | Công cụ AI | Tôi nhờ AI làm gì (tóm tắt prompt) | Kết quả AI đưa ra | Nằm ở đâu trong repo |
|---|---|---|---|---|
| 1 | Claude Code | Đọc phân công và chạy lại case study trên máy Ubuntu của tôi; sửa README theo lỗi gặp | Ghi lỗi JDK 17 (`release version 25 not supported`); tôi cài JDK 25 bằng apt; build 42/42 pass; thêm hướng dẫn Linux vào README | `README.md` mục "Chạy nhanh" |
| 2 | Claude Code | Viết thêm test tích hợp cho các ca chưa có test | 3 test: 404 `MEMBER_NOT_FOUND`, mượn bị từ chối không khóa sách, cuốn thứ 4 bị `LIMIT_REACHED` | `case-study/src/test/java/vn/edu/seminar/web/LoanFlowEdgeCaseTest.java` |
| 3 | Claude Code | Viết mô tả nghiệp vụ, sơ đồ luồng và script demo cho Video C | Tài liệu nghiệp vụ + sơ đồ Mermaid + đề xuất slide; script chạy 7 request | `docs/thuc-hanh/MoTa_NghiepVu_CaseStudy.md`, `scripts/demo_case_study.sh` |

## 3. Tôi đã review và kiểm chứng gì
- Tôi đã tự chạy lại: `case-study/mvnw -B -ntp -f case-study/pom.xml clean verify` → BUILD SUCCESS, 52/52 test, 0 failure/error/skipped, JaCoCo gate báo `All coverage checks have been met`; `case-study/mvnw -B -ntp -f case-study/pom.xml test -Dtest=LoanFlowEdgeCaseTest` → 3/3 pass; `scripts/demo_case_study.sh` → 7/7 request đúng mã (201, 409, 404, 404, 400, 409, 201).
- Tôi đã đọc hiểu: thứ tự kiểm tra trong `LoanService.borrow` (sách → sách còn trên kệ → thành viên → số sách đang mượn → nợ phí) và việc chỉ lưu phiếu/đổi trạng thái sách sau khi qua hết; test kiểm tra thêm trạng thái trong H2 để chắc request bị từ chối không ghi dữ liệu; script tự bật/tắt ứng dụng và H2 reset mỗi lần chạy.
- AI sai hoặc thiếu ở: con số `42/42` trong bảng ban đầu chỉ đúng trước khi merge `seminar-core`; sau merge bộ test là `52/52`. AI chưa cập nhật lại số này và chưa thể điền timestamp Video C vì video chưa quay.
- Tôi đã sửa: ghi rõ `42/42` (trước merge) và `52/52` (sau merge) trong bảng công việc/kịch bản Video C; thêm bước build JAR vào phần chuẩn bị quay; giữ trạng thái "chưa quay" thay vì điền timestamp giả.

## 4. Phần tôi tự làm, không dùng AI
Tôi tự cài JDK 25 (`sudo apt install -y openjdk-25-jdk-headless`), kiểm tra `java -version`/`mvnw -v`, tự chạy build, test và script demo rồi đối chiếu từng mã HTTP. Tôi tự đọc `LoanService.borrow`, `data.sql`, `LoanFlowEdgeCaseTest` để xác nhận nội dung AI viết khớp với nghiệp vụ và dữ liệu mẫu; tự quyết định giữ trạng thái "chưa quay" và không bịa timestamp; tự commit các thay đổi và tạo PR #16. Phần chữ do AI soạn (mô tả nghiệp vụ, script, README) tôi đã đọc lại và chỉnh theo kết quả chạy thật.

## 5. Điều tôi chưa chắc hoặc chưa kiểm được
Video C chưa quay nên chưa có URL/timestamp; kịch bản C-01..C-06 mới là bản chuẩn bị. Tôi chưa thử trên macOS/Windows hoặc máy hoàn toàn trống; README mới chỉ ghi nhánh Ubuntu 26.04 đã thử. Các kết quả 52/52 và 7 request là chạy local, chưa đối chiếu với run GitHub Actions mới nhất. Tôi cũng chưa kiểm tra tình huống nhiều instance/tải đồng thời (`synchronized` chỉ trong một tiến trình) và chưa có chức năng trả sách để kiểm luồng đó.

## 6. Xác nhận
Tôi xác nhận nội dung trên là đúng sự thật và tôi chịu trách nhiệm với phần của mình.

Ngày: 30/10/2026 · Ký tên (họ tên): Nguyễn Lê Thế Vinh
