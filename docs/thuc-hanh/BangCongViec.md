# Bảng công việc đến hết Tuần 6

Bảng theo dõi dùng chung theo `PhanCong_NhiemVu.md`. Cập nhật cấu trúc ngày 29/10/2026: giữ các ghi nhận lịch sử, đưa AI/paper vào cùng bảng W06 với Unit Test/Coverage/CI; không gán lại tác giả commit. Các trạng thái “đã chạy” phải đọc cùng evidence và người thực hiện.

## Thành viên phụ trách


| Vai trò | MSSV | Họ tên | Phụ trách |
|---|---|---|---|
| TV1 | 23120207 | Nguyễn Bảo An | Unit Test, JUnit/Mockito |
| TV2 | 23120202 | Phạm Quang Vinh | CI/CD, Build Java 25 & Benchmark |
| TV3 | 23120231 | Trương Nhật Đạt | Code Coverage, JaCoCo, coverage gate và mutation testing |
| TV4 | 23120190 | Nguyễn Lê Thế Vinh | Case study, REST API, persistence và demo tích hợp |
| TV5 | 23120205 | Ngô Gia An | AI, paper, trưởng nhóm; hợp nhất slide/HTML |


## Tiến độ Tuần 05 — kỳ trước

Các dòng W05 ghi trạng thái và minh chứng của kỳ trước; không gán các thay đổi hiện tại cho Phạm Quang Vinh.

| ID | Vai trò | Công việc | Trạng thái sản phẩm | Minh chứng/vị trí |
|---|---|---|---|---|
| W05-01 | TV1 | Tổng hợp đề xuất, kế hoạch tuần | Có tài liệu | `nop-lan-1/`, `KeHoach_BaoCao_HangTuan.md` |
| W05-02 | TV1 | Workflow 3 job, JDK 25, cache/artifact | Viết xong, kiểm tra tĩnh; chưa chạy GitHub | `.github/workflows/ci.yml`, `evidence/tuan-05/workflow-lint/` |
| W05-04 | TV1 | PR đỏ/xanh, required checks, GitHub board | Chưa làm trên dịch vụ: quyền hiện tại READ | `evidence/tuan-05/github-access.json` |
| W05-05 | TV2 | UT-1, UT-2, UT-3 | Đã chạy tại máy | `FineCalculatorTest`, `LoanServiceTest`, log `final/` |
| W05-06 | TV2 | 4 vòng TDD | Có replay chạy thật; chưa có lịch sử commit nhóm | `evidence/tuan-05/tdd-replay/` |
| W05-07 | TV2 | Tài liệu test, dữ liệu biên, giới hạn mock | Có bản thực hành | `docs/thuc-hanh/`, `fine-cases.csv` |
| W05-08 | TV3 | CC-1/2/3, coverage gate | Đã chạy tại máy | `baseline/`, `gate-fail/`, `final/` trong evidence |
| W05-09 | TV3 | Mutation đối chiếu bộ mạnh/yếu | Đã chạy tại máy | `pit-strong/`, `pit-weak/` |
| W05-10 | TV3; TV1 hỗ trợ cache | Đo thời gian JaCoCo, cache | JaCoCo đã đo 3 lượt/cấu hình; cache Java 25 đã đủ 3/3 cặp thành công, giữ riêng các lượt tải lỗi | `benchmark-jacoco/`, `benchmark-cache/` |
| W05-11 | TV4 | Case study tính phí, mượn sách, endpoint | Build/chạy được, H2 in-memory qua Spring Data JPA | `case-study/src/main/` |
| W05-12 | TV4 | Test luồng thật và HTTP smoke | Đã chạy tại máy | `LoanFlowTest`, `http-smoke/results.json` |
| W05-13 | TV5 | AI-1, AI-2, AI-4 | Có output Codex tương tác, đã chạy test; chờ nhóm review | `ai/`, `ai-draft-recheck/`, `ai-improved/`, `ai-data/` |
| W05-14 | TV5 | AI-3 chuẩn bị prompt/workflow/live client | Có code và kiểm tra cục bộ; chưa gọi API thật | `scripts/ai_review.py`, `ai-review-prepared/` |
| W05-15 | TV5 | Bản nháp slide và báo cáo | Có nguồn, chờ nhóm duyệt nội dung và trình bày | `slides/index.html`, `report/main.tex`, `BaoCao_ChiTiet.md` |
| W05-16 | Cả nhóm | Review AI, xác nhận đóng góp và góp ý giảng viên | Đã điền danh tính; chờ xác nhận thực tế | Báo cáo Tuần thực hành 04 |

