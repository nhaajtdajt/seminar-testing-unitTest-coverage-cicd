# AI-4: đối chứng do người viết độc lập

Trạng thái ngày 28/10/2026: **chưa có dữ liệu người viết**. Ngô Gia An xác nhận chưa có bộ đối chứng; Codex chỉ tạo công cụ và mẫu rỗng. Không dùng bộ tham chiếu có sẵn trong repo làm đối chứng độc lập.

1. Người viết chỉ nhận đặc tả: NORMAL 2.000 VND/ngày, không ân hạn; VIP ân hạn 2 ngày rồi 1.000 VND/ngày; trần 50.000 VND; ngày âm hoặc tier null gây `IllegalArgumentException`. Tự xác định các ca và tự tính kết quả, không mở CSV AI hoặc test tham chiếu trước.
2. Chép `cases.template.csv` thành `cases.csv`. Cột `tier` dùng NORMAL, VIP hoặc NULL. Ca hợp lệ điền tiền và để trống `expectedException`; ca lỗi để trống tiền và điền `IllegalArgumentException`. Có ít nhất một ca hợp lệ và một ca lỗi; không lặp đầu vào.
3. Chính người viết thực hiện lệnh khóa (thay tên thật):

```bash
python3 scripts/ai4_compare.py freeze ai/human/cases.csv ai/human/frozen \
  --author 'Họ tên người tự viết' --attest-independent
git add ai/human/cases.csv ai/human/frozen
git commit -m 'test(ai4): freeze independently authored boundary oracle'
```

4. Sau khi khóa mới mở dữ liệu AI, đối chiếu và thực thi oracle trên Java:

```bash
python3 scripts/ai4_compare.py compare ai/human/frozen ai/data/AI-4-boundaries.csv \
  --output evidence/gia-an/ai4-human-comparison.json
case-study/mvnw -B -ntp -f case-study/pom.xml -Pai-human clean verify
```

Giữ `receipt.json` và commit trước so sánh. Công cụ kiểm SHA-256 để phát hiện sửa dữ liệu sau khóa; không thể tự chứng minh lời xác nhận độc lập. Nếu đã xem output AI thì nhờ người khác viết, không ký xác nhận sai. Ca trùng khác kỳ vọng phải đối chiếu đặc tả; không mặc định AI hay người đúng. Không ghi tỷ lệ đối chứng trước khi có CSV thật.
