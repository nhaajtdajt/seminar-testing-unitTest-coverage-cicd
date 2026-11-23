# Chuẩn bị CSV người viết — LoanService

**Trạng thái 30/10/2026:** Gia An cung cấp 10 ca; theo yêu cầu người dùng, Codex đã
chỉnh ba ca theo source hiện tại (hạn mức 3, `LIMIT_REACHED`) và khóa tại
[frozen/cases.csv](frozen/cases.csv), [receipt](frozen/receipt.json).
Bản hiện tại có AI hỗ trợ đối chiếu/chỉnh theo implementation, **không phải đối chứng
độc lập**. [Notes nguồn và các thay đổi](cases-notes.md). Không dùng CSV FineCalculator.
`cases.template.csv` vẫn là mẫu header trống cho lần thiết kế khác.

## Cách điền

Chép `cases.template.csv` thành `cases.csv`, giữ đúng tên/thứ tự cột. Dùng trình soạn
thảo văn bản, UTF-8, dấu phẩy; mỗi hàng là một ca, không để hàng ghi chú trong CSV.

| Cột | Ý nghĩa / biểu diễn |
|---|---|
| `bookId` | Số nguyên `long` truyền vào `borrow` |
| `memberId` | Số nguyên `long` truyền vào `borrow` |
| `bookExists` | `true`/`false`: repository trả sách hay `Optional.empty()` |
| `bookAvailable` | `true`/`false`: trạng thái available của sách nếu sách tồn tại |
| `memberExists` | `true`/`false`: repository trả thành viên hay `Optional.empty()` |
| `activeLoans` | Số nguyên không âm: repository trả số sách đang mượn |
| `unpaidFine` | Số thập phân `BigDecimal`, dùng dấu chấm, không có phân cách hàng nghìn |
| `expectedOutcome` | `SUCCESS` hoặc `ERROR`, do người viết xác định |
| `expectedCode` | Thành công: `NONE`; lỗi: tên `LoanException.Code` mà người viết chọn |

Dùng `NONE` thay ô rỗng để tránh cách xử lý null/blank của CSV/JUnit khác nhau.
Luôn điền đầy đủ trạng thái dependency, kể cả khi một lỗi xảy ra trước làm trạng thái
phía sau không được đọc. Không lặp nguyên tổ hợp bảy cột input.

Đối chiếu API và yêu cầu được nhóm chấp nhận. Nếu chỉ dựa vào source, ghi rõ đang
kiểm hành vi implementation; source không phải đặc tả nghiệp vụ độc lập.
Các kiểu liên quan: `LoanService`, `Book`, `Member`, `LoanException`, ba repository.
Tự chọn các phân vùng, biên, thứ tự ưu tiên lỗi và tự tính expected; mẫu này không
đưa ca mẫu để bạn chép lại. Nếu thử ngoài miền nghiệp vụ, ghi riêng giả định trong notes.

Harness do Gemini sinh sau này cần được review: parse đúng chín cột; kiểm mã lỗi
bằng `LoanException.code()`; thành công kiểm phiếu mượn, thời gian cố định, ID hợp lệ,
phiếu được lưu và sách chuyển sang unavailable; lỗi không được ghi phiếu/sách.
Đây là yêu cầu kiểm chất lượng harness, không phải bộ expected đã được thực thi.

## Nguồn dữ liệu và khóa

Bản hiện tại đã khóa với khai báo source-assisted đúng nguồn gốc; không cần freeze lại
và không chạy `--attest-independent` cho bản AI đã hỗ trợ chỉnh này. `receipt.json` ghi
hash CSV/source/notes và tác giả, không tự chứng minh đúng đặc tả nghiệp vụ.

Để quay ngay, dùng [Preparation Loan](../../../docs/thuc-hanh/Preparation_QuayVideo_AI1_AI4_Loan.md).
AI-4 đọc bộ frozen ở trên và chỉ gửi header cho bước schema; dữ liệu human không được gửi Gemini.
Nếu sau này cần một bộ độc lập mới, người chưa xem test/data AI phải tự thiết kế input và
expected dựa trên đặc tả được chấp nhận, ghi nguồn và khóa trước đối chiếu.
