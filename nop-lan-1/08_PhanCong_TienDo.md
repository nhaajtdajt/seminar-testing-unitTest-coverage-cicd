# Phân công nhóm & Tiến độ

**Phụ trách:** TV1 (trưởng nhóm)

---

## 1. Thành viên và vai trò

> *Nhóm điền tên và MSSV vào cột "Thành viên" trước khi nộp.*

| Vai | Thành viên (MSSV) | Phụ trách nội dung | Phần tài liệu sở hữu |
|---|---|---|---|
| **TV1** — Trưởng nhóm / CI-CD | | Pipeline CI/CD, quản lý repository và bảng công việc, tổng hợp tài liệu | Outline CI/CD · phân công & tiến độ · đề xuất tổng hợp · file cấu hình pipeline |
| **TV2** — Unit Test | | Lý thuyết unit test, JUnit + Mockito | Outline Unit Test · bộ test cho lớp nghiệp vụ cho mượn sách |
| **TV3** — Code Coverage | | JaCoCo, mutation testing, luận điểm "coverage ≠ chất lượng" | Outline Code Coverage · cấu hình coverage và coverage gate |
| **TV4** — Case study | | Mã nguồn nghiệp vụ, lớp tính phí, REST endpoint | Mã nguồn case study · bộ test cho lớp tính phí và endpoint |
| **TV5** — AI & trình bày | | Bốn demo AI, slide, báo cáo | Kế hoạch AI & quy ước AI · slide · báo cáo |

**Việc chung** (mỗi người viết phần công cụ mình phụ trách, TV1 ghép lại):
khảo sát & so sánh công cụ · ma trận demo · danh sách câu hỏi cho GVTH.

**Nguyên tắc tránh giẫm chân:** mỗi thành viên **sở hữu một tập file riêng**; cần sửa file
của người khác thì mở một issue gán cho chủ file thay vì sửa thẳng. Nhờ vậy 5 người làm song
song mà không xung đột khi merge.

---

## 2. Cách nhóm tạo minh chứng

Đề yêu cầu *"các đợt tính điểm cần thể hiện rõ ràng công việc của các thành viên (kèm minh
chứng)"*. Nhóm dùng **ba lớp minh chứng** chồng lên nhau, không dựa vào một nguồn duy nhất:

| Lớp | Minh chứng | Trả lời câu hỏi gì |
|---|---|---|
| **1. Việc được giao** | Một **issue** cho mỗi đầu việc, gán đúng người, gắn nhãn theo trụ (`unit-test` / `coverage` / `cicd` / `ai` / `trinh-bay`) | *Ai được giao việc gì?* |
| **2. Việc đã làm** | **Commit** có tên tác giả, nội dung commit dẫn số issue tương ứng | *Ai thực sự đã làm gì?* |
| **3. Tiến độ theo thời gian** | **Bảng công việc** dạng kanban: `Dự kiến` → `Đang làm` → `Chờ review` → `Xong` | *Việc diễn ra lúc nào, có đều không?* |

**Bảng tổng hợp đóng băng theo mốc nộp:** ở mỗi mốc (Tuần 6, Tuần 12), trưởng nhóm sẽ kết
xuất số commit theo từng thành viên và danh sách issue theo người, dán vào một mục của tài
liệu này **kèm ngày chốt**. Số liệu được đóng băng sẵn, thầy/cô không phải tự tra.

> *Lưu ý:* ở thời điểm nộp lần 1 này, phần bảng công việc trên nền tảng đang được dựng và
> sẽ có dữ liệu từ tuần 3. Nhóm không kê khai sẵn những gì chưa thực sự diễn ra.

---

## 3. Quy tắc làm việc nhóm

1. **Một đầu việc = một issue = một nhánh = một Pull Request.**
2. **Pull Request phải xanh mới được merge.** Coverage gate là một phần của pipeline, nên
   không ai merge được mã làm tụt độ phủ của lớp quan trọng xuống dưới ngưỡng.
3. **Không sửa file người khác sở hữu** — mở issue gán cho chủ file.
4. **Họp chốt tiến độ mỗi tuần một lần**; trưởng nhóm ghi lại 5 dòng kết luận vào issue
   tương ứng. Không cần biên bản dài, nhưng phải có dấu vết theo thời gian.
5. **Người commit chịu trách nhiệm nội dung**, kể cả phần do AI sinh ra (xem `07_KeHoach_AI.md`).

---

## 4. Tiến độ dự kiến

> *Mốc tuần theo lịch môn học; nhóm sẽ điều chỉnh theo ngày cụ thể thầy/cô xác nhận ở buổi
> kickoff.*

| Tuần | Nội dung | Người chịu trách nhiệm chính | Trạng thái |
|---|---|---|---|
| **2–3** | Phân tích đề; chốt phạm vi, case study, bộ công cụ; viết toàn bộ tài liệu đề xuất này; dựng repository và khung case study chạy được | Cả nhóm; TV1 tổng hợp | **Đang nộp / trình GVTH** |
| **3** | Case study hoàn chỉnh: mã nghiệp vụ + bộ unit test (demo UT-1, UT-2, UT-3) | TV4 (mã nguồn), TV2 (test) | Dự kiến |
| **4** | Coverage đầy đủ: báo cáo, coverage gate, chứng minh "coverage ≠ chất lượng" bằng mutation testing (demo CC-1 → CC-3) | TV3 | Dự kiến |
| **5** | Pipeline CI ba cấp độ + viết cấu hình Jenkins để đối chiếu (demo CI-1 → CI-3) | TV1 | Dự kiến |
| **5** | Bốn demo AI, đo số liệu, viết bảng đối chiếu | TV5 | Dự kiến |
| **5–6** | Slide, báo cáo chi tiết, bài tập áp dụng, quay video demo | TV5 (slide/báo cáo), cả nhóm (video) | Dự kiến |
| **6** | **Nộp bài chấm điểm**: slide, báo cáo, video, bài tập áp dụng, mã nguồn, phân công kèm minh chứng | TV1 tổng hợp | Dự kiến |
| Trước tuần seminar | Trình bày thử với GVTH, ghi nhận góp ý, chỉnh sửa | Cả nhóm | Dự kiến |
| Tuần seminar | Seminar trước lớp | Cả nhóm | Dự kiến |
| **12** | Nộp bản hiệu chỉnh cuối môn học | TV1 tổng hợp | Dự kiến |

**Rủi ro nhóm đã nhận diện và cách xử lý:**

| Rủi ro | Cách xử lý |
|---|---|
| Khối lượng lớn (7 loại sản phẩm phải nộp), dễ trễ mốc Tuần 6 | Chia thành các gói nhỏ, **mỗi gói cho ra sản phẩm chạy được**, làm tuần tự theo bảng trên thay vì làm song song dở dang mọi thứ |
| Nhóm hiểu sai yêu cầu "Record and Playback / Data driven / Checkpoints" | Đưa thành câu hỏi riêng, hỏi **ngay buổi kickoff**, trước khi đầu tư làm demo |
| Công cụ không chạy được trên môi trường của thành viên | Pipeline CI chạy trên máy ảo chuẩn → là nguồn tham chiếu chung khi máy cá nhân khác nhau |
| Phiên bản thư viện mới, tài liệu trên mạng chủ yếu viết cho bản cũ | Ghi chú rõ điểm khác biệt trong báo cáo; sẵn sàng hạ về phiên bản phổ biến hơn nếu thầy/cô thấy nên ưu tiên việc lớp dễ làm theo |
