# Bảng công việc đến hết Tuần 6

## Cập nhật hiện hành 28/10/2026 — phần Ngô Gia An (23120205)

Căn cứ `PhanCong_NhiemVu.md` hiện tại: Gia An phụ trách AI, paper, hợp nhất trình bày và trưởng nhóm; Bảo An phụ trách Unit Test. Các mục W05/W06 phía dưới là ghi nhận lịch sử, không thay phân công hiện tại. **Video bắt buộc**; quyết định tạm loại video ở ghi nhận cũ đã được thay bởi yêu cầu ngày 28/10. Chỉ cập nhật phần được giao cho Gia An trong phiên này.

| ID | Công việc hiện tại | Trạng thái | Minh chứng |
|---|---|---|---|
| GA-AI4 | Đối chứng độc lập dữ liệu biên | Đã nhận/khóa 23 ca + notes Gia An cung cấp trước so sánh; 11 ca chung khớp; Java 23/23 vs AI 13/13 pass. Codex chạy; độc lập theo notes, chờ người review | `ai/human/`, `docs/gia-an/AI4_KetQua.md`, `evidence/gia-an/ai4-*` |
| GA-AI5 | Workflow AI trên LoanService | Đã chạy local, chờ người review: 2→10 test, branch 3/6→6/6, PIT 9/9 | `evidence/gia-an/`, `ai/results/AI-5-loan-review.md` |
| GA-PAPER | Chọn/kiểm hạng/chạy paper có code | CoverUp replay phân tích + dry-run; ChatUniTest parse pass; generation thực nghiệm còn chờ | `research/`, `evidence/gia-an/papers/` |
| GA-DECL | Khai báo dùng AI | Đã ghi phần Codex, chờ Gia An tự chạy/review/ký | `ai-usage-declaration/01_NgoGiaAn.md` |
| GA-SLIDE | Hợp nhất slide/báo cáo | Đã bổ sung AI/paper/video và trạng thái, nền trắng/chữ đen | `slides/`, báo cáo mục 9 |
| GA-VIDEO | Artifact AI/paper cho video | GA-01..07 đã có danh mục; chưa quay/đăng | `docs/gia-an/Video_Artifacts.md` |
| GA-LEAD | Họp, gặp GV trước hạn 3–4 ngày, nộp | Có checklist; chờ hạn thật, hành động và xác nhận của nhóm | `docs/gia-an/DieuPhoi.md` |

Mọi lượt mới do Codex chạy local; chưa có PR/push hoặc xác nhận reviewer chéo. Tiến độ paper chưa đủ để đánh dấu hoàn thành yêu cầu E.

---

## Ghi nhận lịch sử trước cập nhật trên


Đây là bảng theo dõi trong repository, chưa đồng bộ thành GitHub Issues/Projects. Các dòng W05 giữ vai trò/mốc công việc được ghi trong lịch sử; theo xác nhận của người dùng, tiến độ Tuần 05 kỳ trước do Phạm Quang Vinh đảm nhận. Các hạng mục W06 hiện tại do Ngô Gia An đảm nhận; không dùng bảng này để sửa tác giả commit lịch sử hoặc khẳng định thành viên khác đã review.

Theo xác nhận của người dùng, Tuần 05 là tiến độ kỳ trước do Phạm Quang Vinh đảm nhận; các dòng W05 bên dưới là phần lịch sử của kỳ trước. Phần đang thực hiện trong workspace là Tuần 06, do Ngô Gia An đảm nhận toàn bộ năm vai trò. Không sửa tác giả các commit lịch sử.

## Thành viên phụ trách

| Vai trò | MSSV | Họ tên | Phụ trách |
|---|---|---|---|
| TV1 | 23120207 | Nguyễn Bảo An | Trưởng nhóm, Unit Test, JUnit/Mockito và tổng hợp báo cáo |
| TV2 | 23120202 | Phạm Quang Vinh | CI/CD, Build Java 25 & Benchmark |
| TV3 | 23120231 | Trương Nhật Đạt | Code Coverage, JaCoCo, coverage gate và mutation testing |
| TV4 | 23120190 | Nguyễn Lê Thế Vinh | Case study, REST API, persistence và demo tích hợp |
| TV5 | 23120205 | Ngô Gia An | AI, slide, báo cáo chi tiết và điều phối video |

## Tiến độ Tuần 05 — kỳ trước

Các dòng W05 ghi trạng thái và minh chứng của kỳ trước; không gán các thay đổi hiện tại cho Phạm Quang Vinh.

