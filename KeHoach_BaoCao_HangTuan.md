# Kế hoạch công việc và báo cáo hàng tuần của nhóm

**Môn học:** Kiểm thử phần mềm

**Chủ đề:** Unit Test · Code Coverage · CI/CD

**Nhóm:** Nhóm 09 (Group09)

**Cập nhật:** Hiện tại là **Tuần thực hành 04** theo xác nhận của nhóm; một phần công việc dự kiến cho Tuần 05 đã được thực hiện sớm. Kết quả và phần còn thiếu được tổng hợp trong [Báo cáo Tuần thực hành 04](bao-cao-tuan/BaoCao_Tuan_04.md).

**Thành viên:** TV1: Nguyễn Bảo An (23120207); TV2: Phạm Quang Vinh (23120202); TV3: Trương Nhật Đạt (23120231); TV4: Nguyễn Lê Thế Vinh (23120190); TV5: Ngô Gia An (23120205)

> Đây là **kế hoạch dự kiến**, không phải báo cáo công việc đã hoàn thành. Nhóm em sẽ ghi kết quả thực tế và đường dẫn minh chứng vào báo cáo của từng tuần. Số tuần theo lịch môn học; ngày nộp và tuần seminar sẽ cập nhật khi giảng viên xác nhận. Các tuần đã qua chỉ điền kết quả khi có minh chứng, không ghi hoàn thành theo kế hoạch.

## 1. Phân công cố định

| Thành viên | Vai trò | Trách nhiệm xuyên suốt |
|---|---|---|
| Nguyễn Bảo An (TV1, 23120207) | Trưởng nhóm, Unit Test | Quản lý tiến độ, JUnit, Mockito, dữ liệu kiểm thử, tổng hợp và nộp báo cáo tuần |
| Phạm Quang Vinh (TV2, 23120202) | CI/CD, Build & Benchmark | Quản trị hạ tầng build Java 25, GitHub Actions/Jenkins, đo benchmark hiệu năng |
| Trương Nhật Đạt (TV3, 23120231) | Code Coverage | JaCoCo, coverage gate, mutation testing, tài liệu và demo coverage |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Case study | Mã nguồn ứng dụng quản lý thư viện, nghiệp vụ, REST endpoint, hỗ trợ demo tích hợp |
| Ngô Gia An (TV5, 23120205) | AI và trình bày | Bốn demo AI, slide, báo cáo chi tiết, điều phối video |

Mỗi thành viên gửi cho TV1 trước khi chốt báo cáo tuần: **việc được giao → việc thực hiện → kết quả đo được → minh chứng → khó khăn → việc tuần sau**. TV1 tổng hợp, cả nhóm rà soát rồi mới nộp. Một đường dẫn issue/PR, commit, log chạy, ảnh hoặc tài liệu là minh chứng; kế hoạch hoặc lời kể không thay thế cho kết quả thực hiện.

## 2. Kế hoạch theo tuần

### Tuần 2 — Xác định phạm vi và chuẩn bị gặp giảng viên

| Người | Việc dự kiến | Sản phẩm/minh chứng cần có |
|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | Đọc yêu cầu, tạo danh sách đầu việc, thống nhất case study và câu hỏi cho giảng viên. | Bảng việc, đề xuất nội dung, danh sách câu hỏi. |
| Nguyễn Bảo An (TV2, 23120207) | Phác thảo Unit Test, chọn JUnit/Mockito và các ca kiểm thử của nghiệp vụ mượn sách. | Outline Unit Test, danh sách ca kiểm thử dự kiến. |
| Trương Nhật Đạt (TV3, 23120231) | Phác thảo Code Coverage, chọn JaCoCo và cách chứng minh line coverage khác branch coverage. | Outline Coverage, kịch bản đo trước/sau. |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Thiết kế nghiệp vụ ứng dụng thư viện: tính phí, mượn sách, endpoint. | Mô tả nghiệp vụ, sơ đồ/khung mã nguồn nếu đã làm. |
| Ngô Gia An (TV5, 23120205) | Phác thảo phần AI, bố cục slide và báo cáo. | Kế hoạch AI, dàn ý slide/báo cáo. |

### Tuần 3 — Chốt góp ý và dựng bản chạy đầu tiên

