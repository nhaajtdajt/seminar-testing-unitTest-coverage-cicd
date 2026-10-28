# Minh chứng phần Ngô Gia An (23120205), 28/10/2026

Tất cả lượt mới trong mục này do Codex chạy bằng công cụ tại máy, **local**, không phải GitHub Actions/Jenkins. Các xác nhận người tự review/chạy lại còn chờ. Source đề bài: `PhanCong_NhiemVu.md` hiện tại.

| Mục | Evidence | Kết quả |
|---|---|---|
| Bộ chuẩn | [full-verify/run.json](full-verify/run.json), log/XML cùng thư mục | 39 test, không failure/error/skipped, gate pass |
| AI Loan nháp | [loan-draft/run.json](loan-draft/run.json), [gaps](loan-draft/gaps.json) | 2 test; LoanService line 14/17, branch 3/6 |
| AI Loan bổ sung | [loan-improved/run.json](loan-improved/run.json) | 10 test; line 17/17, branch 6/6 |
| Fixture oracle sai | [loan-mistake/run.json](loan-mistake/run.json) | Maven exit 1, đúng 1 assertion failure; fixture cố ý cài sai, không phải lỗi quan sát từ API |
| Mutation | [loan-mutation-retry2/run.json](loan-mutation-retry2/run.json), [mutations.xml](loan-mutation-retry2/mutations.xml) | 9 KILLED/9; hai lượt trước lỗi cache/quyền và HTTP 502, không có mutation score |
| AI-4 tooling | [ai4-tooling.json](ai4-tooling.json) | Fixture synthetic kiểm công cụ; không có oracle người viết |
| CoverUp replay | [papers/coverup-mt/run.json](papers/coverup-mt/run.json), log 163 module | Overall line+branch 89,0% vs MuTAP gpt4o_zero 76,8%; phân tích dữ liệu công bố bằng script tác giả |
| CoverUp source nhóm | [papers/coverup-group-dry-retry/run.json](papers/coverup-group-dry-retry/run.json) | Dry-run pass; smoke coverage 23,6% không đổi; không gọi model/sinh test |
| ChatUniTest gốc | [papers/chatunitest-preflight-final/run.json](papers/chatunitest-preflight-final/run.json) | Thiếu dependencies/config/MySQL/API; chưa tái lập |
| ChatUniTest hiện tại | [papers/chatunitest-parse/run.json](papers/chatunitest-parse/run.json), [context LoanService](papers/chatunitest-parse/LoanService/class.json) | Plugin 2.1.1 parse được 20 class/28 method trên bản sao; không generation |

Không sửa lại log lỗi thành thành công, không dùng test report từ lượt khác làm bằng chứng. Các collector giữ thư mục output bất biến, kiểm report mới và thay đường dẫn cá nhân bằng placeholder. Paper parse log được sao từ command chạy thật; timestamp nằm trong Maven log. Source công khai, revision, dependencies và cách tái hiện xem `research/`.

Các mục **chưa hoàn thành**: oracle AI-4 do người viết và so độc lập; generation thực nghiệm hai paper; reviewer/người dùng tự xác nhận; video/YouTube/timestamp; họp/gặp GV/nộp bài.
