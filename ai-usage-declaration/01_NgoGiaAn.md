# Ngô Gia An (23120205): AI, paper và trình bày

> Theo template 6 mục chung. Cập nhật 29/10/2026 theo xác nhận/yêu cầu của Gia An trong phiên làm việc: đã thực hiện và review phần AI/paper với Codex hỗ trợ. Mỗi lượt chạy được ghi rõ người thao tác; không nhận các lượt tự động là Gia An tự gõ lệnh hoặc review độc lập.

## 1. Phần việc của tôi

- Phụ trách AI-1/2/3/4, đối chứng dữ liệu người–AI, thử trên LoanService; chọn/kiểm hạng/chạy hai paper có source, tổng hợp kết quả và khai báo AI.
- Slide/HTML và báo cáo AI/paper đã hợp nhất. Quay video và điều phối nộp/trình bày làm sau; không đánh dấu đã quay hoặc đã có xác nhận của giảng viên.
- PR triển khai AI: [#13](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/13), các commit `b4b4d30`, `3bdbbc8`, `6c928b0`, `f351e88`. Phần paper: nhánh `codex/paper-live-results`; đối chiếu commit thật bằng Git, không gán lại tác giả lịch sử.

## 2. Tôi đã dùng AI như thế nào

| # | Công cụ | Tôi nhờ làm gì | Output | Vị trí |
|---|---|---|---|---|
| 1 | Codex | Đọc source/phân công, chuẩn bị script/prompt tổng quát; sửa vòng chạy, repair/review/apply và cleanup | Code và kiểm thử offline; đồng bộ test sau bước review được xác nhận | `scripts/`, `ai/prompts/`, PR #13 |
| 2 | Gemini 3.6 Flash | Sinh và bổ sung test theo source/schema/coverage | Lượt LoanService mới: 7 test nháp + 3 bổ sung; apply tạo hai file test mới rồi xóa output tạm | Hai file `LoanServiceGemini*Test` trên PR #13; không lưu output gemini-live |
| 3 | Codex/Gemini | Chuẩn bị AI-4; khóa dữ liệu người dùng cung cấp, sinh/so/chạy dữ liệu AI | Giữ nguyên CSV/notes của Gia An; báo cáo phân biệt so CSV với chạy Java, không sửa human oracle để khớp AI | `ai/human/`, `scripts/ai4_compare.py`, hướng dẫn AI-1/2/4 |
| 4 | Gemini 3.6 Flash trong CI | Review diff PR song song test/coverage, cập nhật comment khi pass hoặc fail | PR #13 review hoàn tất, không finding; summary có số test và JaCoCo thật | Workflow và [comment PR](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/13#issuecomment-6498531583) |
| 5 | Codex + tra cứu nguồn chính thức | Chọn paper, kiểm hạng, chạy tool/mã phân tích tác giả, thu output gọn | CoverUp + Gemini 3.6 và Pynguin; phân tích dữ liệu công bố, generation benchmark và thử source nhóm | `research/`, `evidence/tuan-06/papers/` |
| 6 | Codex | Biên tập báo cáo/hướng dẫn, bỏ trial cũ và output trùng; hợp nhất slide | Tài liệu cùng format nhóm, chỉ giữ output cần đối chiếu; slide 24–29 cập nhật AI/paper và Video E | `docs/thuc-hanh/`, `slides/`, declaration và evidence |

Pynguin dùng tìm kiếm DynaMOSA, không gọi Gemini/LLM. CoverUp lượt mới có gọi Gemini thật. Codex thu output từ công cụ và biên tập tài liệu; không dùng response tự viết thay kết quả thực thi của tác giả.

## 3. Tôi đã review và kiểm chứng gì

- **Xác nhận review:** Gia An xác nhận đã thực hiện/review phần AI/paper trong phiên làm việc ngày 29/10 và yêu cầu cập nhật khai báo sau khi chạy xong. Đây là xác nhận của người phụ trách, không nhận là review mù hay xác nhận thay thành viên khác.
- **Gia An tự thao tác:** chuẩn bị CSV/notes đối chứng độc lập; tự chạy Gemini AI-1/2 trên LoanService trong Terminal; tự chạy CoverUp + Gemini trên benchmark f003. Codex đọc và đối chiếu output sau đó.
- **Codex chạy theo ủy quyền:** pipeline AI mới → apply, offline checks, kiểm CI/AI-3, phân tích paper và các lượt generation bổ sung trên benchmark/source nhóm. Không gán những lệnh đó là Gia An tự gõ.
- **AI runtime:** LoanService Gemini 7 → 10 test pass, target line 17/17, branch 6/6; apply kiểm toàn suite 49 test/gate pass. [CI 40889189664](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40889189664) có đủ sáu job xanh, gồm review Gemini 3.6 và summary; 74 offline Python checks trên PR #13.
- **Đối chứng trước đây:** Java human CSV 23/23, AI CSV 13/13; 11 input chung khớp expected. Bộ AI-5 Codex tương tác là một lượt riêng, không gán cho Gemini/paper.
- **Paper CoverUp:** phân tích MT 163 module: 89,0% vs 76,8%; f003 cả bộ 3 pass, line/branch 100%; source nhóm 7 pass, kết hợp 23,6% → 96,4%.
- **Paper Pynguin:** notebook 134 module/40.200 dòng/30 lượt mỗi cấu hình khớp output tác giả; benchmark mới coverage nội bộ 81,48% bằng median công bố đúng module/config, **10 pass + 5 xfail**. Trên source nhóm, bản có seed có 2 pass nhưng thiếu assertion, coverage bằng smoke baseline.
- **Điểm phải sửa/đọc kỹ:** code/test do AI sinh vẫn cần kiểm assertion/oracle; AI-2 có thể không tăng coverage. Pynguin group trial minh họa giới hạn input filesystem/XML. Không đổi source, xóa test lỗi hoặc hạ gate để làm đẹp số liệu.

## 4. Phần tôi tự làm, không dùng AI

CSV và notes thiết kế 23 ca do Gia An cung cấp trước khi so AI; notes tuyên bố chỉ dùng đặc tả, chưa xem AI/test tham chiếu. Codex giữ nguyên dữ liệu và ghi receipt. Hash/commit xác định phiên bản, không chứng minh tác giả hay tính độc lập; Gia An chịu trách nhiệm tuyên bố này.

Thực nghiệm paper dùng tool/mã phân tích của tác giả, có Codex hỗ trợ thiết lập/chạy/tổng hợp; không kê phần đó là tự viết không dùng AI.

## 5. Điều tôi chưa chắc hoặc chưa kiểm được

- Paper mới tái hiện có giới hạn: phân tích dữ liệu công bố và một lượt generation benchmark mỗi bài, cộng source nhóm. Chưa chạy mới toàn benchmark nhiều seed hoặc mutation RQ3; môi trường/model có khác biệt đã ghi trong research.
- 100% coverage hoặc test pass không chứng minh đúng mọi nghiệp vụ; `xfail` không được cộng vào số pass. Hai tool paper thử trên source Python của nhóm, không nhận là generation JUnit cho LoanService.
- Reviewer chéo của thành viên khác chưa xác nhận. Video/URL/timestamp và gặp GV chưa hoàn tất. Slide/HTML đã có chỗ để gắn URL/timestamp sau khi quay.
- Họp/nộp bài/Google Sheet và chữ ký chính thức trên bản xuất vẫn do thành viên thực hiện.

## 6. Xác nhận

- [x] Gia An xác nhận đã thực hiện và review phần AI/paper với AI hỗ trợ, theo yêu cầu trong phiên ngày 29/10/2026.
- [x] Khai báo phân biệt lượt Gia An tự chạy, lượt Codex chạy và output tool tác giả; giữ giới hạn thí nghiệm.
- [ ] Thành viên khác review chéo và ký xác nhận phần họ thực sự kiểm.

Ngày ghi nhận: **29/10/2026** · Người xác nhận trong phiên: **Ngô Gia An (23120205)**. Chữ ký trên bản nộp do Gia An tự ký.
