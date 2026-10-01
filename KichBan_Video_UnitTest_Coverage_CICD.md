# KỊCH BẢN VIDEO — Unit Test · Code Coverage · CI/CD
### Video explainer cho seminar môn Kiểm thử phần mềm

> **Trạng thái:** Đây là **kịch bản (storyboard)** để duyệt nội dung. Chưa dựng video/artifact. Sau khi chốt kịch bản sẽ chuyển thành artifact HTML động hoặc video.

---

## 1. Thông tin chung

| Hạng mục | Nội dung |
|---|---|
| **Thời lượng mục tiêu** | ~5 phút (300 giây) — có thể rút còn 3 phút bằng cách lược Act 2 |
| **Phong cách hình ảnh** | Phẳng (flat/minimal), sạch, màu chủ đạo xanh dương + xám, điểm nhấn xanh lá (pass) / đỏ (fail) |
| **Tông giọng lời bình** | Thân thiện, rõ ràng, giải thích như một đàn anh hướng dẫn — không hàn lâm khô khan |
| **Đối tượng** | Sinh viên CNTT đã biết lập trình cơ bản, chưa rành quy trình kiểm thử tự động |
| **Thông điệp xuyên suốt** | Ba chủ đề là ba mắt xích của **một dây chuyền đảm bảo chất lượng tự động** |
| **Nhạc nền** | Nhẹ, tiết tấu vừa (lo-fi/corporate), giảm âm khi có lời bình |
| **Text trên màn hình** | Tiếng Việt, font sans-serif đậm, tối đa 1–2 dòng/khung |

**Cấu trúc 5 hồi (act):**

| Hồi | Nội dung | Mốc thời gian |
|---|---|---|
| Act 0 | Mở đầu — đặt vấn đề | 0:00 – 0:25 |
| Act 1 | Unit Test | 0:25 – 1:35 |
| Act 2 | Code Coverage | 1:35 – 2:50 |
| Act 3 | CI/CD | 2:50 – 3:55 |
| Act 4 | Jenkins — ghép cả ba | 3:55 – 4:40 |
| Act 5 | Tổng kết | 4:40 – 5:00 |

---

## 2. Bảng phân cảnh chi tiết

Ký hiệu: **HÌNH** = những gì hiển thị trên màn hình · **LỜI** = lời bình (voiceover) · **ANIM** = gợi ý chuyển động.

---

### ACT 0 — MỞ ĐẦU (0:00 – 0:25)

**Cảnh 1 — Hook đặt vấn đề** · ⏱ 0:00 – 0:25

- **HÌNH:** Màn hình chia 5 ô nhỏ, mỗi ô là một lập trình viên đang gõ code trên cùng một dự án. Ở giữa hiện dấu hỏi lớn.
- **TEXT:** "5 người cùng sửa 1 dự án..."
- **LỜI:** *"Hãy tưởng tượng nhóm bạn có 5 người, mỗi ngày cùng sửa một dự án. Câu hỏi đặt ra: làm sao biết đoạn code bạn vừa viết hôm nay không làm hỏng tính năng của người khác — mà không phải ngồi kiểm tra lại bằng tay toàn bộ chương trình?"*
- **ANIM:** Năm ô code xuất hiện lần lượt (stagger). Dấu hỏi phóng to, rung nhẹ. Chuyển cảnh: dấu hỏi "nổ" thành tiêu đề.
- **TEXT chốt:** "Câu trả lời: KIỂM THỬ TỰ ĐỘNG" → hiện tiêu đề video: *Unit Test · Code Coverage · CI/CD*.

---

### ACT 1 — UNIT TEST (0:25 – 1:35)

**Cảnh 2 — Unit test là gì** · ⏱ 0:25 – 0:50

- **HÌNH:** Một hàm `add(a, b)` nằm giữa màn hình. Một "robot test" nhỏ cầm kính lúp soi vào hàm, đưa vào `2, 3` → nhận ra `5` → hiện dấu ✓ xanh.
- **TEXT:** "Unit Test = kiểm thử MỘT đơn vị nhỏ nhất, độc lập"
- **LỜI:** *"Mắt xích đầu tiên là Unit Test — kiểm thử đơn vị. Nó kiểm tra đơn vị nhỏ nhất của chương trình, thường là một hàm, một cách độc lập. Cho đầu vào, kiểm tra xem đầu ra có đúng như mong đợi không. Nhanh, tự động, và khi sai thì chỉ ngay hàm nào hỏng."*
- **ANIM:** Số `2` và `3` chạy vào hàm; kết quả `5` bật ra; dấu ✓ nảy lên.

