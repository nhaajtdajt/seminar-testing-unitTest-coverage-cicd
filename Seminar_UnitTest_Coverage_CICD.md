# Unit Test · Code Coverage · CI/CD
### Tài liệu chuẩn bị kiến thức — Môn Kiểm thử phần mềm

> **Mục đích tài liệu:** Giúp người đọc nắm vững bản chất, thuật ngữ, công cụ và cách vận dụng của ba chủ đề Unit Test, Code Coverage và CI/CD (trọng tâm Jenkins). Tài liệu viết theo hướng *học để hiểu sâu và trả lời được câu hỏi*, không phải theo hướng trình chiếu.

---

## Mục lục
1. [Bối cảnh: ba chủ đề liên hệ với nhau thế nào](#1-bối-cảnh-ba-chủ-đề-liên-hệ-với-nhau-thế-nào)
2. [Unit Test](#2-unit-test)
3. [Code Coverage](#3-code-coverage)
4. [CI/CD](#4-cicd)
5. [Jenkins](#5-jenkins)
6. [Tích hợp cả ba trong một pipeline](#6-tích-hợp-cả-ba-trong-một-pipeline)
7. [Best practices & cạm bẫy](#7-best-practices--cạm-bẫy)
8. [Thuật ngữ cần nhớ](#8-thuật-ngữ-cần-nhớ)
9. [Câu hỏi ôn tập & tài liệu tham khảo](#9-câu-hỏi-ôn-tập--tài-liệu-tham-khảo)

---

## 1. Bối cảnh: ba chủ đề liên hệ với nhau thế nào

Trong phát triển phần mềm hiện đại, chất lượng không được đảm bảo bằng cách "kiểm tra thủ công ở cuối dự án" mà bằng một hệ thống kiểm thử **tự động, liên tục**. Ba chủ đề của seminar chính là ba lớp của hệ thống đó, bổ sung cho nhau:

- **Unit Test** trả lời câu hỏi *"từng đơn vị code có chạy đúng không?"*. Đây là loại kiểm thử ở mức thấp nhất, nhanh nhất và được viết nhiều nhất.
- **Code Coverage** trả lời câu hỏi *"bộ unit test đã kiểm tra tới đâu, còn bỏ sót phần nào?"*. Nó đo lường mức độ đầy đủ của test, giúp phát hiện vùng code chưa được bảo vệ.
- **CI/CD** trả lời câu hỏi *"làm sao để test và kiểm tra coverage được chạy tự động mỗi khi code thay đổi, và đưa sản phẩm tới người dùng một cách an toàn?"*. Nó là lớp tự động hóa bao bọc hai lớp trên.

Mối quan hệ nhân quả:

- Nếu **không có unit test**, ta không có cơ sở tự động để biết code đúng hay sai.
- Nếu **có test nhưng không đo coverage**, ta không biết test đã đủ hay còn lỗ hổng lớn.
- Nếu **có cả test và coverage nhưng chạy thủ công**, sớm muộn con người sẽ quên chạy, hoặc chạy không nhất quán giữa các máy.

Vì vậy, một quy trình trưởng thành sẽ kết hợp cả ba: viết unit test → đo coverage như một tiêu chí chất lượng → đưa cả hai vào pipeline CI/CD để chạy tự động.

---

## 2. Unit Test

### 2.1. Định nghĩa

**Unit test (kiểm thử đơn vị)** là việc kiểm thử **đơn vị nhỏ nhất, độc lập** của phần mềm — thông thường là một hàm (function) hoặc một phương thức (method) — nhằm xác minh rằng với một đầu vào xác định, đơn vị đó cho ra đầu ra đúng như mong đợi.

Ba đặc điểm cốt lõi của unit test:

1. **Nhỏ (granular):** kiểm thử một đơn vị logic, không phải cả luồng nghiệp vụ.
2. **Độc lập (isolated):** đơn vị được tách khỏi các phụ thuộc bên ngoài (database, mạng, file, thời gian...) bằng kỹ thuật test double.
3. **Tự động (automated):** chạy bằng framework, tự kết luận đúng/sai, không cần con người quan sát.

### 2.2. Vị trí trong kim tự tháp kiểm thử (Test Pyramid)

Kim tự tháp kiểm thử (Mike Cohn) mô tả tỉ lệ hợp lý giữa các loại test:

- **Unit test (đáy):** số lượng nhiều nhất. Nhanh (mili-giây), rẻ, khi fail thì chỉ rõ chính xác hàm nào sai.
- **Integration test (giữa):** kiểm thử nhiều module/thành phần ghép thật với nhau (ví dụ service + database). Số lượng vừa phải, chậm hơn.
- **End-to-End / UI test (đỉnh):** kiểm thử toàn hệ thống từ góc nhìn người dùng. Ít nhất, chậm nhất, đắt nhất, dễ "giòn" (flaky).

Lý do unit test nên chiếm số lượng lớn nhất: chúng cho **phản hồi nhanh** và **khoanh vùng lỗi chính xác**. Nếu một integration test fail, nguyên nhân có thể nằm ở hàng chục chỗ; nếu một unit test fail, ta biết ngay đơn vị nào hỏng.

### 2.3. Nguyên tắc FIRST — tiêu chí của một unit test tốt

| Chữ | Nguyên tắc | Giải thích chi tiết |
|-----|-----------|---------------------|
| **F** | Fast (nhanh) | Một unit test phải chạy trong mili-giây. Toàn bộ bộ test hàng nghìn ca nên hoàn tất trong vài giây để lập trình viên chạy thường xuyên mà không ngại chờ. |
| **I** | Isolated (độc lập) | Không phụ thuộc vào test khác, không phụ thuộc thứ tự chạy, không dùng chung trạng thái. Mỗi test tự chuẩn bị và tự dọn dẹp dữ liệu của mình. |
| **R** | Repeatable (lặp lại được) | Chạy nhiều lần, ở nhiều máy, nhiều thời điểm đều cho cùng kết quả. Không phụ thuộc yếu tố ngẫu nhiên, giờ hệ thống, hay mạng. |
| **S** | Self-validating (tự kiểm chứng) | Test tự khẳng định pass/fail qua các câu lệnh assert, không cần người đọc log so sánh bằng mắt. |
| **T** | Timely (đúng lúc) | Viết test sớm — lý tưởng là ngay khi viết code, hoặc trước khi viết code (theo TDD). Test viết muộn thường bị bỏ hoặc viết qua loa. |

### 2.4. Cấu trúc AAA (Arrange – Act – Assert)

Hầu hết unit test được tổ chức theo ba bước rõ ràng:

- **Arrange (chuẩn bị):** thiết lập dữ liệu đầu vào, khởi tạo đối tượng, cấu hình các test double cần thiết.
- **Act (thực thi):** gọi đúng một hàm/method đang được kiểm thử.
- **Assert (kiểm chứng):** so sánh kết quả thực tế với kết quả mong đợi.

Việc tách rõ ba bước giúp test dễ đọc và dễ bảo trì. Một biến thể tương đương là **Given – When – Then** (thường dùng trong BDD).

### 2.5. Ví dụ minh họa (đa ngôn ngữ)

Cùng một bài toán — kiểm thử hàm cộng hai số — được viết trong ba hệ sinh thái phổ biến. Điểm đáng chú ý: cú pháp và framework khác nhau nhưng **tư duy AAA giống hệt nhau**.

**Java — JUnit 5:**

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class CalculatorTest {
    @Test
    void add_haiSoDuong_traVeTongDung() {
        Calculator calc = new Calculator();   // Arrange
        int result = calc.add(2, 3);          // Act
        assertEquals(5, result);              // Assert
    }
}
```

**Python — pytest:**

```python
def test_add_hai_so_duong_tra_ve_tong_dung():
    calc = Calculator()         # Arrange
    result = calc.add(2, 3)     # Act
    assert result == 5          # Assert
```

**JavaScript — Jest:**

```javascript
test('add hai số dương trả về tổng đúng', () => {
  const calc = new Calculator();   // Arrange
  const result = calc.add(2, 3);   // Act
  expect(result).toBe(5);          // Assert
});
```

### 2.6. Test Double: Mock, Stub và các biến thể

Trong thực tế, hàm cần test thường phụ thuộc vào thành phần bên ngoài (database, web service, hệ thống file...). Nếu để test gọi thật những thứ này, test sẽ chậm và không ổn định — vi phạm FIRST. Giải pháp là thay chúng bằng **test double** (đối tượng giả lập đóng vai thay thế).

Các loại test double thường gặp (phân loại theo Gerard Meszaros / Martin Fowler):

- **Dummy:** đối tượng truyền vào cho đủ tham số nhưng không được dùng.
- **Stub:** cung cấp sẵn câu trả lời cố định cho các lời gọi trong test (ví dụ: "khi gọi `findById(1)` thì trả về user mẫu"). Dùng để *điều khiển đầu vào gián tiếp*.
- **Mock:** giống stub nhưng còn **ghi nhận và kiểm chứng cách nó bị gọi** (gọi đúng hàm nào, bao nhiêu lần, với tham số gì). Dùng để *kiểm chứng hành vi (behavior verification)*.
- **Fake:** cài đặt đơn giản có hoạt động thật nhưng không dùng được cho production (ví dụ database trong bộ nhớ).
- **Spy:** bọc đối tượng thật và ghi lại thông tin về cách nó được gọi.

Ví dụ với **Java + Mockito** — thay repository thật bằng đối tượng giả:

```java
UserRepository repo = mock(UserRepository.class);      // tạo mock
when(repo.findById(1)).thenReturn(new User("An"));     // stub hành vi trả về

UserService service = new UserService(repo);
assertEquals("An", service.getUserName(1));            // kiểm chứng kết quả

verify(repo).findById(1);   // kiểm chứng hành vi: repo đã được gọi đúng 1 lần
```

Phân biệt quan trọng: **stub** phục vụ *state verification* (kiểm tra kết quả trả về), còn **mock** phục vụ *behavior verification* (kiểm tra sự tương tác đã diễn ra đúng cách).

### 2.7. Nên và không nên viết unit test cho cái gì

- **Nên tập trung:** logic nghiệp vụ, thuật toán, xử lý điều kiện rẽ nhánh, tính toán, xử lý trường hợp biên và trường hợp lỗi, các hàm thuần (pure function).
- **Phù hợp loại test khác hơn:** code chủ yếu là "keo dán" gọi nhiều hệ thống ngoài → nên dùng integration test; luồng người dùng đầu-cuối → dùng E2E test.
- **Không nên lạm dụng:** test getter/setter tầm thường, test lại thư viện bên thứ ba (đã được tác giả của nó test), hoặc viết test rỗng chỉ để nâng con số coverage.

### 2.8. Liên hệ với TDD

**TDD (Test-Driven Development)** là phương pháp viết test *trước* khi viết code, theo vòng lặp **Red – Green – Refactor**:

1. **Red:** viết một test cho tính năng chưa tồn tại → test fail.
2. **Green:** viết đoạn code tối thiểu để test pass.
3. **Refactor:** dọn dẹp code trong khi vẫn giữ test xanh.

TDD không bắt buộc, nhưng là một cách tự nhiên để đảm bảo code luôn có test và có khả năng kiểm thử (testable) tốt.

---

## 3. Code Coverage

### 3.1. Định nghĩa

**Code coverage (độ phủ mã nguồn)** là một **chỉ số đo lường** cho biết tỉ lệ phần trăm mã nguồn **được thực thi** khi bộ test chạy. Nó trả lời: *"Bộ test đã chạm tới bao nhiêu phần của chương trình, và phần nào chưa bao giờ được kiểm thử?"*

Cần hiểu đúng bản chất: coverage đo **phạm vi code được chạy qua trong lúc test**, chứ **không** đo chất lượng của các câu assert. Đây là nguồn gốc của hiểu lầm phổ biến nhất về coverage (xem mục 3.5).

### 3.2. Các loại coverage

Xét ví dụ:

```python
def phan_loai(diem):
    if diem >= 5:
        return "Đậu"
    else:
        return "Rớt"
```

- **Statement / Line Coverage:** tỉ lệ *câu lệnh* (hoặc dòng) được thực thi. Mức cơ bản nhất.
- **Branch / Decision Coverage:** tỉ lệ *nhánh rẽ* (mỗi hướng true/false của if, mỗi case của switch) được thực thi. Chặt hơn statement coverage.
- **Function / Method Coverage:** tỉ lệ *hàm/method* được gọi ít nhất một lần.
- **Condition Coverage:** tỉ lệ các *điều kiện con* (từng vế trong `&&`, `||`) đạt cả giá trị true lẫn false. Chặt hơn nữa.
- **Path / MC-DC Coverage:** phủ các *đường đi* / tổ hợp điều kiện. Rất chặt, dùng cho hệ thống an toàn trọng yếu (hàng không, y tế) theo các chuẩn như DO-178C.

Với ví dụ trên:
- Chỉ một test `phan_loai(8)` đã cho **statement coverage** khá cao (chạy qua dòng `if` và `return "Đậu"`) nhưng **bỏ sót hoàn toàn** nhánh `else` → `return "Rớt"`.
- Phải có **cả** `phan_loai(8)` **và** `phan_loai(3)` mới đạt **branch coverage 100%**.

→ Đây là lý do khi đánh giá độ an toàn, **branch coverage** cho thông tin có ý nghĩa hơn line coverage.

### 3.3. Công cụ coverage theo ngôn ngữ

| Ngôn ngữ | Công cụ phổ biến | Ghi chú |
|----------|------------------|---------|
| Java | **JaCoCo** | Tiêu chuẩn de-facto; tích hợp Maven/Gradle; xuất HTML, XML |
| Python | **coverage.py** (thường qua `pytest-cov`) | Lệnh: `pytest --cov=module` |
| JavaScript/TS | **Istanbul / nyc** | Jest tích hợp sẵn: `jest --coverage` |
| C/C++ | **gcov / lcov** | Đi kèm trình biên dịch GCC |
| C#/.NET | **Coverlet** | Tích hợp `dotnet test` |
| Ruby | **SimpleCov** | — |

Các **định dạng báo cáo** thường gặp — quan trọng vì công cụ CI và các nền tảng phân tích như SonarQube cần đọc được chúng:
- **Cobertura XML**, **JaCoCo XML**, **LCOV**, và báo cáo **HTML** cho con người xem trực quan.

### 3.4. Cách đọc một báo cáo coverage

Một báo cáo điển hình liệt kê từng file kèm tỉ lệ line/branch và các dòng chưa được phủ:

```
File                    Lines    Branch   Dòng chưa phủ
──────────────────────────────────────────────────────
calculator.py           100%     100%     —
user_service.py          85%      70%     42–45 (nhánh xử lý lỗi)
payment.py               40%      25%     phần lớn chưa test
──────────────────────────────────────────────────────
TỔNG                     78%      68%
```

Giá trị của báo cáo không nằm ở con số tổng, mà ở chỗ nó **chỉ ra vùng rủi ro**: trong ví dụ trên, `payment.py` là module quan trọng (thanh toán) nhưng coverage thấp → đây là nơi cần ưu tiên bổ sung test.

### 3.5. Những hiểu lầm quan trọng về coverage

Đây là phần dễ bị hỏi và dễ hiểu sai nhất, cần nắm chắc:

1. **Coverage cao không có nghĩa là test tốt.** Một test có thể *chạy qua* một dòng code mà **không** assert gì có ý nghĩa về dòng đó. Code được "phủ" nhưng hành vi sai vẫn không bị phát hiện.
2. **100% coverage không có nghĩa là không còn bug.** Coverage không bắt được: lỗi logic ở các tổ hợp điều kiện chưa test, lỗi ở trường hợp biên, lỗi tương tranh (race condition), lỗi do đầu vào ngoài dự kiến.
3. **Line coverage 100% vẫn có thể bỏ sót nhánh** (như ví dụ `phan_loai`). Luôn xem thêm branch coverage.

Phát biểu đúng bản chất: *coverage là điều kiện cần, không phải điều kiện đủ*. Code không được phủ thì chắc chắn có rủi ro chưa kiểm soát; nhưng code được phủ 100% vẫn có thể sai nếu các assert hời hợt.

### 3.6. Ngưỡng coverage hợp lý

- Không tồn tại con số "vàng" cho mọi dự án. Mức **70–80%** thường được coi là hợp lý trong thực tế.
- Theo đuổi 100% bằng mọi giá dễ dẫn tới test giả tạo (assert yếu, test rỗng) → tốn công mà không tăng chất lượng thật.
- Cách dùng đúng: đặt một **ngưỡng tối thiểu** làm "quality gate" trong CI (ví dụ branch coverage ≥ 70%) và tập trung coverage vào **những module quan trọng/rủi ro cao**, thay vì dàn đều.

---

## 4. CI/CD

### 4.1. Ba khái niệm: CI, Continuous Delivery, Continuous Deployment

| Thuật ngữ | Tên đầy đủ | Bản chất |
|-----------|-----------|---------|
| **CI** | Continuous Integration (Tích hợp liên tục) | Mỗi khi lập trình viên push code, hệ thống **tự động build và chạy test** để phát hiện lỗi/xung đột tích hợp sớm. Khuyến khích merge thường xuyên (ít nhất mỗi ngày). |
| **CD** | Continuous Delivery (Phân phối liên tục) | Mở rộng CI: sau khi pass, sản phẩm luôn được **đóng gói ở trạng thái sẵn sàng phát hành**. Việc đưa lên production là một **bước thủ công** (bấm nút) do con người quyết định. |
| **CD** | Continuous Deployment (Triển khai liên tục) | Như Continuous Delivery nhưng bước đưa lên production cũng **tự động hoàn toàn**, không cần con người can thiệp (với điều kiện mọi kiểm thử đều pass). |

Khác biệt mấu chốt giữa hai chữ "CD": **Continuous Delivery** luôn *sẵn sàng* deploy nhưng *con người bấm nút*; **Continuous Deployment** *tự động* deploy luôn. Khác nhau đúng một bước phê duyệt của con người.

### 4.2. Cấu trúc một pipeline CI/CD điển hình

Một pipeline là chuỗi các giai đoạn (stage) chạy tuần tự, mỗi giai đoạn chỉ chạy nếu giai đoạn trước thành công:

```
Push code → Checkout → Build → Test → Coverage → Quality Gate → (Package) → Deploy
```

- **Checkout:** lấy mã nguồn mới nhất từ kho (Git).
- **Build:** biên dịch, phân giải phụ thuộc.
- **Test:** chạy unit test (và các loại test khác).
- **Coverage:** đo độ phủ, xuất báo cáo.
- **Quality Gate:** điểm quyết định — nếu test fail hoặc coverage dưới ngưỡng thì pipeline **dừng (fail)**, không cho đi tiếp.
- **Deploy:** triển khai lên môi trường (staging/production).

Chính tại đây, **Unit Test và Coverage trở thành hai trạm kiểm soát chất lượng (quality gate) tự động** trong pipeline. Đây là điểm ba chủ đề của seminar gặp nhau.

### 4.3. Lợi ích của CI/CD

- **Phát hiện lỗi sớm:** sai ở commit nào lộ ra ngay ở commit đó, chi phí sửa thấp.
- **Giảm vấn đề môi trường ("works on my machine"):** mọi thứ build/test trên môi trường chuẩn, nhất quán của CI.
- **Phát hành nhanh và an toàn:** quy trình tự động, lặp lại được, giảm lỗi do thao tác tay.
- **Tăng tự tin khi refactor/thay đổi:** luôn có lưới kiểm thử tự động chạy phía sau.

---

## 5. Jenkins

### 5.1. Jenkins là gì

**Jenkins** là một **máy chủ tự động hóa (automation server) mã nguồn mở**, viết bằng Java. Nó có nguồn gốc từ dự án Hudson (Sun Microsystems) và tách ra thành Jenkins năm 2011. Jenkins là một trong những công cụ CI/CD lâu đời và được dùng rộng rãi nhất.

Đặc điểm nổi bật:
- **Hệ sinh thái plugin rất lớn** (hơn 1.800 plugin): tích hợp Git, Maven/Gradle, Docker, JaCoCo, Slack, cloud... Gần như mọi công cụ đều có plugin kết nối.
- **Tự host (self-hosted):** cài trên máy chủ riêng, kiểm soát toàn bộ — phù hợp doanh nghiệp, môi trường on-premise, yêu cầu bảo mật nội bộ.
- **Rất linh hoạt:** tùy biến được gần như mọi quy trình, nhưng đổi lại cần công cài đặt và bảo trì.

So sánh ngắn với lựa chọn khác: **GitHub Actions / GitLab CI** là dịch vụ tích hợp sẵn trong nền tảng Git tương ứng, cấu hình bằng YAML, khởi động nhanh, phù hợp dự án nhỏ/vừa; **Jenkins** mạnh về linh hoạt và tự chủ hạ tầng nhưng cần vận hành nhiều hơn.

### 5.2. Kiến trúc Controller – Agent

Jenkins hoạt động theo mô hình phân tán:

- **Controller (trước đây gọi là "master"):** bộ não trung tâm — lập lịch công việc, quản lý cấu hình và job, cung cấp giao diện web, lưu trữ kết quả. Controller *điều phối* chứ không nên là nơi chạy build nặng.
- **Agent (node):** máy thực thi — nơi job thực sự chạy build/test. Có thể có nhiều agent trên nhiều hệ điều hành.

Lợi ích của mô hình này:
- **Chạy song song** nhiều job trên nhiều agent → tăng tốc.
- **Kiểm thử đa môi trường:** cùng một code có thể test đồng thời trên Linux, Windows, macOS, hoặc nhiều phiên bản runtime.
- **Mở rộng (scale):** thêm agent khi khối lượng công việc tăng.

### 5.3. Cách định nghĩa công việc: Freestyle vs Pipeline

- **Freestyle job:** cấu hình qua giao diện web bằng cách bấm chọn. Dễ bắt đầu nhưng khó version control và khó tái lập.
- **Pipeline (khuyến nghị hiện đại):** mô tả toàn bộ quy trình bằng mã trong một file tên **`Jenkinsfile`** đặt ngay trong kho mã nguồn. Đây gọi là **Pipeline as Code**.

Ưu điểm của Pipeline as Code:
- Pipeline được **version control** cùng với code (xem được lịch sử thay đổi, review như code).
- Tái lập được, dễ chia sẻ, dễ khôi phục.
- Có hai cú pháp: **Declarative** (cấu trúc rõ ràng, khuyến nghị cho đa số) và **Scripted** (linh hoạt theo kiểu lập trình Groovy).

### 5.4. Các khái niệm trong Jenkinsfile

Khung một Jenkinsfile Declarative:

```groovy
pipeline {
    agent any                       // chạy trên agent bất kỳ khả dụng
    stages {
        stage('Build')    { steps { /* các bước biên dịch */ } }
        stage('Test')     { steps { /* chạy unit test */ } }
        stage('Coverage') { steps { /* đo & publish coverage */ } }
        stage('Deploy')   { steps { /* triển khai */ } }
    }
    post {
        always  { /* luôn chạy: lưu báo cáo, dọn dẹp */ }
        failure { /* chạy khi pipeline fail: gửi cảnh báo */ }
    }
}
```

Các thành phần cần nắm:
- **`pipeline`**: khối bao ngoài toàn bộ.
- **`agent`**: chỉ định nơi chạy (agent nào).
- **`stage`**: một giai đoạn có tên (Build, Test, Deploy...). Mỗi stage hiển thị thành một ô riêng trên giao diện để dễ theo dõi stage nào pass/fail.
- **`steps`**: các hành động cụ thể bên trong một stage.
- **`post`**: các hành động chạy *sau* pipeline tùy theo kết quả (`always`, `success`, `failure`, `unstable`), thường dùng để lưu báo cáo và gửi thông báo.

---

## 6. Tích hợp cả ba trong một pipeline

Phần này thể hiện cách Unit Test, Coverage và CI/CD kết nối thành một mạch thống nhất. Ví dụ dưới là một `Jenkinsfile` cho dự án Java/Maven:

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps { checkout scm }                     // lấy code mới nhất từ Git
        }

        stage('Build') {
            steps { sh 'mvn -B compile' }              // biên dịch
        }

        stage('Unit Test') {
            steps { sh 'mvn test' }                    // (1) chạy unit test (JUnit)
            post {
                always { junit 'target/surefire-reports/*.xml' }  // hiển thị kết quả test
            }
        }

        stage('Coverage') {
            steps { sh 'mvn jacoco:report' }           // (2) sinh báo cáo coverage (JaCoCo)
            post {
                always {
                    jacoco(changeBuildStatus: true,    // đặt ngưỡng làm quality gate
                           minimumBranchCoverage: '70')// branch < 70% → build FAIL
                }
            }
        }

        stage('Deploy') {
            when { branch 'main' }                     // chỉ deploy nhánh main
            steps { sh './deploy.sh' }                 // (3) triển khai
        }
    }

    post {
        success { echo 'Pipeline xanh — code đạt chuẩn để merge/deploy' }
        failure { echo 'Pipeline đỏ — có test fail hoặc coverage dưới ngưỡng' }
    }
}
```

Diễn giải theo mạch ba chủ đề:

1. **Unit Test** (stage *Unit Test*): lưới kiểm thử được chạy tự động mỗi lần có code mới.
2. **Coverage** (stage *Coverage* với `minimumBranchCoverage: '70'`): coverage trở thành **quality gate** — nếu branch coverage tụt dưới 70%, build bị đánh dấu fail và pipeline dừng.
3. **CI/CD** (toàn bộ pipeline + stage *Deploy*): Jenkins tự động vận hành cả dây chuyền mỗi lần push; chỉ khi tất cả pass, code mới được đưa lên nhánh `main`/triển khai.

Toàn bộ quy trình — *code → test → đo coverage → gác cổng chất lượng → triển khai* — diễn ra tự động, không cần thao tác thủ công.

---

## 7. Best practices & cạm bẫy

### Thực hành tốt
- Viết unit test tuân thủ FIRST; dùng test double để cô lập phụ thuộc ngoài.
- Theo dõi **branch coverage**, không chỉ line; đặt coverage làm **quality gate** trong CI.
- Dùng **Pipeline as Code** (Jenkinsfile trong repo) để version control quy trình.
- Thiết kế pipeline **fail fast**: xếp bước nhanh (unit test) trước bước chậm (integration, E2E, deploy) để lỗi lộ ra sớm, tiết kiệm thời gian.
- Tự động **thông báo** kết quả (Slack/email) để cả nhóm biết ngay khi pipeline đỏ.
- Giữ pipeline **nhanh**; cân nhắc chạy song song trên nhiều agent.

### Cạm bẫy thường gặp
- **Chạy theo con số coverage** dẫn tới test rỗng, assert hời hợt — coverage cao mà chất lượng thấp.
- **Test phụ thuộc lẫn nhau hoặc phụ thuộc thứ tự chạy** → sinh ra *flaky test* (lúc pass lúc fail).
- **Test chạm tài nguyên thật** (database, mạng) → chậm và không ổn định; nên dùng test double hoặc fake.
- **Pipeline quá chậm** khiến lập trình viên nản và tìm cách bỏ qua.
- **"Xanh giả":** tắt/bỏ qua test fail cho pipeline pass nhanh — làm vô hiệu hóa toàn bộ ý nghĩa của quality gate.

---

## 8. Thuật ngữ cần nhớ

| Thuật ngữ | Giải thích ngắn |
|-----------|-----------------|
| Unit test | Kiểm thử một đơn vị code nhỏ nhất, độc lập |
| Test Pyramid | Mô hình tỉ lệ test: nhiều unit, ít E2E |
| FIRST | Fast, Isolated, Repeatable, Self-validating, Timely |
| AAA | Arrange – Act – Assert: cấu trúc một test |
| Test double | Đối tượng giả thay thế phụ thuộc (dummy, stub, mock, fake, spy) |
| Stub | Test double cung cấp dữ liệu trả về định sẵn (state verification) |
| Mock | Test double kiểm chứng cách nó bị gọi (behavior verification) |
| TDD | Red – Green – Refactor: viết test trước code |
| Code coverage | % code được thực thi khi chạy test |
| Branch coverage | % nhánh rẽ (if/else, case) được thực thi |
| Quality gate | Điều kiện chất lượng bắt buộc vượt qua để pipeline đi tiếp |
| CI | Continuous Integration: tự động build + test mỗi lần push |
| Continuous Delivery | Luôn sẵn sàng phát hành; deploy là bước thủ công |
| Continuous Deployment | Deploy lên production hoàn toàn tự động |
| Pipeline | Chuỗi các stage tự động từ code tới triển khai |
| Jenkins | Automation server mã nguồn mở cho CI/CD |
| Controller / Agent | Bộ não điều phối / máy thực thi job trong Jenkins |
| Jenkinsfile | File mô tả pipeline (Pipeline as Code) |

---

## 9. Câu hỏi ôn tập & tài liệu tham khảo

### Câu hỏi ôn tập (tự kiểm tra mức độ hiểu)

1. Vì sao unit test nên chiếm số lượng nhiều nhất trong test pyramid?
2. Phân biệt stub và mock. Mỗi loại phục vụ kiểu kiểm chứng nào?
3. Vì sao line coverage 100% vẫn có thể bỏ sót lỗi? Loại coverage nào khắc phục được?
4. "100% coverage nghĩa là không còn bug" — nhận định này đúng hay sai? Giải thích.
5. Phân biệt Continuous Delivery và Continuous Deployment.
6. Quality gate là gì, và Unit Test/Coverage đóng vai trò quality gate như thế nào trong pipeline?
7. Mô tả vai trò của Controller và Agent trong kiến trúc Jenkins.
8. Pipeline as Code là gì và vì sao nó tốt hơn cấu hình qua giao diện?
9. Nêu ba cạm bẫy thường gặp khi dùng coverage/CI và cách tránh.

### Tài liệu tham khảo

- Martin Fowler — *UnitTest*, *ContinuousIntegration*, *ContinuousDelivery*, *TestPyramid*, *TestDouble* (martinfowler.com)
- Gerard Meszaros — *xUnit Test Patterns* (phân loại test double)
- Kent Beck — *Test-Driven Development: By Example*
- JUnit 5 User Guide — junit.org/junit5
- pytest Documentation — docs.pytest.org
- JaCoCo — jacoco.org
- Jenkins User Handbook & Pipeline Syntax — jenkins.io/doc
- Jez Humble & David Farley — *Continuous Delivery*
