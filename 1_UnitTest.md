# Phần 1 — UNIT TEST (Kiểm thử đơn vị)
### Tài liệu chuẩn bị seminar · Môn Kiểm thử phần mềm

> **Vị trí trong chuỗi seminar:** Đây là mắt xích **đầu tiên** trong dây chuyền đảm bảo chất lượng tự động: **Unit Test → [Code Coverage](2_CodeCoverage.md) → [CI/CD](3_CICD.md)**. Unit Test *tạo ra lưới an toàn*; Coverage *đo lỗ hổng của lưới*; CI/CD *tự động chạy lưới mỗi khi code thay đổi*.

---

## Mục lục
1. [Định nghĩa & bản chất](#1-định-nghĩa--bản-chất)
2. [Vị trí trong kim tự tháp kiểm thử](#2-vị-trí-trong-kim-tự-tháp-kiểm-thử)
3. [Nguyên tắc FIRST](#3-nguyên-tắc-first)
4. [Cấu trúc AAA](#4-cấu-trúc-aaa)
5. [Ví dụ đa ngôn ngữ](#5-ví-dụ-đa-ngôn-ngữ)
6. [Test Double: Mock, Stub và các biến thể](#6-test-double-mock-stub-và-các-biến-thể)
7. [Nên / không nên test cái gì](#7-nên--không-nên-test-cái-gì)
8. [Quan hệ với TDD](#8-quan-hệ-với-tdd)
9. [Best practices & cạm bẫy](#9-best-practices--cạm-bẫy)
10. [Thuật ngữ & câu hỏi ôn tập](#10-thuật-ngữ--câu-hỏi-ôn-tập)

---

## 1. Định nghĩa & bản chất

**Unit test (kiểm thử đơn vị)** là việc kiểm thử **đơn vị nhỏ nhất, độc lập** của phần mềm — thường là một hàm (function) hoặc một phương thức (method) — nhằm xác minh rằng với một đầu vào xác định, đơn vị đó cho ra đầu ra đúng như mong đợi.

Ba đặc điểm cốt lõi:

1. **Nhỏ (granular):** kiểm thử một đơn vị logic, không phải cả luồng nghiệp vụ.
2. **Độc lập (isolated):** đơn vị được tách khỏi phụ thuộc bên ngoài (database, mạng, file, thời gian…) bằng kỹ thuật *test double*.
3. **Tự động (automated):** chạy bằng framework, tự kết luận đúng/sai, không cần con người quan sát bằng mắt.

**Vì sao quan trọng?** Unit test cho **phản hồi nhanh** và **khoanh vùng lỗi chính xác**. Khi một unit test fail, ta biết ngay chính xác hàm nào hỏng — thay vì phải dò khắp hệ thống. Đây là nền tảng giúp nhóm nhiều người cùng sửa code mà không sợ làm hỏng tính năng của nhau.

---

## 2. Vị trí trong kim tự tháp kiểm thử

Kim tự tháp kiểm thử (Test Pyramid — Mike Cohn) mô tả tỉ lệ hợp lý giữa các loại test:

```
            /\
           /  \      E2E / UI test  (ít nhất)
          /----\     - kiểm thử toàn hệ thống từ góc nhìn người dùng
         /      \    - chậm, đắt, dễ "giòn" (flaky)
        /--------\
       /          \  Integration test  (vừa phải)
      /            \ - kiểm thử nhiều module ghép thật với nhau
     /--------------\
    /                \ UNIT TEST  (nhiều nhất)  ← nền móng
   /                  \ - nhanh (mili-giây), rẻ, khoanh vùng lỗi chính xác
  /____________________\
```

- **Unit test (đáy):** số lượng nhiều nhất, nhanh nhất.
- **Integration test (giữa):** kiểm thử các thành phần ghép thật (ví dụ service + database).
- **E2E/UI test (đỉnh):** kiểm thử cả hệ thống; ít nhất vì chậm và dễ hỏng vặt.

**Lý do unit test nên chiếm số lượng lớn nhất:** nếu một integration test fail, nguyên nhân có thể nằm ở hàng chục chỗ; nếu một unit test fail, ta biết ngay đơn vị nào sai. Càng xuống đáy, test càng nhanh – rẻ – dễ chẩn đoán.

---

## 3. Nguyên tắc FIRST

Một unit test tốt cần thỏa 5 tiêu chí **FIRST**:

| Chữ | Nguyên tắc | Giải thích |
|-----|-----------|-----------|
| **F** | **Fast** (nhanh) | Chạy trong mili-giây; cả bộ test hàng nghìn ca nên xong trong vài giây để lập trình viên chạy thường xuyên. |
| **I** | **Isolated** (độc lập) | Không phụ thuộc test khác, không phụ thuộc thứ tự chạy, không dùng chung trạng thái. Mỗi test tự chuẩn bị & tự dọn dẹp. |
| **R** | **Repeatable** (lặp lại được) | Chạy nhiều lần, nhiều máy, nhiều thời điểm đều cho cùng kết quả. Không phụ thuộc random, giờ hệ thống, mạng. |
| **S** | **Self-validating** (tự kiểm chứng) | Tự khẳng định pass/fail qua assert, không cần người đọc log so sánh bằng mắt. |
| **T** | **Timely** (đúng lúc) | Viết sớm — lý tưởng là ngay khi (hoặc trước khi) viết code. Test viết muộn thường bị bỏ hoặc làm qua loa. |

---

## 4. Cấu trúc AAA

Hầu hết unit test được tổ chức theo ba bước **Arrange – Act – Assert**:

- **Arrange (chuẩn bị):** thiết lập dữ liệu đầu vào, khởi tạo đối tượng, cấu hình test double.
- **Act (thực thi):** gọi đúng một hàm/method cần kiểm thử.
- **Assert (kiểm chứng):** so sánh kết quả thực tế với kết quả mong đợi.

Việc tách rõ ba bước giúp test dễ đọc và dễ bảo trì. Một biến thể tương đương là **Given – When – Then** (thường dùng trong BDD — Behavior-Driven Development).

---

## 5. Ví dụ đa ngôn ngữ

Cùng một bài toán — kiểm thử hàm cộng hai số — viết trong ba hệ sinh thái phổ biến. Điểm đáng chú ý: **cú pháp khác nhau nhưng tư duy AAA giống hệt nhau**.

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

> **Mẹo đặt tên test:** nên mô tả *điều kiện + hành vi mong đợi*, ví dụ `add_haiSoDuong_traVeTongDung` hoặc `chia_choSoKhong_nemNgoaiLe`. Tên tốt giúp khi test fail là đọc tên biết ngay vấn đề.

---

## 6. Test Double: Mock, Stub và các biến thể

Thực tế hàm cần test thường phụ thuộc vào thành phần bên ngoài (database, web service, hệ thống file…). Nếu để test gọi thật những thứ này, test sẽ **chậm và không ổn định** — vi phạm FIRST. Giải pháp: thay chúng bằng **test double** (đối tượng giả đóng vai thay thế).

Phân loại (theo Gerard Meszaros / Martin Fowler):

| Loại | Vai trò |
|------|---------|
| **Dummy** | Truyền vào cho đủ tham số nhưng không được dùng thật. |
| **Stub** | Cung cấp sẵn **câu trả lời cố định** cho lời gọi trong test. Phục vụ *state verification* (kiểm tra kết quả). |
| **Mock** | Giống stub nhưng còn **ghi nhận & kiểm chứng cách nó bị gọi** (hàm nào, bao nhiêu lần, tham số gì). Phục vụ *behavior verification*. |
| **Fake** | Cài đặt đơn giản có chạy thật nhưng không dùng cho production (ví dụ DB trong bộ nhớ). |
| **Spy** | Bọc đối tượng thật và ghi lại thông tin về cách nó được gọi. |

**Ví dụ — Java + Mockito:**

```java
UserRepository repo = mock(UserRepository.class);      // tạo mock
when(repo.findById(1)).thenReturn(new User("An"));     // stub hành vi trả về

UserService service = new UserService(repo);
assertEquals("An", service.getUserName(1));            // state verification: kiểm kết quả

verify(repo).findById(1);   // behavior verification: repo đã được gọi đúng 1 lần
```

**Phân biệt mấu chốt:** *stub* phục vụ kiểm tra **kết quả trả về**; *mock* phục vụ kiểm tra **sự tương tác đã diễn ra đúng cách**.

> **Ẩn dụ dễ nhớ:** muốn test túi khí xe hơi, bạn không lao xe thật vào tường — bạn dùng *hình nộm* (mock) để mô phỏng va chạm.

---

## 7. Nên / không nên test cái gì

- **Nên tập trung:** logic nghiệp vụ, thuật toán, xử lý điều kiện rẽ nhánh, tính toán, trường hợp biên, xử lý lỗi, các hàm thuần (pure function — cùng input luôn cho cùng output, không tác dụng phụ).
- **Phù hợp loại test khác hơn:** code chủ yếu là "keo dán" gọi nhiều hệ thống ngoài → nên dùng *integration test*; luồng người dùng đầu-cuối → dùng *E2E test*.
- **Không nên lạm dụng:** test getter/setter tầm thường, test lại thư viện bên thứ ba (đã được tác giả của nó test), hoặc viết test rỗng chỉ để nâng con số [coverage](2_CodeCoverage.md).

---

## 8. Quan hệ với TDD

**TDD (Test-Driven Development)** là phương pháp viết test *trước* khi viết code, theo vòng lặp **Red – Green – Refactor**:

1. **Red:** viết một test cho tính năng chưa tồn tại → test fail (đỏ).
2. **Green:** viết đoạn code tối thiểu để test pass (xanh).
3. **Refactor:** dọn dẹp code trong khi vẫn giữ test xanh.

TDD không bắt buộc, nhưng là một cách tự nhiên đảm bảo code luôn có test và có *khả năng kiểm thử* (testability) tốt — vì code được thiết kế để dễ test ngay từ đầu.

---

## 9. Best practices & cạm bẫy

### Thực hành tốt
- Tuân thủ **FIRST**; mỗi test kiểm một hành vi, đặt tên test rõ nghĩa.
- Dùng **test double** để cô lập phụ thuộc ngoài → test nhanh và ổn định.
- Test cả **trường hợp biên** và **trường hợp lỗi** (ngoại lệ), không chỉ "happy path".
- Giữ test **đơn giản và dễ đọc**; test là tài liệu sống mô tả hành vi của code.

### Cạm bẫy thường gặp
- **Flaky test:** test phụ thuộc thứ tự chạy, thời gian, hoặc random → lúc pass lúc fail, làm mất niềm tin vào bộ test.
- **Test chạm tài nguyên thật** (DB, mạng) → chậm, không ổn định.
- **Assert hời hợt:** code được chạy qua nhưng không kiểm tra gì có ý nghĩa → [coverage](2_CodeCoverage.md) cao mà vẫn sót bug.
- **Over-mocking:** mock quá nhiều khiến test chỉ còn kiểm tra chính các mock, mất liên hệ với hành vi thật.

---

## 10. Thuật ngữ & câu hỏi ôn tập

### Thuật ngữ
| Thuật ngữ | Nghĩa ngắn |
|-----------|-----------|
| Unit test | Kiểm thử một đơn vị code nhỏ nhất, độc lập |
| Test Pyramid | Mô hình tỉ lệ test: nhiều unit, ít E2E |
| FIRST | Fast · Isolated · Repeatable · Self-validating · Timely |
| AAA | Arrange – Act – Assert |
| Test double | Đối tượng giả thay thế phụ thuộc |
| Stub / Mock | Trả dữ liệu định sẵn / kiểm chứng cách bị gọi |
| Fake / Spy / Dummy | Cài đặt giả chạy thật / bọc ghi nhận / chỉ cho đủ tham số |
| TDD | Red – Green – Refactor: viết test trước code |
| Flaky test | Test lúc pass lúc fail không ổn định |

### Câu hỏi ôn tập
1. Vì sao unit test nên chiếm số lượng nhiều nhất trong test pyramid?
2. Giải thích từng chữ trong FIRST.
3. Phân biệt stub và mock — mỗi loại phục vụ kiểu kiểm chứng nào?
4. Khi nào nên dùng integration test thay vì unit test?
5. TDD là gì? Mô tả vòng lặp Red – Green – Refactor.
6. Vì sao "assert hời hợt" lại nguy hiểm dù test vẫn pass?

### Tài liệu tham khảo
- Martin Fowler — *UnitTest*, *TestPyramid*, *TestDouble* (martinfowler.com)
- Gerard Meszaros — *xUnit Test Patterns*
- Kent Beck — *Test-Driven Development: By Example*
- JUnit 5 User Guide (junit.org/junit5) · pytest (docs.pytest.org)

---
*Phần tiếp theo → [Phần 2 — Code Coverage](2_CodeCoverage.md)*