| ID | Vai trò | Công việc | Trạng thái sản phẩm | Minh chứng/vị trí |
|---|---|---|---|---|
| W05-01 | TV1 | Tổng hợp đề xuất, kế hoạch tuần | Có tài liệu | `nop-lan-1/`, `KeHoach_BaoCao_HangTuan.md` |
| W05-02 | TV1 | Workflow 3 job, JDK 25, cache/artifact | Viết xong, kiểm tra tĩnh; chưa chạy GitHub | `.github/workflows/ci.yml`, `evidence/tuan-05/workflow-lint/` |
| W05-03 | TV1 | Jenkins đối chiếu | Có cấu hình; chưa chạy Jenkins | `Jenkinsfile` |
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

Theo chỉ đạo hiện tại của Ngô Gia An (23120205), các hạng mục của cả năm vai trò trong tuần này do Ngô Gia An đảm nhận. AI hỗ trợ biên tập/tái hiện; dòng này không sửa lại tác giả lịch sử trong Git và không khẳng định các thành viên khác đã review. Theo chỉ đạo mới nhất, video/kịch bản/ảnh demo tạm thời được loại khỏi checklist nộp tuần 6; source, test, báo cáo, AI/Git và visualization văn bản vẫn thuộc phạm vi bắt buộc.

| ID | Phạm vi kế hoạch Tuần 6 | Người đảm nhận tuần này | Tiến độ thực tế | Bằng chứng/ghi chú |
|---|---|---|---|---|
| W06-01 | TV1: kiểm kê source, phân công và minh chứng | Ngô Gia An (23120205) | Đã tách evidence Tuần 06, cập nhật chỉ mục và thêm ảnh JaCoCo; ZIP chuẩn bị tại `bai-nop/Group09-06.zip` | Bảng này, README, `evidence/tuan-06/README.md`; xác nhận nhóm/nộp chính thức còn phải do nhóm thực hiện |
| W06-02 | TV2: chốt Unit Test và bài tập | Ngô Gia An (23120205) | Tài liệu/bài tập có; lượt verify thành công gần nhất 33/33; demo ngoài checklist nộp tuần 6 | `docs/thuc-hanh/HuongDan_Demo.md`, `BaiTap_Tuan_06.md`, `evidence/tuan-06/source-verify/surefire-reports/` |
| W06-03 | TV3: chốt Coverage, CC-1/2/3, bài đọc báo cáo | Ngô Gia An (23120205) | Tài liệu có; full coverage verify pass; demo ngoài checklist nộp tuần 6 | `BaiTap_Tuan_06.md`, `evidence/tuan-06/source-verify/site/jacoco/`; PIT comparisons and gate examples remain in prior-week evidence |
| W06-04 | TV4: đóng gói source và hướng dẫn chạy lại | Ngô Gia An (23120205) | Source và hướng dẫn có; HTTP smoke 5/5 trên JAR Java 25; ảnh request 201/409 được giữ tùy chọn ngoài checklist | `case-study/`, `README.md`, `evidence/tuan-06/http-smoke-java25/`; dữ liệu H2 mẫu xem `case-study/src/main/resources/data.sql` |
| W06-05 | TV5: slide, báo cáo chi tiết, AI, bài tập, link | Ngô Gia An (23120205) | Slide/báo cáo/AI declaration/bài tập có; Gemini API live và evaluation fixture đạt 4/4; demo ngoài checklist nộp tuần 6 | `slides/`, `docs/thuc-hanh/BaoCao_ChiTiet.md`, `BaiTap_Tuan_06.md`, `evidence/tuan-06/ai-review/` |
| W06-06 | TV3: các loại coverage, JaCoCo đo gì, công cụ thứ hai, điểm yếu công cụ, kịch bản video | Trương Nhật Đạt (23120231), AI hỗ trợ (Claude Code) | Ví dụ `LoanPeriodPolicy` + bộ T1–T4 và bảng 6 loại coverage; bảng JaCoCo đo/không đo; OpenClover chạy thật, so 6 tiêu chí; demo mức trần ẩn trong `Math.min`, mutant tương đương, chi phí PIT; kịch bản Video B có timestamp. **Chưa quay video.** | `BaoCao_ChiTiet.md` mục 3.1–3.4, 5.2; `HuongDan_Demo.md` CC-0, CC-0b, CC-5, CC-6; `evidence/tuan-06/coverage-types/`, `openclover/`, `coverage-blindspot/`, `pit-cost/` |

**Giới hạn ghi nhận:** lượt kiểm tra đầy đủ và smoke API là chạy local, không phải GitHub Actions/Jenkins hoặc triển khai production. Gemini API đã được gọi live trên diff fixture; evaluation 4/4 chỉ xác nhận phát hiện được lỗi seed trong fixture, không đánh giá độc lập/toàn diện source. Video/kịch bản/ảnh demo nằm ngoài checklist nộp tuần 6 theo chỉ đạo mới nhất; các ảnh đã có được giữ làm minh chứng phụ.
