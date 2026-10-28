# Artifact để quay video — Ngô Gia An (23120205)

Ngày chuẩn bị: 28/10/2026. **Chưa quay, chưa đăng YouTube; timestamp thực tế điền sau khi quay.** Đây là danh mục đầu vào/đầu ra và nội dung cần thấy trên màn hình, chưa phải bản hướng dẫn thao tác quay. Kịch bản quay chi tiết sẽ làm ở bước sau theo yêu cầu của Gia An.

## Các video phần Gia An

| ID | Nội dung / mức | Artifact đã chuẩn bị | Điều người xem cần thấy | Trạng thái |
|---|---|---|---|---|
| GA-01 | Setup AI demo | JDK 25, Maven Wrapper, `scripts/run_ai_demo.py`, các profile trong POM | Bộ chuẩn chạy xanh; phân biệt Codex tương tác và Gemini API | Đủ đầu vào, chờ quay |
| GA-02 | Cơ bản: AI nháp → coverage | `LoanServiceAiDraftTest`, `loan-draft/run.json`, `loan-draft/gaps.json` | 2 test pass nhưng 3/6 branch; chỉ đúng chỗ còn thiếu | Đã chạy, chờ quay |
| GA-03 | Phức tạp: bổ sung → mutation | `LoanServiceAiImprovedTest`, `loan-improved/`, `loan-mutation-retry2/` | 10 test, 6/6 branch, PIT 9/9; xem cả assertion và side effect | Đã chạy, chờ quay |
| GA-04 | Trường hợp AI/test oracle sai | `LoanServiceAiMistakeTest`, `loan-mistake/` | Giới hạn là >=3; fixture cố ý kỳ vọng sai làm đỏ 1 assertion | Đã chạy, chờ quay; ghi nhãn fixture cài sẵn |
| GA-05 | Data driven và AI-4 đối chứng | `ai/human/README.md`, mẫu CSV, `ai4_compare.py`, profile `ai-human` | Người tự viết dữ liệu → khóa commit/hash → mới so với AI → chạy Java | Công cụ đủ; thiếu CSV do người tự viết |
| GA-06 | Paper CoverUp | `research/papers.json`, `research/README.md`, `papers/coverup-mt/`, `papers/coverup-group-dry-retry/` | Nguồn/rank, script tác giả, bảng 163 module, 89,0% vs 76,8%; dry-run không sinh test | Có replay phân tích + dry-run; thiếu lượt sinh test mới |
| GA-07 | Paper ChatUniTest | Source tác giả, `research/chatunitest/`, preflight và môi trường bản sao | Generation–validation–repair, target LoanService, tương thích môi trường; chỉ trình bày kết quả đã chạy | Chưa tái lập thí nghiệm/sinh test; không quay như đã thành công |

Các đường dẫn evidence trong bảng có gốc `evidence/gia-an/`. Dùng JSON/XML/log đã lưu làm dự phòng khi mạng yếu. Không dùng số liệu cũ để nói là lượt vừa chạy.

## Lệnh dựng lại artifact AI

Chạy tuần tự từ gốc repository, mỗi `--output` phải là thư mục mới để giữ bằng chứng. Script trả 0 khi kịch bản đạt kỳ vọng; Maven bên trong GA-04 phải trả 1 và đúng một assertion failure.

```bash
python3 scripts/run_ai_demo.py full --output /tmp/ga-full
python3 scripts/run_ai_demo.py draft --output /tmp/ga-draft
python3 scripts/coverage_gaps.py /tmp/ga-draft/jacoco.xml \
  --source-root case-study/src/main/java --output /tmp/ga-draft/gaps.json
python3 scripts/run_ai_demo.py improved --output /tmp/ga-improved
python3 scripts/run_ai_demo.py mistake --output /tmp/ga-mistake
python3 scripts/run_ai_demo.py mutation --output /tmp/ga-mutation
```

`clean` xóa report trong `target`, nên mở bản evidence tương ứng để so trước/sau. Không chạy hai Maven scenario cùng lúc. Lệnh full cuối buổi khôi phục JAR/report chuẩn nếu cần chạy ứng dụng.

## Video toàn nhóm cần đưa lên slide

| Nhóm video | Người phụ trách theo PhanCong_NhiemVu.md | Nội dung phải nhắc trên slide | Trạng thái liên kết |
|---|---|---|---|
| UT-1/2/3 + giới hạn | Nguyễn Bảo An | Setup, chạy test, CSV data driven, Mockito, trường hợp tool không xử lý tốt | Chờ người phụ trách quay và cung cấp URL |
| CC-1..6 | Trương Nhật Đạt | Setup, coverage trước/sau, gate, công cụ thứ hai, coverage cao vẫn bỏ lỗi, mutation | Chờ URL |
| CI-1/2/3 + giới hạn | Phạm Quang Vinh | Setup, cache/artifact, PR đỏ→xanh, required checks, lỗi CI | Chờ URL và runtime dịch vụ |
| Case study / integration | Nguyễn Lê Thế Vinh | Nghiệp vụ thư viện, app/H2, HTTP 201/409 và integration | Chờ URL |

Sau khi quay, điền vào bảng dưới. Không gắn URL placeholder vào slide như thể là video có thật. Nếu gộp clip, ghi timestamp cho **từng mức/demo** thay vì một video 2–3 phút cho toàn nhóm.

| ID | YouTube URL thật | Timestamp bắt đầu–kết thúc thật | Người quay / ngày | Đã xem lại khớp slide? |
|---|---|---|---|---|
| GA-01 | Chưa có | Chưa quay | Chưa xác nhận | Chưa |
| GA-02 | Chưa có | Chưa quay | Chưa xác nhận | Chưa |
| GA-03 | Chưa có | Chưa quay | Chưa xác nhận | Chưa |
| GA-04 | Chưa có | Chưa quay | Chưa xác nhận | Chưa |
| GA-05 | Chưa có | Chưa quay | Chưa xác nhận | Chưa |
| GA-06 | Chưa có | Chưa quay | Chưa xác nhận | Chưa |
| GA-07 | Chưa có | Chưa quay | Chưa xác nhận | Chưa |
