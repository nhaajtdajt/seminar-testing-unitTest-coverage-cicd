# Ngô Gia An (23120205): AI, paper và trình bày

Cập nhật 28/10/2026 theo `PhanCong_NhiemVu.md` hiện tại. **Bản khai do Codex hỗ trợ biên tập, chờ Gia An tự review và xác nhận.**

## 1. Phần việc được giao

AI-4 đối chứng độc lập; mở rộng AI trên LoanService; chọn/kiểm hạng/chạy paper có code; hợp nhất slide/báo cáo; chuẩn bị artifact video AI/paper và điều phối trưởng nhóm. Triển khai trực tiếp trên `seminar-core` theo yêu cầu của Gia An, commit bằng identity Git đã có (`bingsu`), không đổi tác giả lịch sử. Chưa push/tạo PR.

## 2. AI đã hỗ trợ như thế nào

| Công cụ | Người dùng yêu cầu | AI thực hiện | Artifact |
|---|---|---|---|
| Codex (OpenAI), phiên 28/10/2026 | Đọc đúng phân công hiện tại, implement và commit từng thay đổi | Kiểm source, sửa Mockito agent, tạo test/script, chạy lệnh kiểm chứng | `case-study/pom.xml`, `scripts/run_ai_demo.py`, `evidence/gia-an/` |
| Codex | Chuẩn bị đối chứng AI-4 để người tự điền sau | Mẫu rỗng, freeze/hash, compare, runner Java; dùng fixture synthetic kiểm công cụ | `ai/human/`, `scripts/ai4_compare.py`, `FineCalculatorHumanDataTest` |
| Codex | Thử workflow AI trên lớp khác | Sinh nháp/bổ sung LoanService; fixture oracle sai ghi nhãn; đo coverage/PIT | `LoanServiceAi*Test`, `ai/prompts/AI-5-loan-service.md`, `ai/results/AI-5-loan-review.md` |
| Codex + web/terminal | Chọn paper có code, kiểm hạng và thử artifact | Kiểm trang công bố/CORE; chạy script phân tích CoverUp, dry-run source nhóm; ChatUniTest preflight và parse | `research/`, `scripts/paper_experiments.py`, `evidence/gia-an/papers/` |
| Codex | Hợp nhất trình bày, artifact trước khi quay | Viết phần AI/paper/video; cập nhật JSON/HTML/Markdown, xuất PDF; danh mục video | `slides/`, `docs/gia-an/`, báo cáo chi tiết, `output/pdf/` |

Các lượt lệnh evidence do **Codex chạy bằng công cụ trong workspace**. Chưa ghi nhận Gia An tự chạy lại hoặc thành viên khác review. Không có Gemini/model API được gọi trong các thí nghiệm mới này; output Gemini có sẵn thuộc lượt cũ.

## 3. AI đã kiểm bằng công cụ

- Bộ chuẩn: 39 test pass trên JDK 25.0.5; coverage gate pass.
- LoanService AI: 2 test, branch 3/6 → 10 test, branch 6/6; PIT 9/9 mutant. Fixture sai fail 1 assertion đúng dự kiến.
- Đối chứng: Python test kiểm mẫu rỗng, duplicate, disagreement, tampering; Java runner thử bằng 3 ca **synthetic**, không nhận là dữ liệu người viết.
- CoverUp: script tác giả phân tích MT 163 module, overall line+branch 89,0% vs 76,8%; dry-run source Python nhóm pass. Chưa sinh lại test bằng model.
- ChatUniTest: kiểm prerequisites artifact gốc; plugin 2.1.1 parse bản sao case study đạt 20 class/28 method. Chưa có generation hay tái lập thí nghiệm gốc.

## 4. Hạn chế và sửa sai

- Mockito self-attach lỗi tại máy trên JDK 25; startup javaagent giữ argLine JaCoCo đã khắc phục, 39 test pass.
- Collector từng gắn Surefire cũ vào lượt PIT thất bại trước clean. Đã bỏ metadata cũ, ghi chú sửa và thêm kiểm thời gian sửa report. Giữ log lỗi thật.
- PIT: từng lỗi quyền cache và HTTP 502; retry thành công lưu riêng. CoverUp dry-run đầu lỗi tải tokenizer, retry thành công riêng.
- ChatUniTest parse đầu thiếu JAR; đóng gói bản sao rồi parse thành công. Fragment có tham số prune không được bản plugin phát hành nhận, đã bỏ khỏi fragment; không ảnh hưởng kết quả parse.
- Paper còn thiếu generation mới. Không lấy AI-5 thay cho kết quả paper.
- Hash không chứng minh dữ liệu do người viết độc lập; vẫn cần xác nhận thật và commit trước đối chiếu.

## 5. Gia An tự điền sau khi review

- Tôi tự chạy lại (lệnh, ngày, kết quả): **chưa xác nhận**.
- Tôi đã đọc hiểu source/test/script: **chưa xác nhận**.
- Tôi tự sửa gì và vì sao: **chưa xác nhận**.
- Phần tôi tự làm không dùng AI: **chưa kê khai**; không gán phần Codex vừa tạo là người tự viết.
- Oracle AI-4: **chưa có**, Gia An đã xác nhận tự điền sau.
- Reviewer chéo và commit/PR họ đã đọc: **chưa có xác nhận**.

## 6. Xác nhận cá nhân

- [ ] Tôi đã đối chiếu khai báo với commit/artifact thật.
- [ ] Tôi đã chạy lại, hiểu phần của mình và điền mục 5.
- [ ] Tôi chịu trách nhiệm nội dung nộp và giải thích được giới hạn.

Ngày xác nhận và chữ ký Gia An: **chờ người dùng tự điền**.
