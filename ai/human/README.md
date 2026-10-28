# AI-4: đối chứng do người viết độc lập

Trạng thái cập nhật 28/10/2026: **đã nhận và khóa 23 ca cùng ghi chú do Gia An cung cấp**. Hai tệp được giữ nguyên byte tại [cases.csv](cases.csv) và [cases-notes.md](cases-notes.md); ghi chú tuyên bố chỉ dựa trên đặc tả, chưa xem dữ liệu AI/test tham chiếu. Codex thực hiện nhập/khóa thay mặt người dùng theo yêu cầu đồng bộ, rồi commit `0e58f5f` trước khi so sánh. Không tự chứng minh quá trình viết độc lập thay người dùng.

Đã chạy: bộ Gia An **23/23 pass, 10/10 branch**; CSV AI **13/13 pass, 8/10 branch** của FineCalculator. Có 11 đầu vào chung, cả 11 khớp kỳ vọng. [Kết quả và giới hạn](../../docs/gia-an/AI4_KetQua.md), [receipt](frozen/receipt.json). Chưa có xác nhận Gia An tự chạy lại; video còn chờ quay.

Các bước dưới mô tả quy trình tái sử dụng. Bản `frozen/` hiện tại đã tồn tại; không chạy freeze đè hoặc sửa bộ dữ liệu đã khóa. Ghi chú gốc được giữ nguyên, kể cả câu mô tả chưa freeze tại thời điểm người dùng viết tệp.

1. Người viết chỉ nhận đặc tả: NORMAL 2.000 VND/ngày, không ân hạn; VIP ân hạn 2 ngày rồi 1.000 VND/ngày; trần 50.000 VND; ngày âm hoặc tier null gây `IllegalArgumentException`. Tự xác định các ca và tự tính kết quả, không mở CSV AI hoặc test tham chiếu trước.
2. Chép `cases.template.csv` thành `cases.csv`. Cột `tier` dùng NORMAL, VIP hoặc NULL. Ca hợp lệ điền tiền và để trống `expectedException`; ca lỗi để trống tiền và điền `IllegalArgumentException`. Có ít nhất một ca hợp lệ và một ca lỗi; không lặp đầu vào.
3. Người viết hoặc người được ủy quyền thực hiện lệnh khóa (thay tên thật và ghi rõ ai chạy lệnh):

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
