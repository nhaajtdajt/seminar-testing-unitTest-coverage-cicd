# AI-2 — Đọc gap, sinh test, chạy lại

Đầu vào: báo cáo XML từ lượt `ai-draft-recheck` và source `FineCalculator.java`. JSON trích thực tế: `AI-2-gaps.json`. Codex trong phiên tương tác đã đối chiếu các vị trí sau:

| Vị trí | Nhánh còn thiếu được xác định từ source | Test bổ sung |
|---|---|---|
| Điều kiện `tier == null` | Chưa đi vào nhánh ném lỗi | Gọi `(1, null)`, kỳ vọng IllegalArgumentException. |
| Điều kiện `daysLate < 0` | Chưa đi vào nhánh ném lỗi | Gọi `(-1, NORMAL)`, kỳ vọng IllegalArgumentException. |
| Ternary chọn dailyRate | Nhánh VIP sau khi vượt ngày gia hạn chưa được chạy | Gọi `(3, VIP)`, kỳ vọng 1.000. |

Test tại `FineCalculatorAiGapsTest.java`. Profile `ai-improved` chạy 3 test ban đầu + 3 test bổ sung và giữ gate 90%; không dùng bộ đầy đủ để làm tăng số liệu của demo này. So 70% nhánh trước với kết quả chạy thật sau trong `evidence/tuan-05/ai-improved`.

XML chỉ cung cấp số nhánh bỏ sót tại dòng; các điều kiện cụ thể trong bảng được suy ra sau khi đọc source. Đây là demo AI hỗ trợ tương tác, không phải API tự động và chưa được thành viên nhóm xác nhận độc lập.
