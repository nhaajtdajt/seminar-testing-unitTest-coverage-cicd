# Ghi chú thiết kế bộ kiểm thử độc lập

Chỉ sử dụng đặc tả nghiệp vụ được cung cấp; chưa tham chiếu AI/test tham chiếu.

NORMAL: min(50000, daysLate × 2000). VIP: min(50000, max(0, daysLate − 2) × 1000). Ngày âm hoặc tier NULL: IllegalArgumentException.

| # | daysLate | tier | Lý do chọn | Kết quả mong đợi / cách tính |
|---:|---:|---|---|---|
| 1 | 0 | NORMAL | Không trễ | min(50000, daysLate × 2000) = 0 |
| 2 | 1 | NORMAL | Ngày trễ dương nhỏ nhất | min(50000, daysLate × 2000) = 2000 |
| 3 | 2 | NORMAL | Trường hợp thông thường | min(50000, daysLate × 2000) = 4000 |
| 4 | 24 | NORMAL | Ngay dưới mức trần | min(50000, daysLate × 2000) = 48000 |
| 5 | 25 | NORMAL | Chạm trần | min(50000, daysLate × 2000) = 50000 |
| 6 | 26 | NORMAL | Vượt trần một ngày | min(50000, daysLate × 2000) = 50000 |
| 7 | 100 | NORMAL | Vượt xa trần | min(50000, daysLate × 2000) = 50000 |
| 8 | -1 | NORMAL | Âm sát 0 | Đầu vào không hợp lệ → IllegalArgumentException |
| 9 | -10 | NORMAL | Âm xa 0 | Đầu vào không hợp lệ → IllegalArgumentException |
| 10 | 0 | VIP | Không trễ | min(50000, max(0, daysLate − 2) × 1000) = 0 |
| 11 | 1 | VIP | Trong ân hạn | min(50000, max(0, daysLate − 2) × 1000) = 0 |
| 12 | 2 | VIP | Ngày cuối ân hạn | min(50000, max(0, daysLate − 2) × 1000) = 0 |
| 13 | 3 | VIP | Ngày đầu chịu phí | min(50000, max(0, daysLate − 2) × 1000) = 1000 |
| 14 | 4 | VIP | Ngày thứ hai chịu phí | min(50000, max(0, daysLate − 2) × 1000) = 2000 |
| 15 | 51 | VIP | Ngay dưới mức trần | min(50000, max(0, daysLate − 2) × 1000) = 49000 |
| 16 | 52 | VIP | Chạm trần | min(50000, max(0, daysLate − 2) × 1000) = 50000 |
| 17 | 53 | VIP | Vượt trần một ngày | min(50000, max(0, daysLate − 2) × 1000) = 50000 |
| 18 | 100 | VIP | Vượt xa trần | min(50000, max(0, daysLate − 2) × 1000) = 50000 |
| 19 | -1 | VIP | Âm sát 0 | Đầu vào không hợp lệ → IllegalArgumentException |
| 20 | -10 | VIP | Âm xa 0 | Đầu vào không hợp lệ → IllegalArgumentException |
| 21 | 0 | NULL | Tier null tại biên 0 | Đầu vào không hợp lệ → IllegalArgumentException |
| 22 | 2 | NULL | Tier null với ngày dương | Đầu vào không hợp lệ → IllegalArgumentException |
| 23 | -1 | NULL | Đồng thời ngày âm và tier null | Đầu vào không hợp lệ → IllegalArgumentException |

Không có cặp (daysLate, tier) trùng lặp. Có ca hợp lệ và ca lỗi. Chưa chạy freeze hoặc commit.