**Cảnh 3 — Cấu trúc AAA** · ⏱ 0:50 – 1:10

- **HÌNH:** Khối code test hiện ra, tô sáng 3 phần theo màu: Arrange (xanh dương), Act (cam), Assert (xanh lá).
  ```
  Calculator calc = new Calculator();   // Arrange
  int result = calc.add(2, 3);          // Act
  assertEquals(5, result);              // Assert
  ```
- **TEXT:** "Công thức viết test: Arrange → Act → Assert"
- **LỜI:** *"Mọi unit test đều theo một công thức ba bước, gọi tắt là AAA: Arrange — chuẩn bị dữ liệu; Act — gọi hàm cần kiểm thử; và Assert — so sánh kết quả thực tế với kết quả mong đợi. Nắm công thức này là viết được test ở bất kỳ ngôn ngữ nào."*
- **ANIM:** Ba dòng sáng lên lần lượt theo lời đọc; nhãn Arrange/Act/Assert trượt vào bên phải mỗi dòng.

**Cảnh 4 — Một tư duy, nhiều ngôn ngữ** · ⏱ 1:10 – 1:25

- **HÌNH:** Ba thẻ (card) nằm ngang: Java (JUnit) · Python (pytest) · JavaScript (Jest), cùng tô sáng cấu trúc AAA giống nhau.
- **TEXT:** "Khác ngôn ngữ — cùng tư duy"
- **LỜI:** *"Dù là JUnit của Java, pytest của Python hay Jest của JavaScript — cú pháp khác nhau nhưng tư duy y hệt. Học một cái là hiểu được tất cả."*
- **ANIM:** Ba thẻ lật (flip) lần lượt; khung AAA nhấp nháy đồng bộ ở cả ba.

**Cảnh 5 — Mock & nguyên tắc FIRST** · ⏱ 1:25 – 1:35

- **HÌNH:** Hàm cần test nối tới một "Database" thật (biểu tượng trụ dữ liệu). Database bị gạch mờ đi, thay bằng một "hình nộm" (mock) dán nhãn Mock.
- **TEXT:** "Phụ thuộc ngoài → thay bằng Mock/Stub · Test phải: Fast, Isolated, Repeatable..."
- **LỜI:** *"Khi hàm phụ thuộc database hay mạng, ta thay chúng bằng đồ giả — gọi là mock hoặc stub — để test luôn nhanh và ổn định. Giống như test túi khí xe hơi, ta dùng hình nộm chứ không lao xe thật vào tường."*
- **ANIM:** Trụ database chuyển xám + mờ; mock trượt vào thay thế; 5 chữ FIRST hiện thành một hàng icon nhỏ.

---

### ACT 2 — CODE COVERAGE (1:35 – 2:50)

**Cảnh 6 — Lưới có lỗ thủng** · ⏱ 1:35 – 1:55

- **HÌNH:** Unit test được vẽ như một tấm lưới an toàn hứng phía dưới code. Zoom vào thấy lưới có vài lỗ thủng.
- **TEXT:** "Có test rồi... nhưng đã test ĐỦ chưa?"
- **LỜI:** *"Nhưng viết test xong, một câu hỏi mới xuất hiện: liệu bộ test đã phủ hết code chưa, hay vẫn còn những chỗ chưa ai kiểm tra? Đó là lúc cần đến Code Coverage — độ phủ mã nguồn."*
- **ANIM:** Lưới xuất hiện; camera zoom lộ các lỗ thủng phát sáng đỏ.

**Cảnh 7 — Coverage là gì** · ⏱ 1:55 – 2:10

