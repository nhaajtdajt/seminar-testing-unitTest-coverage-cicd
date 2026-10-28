# AI-4: đối chiếu bộ ca Gia An cung cấp với CSV AI

Ngày đồng bộ: 28/10/2026. Thành viên: Ngô Gia An (23120205). Codex nhập và giữ nguyên hai tệp người dùng gửi: [cases.csv](../../ai/human/cases.csv), [cases-notes.md](../../ai/human/cases-notes.md).

## 1. Nguồn và thứ tự thực hiện

Ghi chú người dùng cung cấp tuyên bố chỉ sử dụng đặc tả nghiệp vụ, chưa tham chiếu dữ liệu AI/test tham chiếu. Đây là **xác nhận trong tài liệu người dùng**, không phải điều Codex có thể quan sát hay tự chứng minh về quá trình viết. Codex không sinh thêm hoặc sửa đầu vào/kỳ vọng trong bộ đối chứng.

1. Kiểm định dạng, trùng đầu vào và số dòng ghi chú: CSV có 23 ca, ghi chú có đúng 23 dòng tương ứng.
2. Chép nguyên byte hai tệp vào repo; tạo bản khóa và receipt, ghi rõ Codex thực hiện thay mặt người dùng theo yêu cầu đồng bộ.
3. Commit khóa **`0e58f5f`** trước khi chạy so sánh của lượt này.
4. Chạy compare, rồi chạy Java lần lượt bằng hai profile cô lập; giữ evidence từng bộ trước khi lượt sau `clean`.

CSV gốc và bản khóa có SHA-256 `97370c36a2d331a95681b42cff20938d69f0053535d3de0df815281915637fa1`. Receipt có cả hash ghi chú: [receipt.json](../../ai/human/frozen/receipt.json). Dòng “chưa chạy freeze hoặc commit” trong ghi chú được giữ nguyên vì mô tả thời điểm người dùng viết tệp, trước lượt đồng bộ này.

## 2. Bạn làm có đúng hướng không?

**Đúng hướng AI-4.** Các ca tự thiết kế kiểm NORMAL/VIP, ân hạn, trước–đúng–sau mức trần, vượt xa trần, ngày âm và tier null. Mỗi ca có lý do và phép tính; hai tệp khớp nhau. Cả 23 kỳ vọng đều phù hợp với implementation hiện tại khi chạy Java.

Bộ đối chứng chưa có `Integer.MAX_VALUE`; đây là khoảng trống về đầu vào cực lớn, không làm các kỳ vọng đã viết thành sai. Giữ bản khóa đầu tiên; nếu mở rộng sau khi xem AI, ghi bộ bổ sung là dữ liệu sau đối chiếu, không gọi nó là bộ độc lập ban đầu.

## 3. Kết quả đối chiếu

Nguồn số liệu: [ai4-human-comparison.json](../../evidence/gia-an/ai4-human-comparison.json).

| Chỉ số | Kết quả |
|---|---:|
| Bộ Gia An cung cấp | 23 ca: 16 hợp lệ, 7 ca lỗi |
| CSV AI có sẵn | 13 ca hợp lệ, không chứa ca lỗi |
| Đầu vào chung | 11 |
| Kỳ vọng khớp trên đầu vào chung | 11/11 |
| Cùng đầu vào nhưng kỳ vọng khác | 0 |
| Chỉ có trong bộ Gia An | 12: 5 hợp lệ, 7 ca lỗi |
| Chỉ có trong AI | 2: `Integer.MAX_VALUE` với NORMAL và VIP |

Năm đầu vào hợp lệ chỉ có trong bộ Gia An: NORMAL 2 ngày, VIP 0 ngày, VIP 4 ngày và 100 ngày cho mỗi hạng. Bảy ca lỗi nằm trong CSV và ghi chú gốc. Khác biệt đầu vào không đồng nghĩa lỗi: một số ca khác nhau kiểm cùng hành vi. Không diễn giải tỷ lệ trùng đầu vào là accuracy của mô hình.

## 4. Thực thi trên Java thật

| Bộ dữ liệu | Test | Failure / error / skipped | FineCalculator line | FineCalculator branch |
|---|---:|---|---:|---:|
| Gia An: profile `ai-human` | 23 pass | 0 / 0 / 0 | 11/11 | 10/10 (100%) |
| AI: profile `ai-data` | 13 pass | 0 / 0 / 0 | 9/11 | 8/10 (80%) |

Hai lượt `clean verify` đều exit 0 trên JDK 25.0.5. Gate FineCalculator được skip theo cấu hình hai profile demo; không báo kết quả này là kiểm tra quality gate. Khác biệt coverage xuất phát từ bộ AI chỉ chứa đầu vào hợp lệ nên chưa chạy hai nhánh ném lỗi. Bộ chuẩn của repo có các test lỗi riêng; không suy rộng 80% của profile CSV thành coverage toàn project.

- [Lệnh, hash và tổng hợp bộ Gia An](../../evidence/gia-an/ai4-human-run/run.json), [log](../../evidence/gia-an/ai4-human-run/output.log), [JaCoCo XML](../../evidence/gia-an/ai4-human-run/jacoco.xml).
- [Lệnh, hash và tổng hợp bộ AI](../../evidence/gia-an/ai4-ai-run/run.json), [log](../../evidence/gia-an/ai4-ai-run/output.log), [JaCoCo XML](../../evidence/gia-an/ai4-ai-run/jacoco.xml).

Các lượt chạy trên do **Codex** thực hiện bằng công cụ ở máy local. Chưa có xác nhận Gia An tự chạy lại hay reviewer khác đã kiểm.

## 5. Tái hiện để chuẩn bị video GA-05

```bash
python3 scripts/ai4_compare.py compare ai/human/frozen ai/data/AI-4-boundaries.csv \
  --output /tmp/ai4-human-comparison.json
python3 scripts/run_ai_demo.py human --output /tmp/ai4-human-replay
python3 scripts/run_ai_demo.py data --output /tmp/ai4-ai-replay
```

Chọn thư mục output mới nếu đã chạy trước đó. Chạy tuần tự; collector giữ report và từ chối chạy bộ người viết nếu hash bản khóa không khớp receipt. Video mở ghi chú, commit khóa, JSON so sánh và log/report của hai lượt. Chưa quay hoặc đăng video.

## 6. Kết luận và giới hạn

Bộ người dùng cung cấp hợp lệ và đúng chủ đề; nó bổ sung kiểm đầu vào lỗi mà CSV AI chưa có. AI bổ sung hai đầu vào cực lớn chưa có trong bộ người dùng. Không có kỳ vọng mâu thuẫn trong 11 ca chung, và toàn bộ ca của mỗi bộ đều pass khi thực thi riêng.

Đây là một phép so sánh trên một lớp/một bộ AI có sẵn, không phải benchmark độc lập trên nhiều mô hình. Hash và commit giữ dấu vết dữ liệu, không chứng minh tác giả hoặc tính độc lập; tuyên bố độc lập được dẫn từ ghi chú. 100% branch không chứng minh mọi lỗi đã bị loại bỏ. Gia An cần đọc kết quả, tự chạy lại và xác nhận khai báo cá nhân; video còn chờ quay.