| Người | Việc dự kiến | Sản phẩm/minh chứng cần có |
|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | Ghi nhận góp ý của giảng viên, chốt phạm vi demo; dựng workflow CI tối thiểu. | Biên bản/góp ý thực tế, commit workflow, link lần chạy nếu có. |
| Nguyễn Bảo An (TV2, 23120207) | Cài JUnit; viết demo UT-1 và các test đầu tiên cho lớp tính phí. | Mã test, log `mvn test`, báo cáo Surefire. |
| Trương Nhật Đạt (TV3, 23120231) | Cài JaCoCo; sinh báo cáo CC-1 trên mã nguồn thật. | Cấu hình plugin, log `mvn verify`, báo cáo HTML. |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Hoàn thiện khung case study và lớp tính phí, cung cấp đặc tả cho TV2/TV3. | Mã nguồn chạy được, đặc tả các nhánh nghiệp vụ. |
| Ngô Gia An (TV5, 23120205) | Tạo prompt và tiêu chí rà soát cho AI-1, AI-4; dựng khung báo cáo. | Prompt mẫu, checklist review, dàn trang báo cáo. |

### Tuần 4 — Hoàn thiện Unit Test và Coverage

| Người | Việc dự kiến | Sản phẩm/minh chứng cần có |
|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | Review PR mã nguồn/test, duy trì bảng việc và chuẩn bị tích hợp coverage vào CI. | PR review, bảng tiến độ, workflow cập nhật. |
| Nguyễn Bảo An (TV2, 23120207) | Làm UT-2 (TDD, test đọc CSV) và UT-3 (Mockito cho các nhánh mượn sách). | Các lần commit đỏ/xanh, CSV, mã test, log chạy. |
| Trương Nhật Đạt (TV3, 23120231) | Làm CC-2 trước/sau khi thêm test; CC-3 coverage gate; thử mutation testing. | Hai báo cáo coverage, log gate fail/pass, kết quả mutation. |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Hoàn thiện lớp mượn sách, repository giả lập và REST endpoint; sửa lỗi lộ ra từ test. | Mã nguồn, test tầng web nếu có, PR sửa lỗi. |
| Ngô Gia An (TV5, 23120205) | Chạy AI-1 và AI-4 trên mã/đặc tả thực tế, ghi lỗi AI và phần phải sửa tay. | Prompt, bản AI tạo, bản đã review, bảng so sánh dữ liệu. |

### Tuần 5 — Tích hợp CI/CD, AI và các demo phức tạp

| Người | Việc dự kiến | Sản phẩm/minh chứng cần có |
|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | Làm CI-1/2/3: workflow, cache/artifact, pipeline nhiều job, PR đỏ rồi xanh; viết bản Jenkins để đối chiếu. | Link run/PR, log, artifact, file workflow/Jenkinsfile, số đo thời gian. |
| Nguyễn Bảo An (TV2, 23120207) | Rà soát assertion, dữ liệu biên, hướng dẫn người học chạy Unit Test. | Bộ test ổn định, hướng dẫn UT-1/2/3, hạn chế của JUnit/Mockito. |
| Trương Nhật Đạt (TV3, 23120231) | Gắn coverage gate vào CI, đối chiếu coverage với chất lượng test bằng mutation testing. | Log CI đỏ/xanh, báo cáo JaCoCo/PIT, phần giải thích số liệu. |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Chuẩn bị dữ liệu và luồng demo xuyên suốt trên case study; kiểm tra khả năng chạy lại từ đầu. | Script/dữ liệu demo, hướng dẫn chạy, lỗi và cách khắc phục. |
| Ngô Gia An (TV5, 23120205) | Làm AI-2/3, hoàn thiện bảng đánh giá AI; ghép nội dung lý thuyết vào slide và báo cáo. | Script/prompt AI, kết quả đối chiếu, bản nháp slide/báo cáo. |

### Tuần 6 — Hoàn thiện gói nộp chấm điểm

| Người | Việc dự kiến | Sản phẩm/minh chứng cần có |
|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | Kiểm kê gói nộp, tổng hợp phân công và minh chứng từng người, nộp đúng mốc. | Danh mục file/link nộp, bảng đóng góp, bản báo cáo tuần 6. |
| Nguyễn Bảo An (TV2, 23120207) | Chốt tài liệu Unit Test, quay phần demo UT và soạn bài tập áp dụng. | Mục báo cáo, video/link video, bài tập và đáp án gợi ý. |
| Trương Nhật Đạt (TV3, 23120231) | Chốt tài liệu Coverage, quay CC-1/2/3 và bài tập đọc báo cáo. | Mục báo cáo, video/link video, báo cáo đo đã lưu. |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Đóng gói source code, hướng dẫn cài/chạy và xác minh dữ liệu demo. | Repository/source, README chạy lại, log kiểm tra. |
| Ngô Gia An (TV5, 23120205) | Biên tập slide, báo cáo chi tiết, video và phần AI; kiểm tra liên kết, khả năng đọc. | Slide, báo cáo, danh sách link video, phần AI và bài tập. |

**Mốc kiểm:** Gói Tuần 6 cần có gần như toàn bộ nội dung seminar chính thức theo yêu cầu môn học: lý thuyết; khảo sát/so sánh; ít nhất 2–3 công cụ được hướng dẫn và demo; AI; slide; báo cáo; video; bài tập; source; phân công kèm minh chứng. Phần nào chưa đạt phải ghi rõ trong báo cáo, người xử lý và hạn hoàn thành.

