# Minh chứng paper — Artifact tác giả (28/10/2026)

**Phụ trách:** Ngô Gia An (23120205), Codex hỗ trợ chạy/thu kết quả local. Source, revision và dependencies ở [research/papers.json](../../../research/papers.json) và [hướng dẫn](../../../research/README.md). Không tự implement lại phương pháp của paper.

| Lượt | Kết quả | Mức được phép kết luận | Minh chứng |
|---|---|---|---|
| CoverUp reanalysis MT | 163 module; overall line+branch 89,0% vs MuTAP 76,8% | Chạy script tác giả phân tích dữ liệu công bố, không sinh test mới | [coverup-mt/run.json](coverup-mt/run.json), log cùng thư mục |
| CoverUp dry-run | 23,6% coverage smoke trước/sau; exit 0 | Chạy tool gốc ở dry-run trên script nhóm, không gọi model | [coverup-group-dry-retry/run.json](coverup-group-dry-retry/run.json) |
| CoverUp dry-run lỗi mạng | Lỗi tải tokenizer, exit 1 | Lượt chưa thành công, giữ riêng | [coverup-group-dry/run.json](coverup-group-dry/run.json) |
| ChatUniTest gốc preflight | Thiếu config/MySQL/API/thư viện | Chỉ kiểm prerequisites, chưa tái lập | [chatunitest-preflight-final/run.json](chatunitest-preflight-final/run.json) |
| ChatUniTest plugin parse | 20 class/28 method, exit 0; endpoint localhost không có model | Thử parser bản plugin hiện tại trên bản sao case study, chưa generation | [chatunitest-parse/run.json](chatunitest-parse/run.json), [context LoanService](chatunitest-parse/LoanService/class.json) |
| ChatUniTest parse lỗi | Thiếu JAR, exit 1 | Đóng gói rồi thử lại ở lượt riêng | [chatunitest-parse-failed/run.json](chatunitest-parse-failed/run.json) |

## Cách tái hiện

Dùng `scripts/paper_experiments.py` và `research/chatunitest/prepare_trial.py` theo `research/README.md`. Các lệnh phải chỉ định output mới. Đọc cả `scope` và `new_model_generation` trong metadata; exit 0 của reanalysis/dry-run/parse không đồng nghĩa tái lập generation.

## Phần chưa làm

- Sinh test mới bằng tool tác giả trên benchmark gốc và source nhóm; lưu model/tham số/chi phí cùng số test compile/pass và coverage.
- Đối chiếu kết quả generation với paper; dependencies/môi trường khác phải ghi rõ.
- Xác nhận GV chấp nhận demo track của ChatUniTest. FSE A* là hạng venue, không gán trực tiếp cho từng bài.

Ngày 29/10 các tệp được chuyển từ thư mục cá nhân sang chủ đề paper; giữ nguyên byte của log/metadata/output. Không dùng AI-5 Codex thay kết quả ChatUniTest.
