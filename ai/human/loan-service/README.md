# Chuẩn bị CSV người viết — LoanService

Mẫu này chỉ có header, **chưa có ca kiểm thử hay expected**. Gia An tự điền dữ liệu;
Codex chuẩn bị cấu trúc cột, không viết bộ đối chứng. Không dùng CSV FineCalculator
ở thư mục cha cho LoanService.

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

Điền [cases-notes.md](cases-notes.md) bằng thông tin thật trước khi khóa. Nếu đã xem
test/data AI của LoanService từ các lượt trước, bộ mới không thể được gọi là độc lập
với những dữ liệu đó. Khi cần đối chứng độc lập, nhờ người chưa xem tự viết; ghi đúng
tên tác giả. Vẫn có thể giữ bộ tham khảo để học nhưng không ký `--attest-independent`
cho bộ không đáp ứng điều kiện.

Chỉ chạy khi `cases.csv` đã có ca và người thực sự viết có thể xác nhận điều kiện trên:

```bash
python3 scripts/ai_generate.py freeze \
  --class LoanService --csv ai/human/loan-service/cases.csv \
  --author "TEN_NGUOI_THUC_SU_TU_VIET" --attest-independent \
  --output ai/human/loan-service/frozen
```

Chạy từ gốc repo, thay tên placeholder. Lệnh offline; không sửa bộ frozen đã có.
Hash ghi nhận dữ liệu tại thời điểm khóa, không tự chứng minh tác giả hay độc lập.
Sau khi khóa mới sinh test/CSV AI mới cho lượt quay. Các input bền vững và receipt
có thể commit trước đối chiếu; output `.ai-work/` không commit.

Kịch bản quay và lệnh AI-1/2/3/4: [Preparation Loan](../../../docs/thuc-hanh/Preparation_QuayVideo_AI1_AI4_Loan.md).