- **HÌNH:** Một file code, các dòng được tô: xanh lá = đã chạy khi test, đỏ = chưa chạy. Thanh phần trăm chạy lên "78%".
- **TEXT:** "Code Coverage = % code ĐƯỢC CHẠY khi test"
- **LỜI:** *"Code coverage đo tỉ lệ phần trăm dòng code thực sự được chạy qua khi bộ test chạy. Dòng xanh là đã được kiểm thử, dòng đỏ là chưa. Nó chính là tấm bản đồ chỉ ra chỗ nào còn bỏ ngỏ."*
- **ANIM:** Các dòng đổi màu lần lượt từ trên xuống; thanh % tăng dần có hiệu ứng đếm số.

**Cảnh 8 — Line vs Branch (điểm cốt lõi)** · ⏱ 2:10 – 2:35

- **HÌNH:** Hàm `phan_loai(diem)` có if/else. Chỉ chạy test `diem = 8` → nhánh "Đậu" sáng xanh, nhánh "Rớt" vẫn đỏ, dù thanh Line coverage hiện 100%.
  ```
  if diem >= 5:  return "Đậu"   ← đã test (diem=8)
  else:          return "Rớt"   ← CHƯA test!
  ```
- **TEXT:** "Line 100% VẪN có thể sót nhánh → phải xem BRANCH coverage"
- **LỜI:** *"Và đây là điều quan trọng nhất về coverage. Nếu chỉ test điểm 8, dòng lệnh có thể phủ tới 100%, nhưng ta đã bỏ sót hoàn toàn trường hợp 'Rớt'. Phải test cả điểm 8 lẫn điểm 3 mới thực sự an toàn. Vì vậy đừng chỉ nhìn Line coverage — hãy nhìn Branch coverage, độ phủ nhánh."*
- **ANIM:** Nhánh else nhấp nháy đỏ cảnh báo; khi thêm test `diem=3`, nhánh else chuyển xanh, thanh Branch nhảy từ 50% lên 100%.

**Cảnh 9 — Cảnh báo & công cụ** · ⏱ 2:35 – 2:50

- **HÌNH:** Câu khẩu hiệu lớn giữa màn hình; bên dưới là logo/tên công cụ: JaCoCo (Java), coverage.py (Python), Istanbul (JS).
- **TEXT:** "Coverage cho biết bạn test ở ĐÂU — không nói test TỐT hay không"
- **LỜI:** *"Nhưng nhớ: coverage cao không có nghĩa là test tốt. Nó cho biết bạn đã test ở đâu, chứ không cho biết bạn test có kỹ hay không. 70 đến 80% thường là hợp lý. Mỗi ngôn ngữ có công cụ riêng: JaCoCo cho Java, coverage.py cho Python, Istanbul cho JavaScript."*
- **ANIM:** Khẩu hiệu gõ chữ (typewriter); ba tên công cụ trượt lên từ dưới.

---

### ACT 3 — CI/CD (2:50 – 3:55)

**Cảnh 10 — Vấn đề: ai chạy test?** · ⏱ 2:50 – 3:10

- **HÌNH:** Lập trình viên mệt mỏi phải bấm "chạy test" thủ công mỗi lần; một lần quên → bug lọt ra production (biểu tượng server bốc khói).
- **TEXT:** "Có test + coverage... nhưng CHẠY TAY thì sẽ có ngày QUÊN"
- **LỜI:** *"Giờ ta có test, có coverage. Nhưng nếu lần nào cũng phải chạy bằng tay thì sớm muộn cũng có ngày quên. Mắt xích thứ ba sẽ giải quyết việc đó: CI/CD — tự động hóa toàn bộ dây chuyền."*
- **ANIM:** Nhân vật bấm nút lặp lại; đến lần "quên", server đỏ lên, hiện chữ "Bug lọt production!".

**Cảnh 11 — CI vs CD vs CD** · ⏱ 3:10 – 3:30

- **HÌNH:** Ba khối nối tiếp nhau trượt vào:
  - **CI** (Continuous Integration): "Push code → tự động Build + Test"
  - **CD** (Continuous Delivery): "+ đóng gói sẵn sàng — người BẤM NÚT deploy"
  - **CD** (Continuous Deployment): "+ tự động deploy luôn"
