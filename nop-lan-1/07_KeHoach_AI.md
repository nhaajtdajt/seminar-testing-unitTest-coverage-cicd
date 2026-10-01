# Kế hoạch áp dụng AI + Quy ước sử dụng AI của nhóm

**Phụ trách:** TV5

> Đề yêu cầu *"trình bày khả năng áp dụng AI vào chủ đề testing được giao seminar với các
> demo cụ thể, có khả năng tổng quát hóa, tái sử dụng"*.
>
> Nhóm hiểu **"tái sử dụng"** nghĩa là: mỗi demo phải để lại một **tài sản** — một prompt
> template có tham số, hoặc một script — mà người khác lấy về dùng cho project của họ được.
> Không phải một đoạn hội thoại chụp màn hình lại.

---

## PHẦN A — BỐN DEMO AI

## Bốn nguyên tắc chung

1. **Mỗi demo để lại một tài sản có đường dẫn cố định trong repository.** Tài sản là file,
   không phải ảnh chụp.
2. **Mỗi demo phải có số đo trước/sau.** AI nói "đã cải thiện" không được tính; phải có con số.
3. **Nhóm sẽ báo cáo cả số lần AI làm sai.** Ví dụ: AI sinh 12 test thì bao nhiêu test sai,
   sai kiểu gì, nhóm sửa thế nào. Đây là phần trung thực nhất của báo cáo và cũng là bằng
   chứng cho thấy nhóm thực sự review chứ không sao chép.
4. **Khoá API không bao giờ xuất hiện trong mã nguồn, slide hay video.** Khoá chỉ nằm trong
   kho bí mật của nền tảng CI hoặc biến môi trường trên máy cá nhân.

---

### AI-1 — Sinh unit test từ mã nguồn

| | |
|---|---|
| **Mục tiêu** | Từ một lớp chưa có test, AI sinh bộ test chạy được |
| **Đầu vào** | Mã nguồn lớp tính phí trả sách trễ |
| **Tài sản để lại** | Prompt template có tham số: `{{MÃ_NGUỒN}}`, `{{KHUNG_TEST}}`, `{{RÀNG_BUỘC}}` |
| **Số đo** | Độ phủ nhánh trước/sau · số test AI sinh · **số test sai phải sửa tay** · thời gian người bỏ ra |
| **Minh chứng** | Prompt template · hai commit liên tiếp: *"test do AI sinh (chưa sửa)"* → *"test sau khi nhóm review"* · hai báo cáo coverage |
| **Mức tự động** | Semi-automated — người **bắt buộc** review trước khi commit |

**Chỗ làm cho nó tổng quát hóa được:** prompt template buộc AI phải (a) **liệt kê các nhánh
của hàm trước** khi viết test, (b) viết ít nhất một test cho mỗi nhánh, (c) đặt tên test
bằng tiếng Việt mô tả hành vi, (d) **không** được mock các lớp chỉ chứa logic thuần. Ràng
buộc (d) chính là bài học nhóm rút ra từ điểm yếu của Mockito trong phần 1.

**Checklist review bắt buộc, đi kèm prompt template:**

- [ ] Mỗi test có ít nhất một assertion không?
- [ ] Assertion kiểm **giá trị kỳ vọng cụ thể**, hay chỉ kiểm "khác null"?
- [ ] Có test nào chỉ xác nhận lại chính giá trị đã mock (test tự xác nhận) không?
- [ ] Số thập phân có được so sánh đúng cách không (so giá trị, không so cả định dạng)?
- [ ] Tên test có nói được hành vi không, hay chỉ là `test1`, `test2`?
- [ ] AI có bịa ra hàm/thuộc tính không tồn tại trong mã nguồn không?

---

### AI-2 — Đọc báo cáo coverage, vá lỗ hổng độ phủ

