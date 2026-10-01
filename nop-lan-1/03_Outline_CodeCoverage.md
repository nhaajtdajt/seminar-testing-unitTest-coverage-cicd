# Outline chi tiết — Phần 2: CODE COVERAGE

**Phụ trách:** TV3 · **Thời lượng dự kiến khi seminar:** ~25 phút

> Luận điểm xuyên suốt của phần này: **coverage đo *mã được chạy qua*, không đo *mã được
> kiểm chứng*.** Nhóm sẽ chứng minh câu đó bằng một demo chạy thật, chứ không chỉ nói.

---

## 1. Lý thuyết & thuật ngữ

| Mục | Sẽ trình bày điều gì | Chứng minh bằng |
|---|---|---|
| 2.1 Coverage là gì, đo cái gì | Công cụ chỉ biết dòng lệnh nào đã được thực thi; nó **không** biết kết quả có được kiểm chứng hay không | Demo đạt 100% độ phủ với **0 assertion** |
| 2.2 Các loại coverage | Line · Statement · Branch · Method · Class · Condition / MC-DC — khác nhau ở chỗ nào | Đoạn `if (a && b)` minh hoạ line 100% nhưng branch chỉ 50% |
| 2.3 Line vs Branch trên code thật | Lấy đúng lớp tính phí của nhóm: một test phủ hết *dòng* nhưng chỉ phủ một nửa *nhánh* | Hai báo cáo đặt cạnh nhau |
| 2.4 Đọc báo cáo JaCoCo | Ý nghĩa màu xanh/vàng/đỏ; cột *Missed Branches*; cột *Cxty* (độ phức tạp chu trình) | Ảnh chụp báo cáo của chính repository nhóm |
| 2.5 Ngưỡng coverage hợp lý | Vì sao "100% coverage" là mục tiêu sai; vì sao nên đặt ngưỡng theo **lớp quan trọng** thay vì theo toàn project | Cấu hình coverage gate thật trong `pom.xml` |
| 2.6 Mutation testing | Mutant · killed · survived · mutation score; vì sao nó đo được điều coverage không đo được | Báo cáo PIT: mutant **sống** dù coverage 100% |

**Thuật ngữ nhóm sẽ chốt cách dịch:** độ phủ dòng · độ phủ câu lệnh · độ phủ nhánh ·
độ phủ điều kiện · coverage gate (cổng chặn theo độ phủ) · mutation testing (kiểm thử đột biến) ·
mutant sống / mutant bị diệt.

## 2. Công cụ

**Công cụ demo sâu: JaCoCo** (Java Code Coverage) — chuẩn de-facto trong hệ sinh thái Maven.

| Chức năng | Goal Maven | Dùng để làm gì |
|---|---|---|
| Gắn agent đo lúc chạy test | `jacoco:prepare-agent` | Chèn bộ đếm vào bytecode khi class được nạp |
| Sinh báo cáo HTML / XML / CSV | `jacoco:report` | Bản HTML cho người đọc; bản XML cho máy đọc (dùng ở demo AI) |
| Chặn build | `jacoco:check` | Fail build khi độ phủ nhánh tụt dưới ngưỡng |

**Nguyên lý hoạt động — phải nói được trên slide:** JaCoCo **không sửa mã nguồn**. Nó chạy
như một *Java agent*: khi JVM nạp một class, agent chèn các *probe* (bộ đếm) vào bytecode,
ghi kết quả ra file nhị phân `jacoco.exec`, rồi bước `report` ghép file đó với bytecode và
mã nguồn để tô màu. Vì làm việc trên bytecode, JaCoCo phải hỗ trợ đúng phiên bản class file
của JDK đang dùng — đây chính là lý do nhóm phải tra changelog để chọn phiên bản phù hợp
với JDK của mình, và cũng là lý do một công cụ cùng loại (Cobertura) bị nhóm loại.

**Công cụ bổ trợ: PIT (mutation testing).** Nhóm dùng PIT **chỉ để chứng minh điểm yếu của
coverage**, không coi nó là công cụ chính của seminar.

