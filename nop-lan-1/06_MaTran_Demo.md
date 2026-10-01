# Ma trận demo

> Đề yêu cầu mỗi công cụ có **ít nhất 3 kịch bản demo**: *cài đặt · các chức năng cơ bản ·
> các luồng xử lý phức tạp*. Bảng này là **cam kết của nhóm**: mỗi demo làm gì, đo gì, và
> **để lại minh chứng gì** — vì đề nói rõ *"chỉ show được kết quả, không thể hiện được các
> bước làm rõ ràng cụ thể sẽ không được điểm cao"*.

---

## 1. Case study dùng chung cho mọi demo

Ứng dụng **quản lý thư viện** (Java + Spring Boot REST API), nghiệp vụ *cho mượn sách*.
Nhóm chọn nghiệp vụ này vì nó cung cấp đủ ba loại tình huống mà vẫn đủ nhỏ để trình bày
trên slide:

| Thành phần | Đặc điểm | Dùng để demo điều gì |
|---|---|---|
| Lớp **tính phí trả sách trễ** | Logic thuần, không phụ thuộc framework; nhiều nhánh điều kiện: số ngày trễ, số ngày được gia hạn theo hạng thành viên, hệ số giảm theo hạng, mức phí trần | Branch coverage · data-driven test · vòng TDD |
| Lớp **nghiệp vụ cho mượn sách** | Phối hợp 3 repository; **6 nhánh**: sách không tồn tại · sách đang được mượn · thành viên không tồn tại · vượt hạn mức mượn · còn phí trễ chưa trả · mượn thành công | Mockito · phân biệt unit test với integration test |
| **REST endpoint** `POST /api/loans` | Tầng ngoài cùng, có kiểm tra dữ liệu đầu vào | Kiểm thử tầng web · pipeline đầy đủ |

Việc **mọi demo dùng chung một case study** là có chủ ý: người nghe không phải làm quen lại
bài toán ở mỗi phần, và các con số coverage của phần 2 nối trực tiếp được với bộ test của
phần 1 và với pipeline của phần 3.

---

## 2. Chín demo công cụ

| Mã | Công cụ | Kịch bản | Nội dung | Số đo | Minh chứng để lại | Mức tự động |
|---|---|---|---|---|---|---|
| **UT-1** | JUnit | Cài đặt | Thêm thư viện test; chạy `mvn test` lần đầu; đọc output Surefire | Số test, thời gian | Log, thư mục báo cáo Surefire | Fully |
| **UT-2** | JUnit | Cơ bản | Viết lớp tính phí theo TDD (4 vòng đỏ–xanh); cấu trúc AAA; tên test tiếng Việt; chuyển sang test đọc dữ liệu từ file CSV ngoài | Số ca kiểm thử, số vòng TDD | **Commit history từng vòng đỏ/xanh** + file CSV dữ liệu | Fully |
| **UT-3** | Mockito | Phức tạp | Test lớp nghiệp vụ 6 nhánh; mock 3 repository; `verify`; `verify(never())`; `ArgumentCaptor`; đồng hồ cố định | Số nhánh phủ, số điểm kiểm chứng | File test, báo cáo Surefire | Fully |
| **CC-1** | JaCoCo | Cài đặt | Thêm plugin; sinh báo cáo HTML; giải thích từng cột | — | Ảnh chụp báo cáo, log | Fully |
| **CC-2** | JaCoCo | Cơ bản | Đo coverage với 1 test → bổ sung test cho nhánh đỏ → đo lại | **Độ phủ nhánh trước/sau** | **Hai báo cáo HTML** ở hai thời điểm | Fully |
| **CC-3** | JaCoCo | Phức tạp | Bật coverage gate (nhánh ≥ 90% cho lớp tính phí); xoá 1 test → build **fail**; khôi phục → xanh; gắn gate vào CI | Build pass/fail | Log `mvn verify` **cả hai** trạng thái; lần chạy CI đỏ và xanh | Fully |
| **CI-1** | GitHub Actions | Cài đặt | Workflow tối thiểu; xem lần chạy đầu; đọc log từng step | Thời gian chạy | Link lần chạy, ảnh chụp log | Fully |
| **CI-2** | GitHub Actions | Cơ bản | Bật cache thư viện; tải báo cáo coverage về dạng artifact; ghi tóm tắt vào trang summary | **Thời gian build trước/sau cache** (3 lần, lấy trung vị) | Hai link lần chạy, artifact tải được | Fully |
| **CI-3** | GitHub Actions | Phức tạp | 3 job nối tiếp `test → coverage-gate → package`; chạy song song 2 phiên bản JDK; chặn merge khi gate fail; PR đỏ rồi sửa xanh | Job nào fail, vì sao | **Link Pull Request đỏ → xanh**, log chạy song song | Fully |