| | |
|---|---|
| **Mục tiêu** | Biến báo cáo coverage thành việc cụ thể: nhánh nào chưa phủ, cần viết test nào |
| **Đầu vào** | File báo cáo XML do JaCoCo sinh ra |
| **Tài sản để lại** | **Script** lọc báo cáo XML thành danh sách nhánh chưa phủ (kèm tên lớp, tên hàm, số dòng) + prompt template |
| **Số đo** | Độ phủ nhánh trước/sau · số nhánh AI chỉ đúng / chỉ sai |
| **Minh chứng** | Script · output của script · prompt · hai báo cáo coverage |
| **Mức tự động** | Semi-automated |

**Vì sao phải viết script chứ không dán cả file XML cho AI:** báo cáo XML của một project
thật dài hàng nghìn dòng; dán hết vừa tốn chi phí vừa khiến AI bỏ sót. Script lọc còn đúng
phần nhánh **chưa được phủ**, kèm vị trí. Đây chính là chỗ "tổng quát hóa": script chạy được
với **bất kỳ** project Maven dùng JaCoCo nào, không riêng case study của nhóm.

---

### AI-3 — AI nhận xét chất lượng test trên mỗi Pull Request

| | |
|---|---|
| **Mục tiêu** | Mỗi Pull Request được tự động nhận xét về **chất lượng test**, không chỉ về mã nguồn |
| **Đầu vào** | Phần thay đổi của Pull Request |
| **Tài sản để lại** | Một job trong file cấu hình pipeline + prompt nhúng trong job |
| **Số đo** | Trên **một Pull Request có lỗi cài sẵn**: số vấn đề thật AI tìm ra / số báo động giả |
| **Minh chứng** | File cấu hình · ảnh chụp nhận xét của AI trên PR · bảng đối chiếu *"AI nói gì"* vs *"sự thật"* |
| **Mức tự động** | **Fully automated** |

**Ràng buộc bảo mật:** khoá API chỉ nằm trong kho bí mật của GitHub, được tham chiếu bằng
biến, không hard-code, không in ra log, không hiện trong video.

**Phương án dự phòng:** nếu chưa cấu hình kịp kho bí mật, nhóm chạy bản tại máy (script đọc
khoá từ biến môi trường) và chụp kết quả. Khi đó demo hạ xuống mức semi-automated, và nhóm
sẽ **ghi rõ trong báo cáo là đã hạ mức**, không nhận vơ là fully automated.

**Bốn lỗi sẽ cài sẵn trong Pull Request mẫu** (để đo chất lượng nhận xét của AI):

1. Một test không có assertion nào.
2. Một test mock chính lớp tính phí rồi assert lại đúng giá trị đã mock (test tự xác nhận).
3. Một phép so sánh số thập phân sai cách, dẫn tới test đỏ/xanh không đúng bản chất.
4. Một nhánh nghiệp vụ mới được thêm nhưng không có test nào phủ.

---

### AI-4 — Sinh bộ dữ liệu biên cho data-driven test

| | |
|---|---|
| **Mục tiêu** | AI đề xuất các ca biên mà người viết dễ bỏ sót |
| **Đầu vào** | Đặc tả nghiệp vụ tính phí viết bằng tiếng Việt + chữ ký hàm |
| **Tài sản để lại** | Prompt template + file CSV do AI sinh |
| **Số đo** | So bộ của AI với bộ người tự viết: **trùng bao nhiêu ca · AI tìm thêm ca nào · AI bỏ sót ca nào** |
| **Minh chứng** | Prompt · hai file CSV (người viết và AI) · bảng đối chiếu 3 cột |
| **Mức tự động** | Semi-automated |

Đây là phần khớp trực tiếp yêu cầu **"Data driven"** của đề: file CSV được nạp thẳng vào
test chạy nhiều bộ dữ liệu.

**Nhóm sẽ ghi dự đoán ra trước khi chạy, và không sửa lại sau:** nhóm dự đoán AI sẽ tìm ra
các ca *0 ngày trễ*, *đúng ngưỡng gia hạn*, *vượt ngưỡng 1 ngày* và *giá trị âm*; nhưng sẽ
**bỏ sót** ca *số ngày trễ cực lớn* (rủi ro tràn số) và ca *hạng thành viên bị để trống*.
Việc ghi dự đoán trước rồi đối chiếu sau chính là phần "thể hiện công sức tìm hiểu" mà đề
yêu cầu — và nếu dự đoán sai, nhóm sẽ báo cáo đúng như vậy.