**Các công cụ sẽ khảo sát và so sánh** (chi tiết ở `05_KhaoSat_SoSanh_CongCu.md`):
Cobertura · OpenClover · coverage tích hợp trong IntelliJ IDEA · SonarQube (tổng hợp số liệu,
bản thân không tự đo).

## 3. Demo dự kiến

| Mã | Kịch bản | Nội dung | Số đo / minh chứng | Mức tự động |
|---|---|---|---|---|
| **CC-1** | **Cài đặt** | Thêm plugin JaCoCo vào `pom.xml`; chạy `mvn verify`; mở báo cáo HTML; giải thích từng cột | Ảnh chụp báo cáo, log | Fully automated |
| **CC-2** | **Chức năng cơ bản** | Đo coverage khi chỉ có **một** test → xem số; bổ sung test cho các nhánh còn đỏ → đo lại | **Độ phủ nhánh trước/sau**; lưu **cả hai** báo cáo làm minh chứng | Fully automated |
| **CC-3** | **Luồng xử lý phức tạp** | Bật coverage gate: độ phủ nhánh của lớp tính phí phải ≥ 90%; **cố tình xoá một test** → `mvn verify` **fail**; khôi phục → xanh; gắn gate này vào pipeline CI để chặn merge | Log `mvn verify` ở **cả hai** trạng thái; lần chạy CI đỏ và xanh | Fully automated |

## 4. Điểm yếu của công cụ

| Điểm yếu | Cách nhóm sẽ chứng minh |
|---|---|
| **Coverage ≠ chất lượng test** — đây là điểm yếu quan trọng nhất | Viết một test gọi hết mọi nhánh của lớp tính phí mà **không có một assertion nào** → JaCoCo báo 100% độ phủ nhánh. Test này được gắn nhãn riêng để không lẫn vào bộ test thật, và chỉ chạy khi demo |
| **Không phát hiện được assertion yếu** | PIT đổi toán tử `>` thành `>=` trong lớp tính phí → bộ test vẫn xanh → mutant **sống**. JaCoCo hoàn toàn im lặng về chuyện này |
| **Nhánh sinh ra từ lambda / switch pattern đếm khó hiểu** | Viết lại một đoạn bằng `stream().filter()` → báo cáo hiện "thiếu nhánh" ở dòng trông như chỉ có một nhánh; giải thích bằng bytecode được sinh ra |
| **Mã sinh tự động làm loãng số liệu** | Lớp khởi động ứng dụng và các lớp dữ liệu kéo tỉ lệ xuống; phải cấu hình loại trừ → cho thấy con số đổi hẳn sau khi loại trừ, và đặt câu hỏi "con số nào mới là thật" |
| **Số coverage gộp toàn project là vô nghĩa** | Toàn project ~70% nhưng lớp tính phí 100% còn lớp nghiệp vụ 45% → từ đó rút ra: nên đặt gate theo **lớp quan trọng**, không theo trung bình toàn project |
| **Coverage cao có thể khiến nhóm chủ quan** | Trình bày đây là rủi ro về *quy trình*, không phải lỗi kỹ thuật của công cụ: chỉ số đẹp dễ trở thành mục tiêu thay vì thước đo |

## 5. Bài tập áp dụng dự kiến cho lớp

| Bài | Yêu cầu | Gợi ý nhóm sẽ kèm theo |
|---|---|---|
| 1 | Cho sẵn project có coverage 60% — nâng độ phủ **nhánh** lên 90% mà không viết test rỗng | Gợi ý đọc cột *Missed Branches* để biết viết test nào trước |
| 2 | Cho sẵn một bộ test đạt 100% nhưng có 3 test vô nghĩa — tìm ra và giải thích | Gợi ý dấu hiệu: không assertion, assert lại mock, assert hằng số |
| 3 | Cấu hình coverage gate rồi chứng minh nó chặn được một commit làm tụt độ phủ | Gợi ý cấu hình theo lớp thay vì toàn project |

*(Số lượng và mức độ bài tập nhóm xin ý kiến thầy/cô — xem `09_CauHoi_Cho_GV.md`.)*