### Tuần 7 — Rà soát gói đã nộp và sửa lỗi

| Người | Việc dự kiến | Sản phẩm/minh chứng cần có |
|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | Thu nhận phản hồi, mở việc sửa có người phụ trách và hạn xử lý. | Danh sách góp ý/issue, kế hoạch sửa. |
| Nguyễn Bảo An (TV2, 23120207) | Chạy lại demo UT trên môi trường sạch; sửa test không ổn định. | Log chạy lại, PR sửa và giải thích. |
| Trương Nhật Đạt (TV3, 23120231) | Kiểm tra tính đúng của số liệu coverage/mutation trong slide và báo cáo. | Bảng đối chiếu số liệu với báo cáo gốc. |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Kiểm tra người khác có chạy được case study từ README không. | Biên bản chạy lại và lỗi môi trường đã sửa. |
| Ngô Gia An (TV5, 23120205) | Sửa nội dung, hình ảnh/video khó hiểu; thống nhất thuật ngữ. | Bản slide/báo cáo sửa và danh sách thay đổi. |

### Tuần 8 — Thử toàn bộ luồng trình bày

| Người | Việc dự kiến | Sản phẩm/minh chứng cần có |
|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | Điều phối buổi diễn tập, đo thời lượng và điểm chuyển giữa 3 chủ đề. | Lịch diễn tập, bảng thời lượng, việc cần sửa. |
| Nguyễn Bảo An (TV2, 23120207) | Trình bày thử UT-1/2/3 và trả lời câu hỏi về mock, data driven. | Video/ghi chú diễn tập, câu hỏi nhận được. |
| Trương Nhật Đạt (TV3, 23120231) | Trình bày thử CC-1/2/3, giải thích coverage không bảo đảm chất lượng test. | Video/ghi chú diễn tập, câu hỏi nhận được. |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Chạy case study trên máy trình chiếu, chuẩn bị dữ liệu/nhánh dự phòng. | Log chạy, checklist môi trường demo. |
| Ngô Gia An (TV5, 23120205) | Trình bày thử phần AI, kiểm tra slide/video và ghi lỗi bố cục. | Video/ghi chú diễn tập, danh sách chỉnh sửa. |

### Tuần 9 — Trình bày thử với giảng viên và xử lý góp ý

| Người | Việc dự kiến | Sản phẩm/minh chứng cần có |
|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | Liên hệ lịch trình bày thử trước tuần seminar thực tế; ghi và phân công góp ý. | Lịch/ghi nhận buổi gặp, bảng góp ý và người xử lý. |
| Nguyễn Bảo An (TV2, 23120207) | Trả lời góp ý Unit Test, điều chỉnh ví dụ hoặc demo. | PR/tài liệu sửa, log demo mới. |
| Trương Nhật Đạt (TV3, 23120231) | Trả lời góp ý Coverage, sửa phép đo hoặc cách diễn giải nếu cần. | Báo cáo/log mới, trang slide sửa. |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Sửa nghiệp vụ hoặc cách chạy case study theo góp ý. | PR sửa và kết quả chạy lại. |
| Ngô Gia An (TV5, 23120205) | Tổng hợp góp ý về slide, báo cáo, AI và video. | Bản sửa có đánh dấu thay đổi. |

> Nếu tuần seminar được ấn định sớm hơn Tuần 10, nhóm em sẽ chuyển buổi trình bày thử lên **ít nhất một tuần trước tuần seminar**; không giữ cố định Tuần 9.

### Tuần 10 — Chốt bản trình bày trước lớp

| Người | Việc dự kiến | Sản phẩm/minh chứng cần có |
|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | Chốt kịch bản, người nói, thời lượng và link demo dự phòng. | Kịch bản trình bày, checklist cuối. |
| Nguyễn Bảo An (TV2, 23120207) | Chốt phần nói và bản demo Unit Test. | Slide phần UT, lần chạy kiểm tra cuối. |
| Trương Nhật Đạt (TV3, 23120231) | Chốt phần nói và bản demo Coverage. | Slide phần CC, lần chạy kiểm tra cuối. |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Chốt mã nguồn, dữ liệu và môi trường demo. | Tag/commit bản demo, hướng dẫn phục hồi. |
| Ngô Gia An (TV5, 23120205) | Chốt slide, video, báo cáo và phần AI; luyện chuyển cảnh. | Bản trình bày cuối, link video đã kiểm. |

### Tuần 11 — Seminar và ghi nhận câu hỏi