---

## Kết luận nhóm muốn lớp mang về

| AI làm tốt | AI làm không tốt |
|---|---|
| Sinh khung test nhanh — tiết kiệm thời gian gõ | Quyết định **điều gì đáng được kiểm chứng** |
| Liệt kê các ca biên mà người hay quên | Hiểu nghiệp vụ thật đằng sau mã nguồn |
| Đọc báo cáo coverage dài và chỉ ra chỗ còn thiếu | Biết nhánh nào **cố ý** không test |
| Nhắc các lỗi phong cách test lặp đi lặp lại | Tránh tạo ra test tự xác nhận chính nó |

→ **Vị trí đúng của AI trong chủ đề này: tăng tốc bước gõ, không thay thế bước suy nghĩ.**
Mọi test do AI sinh đều phải qua checklist review của AI-1 trước khi vào repository.

---

## PHẦN B — QUY ƯỚC SỬ DỤNG AI CỦA NHÓM

> Đề cho phép dùng AI nhưng yêu cầu: *"nhóm SV cần phải review kết quả AI phát sinh ra, đảm
> bảo nội dung chính xác, rõ ràng, nhận trách nhiệm trên tài liệu phát sinh"*. Phần này là
> cam kết công khai của nhóm về cách làm điều đó.

### 1. Nhóm dùng AI ở đâu, không dùng ở đâu

| Hạng mục | Có dùng AI? | Dùng như thế nào |
|---|---|---|
| Nội dung lý thuyết (slide, báo cáo) | Có | Soạn bản nháp và gợi ý cấu trúc; **mọi định nghĩa kỹ thuật đều được đối chiếu với tài liệu chính thức** trước khi đưa vào |
| Mã nguồn case study | Có | Sinh bản nháp; nhóm đọc hiểu từng dòng và chạy test rồi mới commit |
| Unit test | Có | Qua demo AI-1, AI-4, với checklist review bắt buộc |
| **Số đo** (coverage, thời gian build) | **Không** | Mọi con số đều do nhóm chạy thật và ghi lại. **Không có con số nào do AI phỏng đoán** |
| **Nhận định về điểm yếu công cụ** | **Không** | Đều xuất phát từ tình huống nhóm tự gặp khi làm |
| **Video demo** | **Không** | Nhóm tự quay, tự thuyết minh |

### 2. Ba cửa review bắt buộc

Mọi nội dung do AI sinh ra phải qua đủ ba cửa trước khi vào repository:

1. **Cửa chạy được** — mã nguồn và test phải chạy xanh trên máy người review; tài liệu phải
   qua được script kiểm tra của nhóm.
2. **Cửa đối chiếu nguồn** — mỗi khẳng định kỹ thuật phải chỉ ra được nguồn chính thức
   (tài liệu của JUnit, changelog của JaCoCo, tài liệu GitHub). Không có nguồn thì xoá, hoặc
   ghi rõ *"nhóm chưa kiểm"*.
3. **Cửa người đứng tên** — commit phải do một thành viên cụ thể tạo. **Người commit chịu
   trách nhiệm về nội dung đó, kể cả phần do AI viết.**

### 3. Những điều nhóm tự quy định là không được làm

- Không dán nguyên kết quả AI vào báo cáo khi chưa đọc lại.
- Không dùng số liệu AI "nhớ" được — mọi so sánh định lượng phải tự đo.
- Không để khoá API xuất hiện ở bất cứ đâu trong repository, slide hay video.
- Không lấy tài liệu hay clip của người khác làm kết quả nộp (yêu cầu "chính chủ" của đề).

### 4. Ghi nhận trong báo cáo cuối

Báo cáo sẽ có một mục riêng ghi rõ: nhóm dùng công cụ AI nào, ở bước nào, và **những lần AI
làm sai mà nhóm phát hiện được**, kèm ví dụ cụ thể. Mục này không nhằm tự phê — nó là bằng
chứng cho thấy nhóm thực sự review chứ không chỉ sao chép.