Luồng công việc: Dự kiến → Đang thực hiện → Chờ thành viên review → Hoàn thành có xác nhận. Mỗi thành viên tạo issue/nhánh/PR bằng tài khoản thật khi nhóm có quyền ghi; không tạo commit giả danh hoặc ghi lùi thời gian để bổ sung minh chứng quá khứ.


## Theo dõi tiến độ Tuần 06

W06-01..05 là snapshot công việc tích lũy trước khi phân lại vai trò, không phải phân công hiện hành hoặc xác nhận tất cả thành viên đã tự review. W06-06 trở đi cập nhật theo chủ đề và người phụ trách hiện tại. Video vẫn là yêu cầu seminar; slide/HTML của Gia An đã được hoàn tất sau phần AI/paper.

| ID | Phạm vi kế hoạch Tuần 6 | Người đảm nhận tuần này | Tiến độ thực tế | Bằng chứng/ghi chú |
|---|---|---|---|---|
| W06-01 | TV1: kiểm kê source, phân công và minh chứng | Ngô Gia An (23120205) | Đã tách evidence Tuần 06, cập nhật chỉ mục và thêm ảnh JaCoCo; ZIP chuẩn bị tại `bai-nop/Group09-06.zip` | Bảng này, README, `evidence/tuan-06/README.md`; xác nhận nhóm/nộp chính thức còn phải do nhóm thực hiện |
| W06-02 | TV2: chốt Unit Test và bài tập | Ngô Gia An (23120205) | Tài liệu/bài tập có; lượt verify thành công gần nhất 33/33; demo ngoài checklist nộp tuần 6 | `docs/thuc-hanh/HuongDan_Demo.md`, `BaiTap_Tuan_06.md`, `evidence/tuan-06/source-verify/surefire-reports/` |
| W06-03 | TV3: chốt Coverage, CC-1/2/3, bài đọc báo cáo | Ngô Gia An (23120205) | Tài liệu có; full coverage verify pass; demo ngoài checklist nộp tuần 6 | `BaiTap_Tuan_06.md`, `evidence/tuan-06/source-verify/site/jacoco/`; PIT comparisons and gate examples remain in prior-week evidence |
| W06-04 | TV4: đóng gói source và hướng dẫn chạy lại | Ngô Gia An (23120205) | Source và hướng dẫn có; HTTP smoke 5/5 trên JAR Java 25; ảnh request 201/409 được giữ tùy chọn ngoài checklist | `case-study/`, `README.md`, `evidence/tuan-06/http-smoke-java25/`; dữ liệu H2 mẫu xem `case-study/src/main/resources/data.sql` |
| W06-05 | TV5: slide, báo cáo chi tiết, AI, bài tập, link | Ngô Gia An (23120205) | Slide/báo cáo/AI declaration/bài tập có; Gemini API live và evaluation fixture đạt 4/4; demo ngoài checklist nộp tuần 6 | `slides/`, `docs/thuc-hanh/BaoCao_ChiTiet.md`, `BaiTap_Tuan_06.md`, `evidence/tuan-06/ai-review/` |
| W06-06 | TV3: các loại coverage, JaCoCo đo gì, công cụ thứ hai, điểm yếu công cụ, kịch bản video | Trương Nhật Đạt (23120231), AI hỗ trợ (Claude Code) | Ví dụ `LoanPeriodPolicy` + bộ T1–T4 và bảng 6 loại coverage; bảng JaCoCo đo/không đo; OpenClover chạy thật, so 6 tiêu chí; demo mức trần ẩn trong `Math.min`, mutant tương đương, chi phí PIT; kịch bản Video B có timestamp. **Chưa quay video.** | `BaoCao_ChiTiet.md` mục 3.1–3.4, 5.2; `HuongDan_Demo.md` CC-0, CC-0b, CC-5, CC-6; `evidence/tuan-06/coverage-types/`, `openclover/`, `coverage-blindspot/`, `pit-cost/` |
| W06-07 | TV5: AI-4 đối chứng dữ liệu biên | Ngô Gia An (23120205), Codex hỗ trợ chạy | Khóa 23 ca/notes trước so; 11 ca chung khớp; Java 23/23 vs AI 13/13 pass. Độc lập theo notes; Gia An xác nhận review 29/10, Codex thực thi đối chiếu | `ai/human/`; `evidence/tuan-06/ai-4/` |
| W06-08 | TV5: AI trên LoanService | Ngô Gia An (23120205), Codex hỗ trợ | Nháp 2 → bổ sung 10 test; branch 3/6 → 6/6; PIT 9/9; fixture sai đỏ đúng 1 assertion | `HuongDan_Demo.md` mục 9.4; `evidence/tuan-06/ai-loan/` |
| W06-09 | TV5: paper có source/hạng và thực nghiệm | Ngô Gia An (23120205), Codex hỗ trợ chạy | CoverUp và Pynguin: phân tích dữ liệu công bố, generation mới trên benchmark và thử source nhóm. CoverUp nhóm 7 pass/96,4%; Pynguin benchmark 10 pass + 5 xfail, group có seed 2 pass nhưng không assertion/không tăng coverage so smoke | `research/`; báo cáo mục 9; `evidence/tuan-06/papers/README.md` |
| W06-10 | TV5: khai báo AI, chuẩn hóa docs/evidence | Ngô Gia An (23120205), Codex hỗ trợ | Theo 6 mục chung; Gia An xác nhận thực hiện/review ngày 29/10; phân biệt tự chạy và Codex chạy theo ủy quyền. Chưa có review chéo/chữ ký bản nộp | `ai-usage-declaration/01_NgoGiaAn.md`; `evidence/tuan-06/README.md` |
| W06-11 | TV5: artifact video AI/paper | Ngô Gia An (23120205) | GA-01..07 có đầu vào/bằng chứng; chưa quay/đăng, chưa có URL/timestamp thực tế | `KichBan_QuayVideo_Tuan_06.md`, Video E |
| W06-12 | TV5: hợp nhất slide/HTML | Ngô Gia An (23120205), Codex hỗ trợ | Đã cập nhật nguồn JSON và render lại 32 slide: AI-1..4, CoverUp, Pynguin và tóm tắt Video E; giữ nền trắng/chữ đen | `slides/slides.json`, `slides/index.html`; URL/timestamp điền sau khi quay |
| W06-13 | TV2: CI thật, required checks và điểm yếu | Phạm Quang Vinh (23120202) | Có evidence PR đỏ → xanh; required checks master theo snapshot; GitHub Actions là công cụ CI duy nhất | `evidence/tuan-06/github-actions/`; báo cáo mục 4.1 |
| W06-14 | TV5: pipeline AI-1/2 và AI-3 trên PR thật | Ngô Gia An (23120205), Codex hỗ trợ | Gemini 3.6 LoanService 7 → 10 test; apply tạo test thật, xóa output tạm; 49 test/gate pass, 74 offline checks; sáu job CI xanh và comment review hoàn tất | [PR #13](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/13), run 40889189664; đã merge `seminar-core` tại `bc067ca` |
| W06-15 | TV4: chạy lại từ máy sạch, test tích hợp, mô tả nghiệp vụ, script demo | Nguyễn Lê Thế Vinh (23120190), AI hỗ trợ (Claude Code) | Chạy lại trên Ubuntu 26.04: JDK 17 có sẵn báo `release version 25 not supported`, cài `openjdk-25-jdk-headless` thì `clean verify` 42/42 pass (52/52 sau khi merge `seminar-core` ngày 29/10), gate pass; README thêm hướng dẫn Linux. Thêm 3 test tích hợp (404 `MEMBER_NOT_FOUND`, từ chối không khóa sách, `LIMIT_REACHED`). Script demo 7 request đúng mã. Việc "hàm điều kiện ghép" đã có `LoanPeriodPolicy` (W06-06). **Chưa quay Video C.** | `LoanFlowEdgeCaseTest`; `scripts/demo_case_study.sh`; `docs/thuc-hanh/MoTa_NghiepVu_CaseStudy.md`; `README.md` |


**Giới hạn ghi nhận:** paper là tái hiện có giới hạn, không chạy lại toàn bộ benchmark nhiều seed/mutation. Gia An xác nhận phần AI/paper; thành viên khác tự xác nhận review chéo. AI-3 fixture và PR review là hai lượt riêng; [PR #13 CI/AI đã xanh](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40889189664). Cấu hình required checks phụ thuộc snapshot, không mặc định live.

## Điều phối chung — Ngô Gia An phụ trách

| Mốc | Quy tắc | Ngày thực tế | Bằng chứng |
|---|---|---|---|
| Hạn nộp seminar | Lấy từ thông báo GV | Chưa xác nhận | Link/thông báo GV |
| Gửi slide / gặp GV | Trước hạn nộp 3–4 ngày | Tính sau khi có hạn thật | Lịch hẹn hoặc phản hồi thật |
| Họp nhóm mỗi tuần | Mỗi người báo đã làm / đang làm / vướng | Chưa đặt lịch | Biên bản thật, tên người tham gia |
| Tập trình bày 1 | Chạy đủ tool/video | Chưa đặt lịch | Ghi nhận lỗi cần sửa |
| Tập trình bày 2 | Bấm giờ, kiểm Q&A | Chưa đặt lịch | Thời lượng đo thật |

## Checklist phần AI/paper và bàn giao

- [x] AI-5 LoanService chạy thật và lưu evidence.
- [x] Chuẩn bị bộ công cụ AI-4 để người tự điền.
- [x] Kiểm nguồn paper, hạng venue và artifact.
- [x] Chạy lại phân tích dữ liệu CoverUp và thử dry-run source nhóm.
- [x] Cả hai paper có reanalysis, generation mới trên benchmark và thử source nhóm; output/giới hạn trong evidence.
- [x] Đã nhận CSV/notes Gia An cung cấp; Codex khóa, commit rồi so và chạy Java: 23/23 người dùng, 13/13 AI. Độc lập theo tuyên bố trong notes; Gia An đã review kết quả.
- [x] Gia An xác nhận thực hiện/review AI/paper; declaration ghi rõ ai thao tác từng lượt, chưa ký thay trên bản nộp.
- [ ] Thành viên khác review chéo và xác nhận phần của họ.
- [ ] Đủ URL video và timestamp thật. Slide/HTML đã hợp nhất; chỉ còn điền link/timestamp sau khi quay.
- [ ] Gửi slide / gặp GV trước hạn 3–4 ngày.
- [ ] Điền Google Sheet contribution và xuất git log thật khi nộp.
- [ ] Kiểm gói: ≤20 file, mỗi file ≤20 MB, tổng ≤400 MB; tên ZipTool nếu cần chia/nén; không dùng Google Drive.

Ghi commit thật bằng `git log --date=iso-strict --format='%h | %aI | %an <%ae> | %s' seminar-core`. Bảng contribution phải mô tả đúng phần có AI hỗ trợ, không coi một tài khoản Git là bằng chứng cả nhóm đã thực hiện.