- **TEXT:** "Delivery vs Deployment khác nhau ĐÚNG MỘT bước bấm nút"
- **LỜI:** *"CI — tích hợp liên tục — tự động build và chạy test mỗi lần push code. Continuous Delivery thì luôn giữ sản phẩm sẵn sàng phát hành, nhưng người bấm nút deploy. Còn Continuous Deployment thì deploy tự động luôn. Hai chữ CD khác nhau đúng một bước: ai bấm nút — người hay máy."*
- **ANIM:** Ba khối xếp chồng; ở khối Delivery hiện bàn tay bấm nút; ở Deployment nút tự sáng không cần tay.

**Cảnh 12 — Pipeline chạy như dây chuyền** · ⏱ 3:30 – 3:55

- **HÌNH:** Một băng chuyền ngang với các trạm: **Checkout → Build → Test → Coverage → Quality Gate → Deploy**. Một "gói code" chạy qua từng trạm, mỗi trạm sáng xanh khi pass.
- **TEXT:** "Unit Test & Coverage = QUALITY GATE (trạm gác chất lượng)"
- **LỜI:** *"Tất cả được xâu thành một pipeline — dây chuyền tự động. Code chạy qua từng trạm: lấy code, build, chạy test, đo coverage, rồi tới trạm gác chất lượng. Nếu test fail hoặc coverage dưới ngưỡng, pipeline đỏ và dừng lại — không cho deploy. Đây chính là chỗ cả ba chủ đề gặp nhau."*
- **ANIM:** Gói code trượt qua từng trạm; đến Quality Gate thử một lần FAIL (đỏ, rào chắn hạ xuống), rồi PASS (xanh, rào mở, đi tiếp tới Deploy).

---

### ACT 4 — JENKINS: GHÉP CẢ BA (3:55 – 4:40)

**Cảnh 13 — Jenkins vận hành dây chuyền** · ⏱ 3:55 – 4:15

- **HÌNH:** Nhân vật "bác Jenkins" (biểu tượng ông quản gia của Jenkins) đứng điều khiển băng chuyền ở cảnh trước. Sơ đồ Controller ở giữa, toả ra 3 Agent (Linux/Windows/macOS).
- **TEXT:** "Jenkins = máy chủ tự động hoá CI/CD · Controller điều phối, Agent thực thi"
- **LỜI:** *"Và người vận hành dây chuyền đó, một trong những công cụ phổ biến nhất, là Jenkins — máy chủ tự động hóa mã nguồn mở. Một Controller đóng vai bộ não điều phối, còn các Agent là nơi thực sự chạy build và test — thậm chí song song trên nhiều hệ điều hành."*
- **ANIM:** Controller phát tín hiệu tới 3 agent; mỗi agent chạy một thanh tiến trình.

**Cảnh 14 — Jenkinsfile: Pipeline as Code** · ⏱ 4:15 – 4:40

- **HÌNH:** File `Jenkinsfile` hiện ra, các `stage` tô sáng tương ứng với các trạm băng chuyền ở Act 3; dòng `minimumBranchCoverage: '70'` được khoanh đỏ nổi bật.
  ```groovy
  stage('Unit Test') { steps { sh 'mvn test' } }
  stage('Coverage')  { steps { sh 'mvn jacoco:report' }
      post { always { jacoco(minimumBranchCoverage: '70') } } }
  stage('Deploy')    { when { branch 'main' } ... }
  ```
- **TEXT:** "Cả pipeline nằm trong 1 file Jenkinsfile — quản lý version như code"
- **LỜI:** *"Toàn bộ dây chuyền được viết thành một file text tên Jenkinsfile, đặt ngay trong dự án và quản lý phiên bản như code. Nhìn vào đây thấy rõ cả ba mắt xích: stage Unit Test chạy kiểm thử, stage Coverage đặt ngưỡng 70% làm trạm gác, và stage Deploy chỉ chạy khi mọi thứ xanh."*
- **ANIM:** Mỗi `stage` trong file nối đường sáng tới trạm tương ứng trên băng chuyền; khoanh đỏ dòng ngưỡng coverage.

---

### ACT 5 — TỔNG KẾT (4:40 – 5:00)

**Cảnh 15 — Ba mắt xích, một dây chuyền** · ⏱ 4:40 – 5:00

