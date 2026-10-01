# ĐỌC TRƯỚC — Hướng dẫn gói nộp

**Môn:** Kiểm thử phần mềm — CQ2023/31 · FIT@HCMUS
**Chủ đề seminar:** Unit Test · Code Coverage · CI/CD
**Đợt nộp:** Seminar — Lần 1 — Nội dung chuẩn bị seminar (trước buổi kickoff meeting với GVTH)
**Nhóm:** *(điền GroupID và tên 5 thành viên)*
**Ngày nộp:** 02/10/2026

---

## 1. Gói nộp này gồm gì

| File | Nội dung | Đọc khi nào |
|---|---|---|
| `00_DocTruoc.md` | File này — hướng dẫn đọc | Đầu tiên |
| **`01_DeXuat_NoiDung_Seminar.md`** | **Bản đề xuất chính** — toàn bộ nội dung dự kiến, gọn trong 9 mục | **Nếu chỉ đọc một file, đọc file này** |
| `02_Outline_UnitTest.md` | Outline chi tiết phần Unit Test | Khi cần xem độ sâu phần 1 |
| `03_Outline_CodeCoverage.md` | Outline chi tiết phần Code Coverage | Khi cần xem độ sâu phần 2 |
| `04_Outline_CICD.md` | Outline chi tiết phần CI/CD | Khi cần xem độ sâu phần 3 |
| `05_KhaoSat_SoSanh_CongCu.md` | Khảo sát và so sánh công cụ theo 7 trục | Khi cần xem phần khảo sát |
| `06_MaTran_Demo.md` | 13 demo: làm gì, đo gì, để lại minh chứng gì | Khi cần xem kế hoạch demo |
| `07_KeHoach_AI.md` | 4 demo áp dụng AI + quy ước sử dụng AI của nhóm | Khi cần xem phần AI |
| `08_PhanCong_TienDo.md` | Phân công 5 thành viên, cách tạo minh chứng, tiến độ theo tuần | Khi cần xem phần quản lý nhóm |
| `09_CauHoi_Cho_GV.md` | **7 câu nhóm xin ý kiến thầy/cô ở buổi kickoff** | Trước buổi gặp mặt |

## 2. Tóm tắt một trang

**Nhóm hiểu chủ đề như một chuỗi, không phải ba bài rời:**

> **Unit Test** sinh ra các phép kiểm chứng → **Code Coverage** cho biết phép kiểm chứng đó
> đã chạm tới đâu trong mã nguồn → **CI/CD** bắt buộc cả hai phải chạy ở cổng merge, không
> phụ thuộc việc ai nhớ chạy.

**Case study xuyên suốt:** ứng dụng quản lý thư viện (Java + Spring Boot REST API), nghiệp vụ
cho mượn sách. Đủ ba loại tình huống cần thiết: một lớp logic thuần nhiều nhánh điều kiện
(demo branch coverage và data-driven test), một lớp nghiệp vụ phối hợp nhiều repository với
6 nhánh (demo Mockito), và một REST endpoint (demo kiểm thử tầng web).

**Ba công cụ demo sâu** (mỗi trụ một công cụ, mỗi công cụ đủ 3 kịch bản demo theo yêu cầu đề):

| Trụ | Demo sâu | Sẽ khảo sát & so sánh thêm |
|---|---|---|
| Unit Test | JUnit Jupiter + Mockito + AssertJ | TestNG, Spock, JUnit 4, EasyMock, JMockit, Hamcrest |
| Code Coverage | JaCoCo | Cobertura, OpenClover, coverage của IntelliJ; thêm PIT (mutation testing) |
| CI/CD | GitHub Actions | Jenkins, GitLab CI, CircleCI |

**Số lượng demo dự kiến:** 9 demo công cụ + 4 demo AI = 13 demo.

**Hai yêu cầu trong đề mà nhóm xem là then chốt và thiết kế bài làm xoay quanh:**

1. *"Chỉ show được kết quả, không thể hiện được các bước làm rõ ràng cụ thể sẽ không được
   điểm cao"* → mọi demo để lại dấu vết kiểm chứng được: commit history theo từng vòng TDD,
   log pipeline chạy thật, **hai** báo cáo coverage ở hai thời điểm trước/sau.
2. *"Chỉ rõ những trường hợp công cụ có điểm yếu"* → mỗi công cụ có một mục riêng về điểm
   yếu, và mỗi điểm yếu phải chứng minh bằng code chạy thật, không chỉ nói lý thuyết.

## 3. Điểm quan trọng nhất nhóm xin ý kiến thầy/cô

Đề yêu cầu mỗi công cụ có đủ **Record and Playback · Data driven · Checkpoints**. Nhóm hiểu
đây là khung quen thuộc của công cụ kiểm thử tự động giao diện (Selenium IDE, Katalon), không
ánh xạ trực tiếp sang unit test / coverage / CI-CD. Nhóm đề xuất cách hiểu tương đương:

| Phần trong đề | Nhóm hiểu là |
|---|---|
| **Record and Playback** | Sinh test tự động thay vì gõ tay (IDE tạo khung test, AI sinh test từ source), rồi "playback" = chạy lại bộ test đó trong pipeline |
| **Data driven** | Một test chạy với nhiều bộ dữ liệu: `@ParameterizedTest` đọc dữ liệu từ file CSV bên ngoài |
| **Checkpoints** | Các điểm kiểm chứng làm **fail build**: assertion, `verify()` của Mockito, coverage gate, quality gate trong pipeline |

Nếu cách hiểu này sai, nhóm xin điều chỉnh **ngay ở giai đoạn này**, trước khi đầu tư làm demo.
Chi tiết ở `09_CauHoi_Cho_GV.md`.

## 4. Nhóm đã làm được gì tính tới thời điểm nộp

| Hạng mục | Trạng thái |
|---|---|
| Phân tích đề, chốt phạm vi và tiêu chí thành công | Xong |
| Chốt case study và bộ công cụ | Xong |
| Outline chi tiết cả 3 trụ | Xong — trong gói này |
| Khảo sát & so sánh công cụ theo 7 trục | Xong bản dự kiến — các ô chưa tự kiểm đều ghi rõ *"chưa kiểm"* |
| Thiết kế 13 kịch bản demo kèm số đo | Xong — trong gói này |
| Kế hoạch áp dụng AI + quy ước sử dụng AI | Xong — trong gói này |
| Phân công 5 thành viên, ranh giới file, cách tạo minh chứng | Xong — trong gói này |
| Repository GitHub + khung case study chạy được | Đang dựng, dự kiến xong tuần 3 |
| Các demo, slide, báo cáo, video | Theo tiến độ ở `08_PhanCong_TienDo.md` |

**Nhóm tự đánh giá:** gói nộp lần 1 này là *kế hoạch và thiết kế*, chưa phải sản phẩm demo.
Nhóm chủ động trình bày sớm để xin GVTH góp ý và chỉnh hướng trước khi đầu tư vào phần thực thi.