---

## 3. Bốn demo áp dụng AI

Chi tiết ở `07_KeHoach_AI.md`. Tóm tắt để đặt cạnh chín demo trên:

| Mã | Làm gì | Số đo | Minh chứng để lại | Mức tự động |
|---|---|---|---|---|
| **AI-1** | AI sinh unit test từ một lớp | Coverage trước/sau; **số test AI sinh sai phải sửa tay** | Prompt template, diff giữa bản AI sinh và bản nhóm đã sửa | Semi |
| **AI-2** | AI đọc báo cáo coverage → chỉ nhánh chưa phủ → sinh test còn thiếu | Độ phủ nhánh trước/sau; số nhánh AI chỉ đúng / chỉ sai | Script lọc báo cáo, prompt, hai báo cáo | Semi |
| **AI-3** | AI tự động nhận xét chất lượng test trên mỗi Pull Request | Số vấn đề thật / số báo động giả trên 1 PR có lỗi cài sẵn | Cấu hình job trong pipeline, ảnh chụp nhận xét trên PR | **Fully** |
| **AI-4** | AI sinh bộ dữ liệu biên cho data-driven test | So bộ AI với bộ người viết: trùng bao nhiêu, thêm gì, **bỏ sót gì** | Prompt, hai file CSV, bảng đối chiếu 3 cột | Semi |

---

## 4. Ánh xạ sang ba phần đề bài yêu cầu

Đề yêu cầu mỗi công cụ có đủ **Record and Playback · Data driven · Checkpoints**. Nhóm hiểu
đây là khung của công cụ kiểm thử tự động giao diện, không ánh xạ trực tiếp sang chủ đề này,
nên đề xuất cách hiểu tương đương dưới đây — **xin ý kiến thầy/cô**, chi tiết ở
`09_CauHoi_Cho_GV.md`.

| Phần trong đề | Nhóm hiểu là | Demo tương ứng |
|---|---|---|
| **Record and Playback** | "Record" = sinh test tự động thay vì gõ tay (IDE tạo khung test, AI sinh test từ mã nguồn). "Playback" = chạy lại bộ test đã sinh, tự động, trong pipeline | UT-1 · **AI-1** · CI-1 |
| **Data driven** | Một test chạy với nhiều bộ dữ liệu, dữ liệu tách rời khỏi mã test và đọc từ file CSV bên ngoài | UT-2 · **AI-4** |
| **Checkpoints** | Các điểm kiểm chứng có khả năng **làm fail build**: assertion, `verify()` của Mockito, coverage gate, quality gate trong pipeline | UT-3 · **CC-3** · CI-3 |

---

## 5. Tổng kết

| | Số lượng |
|---|---|
| Demo công cụ | 9 (3 công cụ × 3 kịch bản) |
| Demo áp dụng AI | 4 |
| **Tổng** | **13** |

- Đủ yêu cầu *"ít nhất 3 kịch bản demo"* cho mỗi công cụ.
- Mỗi demo đều ở mức **fully automated** hoặc **semi-automated**, đúng yêu cầu của đề.
- **Mỗi demo đều có ít nhất một số đo và một minh chứng để lại** — đây là cách nhóm đáp ứng
  yêu cầu "thể hiện được các bước làm rõ ràng cụ thể".