- **HÌNH:** Ba biểu tượng ghép thành chuỗi mắt xích khoá vào nhau:
  🛡️ **Unit Test** — "code chạy đúng không?" → 🔦 **Coverage** — "đã test tới đâu?" → 🤖 **CI/CD (Jenkins)** — "tự động chạy mỗi lần đổi code".
- **TEXT:** "Unit Test xây lưới · Coverage soi lỗ hổng · CI/CD tự động kéo lưới ra kiểm tra"
- **LỜI:** *"Tóm lại: Unit Test xây lưới an toàn, Code Coverage soi ra lỗ hổng của lưới, và CI/CD — với Jenkins — tự động kéo lưới ra kiểm tra mỗi lần có người đổi code. Ba mắt xích của một dây chuyền đảm bảo chất lượng tự động. Thiếu một mắt xích, cả hệ thống yếu đi."*
- **ANIM:** Ba icon nối thành chuỗi, khoá "tách" lại với nhau; màn kết hiện tên nhóm + môn học + lời cảm ơn.
- **TEXT kết:** "Nhóm [GroupID] — Kiểm thử phần mềm CQ2023/31 — Cảm ơn đã theo dõi!"

---

## 3. Ghi chú sản xuất (để dựng về sau)

- **Chuyển cảnh chủ đạo:** trượt ngang (slide) theo hướng "dây chuyền đi từ trái sang phải" — củng cố ẩn dụ pipeline.
- **Bảng màu gợi ý:** nền `#0F172A` (xanh đậm) hoặc trắng `#FFFFFF`; xanh dương `#2563EB` (chủ đạo), xanh lá `#16A34A` (pass), đỏ `#DC2626` (fail), xám `#64748B` (phụ).
- **Motion nhất quán:** dùng easing mượt (ví dụ `power2.out` của GSAP) cho mọi phần tử; thời lượng chuyển động 0.4–0.6s.
- **Phụ đề:** nên có phụ đề tiếng Việt khớp lời bình (tăng khả năng tiếp cận + phòng khi chiếu không loa).
- **Khả năng rút gọn:** nếu cần bản 3 phút → gộp Cảnh 4 vào Cảnh 3, lược Cảnh 9, rút Act 4 còn một cảnh.
- **Hướng triển khai đã chọn:** dựng thành **artifact HTML tương tác/động** (băng chuyền pipeline chạy từng stage theo click/scroll) thay cho file video — chiếu trực tiếp khi thuyết trình.

---

## 4. Bảng tóm tắt thời lượng & lời bình (bản rút gọn để thu âm)

| Cảnh | ⏱ | Ý chính của lời bình |
|---|---|---|
| 1 | 0:00 | 5 người cùng sửa code → cần kiểm thử tự động |
| 2 | 0:25 | Unit test = kiểm thử 1 đơn vị nhỏ, độc lập |
| 3 | 0:50 | Công thức AAA: Arrange – Act – Assert |
| 4 | 1:10 | Khác ngôn ngữ, cùng tư duy (JUnit/pytest/Jest) |
| 5 | 1:25 | Mock/Stub thay phụ thuộc ngoài; nguyên tắc FIRST |
| 6 | 1:35 | Test xong — đã đủ chưa? → cần coverage |
| 7 | 1:55 | Coverage = % code được chạy khi test |
| 8 | 2:10 | Line 100% vẫn sót nhánh → xem Branch coverage |
| 9 | 2:35 | Coverage cao ≠ test tốt; JaCoCo/coverage.py/Istanbul |
| 10 | 2:50 | Chạy test bằng tay sẽ có ngày quên → cần CI/CD |
| 11 | 3:10 | CI vs Delivery vs Deployment (khác 1 bước bấm nút) |
| 12 | 3:30 | Pipeline: test & coverage là quality gate |
| 13 | 3:55 | Jenkins: Controller điều phối, Agent thực thi |
| 14 | 4:15 | Jenkinsfile — pipeline as code, ngưỡng coverage 70% |
| 15 | 4:40 | Ba mắt xích, một dây chuyền chất lượng tự động |

---

*Chốt kịch bản này xong, bước tiếp theo là dựng artifact HTML động theo đúng 15 cảnh trên.*