| Người | Việc dự kiến | Sản phẩm/minh chứng cần có |
|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | Điều phối buổi seminar, ghi câu hỏi/góp ý và việc cần bổ sung. | Biên bản ngắn, danh sách câu hỏi. |
| Nguyễn Bảo An (TV2, 23120207) | Trình bày/demo Unit Test, trả lời phần mình phụ trách. | Slide, log hoặc video phần trình bày. |
| Trương Nhật Đạt (TV3, 23120231) | Trình bày/demo Coverage, trả lời phần mình phụ trách. | Slide, log hoặc video phần trình bày. |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Vận hành case study, hỗ trợ xử lý trục trặc demo. | Log/ghi chú buổi demo. |
| Ngô Gia An (TV5, 23120205) | Trình bày AI, điều phối slide/video và ghi phản hồi từ lớp. | Slide, link video, ghi chú phản hồi. |

> Tuần 11 chỉ là **mốc dự kiến** cho seminar. Khi có lịch chính thức, nhóm em sẽ chuyển các việc Tuần 10–11 theo lịch đó và báo cáo đúng tuần thực tế.

### Tuần 12 — Nộp bản hiệu chỉnh cuối môn

| Người | Việc dự kiến | Sản phẩm/minh chứng cần có |
|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | Kiểm kê bản cuối, tổng hợp đóng góp và nộp toàn bộ sản phẩm. | Danh mục nộp, bảng minh chứng 5 người, xác nhận nộp. |
| Nguyễn Bảo An (TV2, 23120207) | Sửa phần Unit Test theo câu hỏi seminar, kiểm tra ví dụ cuối. | Tài liệu/test bản cuối, log chạy. |
| Trương Nhật Đạt (TV3, 23120231) | Sửa phần Coverage, kiểm tra số liệu và báo cáo cuối. | Báo cáo đo bản cuối, slide sửa. |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Chốt source code, README và khả năng tái hiện demo. | Tag/commit cuối, hướng dẫn chạy lại. |
| Ngô Gia An (TV5, 23120205) | Biên tập báo cáo, slide, video, bài tập và phần AI bản cuối. | Bộ tài liệu cuối và danh sách thay đổi. |

## 3. Mẫu dùng để nộp báo cáo từng tuần

Sao chép mẫu dưới đây thành một file cho **mỗi tuần** (ví dụ `BaoCao_Tuan_04.md`). Chỉ điền sự kiện đã xảy ra và đường dẫn minh chứng truy cập được; nếu chưa xong, ghi “Chưa hoàn thành” và kế hoạch xử lý. Trưởng nhóm chốt ngày báo cáo theo lịch lớp, không tự suy đoán ngày nộp.

```markdown
# Báo cáo tiến độ Tuần [số] — Seminar Unit Test · Code Coverage · CI/CD

Nhóm: [mã nhóm]

Khoảng thời gian: [ngày bắt đầu] – [ngày kết thúc]

Ngày chốt báo cáo: [ngày]

Người tổng hợp: [họ tên TV1]

## 1. Kết quả chung

- Mục tiêu tuần: ...
- Kết quả đã hoàn thành: ...
- Nội dung chưa hoàn thành và lý do: ...
- Quyết định/góp ý của giảng viên (nếu có): ...

## 2. Công việc từng thành viên

| Thành viên (MSSV) | Việc được giao | Việc đã thực hiện và kết quả đo được | Trạng thái | Minh chứng (link/file/commit/log) | Khó khăn/việc tuần sau |
|---|---|---|---|---|---|
| TV1 [...] | ... | ... | ... | ... | ... |
| TV2 [...] | ... | ... | ... | ... | ... |
| TV3 [...] | ... | ... | ... | ... | ... |
| TV4 [...] | ... | ... | ... | ... | ... |
| TV5 [...] | ... | ... | ... | ... | ... |

## 3. Kế hoạch tuần tiếp theo

| Thành viên | Việc cụ thể | Sản phẩm dự kiến | Hạn theo lịch nhóm |
|---|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | ... | ... | ... |
| Nguyễn Bảo An (TV2, 23120207) | ... | ... | ... |
| Trương Nhật Đạt (TV3, 23120231) | ... | ... | ... |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | ... | ... | ... |
| Ngô Gia An (TV5, 23120205) | ... | ... | ... |

## 4. Danh mục minh chứng

- Repository/board: ...
- Pull Request/commit: ...
- Log chạy test, coverage, CI hoặc link video: ...
- Báo cáo/slide/biên bản góp ý: ...
```

**Căn cứ lập kế hoạch:** `require.md`, `nop-lan-1/08_PhanCong_TienDo.md`, `nop-lan-1/06_MaTran_Demo.md`, `nop-lan-1/07_KeHoach_AI.md`. Nếu giảng viên điều chỉnh phạm vi hoặc lịch, nhóm cập nhật kế hoạch từ tuần tiếp theo và ghi rõ thay đổi trong báo cáo tuần đó.
