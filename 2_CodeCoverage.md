# Phần 2 — CODE COVERAGE (Độ phủ mã nguồn) & công cụ đo
### Tài liệu chuẩn bị seminar · Môn Kiểm thử phần mềm

> **Vị trí trong chuỗi seminar:** Đây là mắt xích **thứ hai**: [Unit Test](1_UnitTest.md) **→ Code Coverage →** [CI/CD](3_CICD.md). Nếu Unit Test là *tấm lưới an toàn* thì Code Coverage là *chiếc đèn soi ra những lỗ thủng của lưới* — chỉ cho ta biết phần code nào chưa được kiểm thử.

---

## Mục lục
1. [Định nghĩa & bản chất](#1-định-nghĩa--bản-chất)
2. [Các loại coverage](#2-các-loại-coverage)
3. [Ví dụ: Line vs Branch (điểm cốt lõi)](#3-ví-dụ-line-vs-branch-điểm-cốt-lõi)
4. [Công cụ đo coverage theo ngôn ngữ](#4-công-cụ-đo-coverage-theo-ngôn-ngữ)
5. [Định dạng báo cáo & cách đọc](#5-định-dạng-báo-cáo--cách-đọc)
6. [Những hiểu lầm quan trọng](#6-những-hiểu-lầm-quan-trọng)
7. [Ngưỡng coverage hợp lý](#7-ngưỡng-coverage-hợp-lý)
8. [Best practices & cạm bẫy](#8-best-practices--cạm-bẫy)
9. [Thuật ngữ & câu hỏi ôn tập](#9-thuật-ngữ--câu-hỏi-ôn-tập)

---

## 1. Định nghĩa & bản chất

**Code coverage (độ phủ mã nguồn)** là một **chỉ số đo lường** cho biết tỉ lệ phần trăm mã nguồn **được thực thi** khi bộ test chạy. Nó trả lời câu hỏi:

> *"Bộ test đã 'chạm' tới bao nhiêu phần của chương trình, và phần nào chưa bao giờ được kiểm thử?"*

**Cơ chế đo:** công cụ coverage "gắn cảm biến" (instrumentation) vào code — chèn các điểm đánh dấu — rồi theo dõi điểm nào được chạy qua trong lúc test. Kết quả tổng hợp thành tỉ lệ phần trăm và danh sách dòng/nhánh chưa được phủ.

**Điều cần hiểu đúng ngay từ đầu:** coverage đo **phạm vi code được chạy qua**, **không** đo chất lượng của các câu assert. Đây là nguồn gốc của hiểu lầm phổ biến nhất (xem [mục 6](#6-những-hiểu-lầm-quan-trọng)).

---

## 2. Các loại coverage

Xếp từ dễ đạt (lỏng) đến khó đạt (chặt):

| Loại | Đo cái gì |
|------|-----------|
| **Statement / Line Coverage** | % *câu lệnh* (hoặc dòng) được thực thi. Mức cơ bản nhất. |
| **Branch / Decision Coverage** | % *nhánh rẽ* được chạy — mỗi hướng true/false của `if`, mỗi `case` của `switch`. Chặt hơn statement. |
| **Function / Method Coverage** | % *hàm/method* được gọi ít nhất một lần. |
| **Condition Coverage** | % *điều kiện con* (từng vế trong `&&`, `\|\|`) đạt cả true lẫn false. |
| **Path / MC-DC Coverage** | Phủ các *đường đi* / tổ hợp điều kiện. Rất chặt; dùng cho hệ thống an toàn trọng yếu (hàng không, y tế) theo chuẩn như DO-178C. |

> **Thứ tự "sức mạnh":** Statement < Branch < Condition < Path. Branch coverage là mức được khuyến nghị theo dõi trong đa số dự án vì cân bằng giữa ý nghĩa và chi phí.

---

## 3. Ví dụ: Line vs Branch (điểm cốt lõi)

Đây là phần **quan trọng nhất và dễ bị hỏi nhất** của chủ đề. Xét hàm:

```python
def phan_loai(diem):
    if diem >= 5:
        return "Đậu"
    else:
        return "Rớt"
```

**Trường hợp chỉ viết 1 test** `phan_loai(8)`:

| Chỉ số | Kết quả | Vì sao |
|--------|---------|--------|
| Statement/Line | gần như 100% | Dòng `if` và `return "Đậu"` đều chạy |
| **Branch** | **chỉ 50%** | Nhánh `else` (→ `"Rớt"`) **chưa bao giờ chạy** |

→ Chỉ test điểm 8, **line coverage có thể rất cao nhưng ta đã bỏ sót hoàn toàn trường hợp "Rớt"**. Phải có **cả** `phan_loai(8)` **và** `phan_loai(3)` mới đạt **branch coverage 100%**.

**Bài học:** đừng chỉ nhìn Line coverage — hãy nhìn **Branch coverage**, vì nó mới lộ ra lỗ hổng "chưa test nhánh ngược lại". Đây là lý do một con số "90% line" nghe thì đẹp nhưng chưa chắc an toàn.

---

## 4. Công cụ đo coverage theo ngôn ngữ

| Ngôn ngữ | Công cụ phổ biến | Lệnh/ghi chú tiêu biểu |
|----------|------------------|------------------------|
| **Java** | **JaCoCo** | Chuẩn de-facto; tích hợp Maven/Gradle; xuất HTML & XML |
| **Python** | **coverage.py** (thường qua `pytest-cov`) | `pytest --cov=my_module` |
| **JavaScript/TS** | **Istanbul / nyc** | Jest tích hợp sẵn: `jest --coverage` |
| **C/C++** | **gcov / lcov** | Đi kèm trình biên dịch GCC |
| **C#/.NET** | **Coverlet** | Tích hợp `dotnet test` |
| **Ruby** | **SimpleCov** | — |
| **Go** | `go test -cover` | Tích hợp sẵn trong toolchain Go |

**Nền tảng tổng hợp/hiển thị:** SonarQube, Codecov, Coveralls — nhận báo cáo từ các công cụ trên và hiển thị xu hướng coverage theo thời gian, chặn PR nếu coverage giảm.

---

## 5. Định dạng báo cáo & cách đọc

**Các định dạng báo cáo thường gặp** — quan trọng vì công cụ [CI/CD](3_CICD.md) và SonarQube cần đọc được:
- **Cobertura XML**, **JaCoCo XML**, **LCOV** (cho máy/CI đọc)
- **HTML** (cho con người xem trực quan — tô màu từng dòng)

**Một báo cáo điển hình** liệt kê từng file kèm tỉ lệ và các dòng chưa phủ:

```
File                    Lines    Branch   Dòng chưa phủ
──────────────────────────────────────────────────────
calculator.py           100%     100%     —
user_service.py          85%      70%     42–45 (nhánh xử lý lỗi)
payment.py               40%      25%     phần lớn chưa test   ⚠
──────────────────────────────────────────────────────
TỔNG                     78%      68%
```

**Cách đọc đúng:** giá trị của báo cáo không nằm ở con số tổng, mà ở chỗ nó **chỉ ra vùng rủi ro**. Ở ví dụ trên, `payment.py` là module quan trọng (thanh toán) nhưng coverage thấp nhất → đây chính là nơi cần ưu tiên bổ sung test. Coverage là một **tấm bản đồ**, không phải một tấm huy chương.

---

## 6. Những hiểu lầm quan trọng

Phần dễ bị giảng viên hỏi nhất — cần nắm chắc:

1. **Coverage cao KHÔNG có nghĩa là test tốt.**
   Một test có thể *chạy qua* một dòng code mà **không assert gì có ý nghĩa** về dòng đó. Code được "phủ" nhưng hành vi sai vẫn không bị phát hiện.

2. **100% coverage KHÔNG có nghĩa là không còn bug.**
   Coverage không bắt được: lỗi ở các tổ hợp điều kiện chưa test, lỗi trường hợp biên, lỗi tương tranh (race condition), lỗi do đầu vào ngoài dự kiến.

3. **Line coverage 100% vẫn có thể bỏ sót nhánh** (xem [mục 3](#3-ví-dụ-line-vs-branch-điểm-cốt-lõi)). Luôn xem thêm branch coverage.

**Phát biểu đúng bản chất:** *coverage là điều kiện cần, không phải điều kiện đủ.* Code không được phủ thì chắc chắn có rủi ro chưa kiểm soát; nhưng code được phủ 100% vẫn có thể sai nếu các assert hời hợt.

> **Câu chốt để nhớ:** *"Coverage cho biết bạn đã test ở ĐÂU, không cho biết bạn test TỐT hay không."*

---

## 7. Ngưỡng coverage hợp lý

- **Không có con số "vàng"** cho mọi dự án. Mức **70–80%** thường được coi là hợp lý trong thực tế.
- **Theo đuổi 100% bằng mọi giá** dễ dẫn tới *test giả tạo* (assert yếu, test rỗng) → tốn công mà không tăng chất lượng thật.
- **Cách dùng đúng:** đặt một **ngưỡng tối thiểu** làm "quality gate" trong [CI](3_CICD.md) (ví dụ *branch coverage ≥ 70%*), và tập trung coverage vào **những module quan trọng/rủi ro cao** thay vì dàn đều.
- **Theo dõi xu hướng** quan trọng hơn con số tuyệt đối: coverage *không được giảm* khi thêm code mới — đây là quy tắc nhiều nhóm áp dụng (ví dụ qua Codecov/SonarQube).

---

## 8. Best practices & cạm bẫy

### Thực hành tốt
- Theo dõi **branch coverage**, không chỉ line.
- Đưa coverage vào [CI](3_CICD.md) như một **quality gate** tự động (ngưỡng tối thiểu).
- Ưu tiên tăng coverage ở **module rủi ro cao** (thanh toán, bảo mật, logic nghiệp vụ phức tạp).
- Dùng báo cáo HTML để **tìm đúng dòng chưa phủ** và viết test bổ sung có mục tiêu.

### Cạm bẫy thường gặp
- **Chạy theo con số** → đẻ ra test rỗng / assert hời hợt. *Coverage cao ≠ chất lượng cao.*
- **Chỉ nhìn line coverage** → ảo tưởng an toàn, bỏ sót nhánh.
- **Đặt ngưỡng 100% cứng nhắc** → nhóm viết test đối phó, lãng phí công sức.
- **Bỏ qua coverage của test chính nó hoặc code generated** làm méo con số (nên cấu hình loại trừ hợp lý).

---

## 9. Thuật ngữ & câu hỏi ôn tập

### Thuật ngữ
| Thuật ngữ | Nghĩa ngắn |
|-----------|-----------|
| Code coverage | % code được thực thi khi chạy test |
| Statement/Line coverage | % dòng lệnh được chạy |
| Branch coverage | % nhánh rẽ (if/else, case) được chạy |
| Condition coverage | % điều kiện con đạt cả true/false |
| Path / MC-DC | Phủ đường đi/tổ hợp điều kiện (mức chặt nhất) |
| Instrumentation | "Gắn cảm biến" vào code để đo coverage |
| Quality gate | Ngưỡng chất lượng bắt buộc vượt qua trong CI |
| JaCoCo / coverage.py / Istanbul | Công cụ coverage cho Java / Python / JS |

### Câu hỏi ôn tập
1. Code coverage đo cái gì — và **không** đo cái gì?
2. Vì sao line coverage 100% vẫn có thể bỏ sót lỗi? Loại coverage nào khắc phục?
3. "100% coverage nghĩa là không còn bug" — đúng hay sai? Giải thích.
4. Kể tên công cụ coverage cho Java, Python, JavaScript.
5. Ngưỡng coverage bao nhiêu là hợp lý, và vì sao không nên ép 100%?
6. Vì sao nên theo dõi *xu hướng* coverage hơn là con số tuyệt đối tại một thời điểm?

### Tài liệu tham khảo
- JaCoCo — jacoco.org · coverage.py — coverage.readthedocs.io · Istanbul — istanbul.js.org
- Martin Fowler — *TestCoverage* (martinfowler.com)
- SonarQube Documentation — docs.sonarsource.com

---
*Phần trước ← [Phần 1 — Unit Test](1_UnitTest.md) · Phần tiếp theo → [Phần 3 — CI/CD](3_CICD.md)*
