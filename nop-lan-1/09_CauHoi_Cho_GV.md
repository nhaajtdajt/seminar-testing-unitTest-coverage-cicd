# Câu hỏi nhóm xin ý kiến thầy/cô

**Dịp:** Buổi kickoff meeting (Tuần 2–3)

> Thứ tự xếp theo mức ảnh hưởng. **Câu 1 và 2 nếu trả lời khác đi thì nhóm phải làm lại phần
> lớn kế hoạch**, nên nhóm xin hỏi trước. Các câu sau chỉ ảnh hưởng tới chi tiết thực thi.

---

## Câu 1 — Cách hiểu "Record and Playback / Data driven / Checkpoints" **(quan trọng nhất)**

Đề yêu cầu: *"Thông thường, trong một công cụ sẽ có 3 phần: Record and Play back, Data driven,
Checkpoints. Nhóm SV cần có các demo đầy đủ cho 3 phần này."*

Nhóm hiểu đây là khung quen thuộc của **công cụ kiểm thử tự động giao diện** (Selenium IDE,
Katalon, UFT), không ánh xạ trực tiếp sang unit test / code coverage / CI-CD. Nhóm đề xuất
cách hiểu tương đương:

| Phần trong đề | Nhóm hiểu là | Demo tương ứng |
|---|---|---|
| **Record and Playback** | *Record* = sinh test tự động thay vì gõ tay (IDE tạo khung test, AI sinh test từ mã nguồn). *Playback* = chạy lại bộ test đã sinh, tự động, trong pipeline CI | UT-1 · AI-1 · CI-1 |
| **Data driven** | Một test chạy với nhiều bộ dữ liệu; dữ liệu tách rời khỏi mã test, đọc từ file CSV bên ngoài | UT-2 · AI-4 |
| **Checkpoints** | Các điểm kiểm chứng có khả năng **làm fail build**: assertion, `verify()` của Mockito, coverage gate, quality gate trong pipeline | UT-3 · CC-3 · CI-3 |

**Nhóm xin hỏi:**
1. Cách hiểu này có được chấp nhận không?
2. Nếu không, thầy/cô muốn nhóm hiểu ba phần này theo hướng nào trong phạm vi chủ đề
   Unit Test · Code Coverage · CI/CD?
3. Hay chủ đề này được miễn yêu cầu đó vì nó vốn dành cho công cụ kiểm thử giao diện?

---

## Câu 2 — Số lượng công cụ cần demo sâu

Đề yêu cầu *"hướng dẫn sử dụng, demo, vận dụng ít nhất 2-3 công cụ"*. Chủ đề của nhóm có ba
trụ, nên con số này có thể hiểu theo hai cách.

Nhóm dự kiến: **3 công cụ demo sâu** — mỗi trụ một công cụ (JUnit + Mockito, JaCoCo,
GitHub Actions), mỗi công cụ đủ 3 kịch bản demo — **cộng** phần khảo sát và so sánh các công
cụ thay thế theo 7 trục (TestNG, Spock, EasyMock, JMockit, Cobertura, OpenClover, PIT,
Jenkins, GitLab CI, CircleCI).

**Nhóm xin hỏi:** như vậy đã đủ chưa, hay nhóm cần **2 công cụ demo sâu cho mỗi trụ** (tổng 6)?

---

## Câu 3 — Phần áp dụng AI

Đề yêu cầu demo AI *"có khả năng tổng quát hóa, tái sử dụng"*. Nhóm hiểu là mỗi demo phải để
lại một **tài sản dùng lại được** (prompt template có tham số, hoặc script), chứ không phải
một đoạn hội thoại chụp màn hình. Dự kiến 4 demo: sinh unit test · vá lỗ hổng coverage ·
nhận xét Pull Request trong pipeline · sinh dữ liệu biên cho data-driven test.

**Nhóm xin hỏi:**
1. Bốn demo này có đúng kỳ vọng của thầy/cô không?
2. Có hướng nào nên bổ sung không — ví dụ AI sinh ca kiểm thử từ **tài liệu đặc tả** thay vì
   từ mã nguồn?
3. Nhóm dự định báo cáo cả **số lần AI làm sai** và cách nhóm sửa. Phần này có được tính là
   nội dung hợp lệ không, hay thầy/cô muốn nhóm chỉ trình bày trường hợp thành công?

---

## Câu 4 — Bài tập áp dụng cho lớp

Đề yêu cầu *"tạo ra vài bài tập áp dụng có gợi ý thực hiện để các bạn trong lớp có thể làm theo"*.
Nhóm dự kiến 3 bài cho mỗi trụ (tổng 9 bài), mức độ tăng dần.

**Nhóm xin hỏi:**
1. Bao nhiêu bài là phù hợp?
2. Mức độ: chỉ viết test cho mã nguồn cho sẵn, hay bao gồm cả dựng pipeline CI?
3. Có cần kèm đáp án không, hay chỉ cần gợi ý thực hiện?

---

## Câu 5 — Minh chứng phân công công việc

Nhóm dự định dùng **issue** (việc được giao, có gán người) + **commit** (việc đã làm, có tên
tác giả) + **bảng công việc kanban** (tiến độ theo thời gian) trên nền tảng quản lý mã nguồn,
và kết xuất thành bảng tổng hợp đóng băng ở mỗi mốc nộp.

**Nhóm xin hỏi:** cách này có được tính là minh chứng hợp lệ không, hay nhóm cần bổ sung
biên bản họp nhóm / bảng chấm công theo tuần?

---

## Câu 6 — Phiên bản công nghệ

Nhóm chọn JDK và Spring Boot bản mới nhất vì khớp với môi trường sẵn có trên máy của nhóm.
Tuy nhiên, tài liệu và ví dụ phổ biến trên mạng phần lớn viết cho các bản cũ hơn một thế hệ.
Các annotation dùng trong seminar thì giống nhau giữa hai bản.

**Nhóm xin hỏi:** nên giữ bản mới (khớp môi trường nhóm, nhưng lớp tra tài liệu dễ lệch), hay
hạ về bản phổ biến hơn để các bạn trong lớp làm theo dễ hơn? Nhóm ưu tiên theo ý thầy/cô, vì
đề nhấn mạnh bài seminar phải giúp người chưa tìm hiểu *"hiểu và vận dụng ở mức cơ bản"*.

---

## Câu 7 — Mốc thời gian và hình thức nộp

1. **Tuần 6** nộp bài chấm điểm là **ngày nào** cụ thể, và nộp qua kênh nào?
2. Buổi **trình bày thử** trước tuần seminar được đặt lịch như thế nào — nhóm chủ động liên
   hệ thầy/cô hay chờ thông báo?
3. **Thời lượng** buổi seminar chính thức là bao nhiêu phút (để nhóm cân đối 3 phần và phần demo)?
4. Repository của nhóm nên để **công khai** hay **riêng tư**? Nhóm muốn để công khai vì
   pipeline CI được miễn phí không giới hạn, và link log của mỗi lần chạy dùng trực tiếp làm
   minh chứng được. Nếu thầy/cô yêu cầu riêng tư, nhóm sẽ chuyển sang nộp kèm ảnh chụp và
   file kết xuất.

---

## Ghi chú

Nhóm chủ động chuẩn bị các câu hỏi này trước buổi kickoff để buổi gặp tập trung vào việc chốt
hướng, thay vì mất thời gian mô tả lại kế hoạch. Toàn bộ nội dung dự kiến đã được trình bày
trong các tài liệu kèm theo của gói nộp này.
