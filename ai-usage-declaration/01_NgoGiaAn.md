# Ngô Gia An (23120205): AI, paper và trình bày

> Theo template 6 mục chung của nhóm. Cập nhật 29/10/2026: nội dung do Codex hỗ trợ biên tập, chờ Gia An tự review và xác nhận; không tự ký thay người dùng.

## 1. Phần việc của tôi

- Việc được giao: AI-4 đối chứng dữ liệu, thử quy trình AI trên LoanService, chọn/kiểm hạng/chạy paper có code, khai báo AI, video và điều phối. Phần slide/HTML tạm hoãn đến cuối theo yêu cầu ngày 29/10.
- Link PR / commit của tôi: các commit local gồm `1bdadf6`, `1c1e3b6`, `e569765`, `1ef2b11`, `0e58f5f`, `f3df2ee`, `b698bac`, `4cf5467`; xem git log thật để đối chiếu các commit chuẩn hóa tiếp theo. Chưa push hoặc tạo PR cho phần mới trong phiên này.

## 2. Tôi đã dùng AI như thế nào

| # | Công cụ AI | Tôi nhờ AI làm gì (tóm tắt prompt) | Kết quả AI đưa ra | Nằm ở đâu trong repo |
|---|---|---|---|---|
| 1 | Codex, 28/10 | Đọc source và implement phần được giao, commit từng thay đổi | Sửa startup agent Mockito, tạo test/script và chạy kiểm chứng local | `case-study/pom.xml`, `scripts/run_ai_demo.py`, `evidence/tuan-06/` |
| 2 | Codex, 28/10 | Chuẩn bị đối chứng, sau đó đồng bộ CSV/notes người dùng gửi | Mẫu/runner, giữ nguyên dữ liệu, khóa/hash/commit trước so; không sinh/sửa ca người dùng cung cấp | `ai/human/`, `scripts/ai4_compare.py`, `evidence/tuan-06/ai-4/` |
| 3 | Codex, 28/10 | Tái sử dụng quy trình trên LoanService | Nháp/bổ sung, fixture oracle sai ghi nhãn, đo coverage và PIT | `LoanServiceAi*Test`, `ai/prompts/AI-5-loan-service.md`, `evidence/tuan-06/ai-loan/` |
| 4 | Codex + web/terminal, 28/10 | Chọn paper có code và kiểm hạng, thử artifact tác giả | Kiểm nguồn, CoverUp reanalysis/dry-run, ChatUniTest preflight/parse | `research/`, `scripts/paper_experiments.py`, `evidence/tuan-06/papers/` |
| 5 | Codex, 28–29/10 | Biên tập tài liệu; tích hợp core rồi thống nhất format docs/evidence | Docs vào tài liệu chung, evidence theo tuần/chủ đề; giữ slide/HTML core và gỡ bản xuất riêng trước đó theo yêu cầu | `docs/thuc-hanh/`, `evidence/tuan-06/`, lịch sử Git |

Không có Gemini/model API mới được gọi trong các lượt thí nghiệm AI-4/AI-5/paper trên. Lượt Gemini AI-3 có sẵn ngày 23/10 ở `evidence/tuan-06/ai-review/`; không nhận nó là output mới của phiên này.

## 3. Tôi đã review và kiểm chứng gì

- Tôi đã tự chạy lại: **chưa xác nhận**. Các lượt evidence dưới đây do Codex chạy bằng công cụ ở máy local, không phải Gia An tự chạy.
- Tôi đã đọc hiểu: **chưa xác nhận**, Gia An tự điền sau khi xem source/test/script.
- Kiểm chứng bằng công cụ: bộ chuẩn 39 test/gate pass; AI-4 người dùng 23/23, branch 10/10; AI CSV 13/13, branch 8/10; AI-5 nháp 2 → bổ sung 10 test, branch 3/6 → 6/6, PIT 9/9 KILLED; fixture sai fail đúng một assertion.
- Kiểm chứng paper: CoverUp phân tích 163 module, overall line+branch 89,0% vs 76,8%; dry-run source nhóm pass. ChatUniTest plugin parse 20 class/28 method. Chưa generation/tái lập đầy đủ.
- AI sai hoặc thiếu ở: collector ban đầu từng gắn Surefire cũ vào lượt lỗi trước clean; đã loại metadata cũ, ghi chú và thêm kiểm report mới. Fragment ChatUniTest có tham số prune không được bản phát hành nhận; đã bỏ. Fixture oracle sai là cố ý cài, không nhận là lỗi model thật.
- Tôi đã sửa: **chưa có xác nhận phần Gia An tự sửa**. Các sửa agent, collector và tài liệu trên do Codex hỗ trợ; source Git giữ nguyên tác giả lịch sử.

## 4. Phần tôi tự làm, không dùng AI

CSV và ghi chú thiết kế 23 ca do Gia An cung cấp; ghi chú tuyên bố chỉ dùng đặc tả, chưa tham chiếu AI/test tham chiếu. Codex giữ nguyên hai tệp và ghi nguồn trong receipt. Việc kê khai công cụ đã dùng khi soạn và xác nhận cá nhân do Gia An chịu trách nhiệm; hash không chứng minh tác giả hay tính độc lập.

## 5. Điều tôi chưa chắc hoặc chưa kiểm được

- Gia An tự review/chạy lại và reviewer chéo: chưa có xác nhận.
- Generation mới và tái lập đầy đủ hai paper chưa hoàn tất; ChatUniTest thuộc demo track cần xác nhận GV chấp nhận.
- 100% branch hoặc 9/9 mutant không chứng minh mọi lỗi đã được loại bỏ; phép so AI-4 chỉ trên một lớp và một CSV AI có sẵn.
- Video chưa quay/đăng, chưa có URL/timestamp thật. Slide/HTML riêng hoãn đến cuối, hiện dùng nguyên bản core; không ghi là đã hoàn thành phần trình bày mới.
- Ký khai báo, gặp GV, họp/nộp bài/Google Sheet vẫn chờ hành động thật của thành viên.

## 6. Xác nhận

Tôi chỉ xác nhận nội dung đúng sự thật và chịu trách nhiệm sau khi tự đọc, chạy lại và bổ sung phần còn chờ.

- [ ] Gia An đã đối chiếu khai báo với commit/artifact thật.
- [ ] Gia An đã chạy lại, hiểu phần của mình và bổ sung mục 3–5.
- [ ] Gia An xác nhận chịu trách nhiệm và giải thích được giới hạn.

Ngày: **chưa xác nhận** · Ký tên (họ tên): **chờ Gia An tự điền**.
