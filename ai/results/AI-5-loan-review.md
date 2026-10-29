# AI-5: LoanService — kết quả ngày 28/10/2026

Người được phân công: Ngô Gia An (23120205). Code/test và lượt chạy dưới đây do Codex hỗ trợ trong phiên này; chưa có xác nhận người dùng tự review/chạy lại.

| Giai đoạn | Lượt test | LoanService line | LoanService branch | Kết quả |
|---|---:|---:|---:|---|
| Nháp | 2 | 14/17 | 3/6 | 2 pass |
| Bổ sung | 10 (gồm 2 kế thừa từ nháp) | 17/17 | 6/6 | 10 pass |
| Fixture oracle sai | 3 (gồm 2 kế thừa) | Không xuất report vì verify dừng ở test | Không dùng để so coverage | 1 assertion fail đúng kỳ vọng |
| PIT bộ bổ sung | PIT chạy test riêng | — | — | 9 KILLED / 9 mutant, không sống trong tập mutator hiện tại |
| Bộ chuẩn của repo | 39 | 17/17 | 6/6 | Pass; gate FineCalculator pass |

Bằng chứng theo cấu trúc chung: [AI Loan](../../evidence/tuan-06/ai-loan/README.md), [bộ chuẩn 28/10](../../evidence/tuan-06/source-verify-2026-10-28/run.json). Hai lượt PIT trước chưa chạy mutation vì quyền cache và HTTP 502; giữ riêng log lỗi, không tính thành công. Thời gian là local, không suy ra tốc độ CI. Báo cáo ở `site/jacoco/` và `pit-reports/`.

Gap của nháp gồm nhánh sách unavailable, số sách đạt giới hạn và phí còn nợ; test missing member cũng cần để kiểm lambda ném lỗi (JaCoCo không tính exception handling thành một nhánh điều kiện riêng). Bộ bổ sung kiểm count 0/2/3/4, phí 0.00/0.01/1000, mã lỗi cụ thể và side effect không lưu khi bị từ chối. `ArgumentCaptor` và `Clock.fixed` kiểm phiếu lưu thay vì chỉ xác nhận mock trả đúng giá trị đã stub.

Fixture sai cố ý dùng điều kiện tưởng tượng “chỉ chặn khi >3” trong khi source/đặc tả chặn từ >=3. Đây là lỗi **cài sẵn để minh họa**, không phải lỗi quan sát từ một lời gọi Gemini hay từ ChatUniTest. Không sửa source nghiệp vụ để làm test sai pass.

100% branch và 9/9 mutant chỉ mô tả bộ test/mutator được chạy; không chứng minh an toàn đồng thời nhiều instance, transaction rollback hoặc mọi yêu cầu nghiệp vụ. Không đổi logic production trong demo này. [Prompt](../prompts/AI-5-loan-service.md) dùng được cho lớp khác khi thay source/spec và report đầu vào, nhưng mỗi lần phải review oracle.
