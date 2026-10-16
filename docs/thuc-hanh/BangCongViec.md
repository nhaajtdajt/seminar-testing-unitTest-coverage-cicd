# Bảng công việc đến hết Tuần 5

Đây là bảng theo dõi trong repository, chưa đồng bộ thành GitHub Issues/Projects. TV1–TV5 đã được gán thành viên theo yêu cầu của nhóm; phần xác nhận kết quả do các thành viên rà soát trước khi nộp. Các sản phẩm mới được triển khai với Codex trong phiên hiện tại, không dùng bảng này để suy ra tác giả commit hay công lao của từng người trong các tuần trước.

Mốc báo cáo hiện tại là Tuần thực hành 04. Các mã W05 và tiêu đề đến Tuần 5 mô tả phạm vi công việc theo kế hoạch, bao gồm phần đã làm trước; kết quả thực tế được ghi trong báo cáo Tuần 04.

## Thành viên phụ trách

| Vai trò | MSSV | Họ tên | Phụ trách |
|---|---|---|---|
| TV1 | 23120207 | Nguyễn Bảo An | Trưởng nhóm, Unit Test, JUnit/Mockito và tổng hợp báo cáo |
| TV2 | 23120202 | Phạm Quang Vinh | CI/CD, Build Java 25 & Benchmark |
| TV3 | 23120231 | Trương Nhật Đạt | Code Coverage, JaCoCo, coverage gate và mutation testing |
| TV4 | 23120190 | Nguyễn Lê Thế Vinh | Case study, REST API, persistence và demo tích hợp |
| TV5 | 23120205 | Ngô Gia An | AI, slide, báo cáo chi tiết và điều phối video |

## Tiến độ công việc

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
