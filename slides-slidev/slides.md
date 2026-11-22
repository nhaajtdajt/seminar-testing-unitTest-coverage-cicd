---
theme: default
title: Unit Test, Code Coverage và CI/CD
info: Seminar Kiểm thử phần mềm — JUnit, JaCoCo, GitHub Actions
colorSchema: light
aspectRatio: 16/9
canvasWidth: 980
transition: fade
duration: 30min
fonts:
  sans: Be Vietnam Pro
  mono: JetBrains Mono
  weights: '400,600,700'
mermaid:
  theme: neutral
layout: cover
class: text-left
---

# Unit Test, Code Coverage <br> và CI/CD

Kiểm thử tự động với JUnit · JaCoCo · GitHub Actions

<div class="logos">
  <img src="/junit5.svg" alt="JUnit 5" />
  <img src="/openjdk.svg" alt="Java" />
  <img src="/apachemaven.svg" alt="Maven" />
  <img src="/githubactions.svg" alt="GitHub Actions" />
</div>

<!--
Mở đầu: một thay đổi nhỏ có thể làm hỏng chức năng đang chạy. Kiểm tra thủ công sau mỗi lần sửa thì tốn thời gian và khó lặp lại.
Unit Test biến các kiểm tra đó thành test chạy tự động. Bài tập trung vào Unit Test, Code Coverage, coverage gate trong CI/CD, với ba công cụ JUnit, JaCoCo, GitHub Actions.
-->

---
class: unit-visual
---

# Agenda

<ol class="agenda-list">
  <li><b>Unit Testing</b><span>Thiết kế test case và kiểm tra hành vi bằng JUnit, Mockito.</span></li>
  <li><b>Code Coverage</b><span>Đọc báo cáo JaCoCo và đặt coverage gate.</span></li>
  <li><b>CI/CD</b><span>Chạy test, kiểm tra gate và đóng gói với GitHub Actions.</span></li>
  <li><b>AI trong Unit Testing</b><span>Pynguin, CoverUp và quy trình sinh test của nhóm.</span></li>
  <li><b>Case study thư viện, Lab &amp; Q&amp;A</b><span>Tính phí trả sách trễ, thực hành mutation testing và hỏi đáp.</span></li>
</ol>

<style scoped>
.agenda-list { margin: 0; padding: 0; counter-reset: topic; }
.agenda-list li {
  counter-increment: topic;
  display: grid;
  grid-template-columns: 2.25rem 14rem 1fr;
  align-items: center;
  gap: 1rem;
  min-height: 3.45rem;
  margin: 0;
  border-bottom: 1px solid var(--line);
}
.agenda-list li::before {
  content: counter(topic);
  display: grid;
  place-items: center;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: #eff6ff;
  color: var(--accent);
  font-weight: 700;
}
.agenda-list b { font-size: 1.18rem; color: var(--ink); }
.agenda-list span { font-size: 1.05rem; line-height: 1.35; color: var(--muted); }
</style>

---
layout: statement
---

<p class="kicker">Câu hỏi chính</p>

# Test xanh và coverage 100% <br> có chắc chương trình đã đúng không?

<!--
Khi toàn bộ test đều xanh, ta vẫn chưa biết bộ test đã đi qua hết các nhánh hay chưa — Code Coverage trả lời phần đó. Từ coverage, nhóm tạo coverage gate để build thất bại nếu độ phủ dưới ngưỡng.
Đặt câu hỏi này cho khán giả, giữ lại câu trả lời đến cuối bài.
-->

---
layout: cover
class: text-left
---

<div class="flex items-center gap-3 mb-6 text-blue-700">
  <carbon-code class="text-4xl" aria-hidden="true" />
  <span class="kicker">Phần 1 / 5</span>
</div>

# Unit Testing

Thiết kế test case và kiểm tra hành vi bằng JUnit, Mockito.

---
class: unit-visual
---

<p class="kicker">Unit Testing / Test level</p>

# Unit testing và test level

<div class="uv-split"><div>

<p class="uv-lead"><b>Unit testing</b> (component testing) kiểm tra hành vi của một thành phần trong điều kiện cô lập.</p>

<p class="note"><b>System under test (SUT)</b> là phần đang được kiểm tra.</p>

</div><div>

<div class="pyramid uv-pyramid">
  <div class="p1">System testing<small>Hành vi toàn hệ thống</small>
  </div>
  <div class="p2">Component integration testing<small>Tương tác giữa các thành phần</small>
  </div>
  <div class="p3">Unit testing<small>Hành vi của một thành phần</small>
  </div>
</div>

</div></div>

---
class: unit-visual
---

<p class="kicker">Unit Testing / Test level</p>

# Phí giao hàng ở ba test level

<p class="uv-lead">Đơn từ <b>200.000 đồng</b> được miễn phí giao hàng. Phạm vi kiểm tra thay đổi ở từng test level.</p>

<div class="uv-diagram">
  <div class="uv-row">
    <div class="uv-node pick"><carbon-code class="uv-icon" aria-hidden="true" /><b>Unit testing</b><small>Hàm shippingFee trả 0 đồng?</small>
    </div>
    <div class="uv-node"><carbon-connect class="uv-icon" aria-hidden="true" /><b>Component integration</b><small>Thanh toán nhận đúng phí?</small>
    </div>
    <div class="uv-node"><carbon-shopping-cart class="uv-icon" aria-hidden="true" /><b>System testing</b><small>Khách thấy đúng tổng tiền trên xác nhận đơn?</small>
    </div>
  </div>
</div>

<!--
Nguồn định nghĩa: ISTQB CTFL v4.0.1, mục 2.2.1, trang 29.
-->

---
class: unit-visual
---

<p class="kicker">Unit Testing / Mục tiêu và đặc điểm</p>

# Đặc điểm của một unit test tốt

<div class="uv-checks mt-8">
  <div>
    <carbon-checkbox-checked class="uv-icon" aria-hidden="true" />
    <b class="w-52 shrink-0">Một hành vi</b>
    <span>Tên test nêu tình huống và kết quả mong đợi.</span>
  </div>
  <div>
    <carbon-checkbox-checked class="uv-icon" aria-hidden="true" />
    <b class="w-52 shrink-0">Độc lập, lặp lại được</b>
    <span>Test chạy nhanh, cho cùng kết quả ở mọi thứ tự chạy.</span>
  </div>
  <div>
    <carbon-checkbox-checked class="uv-icon" aria-hidden="true" />
    <b class="w-52 shrink-0">Regression testing</b>
    <span>Chạy lại sau khi sửa code để phát hiện hành vi thay đổi.</span>
  </div>
</div>

---
class: unit-visual code-lg
---

<p class="kicker">Unit Testing / Mục tiêu và đặc điểm</p>

# Khi sửa hàm tính phí

```java
int shippingFee(int total) {
    if (total < 0) {
        throw new IllegalArgumentException("Tổng tiền phải không âm");
    }
    return total >= 200_000 ? 0 : 20_000;
}
```

<div class="uv-diagram">
  <div class="uv-row">
    <div class="uv-verdict pass"><b>≥ 200.000</b><span>Đúng ngưỡng → miễn phí</span>
    </div>
    <div class="uv-verdict fail"><b>&gt; 200.000</b><span>Đúng ngưỡng → thu nhầm 20.000 đồng</span>
    </div>
  </div>
</div>

<!--
Hàm chỉ cần tổng tiền làm input. Có thể chạy ca này riêng hoặc sau bất kỳ ca nào khác và thu được cùng kết quả.
-->

---
class: unit-visual
---

<p class="kicker">Unit Testing / Cấu trúc test case / Test oracle</p>

# Test oracle và assertion

<p class="uv-lead"><b>Test oracle</b> xác định kết quả đúng. <b>Assertion</b> so sánh hai kết quả.</p>

<div class="uv-diagram">
  <div class="uv-lane"><b>Test oracle</b><span>── xác định →</span><strong class="pick">Expected result</strong>
  </div>
  <div class="uv-lane"><b>SUT</b><span>── trả về →</span><strong class="neutral">Actual result</strong>
  </div>
  <div class="uv-compare">
    <span>Expected result</span>
    <i aria-hidden="true">→</i>
    <b>Assertion</b>
    <i aria-hidden="true">←</i>
    <span>Actual result</span>
  </div>
</div>

---
class: unit-visual code-lg
---

<p class="kicker">Unit Testing / Cấu trúc test case / Test oracle</p>

# Phí bằng 0 hay chỉ cần không âm?

<p class="uv-lead">Đơn đúng ngưỡng phải có phí <b>0 đồng</b>. Giả sử actual result là <b>20.000 đồng</b>.</p>

```java
int fee = shippingFee(200_000);
assertTrue(fee >= 0);    // Xanh: 20.000 vẫn là số không âm
assertEquals(0, fee);    // Đỏ: bắt được khoản phí thu nhầm
```

<div class="uv-diagram">
  <div class="uv-row">
    <div class="uv-verdict pass"><b>✓ Pass</b><span>Phí không âm, sai lệch bị bỏ sót</span>
    </div>
    <div class="uv-verdict fail"><b>✕ Fail</b><span>Phí khác 0, bắt được lỗi</span>
    </div>
  </div>
</div>

---
class: unit-visual
---

<p class="kicker">Unit Testing / Cấu trúc test case / Arrange–Act–Assert</p>

# Arrange · Act · Assert

<div class="uv-diagram">
  <div class="uv-row">
    <div class="uv-node"><carbon-settings class="uv-icon" aria-hidden="true" /><b>Arrange</b><small>Chuẩn bị SUT, điều kiện và input.</small>
    </div>
    <i class="uv-arrow" aria-hidden="true">→</i>
    <div class="uv-node pick"><carbon-play class="uv-icon" aria-hidden="true" /><b>Act</b><small>Gọi hành vi, lấy actual result.</small>
    </div>
    <i class="uv-arrow" aria-hidden="true">→</i>
    <div class="uv-node"><carbon-checkmark-outline class="uv-icon" aria-hidden="true" /><b>Assert</b><small>So sánh với expected result.</small>
    </div>
  </div>
</div>

---
class: unit-visual code-lg
---

<p class="kicker">Unit Testing / Cấu trúc test case / Arrange–Act–Assert</p>

# Một đơn đúng ngưỡng trong JUnit

```java
@Test
void mienPhiKhiDonDungNguong() {
    int total = 200_000;           // Arrange
    int fee = shippingFee(total);  // Act
    assertEquals(0, fee);          // Assert
}
```

<div class="uv-diagram">
  <div class="uv-row">
    <div class="uv-node"><b>200.000 đ</b><small>Arrange</small>
    </div>
    <i class="uv-arrow" aria-hidden="true">→</i>
    <div class="uv-node pick"><b>shippingFee(total)</b><small>Act</small>
    </div>
    <i class="uv-arrow" aria-hidden="true">→</i>
    <div class="uv-node"><b>0 đ</b><small>Assert</small>
    </div>
  </div>
</div>

---
class: unit-visual
---

<p class="kicker">Unit Testing / Chọn test case / Black-box</p>

# Black-box test techniques

- Equivalence partitioning
- Boundary value analysis
- Decision table testing
- State transition testing

---
class: unit-visual
---

<p class="kicker">Unit Testing / Chọn test case / White-box</p>

# Statement testing

<p class="uv-lead">Chọn input để thực thi <b>câu lệnh mục tiêu</b>, rồi kiểm tra kết quả nó tạo ra.</p>

<div class="uv-diagram">
  <div class="uv-row">
    <div class="uv-node"><carbon-login class="uv-icon" aria-hidden="true" /><b>Input</b><small>Đi vào luồng cần kiểm tra.</small>
    </div>
    <i class="uv-arrow" aria-hidden="true">→</i>
    <div class="uv-node pick"><carbon-code class="uv-icon" aria-hidden="true" /><b>Target statement</b><small>Câu lệnh được thực thi.</small>
    </div>
    <i class="uv-arrow" aria-hidden="true">→</i>
    <div class="uv-node"><carbon-checkmark-outline class="uv-icon" aria-hidden="true" /><b>Assertion</b><small>Đối chiếu kết quả.</small>
    </div>
  </div>
</div>

---
class: unit-visual
---

<p class="kicker">Unit Testing / Chọn test case / White-box</p>

# Branch testing

<p class="uv-lead">Thiết kế input để đi qua các hướng của <b>luồng điều khiển</b>.</p>

<div class="uv-diagram">
  <div class="uv-lane"><b>Điều kiện</b><span>── true →</span><strong class="pick">Chạy thân if</strong>
  </div>
  <div class="uv-lane"><b>Điều kiện</b><span>── false →</span><strong class="neutral">Bỏ qua thân if</strong>
  </div>
</div>

<p class="caption">Với điều kiện ghép, cần tính đến cả thứ tự đánh giá.</p>

---
class: unit-visual
---

<p class="kicker">Unit Testing / Chọn test case / Experience-based</p>

# Error guessing

<p class="uv-lead">Dùng kinh nghiệm để dự đoán một sai sót có thể xảy ra.</p>

<div class="uv-diagram">
  <div class="uv-row">
    <div class="uv-node"><carbon-recently-viewed class="uv-icon" aria-hidden="true" /><b>Lỗi từng gặp</b><small>Nhớ lại dấu hiệu đã thấy.</small>
    </div>
    <i class="uv-arrow" aria-hidden="true">→</i>
    <div class="uv-node pick"><carbon-idea class="uv-icon" aria-hidden="true" /><b>Giả thuyết</b><small>Dự đoán chỗ có thể sai.</small>
    </div>
    <i class="uv-arrow" aria-hidden="true">→</i>
    <div class="uv-node"><carbon-search class="uv-icon" aria-hidden="true" /><b>Test case</b><small>Chọn input làm lộ lỗi.</small>
    </div>
  </div>
</div>

---
class: unit-visual
---

<p class="kicker">Unit Testing / Chọn test case / Experience-based</p>

# Exploratory testing

<p class="uv-lead">Người kiểm thử vừa thiết kế, chạy và đánh giá test khi tìm hiểu chức năng.</p>

<div class="uv-diagram">
  <div class="uv-row">
    <div class="uv-node"><carbon-help class="uv-icon" aria-hidden="true" /><b>Đặt câu hỏi</b><small>Chọn điều cần tìm hiểu.</small>
    </div>
    <i class="uv-arrow" aria-hidden="true">→</i>
    <div class="uv-node pick"><carbon-play class="uv-icon" aria-hidden="true" /><b>Chạy thử</b><small>Quan sát hành vi thực tế.</small>
    </div>
    <i class="uv-arrow" aria-hidden="true">→</i>
    <div class="uv-node"><carbon-renew class="uv-icon" aria-hidden="true" /><b>Điều chỉnh</b><small>Dùng kết quả để chọn lần thử tiếp.</small>
    </div>
  </div>
</div>

<p class="uv-loop">↶ Quay lại với câu hỏi mới</p>

---
class: unit-visual
---

<p class="kicker">Unit Testing / Chọn test case / Experience-based</p>

# Checklist-based testing

<p class="uv-lead">Checklist ghi lại những điều cần rà soát từ kinh nghiệm kiểm thử.</p>

<div class="uv-diagram">
  <div class="uv-checks">
    <div><carbon-checkbox-checked class="uv-icon" aria-hidden="true" /><span>Chọn mục phù hợp với chức năng.</span>
    </div>
    <div><carbon-checkbox-checked class="uv-icon" aria-hidden="true" /><span>Xác định hành vi cần quan sát.</span>
    </div>
    <div><carbon-checkbox-checked class="uv-icon" aria-hidden="true" /><span>Đối chiếu với kết quả mong đợi.</span>
    </div>
  </div>
</div>

---
class: unit-visual
---

<p class="kicker">Unit Testing / Test doubles / Stub</p>

# Stub

<p class="uv-lead"><b>Stub</b> là test double cung cấp câu trả lời định sẵn cho dependency.</p>

<div class="uv-diagram">
  <div class="uv-lane"><b>SUT</b><span>── gọi dependency →</span><strong class="neutral">Stub</strong>
  </div>
  <div class="uv-lane"><b>Stub</b><span>── trả dữ liệu định sẵn →</span><strong class="pick">SUT</strong>
  </div>
</div>

---
class: unit-visual code-lg
---

<p class="kicker">Unit Testing / Test doubles / Stub</p>

# Thành viên đã mượn ba cuốn sách

<p class="uv-lead">Sách còn sẵn, thành viên không nợ phí. Test cần tình huống <b>đã mượn 3 cuốn</b>.</p>

<div class="uv-diagram">
  <div class="uv-lane"><b>LoanService</b><span>── hỏi số sách đang mượn →</span><strong class="neutral">LoanRepository</strong>
  </div>
  <div class="uv-lane"><b>Repository stub</b><span>── trả số lượng →</span><strong class="pick">3 cuốn</strong>
  </div>
</div>

```java
when(loans.countActiveByMemberId(1)).thenReturn(3L);
```

---
class: unit-visual
---

<p class="kicker">Unit Testing / Test doubles / Mock</p>

# Mock

<p class="uv-lead"><b>Mock</b> là test double dùng để xác minh tương tác giữa SUT và dependency.</p>

<div class="uv-diagram">
  <div class="uv-row">
    <div class="uv-node"><carbon-play class="uv-icon" aria-hidden="true" /><b>SUT</b><small>Thực hiện hành vi.</small>
    </div>
    <i class="uv-arrow" aria-hidden="true">→</i>
    <div class="uv-node pick"><carbon-list class="uv-icon" aria-hidden="true" /><b>Mock</b><small>Ghi nhận lời gọi, tham số và số lần.</small>
    </div>
    <i class="uv-arrow" aria-hidden="true">→</i>
    <div class="uv-node"><carbon-checkmark-outline class="uv-icon" aria-hidden="true" /><b>Verify</b><small>Đối chiếu với tương tác mong đợi.</small>
    </div>
  </div>
</div>

---
class: unit-visual code-lg
---

<p class="kicker">Unit Testing / Test doubles / Mock</p>

# Từ chối mượn và không lưu phiếu

<div class="uv-diagram">
  <div class="uv-row">
    <div class="uv-node"><carbon-warning-alt class="uv-icon" aria-hidden="true" /><b>LIMIT_REACHED</b><small>Đã đạt hạn mức 3 cuốn.</small>
    </div>
    <div class="uv-node pick"><carbon-document-blank class="uv-icon" aria-hidden="true" /><b>0 lần gọi save</b><small>Repository không lưu thêm phiếu.</small>
    </div>
  </div>
</div>

```java
assertCode(LIMIT_REACHED);         // Gọi service.borrow và kiểm tra mã lỗi
verify(loans, never()).save(any());
```

<p class="caption">LoanServiceTest.daDatHanMucBaSach · Cùng đối tượng loans cung cấp số sách và ghi nhận lời gọi lưu phiếu.</p>

<!--
Helper assertCode gọi service.borrow(1, 1) rồi kiểm tra mã lỗi. Việc ghi và đọc dữ liệu thật cần integration testing.
-->

---

# Framework Unit Test theo ngôn ngữ

<div class="langs">
  <div class="pick"><carbon-java class="li" /><b>Java</b>JUnit 5 · TestNG</div>
  <div><carbon-logo-python class="li" /><b>Python</b>pytest · unittest</div>
  <div><ph-file-js class="li" /><b>JavaScript / TypeScript</b>Jest · Vitest</div>
  <div><ph-file-c-sharp class="li" /><b>C# / .NET</b>xUnit · NUnit · MSTest</div>
  <div><ph-file-cpp class="li" /><b>C / C++</b>GoogleTest · Catch2</div>
  <div><ph-file-code class="li" /><b>Go</b>package <code>testing</code> có sẵn</div>
</div>

<p class="note">Case study viết bằng <b>Java</b> (Spring Boot + Maven) → nhóm chọn <b>JUnit 5</b>: phổ biến nhất cho Java, chạy sẵn qua Maven Surefire, JaCoCo đo được ngay</p>

<!--
Mỗi ngôn ngữ có framework Unit Test riêng, nhưng ý tưởng giống nhau: tìm test, chạy test, so sánh kết quả bằng assertion, báo pass/fail.
Nhóm chọn JUnit 5 vì case study viết bằng Java: Spring Boot dùng JUnit 5 mặc định, Maven Surefire chạy được ngay, JaCoCo gắn agent vào cùng lần chạy để đo coverage. TestNG cũng dùng được nhưng ít phổ biến hơn với Spring Boot.
Hai paper ở phần sau làm việc với Python nên sinh test dạng pytest.
-->

---
class: unit-visual
---

<p class="kicker">Unit Testing / JUnit</p>

# JUnit cung cấp những gì? <img class="h-logo" src="/junit5.svg" alt="" />

<div class="grid grid-cols-2 gap-4">
  <div class="uv-node"><b>Test discovery &amp; execution</b><small>JUnit nhận diện phương thức có <code>@Test</code>, chạy từng test và báo pass hoặc fail.</small></div>
  <div class="uv-node"><b>Assertions</b><small><code>assertEquals</code> đối chiếu expected với actual. <code>assertThrows</code> kiểm tra ngoại lệ mong đợi.</small></div>
  <div class="uv-node"><b>Test lifecycle</b><small><code>@BeforeEach</code> chuẩn bị dữ liệu trước mỗi test. <code>@AfterEach</code> dọn dẹp sau mỗi test.</small></div>
  <div class="uv-node"><b>Parameterized tests</b><small>Chạy cùng một phép kiểm tra với nhiều bộ input và expected result, chẳng hạn từ file CSV.</small></div>
</div>

<!--
Trong case study Spring Boot, Maven Surefire chạy bộ test JUnit ở bước test của Maven. Nếu assertion thất bại, báo cáo cho biết test nào lỗi để lập trình viên kiểm tra.
-->

---
class: unit-visual code-lg
---

<p class="kicker">Unit Testing / JUnit</p>

# Viết một unit test bằng JUnit

Thành viên thường trả sách trễ <b>1 ngày</b> phải trả phí <b>2.000 đồng</b>.

```java
package vn.edu.seminar.fine;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class FineCalculatorTest {
    @Test
    void treMotNgayTinhPhiHaiNghinDong() {
        var calculator = new FineCalculator();                   // Arrange
        var fee = calculator.calculate(1, MemberTier.NORMAL);    // Act
        assertEquals(2000, fee.intValueExact());                 // Assert
    }
}
```

<style scoped>
.slidev-layout.code-lg .slidev-code { font-size: .98rem !important; line-height: 1.35 !important; }
</style>

<!--
Chính sách thư viện cho ta expected result là 2.000 đồng. @Test đánh dấu phương thức để JUnit chạy. Trong assertEquals, đối số đầu là expected, đối số sau là actual. Phí là BigDecimal tính bằng đồng nên intValueExact lấy số đồng nguyên. Nếu hàm trả 0, JUnit báo test thất bại với expected 2000 và actual 0.
Ví dụ dùng cùng tình huống nghiệp vụ với FineCalculatorBaselineTest và viết assertion bằng API của JUnit Jupiter.
-->

---
class: video
---

# <span class="vtag">Video A</span> Unit Test với JUnit 5 & Mockito

<div class="vbody">
<a class="play" href="https://youtu.be/5CaBhsgvM-Q" target="_blank"><carbon-play-filled-alt class="icon" /><b>Video A</b><span>06:45</span><small>Nguyễn Bảo An</small><u>youtu.be/5CaBhsgvM-Q</u></a>
<div class="tl">
  <div><time>00:00</time><em>Setup</em><span>Java 25, Maven Wrapper, <code>pom.xml</code></span></div>
  <div><time>01:00</time><em>Khái niệm</em><span>AAA, chạy test, đọc báo cáo Surefire</span></div>
  <div><time>02:15</time><em>Data-driven</em><span><code>@ParameterizedTest</code> + CSV, giá trị biên 0 / VIP 2 ngày / trần 50.000đ</span></div>
  <div><time>03:45</time><em>Phức tạp</em><span>Mockito cô lập 3 repository, <code>verify(never())</code>, <code>ArgumentCaptor</code></span></div>
  <div><time>05:15</time><em>Hạn chế</em><span>Anti-pattern: Train Wreck Mocking, Self-fulfilling Prophecy</span></div>
</div>
</div>

<!--
Video A minh họa phần Unit Test và JUnit: setup, quy tắc AAA, data-driven test với CSV, Mockito cô lập dependency và các anti-pattern khi mock.
-->

---
layout: cover
class: text-left
---

<div class="flex items-center gap-3 mb-6 text-blue-700">
  <carbon-chart-bar class="text-4xl" aria-hidden="true" />
  <span class="kicker">Phần 2 / 5</span>
</div>

# Code Coverage

Đọc báo cáo JaCoCo và đặt coverage gate.

---

# Code Coverage là gì?

<div class="formula">Coverage = <span>số thành phần đã được thực thi</span> ÷ <span>tổng số thành phần đo được</span> × 100%</div>

- "Thành phần" có thể là dòng, câu lệnh, nhánh hoặc phương thức
- Nói "80%" phải nói rõ: **80% line** hay **80% branch**?
- Chạy 8/10 dòng → line 80%, nhưng `if` mới đi hướng đúng → branch vẫn thiếu

<p class="note">Coverage = code <b>đã chạy</b>, không phải code <b>đã đúng</b>: test không có assertion vẫn được tính là đã phủ</p>

<!--
Code Coverage, hay độ phủ mã nguồn, cho biết bộ test đã thực thi phần nào của chương trình. Công thức chung: số thành phần đã thực thi chia tổng số thành phần đo được. Thành phần có thể là dòng, câu lệnh, nhánh hay phương thức, nên khi nói 80% phải nói rõ là 80% line hay 80% branch.
Ví dụ một hàm có 10 dòng, test chạy qua 8 dòng thì line coverage 80%. Nhưng trong 8 dòng đó có thể có một câu if mới chạy hướng đúng, chưa chạy hướng sai — line khá cao mà branch vẫn thiếu.
Coverage trả lời ba câu hỏi: test đã đi qua đâu, dòng hoặc nhánh nào chưa kiểm tra, và thêm test thì phạm vi có tăng không. Coverage không tự đánh giá test đúng hay sai: test không có assertion vẫn được tính là đã phủ.
-->

---
class: cmp
---

# Các loại code coverage

| Loại | Câu hỏi cần trả lời | JaCoCo |
|---|---|:---:|
| Statement | Các câu lệnh đã được thực thi chưa? | <span class="eq">≈</span> |
| Line | Các dòng source đã được chạy chưa? | <span class="good">✓</span> |
| Branch / Decision | Mỗi quyết định đã đi cả hướng đúng và sai chưa? | <span class="good">✓</span> |
| Condition | Mỗi điều kiện con đã nhận cả đúng và sai chưa? | <span class="bad">✕</span> |
| MC/DC | Từng điều kiện con có tự làm đổi kết quả không? | <span class="bad">✕</span> |
| Path | Các đường đi khác nhau qua hàm đã chạy chưa? | <span class="bad">✕</span> |
| Method | Mỗi phương thức đã được gọi ít nhất 1 lần chưa? | <span class="good">✓</span> |

<p class="caption">JaCoCo không đếm câu lệnh mà đếm instruction bytecode (≈). Các slide sau dùng <b>một đoạn code chung</b> để thấy từng loại khác nhau.</p>

<!--
Có bảy loại coverage thường gặp. Statement: mỗi câu lệnh đã chạy chưa. Line: mỗi dòng source đã chạy chưa. Branch hay decision: mỗi quyết định đã đi cả hướng đúng và sai chưa. Condition: mỗi điều kiện con trong biểu thức ghép đã nhận cả đúng và sai chưa. MC/DC: từng điều kiện con có được chứng minh là tự làm đổi kết quả không, hay dùng trong hệ thống an toàn cao. Path: các tổ hợp đường đi qua hàm. Method: mỗi phương thức đã được gọi chưa, đây là chỉ số thô nhất.
Không loại nào mô tả đủ chất lượng bộ test. Line tìm dòng bị bỏ sót, branch và condition kiểm tra logic rẽ nhánh, path cho biết các nhánh kết hợp ra sao.
-->

---

# Line coverage khác Statement coverage

```java
int getDiscount(boolean isVip) {
    int discount = 0; if (isVip) discount = 10;   // 1 dòng, nhiều câu lệnh
    return discount;
}
```

| Test | Line | Statement |
|---|:---:|:---:|
| `isVip = false` → 0 | **100%** | chưa đủ: `discount = 10` chưa chạy |
| thêm `isVip = true` → 10 | 100% | **100%** |

<p class="caption">Ví dụ cố ý đặt nhiều câu lệnh trên một dòng. Code thường viết mỗi câu lệnh một dòng nên hai chỉ số hay gần nhau.</p>

<!--
Ví dụ cố ý đặt hai câu lệnh trên cùng một dòng. Test với isVip = false: dòng thứ hai vẫn chạy vì phải gán discount = 0 và kiểm tra điều kiện, dòng return cũng chạy, nên line coverage 100%.
Nhưng câu lệnh discount = 10 chưa chạy vì isVip đang sai, nên statement coverage chưa đạt 100%. Thêm test isVip = true, mong đợi 10, thì statement mới đủ.
Line quan tâm dòng code, statement quan tâm từng câu lệnh trong dòng đó.
-->

---

# Một code chung cho mọi loại coverage

<div class="ex">
<div>

```java
int calculateDiscount(boolean isMember,
                      boolean hasCoupon) {
    int discount = 0;
    if (isMember && hasCoupon) {
        discount = 20;
    }
    return discount;
}
```
<p class="caption">1 quyết định · 2 điều kiện con · 2 đường đi. Thành viên <b>và</b> có phiếu → giảm 20%.</p>

</div>
<div>

| Test | `isMember` | `hasCoupon` | Kết quả |
|---|:---:|:---:|:---:|
| T1 | true | true | 20 |
| T2 | false | true | 0 |
| T3 | true | false | 0 |
| T4 | false | false | 0 |

</div>
</div>

<!--
Để so các loại coverage trên cùng một code, nhóm dùng hàm calculateDiscount: thành viên và có phiếu giảm giá thì giảm 20%, còn lại không giảm.
Hàm có một quyết định isMember && hasCoupon, hai điều kiện con, hai đường đi là vào hoặc bỏ qua thân if.
T1 cả hai đúng. T2 isMember sai. T3 hasCoupon sai. T4 cả hai sai. Slide sau thêm lần lượt từng test.
-->

---
class: cmp
---

# Thêm từng test case: loại coverage nào tăng?

| Bộ test | Statement | Line | Decision | Condition | MC/DC | Path | JaCoCo branch |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| T1 | **100%** | **100%** | 50% | 2/4 | 0/2 | 1/2 | 50% |
| T1 + T2 | <span class="eq">=</span> | <span class="eq">=</span> | **100%** <span class="up">▲</span> | 3/4 <span class="up">▲</span> | 1/2 <span class="up">▲</span> | **2/2** <span class="up">▲</span> | 75% <span class="up">▲</span> |
| T1 + T2 + T3 | <span class="eq">=</span> | <span class="eq">=</span> | <span class="eq">=</span> | **4/4** <span class="up">▲</span> | **2/2** <span class="up">▲</span> | <span class="eq">=</span> | **100%** <span class="up">▲</span> |
| + T4 | <span class="eq">=</span> | <span class="eq">=</span> | <span class="eq">=</span> | <span class="eq">=</span> | <span class="eq">=</span> | <span class="eq">=</span> | <span class="eq">=</span> |

<p class="note">Chỉ T1 đã đủ <b>line 100%</b> nhưng branch mới 50%. T4 dùng đầu vào mới nhưng đi lại đường sai của T2 nên <b>không chỉ số nào tăng</b>.</p>
<p class="caption">JaCoCo branch chạy thật: 2/4 → 3/4 → 4/4 → 4/4. JaCoCo đếm 4 nhánh vì <code>&&</code> dịch thành 2 lệnh rẽ trong bytecode.</p>

<!--
T1 làm cả hai điều kiện đúng nên mọi dòng và câu lệnh đều chạy: statement và line 100%. Nhưng quyết định mới nhận kết quả đúng nên decision và JaCoCo branch mới 50%.
T2 làm isMember sai, bỏ qua thân if: decision và path lên 100%. Vì Java dừng ngay khi isMember sai (short-circuit) nên hasCoupon chưa được kiểm với giá trị sai, JaCoCo branch mới 75%.
T3 giữ isMember đúng, đổi hasCoupon sai: Java phải đánh giá điều kiện thứ hai. Condition, MC/DC và JaCoCo branch đạt 100%.
T4 cả hai sai: test hợp lệ nhưng đi lại đường T2 đã phủ, các chỉ số không tăng. Số test tăng từ ba lên bốn mà coverage giữ nguyên — dữ liệu khác nhau chưa chắc tạo ra dòng, nhánh hay đường đi mới.
Số JaCoCo nhóm đã chạy thật: 2/4, 3/4, 4/4, 4/4.
-->

---

# Coverage cao **không** chứng minh

- Assertion đã đúng
- Mọi giá trị biên đã kiểm tra
- Các thành phần tích hợp đúng
- Chương trình hết lỗi

<div class="vs">
  <div><span>Test A · coverage 100%</span><code>assertThat(fine).isNotNull()</code><p class="bad">✕ Không bắt được sai số tiền</p></div>
  <div><span>Test B · coverage 100%</span><code>isEqualByComparingTo("6000")</code><p class="good">✓ Bắt được sai số tiền</p></div>
</div>

<p class="kicker mt-5">Gặp coverage gap thì làm gì?</p>
<div class="gapsteps">
  <div><b>1</b>Tìm dòng / nhánh thiếu</div>
  <div><b>2</b>Tìm dữ liệu đi vào đó</div>
  <div><b>3</b>Đối chiếu yêu cầu</div>
  <div><b>4</b>Viết assertion cụ thể</div>
  <div><b>5</b>Chạy lại, đọc báo cáo</div>
</div>

<!--
Hai bộ test có thể cùng coverage nhưng khả năng phát hiện lỗi khác nhau: bộ thứ nhất kiểm tra kết quả chính xác, bộ thứ hai chỉ kiểm tra không rỗng. Cả hai chạy qua cùng dòng và nhánh, nhưng bộ thứ nhất bắt lỗi tốt hơn.
Coverage gap là phần code chưa được thực thi: dòng đỏ, nhánh chưa chạy, hoặc điều kiện con chưa nhận đủ đúng và sai. Khi gặp gap: xác định phần thiếu, đọc điều kiện để biết dữ liệu nào đi vào đó, đối chiếu yêu cầu để biết kết quả mong đợi, viết test với assertion cụ thể, rồi chạy lại và đọc báo cáo mới.
Ví dụ nhánh hasCoupon = false chưa phủ thì thêm test khách không có phiếu, kiểm tra kết quả bằng 0. Chạy qua nhánh làm coverage tăng; assertion mới xác nhận kết quả đúng.
-->

---

# JaCoCo

- JUnit chạy test, JaCoCo ghi lại **bytecode** đã được thực thi
- Báo cáo HTML: <span class="good">xanh</span> đã chạy · <span class="bad">đỏ</span> chưa chạy · <span class="warn">vàng</span> phủ một phần
- Branch đếm theo bytecode: `a && b` thành **4 nhánh**
- Đặt **ngưỡng** trong build → coverage gate

<img class="shot sm" src="/jacoco-summary.png" alt="Báo cáo JaCoCo của library-case-study" />

<!--
JaCoCo đo Code Coverage cho Java. JUnit chạy test và kiểm tra assertion, còn JaCoCo theo dõi phần code được thực thi trong lúc đó. Quy trình: Maven khởi động JUnit, JaCoCo ghi nhận bytecode đã chạy, tổng hợp theo package, lớp, phương thức, dòng, rồi tạo báo cáo HTML.
Màu xanh là đã chạy, đỏ là chưa, vàng là dòng có điều kiện mới phủ một phần; ở câu if báo cáo còn ghi số nhánh đã phủ.
Nhóm quan tâm line và branch. Vì JaCoCo đếm branch từ bytecode, biểu thức C1 && C2 cho 4 nhánh chứ không phải 2 như cách đếm decision ở source — đúng như ví dụ T1–T4.
JaCoCo còn kiểm tra ngưỡng trong lúc build: thấp hơn ngưỡng thì Maven báo thất bại. Đó là coverage gate.
-->

---

# Coverage gate

<div class="gate">
  <div class="ok">Branch 92% ≥ 90% → build tiếp tục</div>
  <div class="fail">Branch 85% &lt; 90% → build đỏ, dù test vẫn xanh</div>
</div>

- Case study: `FineCalculator` **branch ≥ 90%**, chỉ đặt cho lớp nghiệp vụ quan trọng
- Bắt được: thêm nhánh mới mà không thêm test, hoặc lỡ xóa test
- Gate **không** tự viết test, không biết expected và assertion đúng hay sai

```xml
<include>vn.edu.seminar.fine.FineCalculator</include>
<counter>BRANCH</counter><value>COVEREDRATIO</value><minimum>0.90</minimum>
```
<p class="caption">Luật gate trong <code>case-study/pom.xml</code></p>

<!--
Coverage gate là điều kiện trong build: đạt ngưỡng thì build tiếp tục, không đạt thì build thất bại. Ví dụ gate 90%: 92% được chấp nhận, 85% làm build đỏ — dù Unit Test vẫn xanh, vì test xanh chỉ nói các tình huống đã viết cho đúng kết quả, còn gate hỏi bộ test đã đi qua đủ nhánh chưa.
Gate phát hiện thay đổi thêm nhánh mà không thêm test, hoặc test quan trọng bị xóa. Build đỏ thì mở báo cáo, tìm nhánh thiếu, đối chiếu yêu cầu.
Không có ngưỡng chung cho mọi dự án. Nhóm đặt branch FineCalculator tối thiểu 90%, nơi sai sót ảnh hưởng trực tiếp đến tiền phí. Gate không thay review code và review test case.
-->

---
class: video
---

# <span class="vtag">Video B</span> Code Coverage & PIT Mutation Testing

<div class="vbody">
<a class="play" href="https://youtu.be/DbqXRK-PThA" target="_blank"><carbon-play-filled-alt class="icon" /><b>Video B</b><span>08:35</span><small>Trương Nhật Đạt</small><u>youtu.be/DbqXRK-PThA</u></a>
<div class="tl">
  <div><time>00:00</time><em>Setup</em><span>JaCoCo agent và PIT trong <code>pom.xml</code></span></div>
  <div><time>01:00</time><em>Khái niệm</em><span>6 loại coverage trên <code>LoanPeriodPolicy</code> (Statement, Decision, MC/DC)</span></div>
  <div><time>03:00</time><em>Đơn giản</em><span>Trước / sau: branch 50% → 100%</span></div>
  <div><time>04:00</time><em>Phức tạp</em><span>Gate fail exit 1; test bẫy 100% branch nhưng PIT chỉ diệt 3/11 mutant</span></div>
  <div><time>06:00</time><em>Hạn chế</em><span>Quyết định ẩn trong <code>Math.min()</code>, mutant tương đương, chi phí PIT</span></div>
</div>
</div>

<!--
Video B minh họa Code Coverage, JaCoCo và coverage gate. Điểm nhấn: test bẫy đạt 100% branch nhưng PIT chỉ diệt 3/11 mutant, đúng thông điệp coverage cao chưa chứng minh test tốt.
-->

---
layout: cover
class: text-left
---

<div class="flex items-center gap-3 mb-6 text-blue-700">
  <carbon-flow class="text-4xl" aria-hidden="true" />
  <span class="kicker">Phần 3 / 5</span>
</div>

# CI/CD

Chạy test, kiểm tra gate và đóng gói với GitHub Actions.

---

# CI/CD với GitHub Actions

<img class="shot pipeline-shot" src="/github-actions-pipeline.png" alt="Pipeline Seminar CI trên GitHub Actions" />

<div class="gate-config-evidence">
  <img src="/coverage-gate-config.png" alt="Cấu hình JaCoCo coverage gate cho FineCalculator" />
  <span><b>Gate đã cấu hình trong Maven</b><code>FineCalculator</code> phải đạt branch covered ratio ≥ <strong>90%</strong>; thấp hơn thì build thất bại.</span>
</div>

<div class="pipeline-notes">
  <span><b>Luồng bắt buộc</b> test → coverage gate → package</span>
  <span><b>Chạy song song</b> Gemini review diff và kiểm tra AI offline</span>
  <span><b>Điểm dừng</b> đóng gói artifact, chưa tự deploy</span>
</div>

<!--
Ảnh là một run thật của Seminar CI. Nhánh chính chạy JUnit, coverage gate và package theo thứ tự; Gemini review diff chạy song song rồi hội tụ vào job tổng hợp.
Ảnh cấu hình cho thấy JaCoCo kiểm riêng FineCalculator với counter BRANCH, value COVEREDRATIO và minimum 0.90. Test lỗi hoặc coverage không đạt thì build thất bại và package không hoàn tất. Nhóm dừng ở Continuous Delivery: tạo artifact có thể phát hành, chưa tự triển khai lên môi trường thật.
-->

---
class: video
---

# <span class="vtag">Video D</span> CI/CD pipeline với GitHub Actions

<div class="vbody">
<a class="play" href="https://youtu.be/vakw7UD_SvU" target="_blank"><carbon-play-filled-alt class="icon" /><b>Video D</b><span>08:45</span><small>Phạm Quang Vinh</small><u>youtu.be/vakw7UD_SvU</u></a>
<div class="tl">
  <div><time>00:00</time><em>Setup</em><span><code>ci.yml</code>, runner <code>ubuntu-latest</code>, Temurin JDK 25</span></div>
  <div><time>01:00</time><em>Khái niệm</em><span>3 job nối bằng <code>needs</code>: test → coverage-gate → package</span></div>
  <div><time>02:15</time><em>Đơn giản</em><span>Run xanh, đọc log, tải artifact JAR và Surefire report</span></div>
  <div><time>04:00</time><em>Phức tạp</em><span>PR đỏ vì thiếu coverage, branch protection chặn nút merge</span></div>
  <div><time>06:30</time><em>Hạn chế</em><span>Cache miss khi sửa <code>pom.xml</code>, runner jitter trên cloud</span></div>
</div>
</div>

<!--
Video D minh họa pipeline GitHub Actions: cấu hình workflow, 3 job, một run xanh, một PR đỏ bị chặn merge, và các sự cố thực tế như cache miss.
-->

---
layout: cover
class: text-left
---

<div class="flex items-center gap-3 mb-6 text-blue-700">
  <carbon-idea class="text-4xl" aria-hidden="true" />
  <span class="kicker">Phần 4 / 5</span>
</div>

# AI trong Unit Testing

Pynguin, CoverUp và quy trình sinh test của nhóm.

---
layout: section
---

<p class="kicker">Research paper</p>

# Nghiên cứu về sinh Unit Test tự động

Hai công trình đã công bố, chạy lại bằng source code của tác giả. <br>
Thử nghiệm AI riêng của nhóm nằm ở phần sau, tách biệt với hai paper này.

<!--
Phần này trình bày hai công trình nghiên cứu đã công bố về sinh Unit Test tự động. Nhóm không tự cài đặt lại paper mà dùng source của tác giả: chạy lại kết quả công bố, rồi thử trên code thực tế của nhóm.
Đây không phải tính năng AI của nhóm; quy trình AI riêng của nhóm cho Java được trình bày sau, như một thử nghiệm độc lập.
-->

---

# Paper 2023 · Pynguin: thuật toán tìm kiếm

<p class="cite">Lukasczyk, Kroiß & Fraser, <i>An empirical study of automated unit test generation for Python</i> <span class="rank">EMSE 2023 · CORE A</span></p>

<div class="paper-process">
  <div><b>1 · Phân tích module</b><span>Đọc API, type hints, hằng số và dependency để tạo input ban đầu.</span></div>
  <div><b>2 · Tiến hóa test</b><span>DynaMOSA tạo, đột biến và kết hợp nhiều test candidate.</span></div>
  <div><b>3 · Thực thi & đo</b><span>Chạy candidate trên code đã instrument; mỗi nhánh chưa phủ là một mục tiêu.</span></div>
  <div><b>4 · Chọn & lặp</b><span>Ưu tiên test tiến gần nhánh mục tiêu; assertion ghi lại output quan sát được.</span></div>
</div>

<div class="stats">
  <div><span>1 module Python benchmark: <code>codetiming._timers</code></span><b>81,48%</b><small>Thuộc thư viện CodeTiming · Pynguin sinh 10 test pass, 5 xfail</small></div>
  <div><span>1 module Python của nhóm</span><b>23,6% → 23,6%</b><small>Baseline → sau Pynguin · filesystem và XML · không cải thiện</small></div>
</div>

<p class="paper-weakness"><b>Nhược điểm của Pynguin:</b> Phụ thuộc ngân sách tìm kiếm; input có cấu trúc và oracle nghiệp vụ khó sinh tự động.</p>
<p class="paper-limit"><b>Vì sao chưa đạt 100%?</b> DynaMOSA chưa khám phá hết các đường đi trong ngân sách 600 giây; module nhóm còn yêu cầu tạo đúng cả đường dẫn và cấu trúc XML.</p>

<!--
Trình bày theo năm xuất bản để không nhầm "paper thứ nhất, thứ hai" với các bước AI của nhóm.
Paper 2023 của Lukasczyk, Kroiß và Fraser đăng trên tạp chí Empirical Software Engineering. Venue hạng A theo bảng CORE2020 — đây là hạng lịch sử của venue, không phải hạng riêng của paper.
Pynguin không dùng LLM. DynaMOSA là thuật toán tìm kiếm tiến hóa nhiều mục tiêu động: mỗi nhánh chưa phủ là một mục tiêu; tool liên tục sinh, đột biến, kết hợp và thực thi candidate, sau đó ưu tiên test có branch distance tốt hơn. Khi đã có chuỗi lệnh, Pynguin quan sát output để thêm assertion, nên assertion vẫn có thể khóa hành vi hiện tại thay vì đặc tả đúng.
Nhóm chạy mới đúng một module Python benchmark là codetiming._timers thuộc thư viện CodeTiming. Một seed 600 giây đạt coverage nội bộ 81,48%, 10 test pass và 5 xfail.
Khi thử trên một module Python của nhóm chuyên đọc file JaCoCo XML, tool phải tạo đồng thời đường dẫn tồn tại và cấu trúc XML hợp lệ. Lượt có seed đạt 23,6% nhưng không tăng so với smoke baseline. Đây là giới hạn trên một module có structured input, không phải kết luận Pynguin luôn kém hiệu quả.
-->

---

# Paper 2025 · CoverUp

<p class="cite">Pizzorno & Berger, <i>CoverUp: Effective High Coverage Test Generation for Python</i> <span class="rank">FSE 2025 · CORE A* (CORE2023)</span></p>

<div class="paper-process">
  <div><b>1 · Đo baseline</b><span>Chạy pytest và SlipCover để tìm chính xác dòng, nhánh chưa phủ.</span></div>
  <div><b>2 · Tạo prompt hẹp</b><span>Gửi source liên quan, test hiện có và coverage gap cho LLM.</span></div>
  <div><b>3 · Sinh & kiểm</b><span>LLM viết pytest; CoverUp chạy test, lấy lỗi và coverage mới.</span></div>
  <div><b>4 · Phản hồi vòng lặp</b><span>Giữ test tăng coverage; sửa hoặc sinh tiếp đến khi hết gap hay ngân sách.</span></div>
</div>

<div class="stats three">
  <div><span>Dữ liệu công bố · toàn bộ 163 module</span><b>89,0%</b><small>CoverUp GPT-4o · coverage line+branch gộp; MuTAP 76,8%</small></div>
  <div><span>1/163 module Python benchmark: <code>f003</code></span><b>100%</b><small>Một bài nhỏ trong bộ HumanEval/MT · Gemini sinh 3 test pass</small></div>
  <div><span>1 module Python của nhóm</span><b>23,6% → 96,4%</b><small>Baseline → sau CoverUp + Gemini · 7 test pass</small></div>
</div>

<p class="paper-limit"><b>Vì sao kết quả tổng chỉ 89%?</b> Trên 163 module, một số prompt không tạo được test hợp lệ hoặc còn trạng thái/nhánh khó kích hoạt trong ngân sách. Module nhóm dừng ở 96,4% vì phần còn thiếu là entrypoint CLI, không chạy khi Unit Test import module.</p>

<!--
Paper 2025 của Pizzorno và Berger công bố tại FSE 2025 (PACMSE). FSE hạng A* theo CORE2023, cũng là hạng của venue.
CoverUp dùng coverage để thu hẹp prompt thay vì yêu cầu LLM viết toàn bộ test một lần. Tool chạy pytest bằng SlipCover, xác định dòng và nhánh chưa phủ, gửi đoạn source liên quan cùng test hiện có cho LLM, rồi chạy test mới. Lỗi cú pháp, lỗi runtime và coverage mới trở thành phản hồi cho vòng sửa hoặc sinh tiếp. Chỉ test hợp lệ và giúp tăng coverage mới được giữ.
Nhóm phân tích lại dữ liệu tác giả công bố của toàn bộ 163 module: CoverUp dùng GPT-4o đạt 89,0% line+branch gộp, MuTAP đạt 76,8%. Bước này không gọi Gemini và không sinh lại 163 bộ test. Không đạt 100% vì một số module không có test hợp lệ hoặc còn nhánh khó kích hoạt trong ngân sách.
Nhóm chạy mới CoverUp với Gemini 3.6 Flash trên đúng một module Python benchmark f003, một bài nhỏ thuộc bộ HumanEval/MT. Ba test pass đạt 100% line và branch coverage. Trên một module Python của nhóm đọc file XML, 7 test pass và coverage gộp 96,4%; phần thiếu là khối CLI chỉ chạy khi gọi file trực tiếp, còn Unit Test import module.
-->

---
layout: section
---

<p class="kicker">Áp dụng của nhóm</p>

# Ứng dụng AI trong Unit Testing

Dùng ý tưởng coverage feedback của <b>Paper 2025</b> và triển khai với <b>LLM</b>. <br>
Mỗi tính năng có đầu vào, bằng chứng chạy và điểm dừng để người thực hiện review.

<!--
Nhóm kế thừa ý tưởng dùng coverage làm phản hồi của Paper 2025, không cài đặt lại CoverUp. Pipeline nhận module mục tiêu cùng source dependency liên quan, chạy test trong project tạm và chỉ chấp nhận sau khi người thực hiện review.
-->

---

# Các tính năng AI hỗ trợ kiểm thử

<div class="ai-features">
  <div><b>Sinh test từ source</b><span>Đọc module mục tiêu, dependency và yêu cầu; LLM sinh Unit Test nháp rồi chạy kiểm chứng.</span></div>
  <div><b>Bổ sung theo coverage</b><span>Đọc test nháp, kết quả JUnit và JaCoCo gaps; đề xuất test còn thiếu mà không xóa baseline.</span></div>
  <div><b>Review pull request</b><span>Review diff test song song với CI và đăng nhận xét tư vấn; không tự sửa hay merge.</span></div>
  <div><b>Sinh & đối chứng dữ liệu biên</b><span>Sinh bộ ca biên, chạy cùng JUnit harness và so với bộ người lập đã khóa trước.</span></div>
</div>

<p class="review-rule"><b>Quy tắc chung:</b> AI đề xuất; JUnit và coverage cung cấp bằng chứng; con người chịu trách nhiệm expected result và assertion.</p>

<!--
Tính năng sinh test đọc một class mục tiêu cùng dependency production liên quan. Bước bổ sung nhận chính test nháp, kết quả chạy và coverage gap. Review pull request chỉ nhận xét diff song song với CI. Phần dữ liệu biên sinh test case rồi đối chứng với bộ người lập bằng cùng test harness.
Các bước chạy tự động không chứng minh expected result đúng. Người thực hiện vẫn review input, oracle và assertion trước khi áp dụng.
-->

---

# Triển khai trên `FineCalculator`

<div class="fact">
  <span>70%</span><em>→</em><span class="hl">100%</span>
</div>
<p class="center-label">branch coverage của lượt triển khai</p>

- Sinh test nháp: Gemini viết 3 test, chạy xanh nhưng branch chỉ 70%
- Bổ sung theo coverage gap: thêm ngày âm, hạng rỗng, nhánh VIP còn thiếu
- Người thực hiện kiểm tra input, expected, assertion trước khi nhận

<!--
Lượt triển khai được quay sẵn để không phụ thuộc mạng và hạn mức API.
Gemini nhận source và quy tắc tính phí, sinh ba test nháp. Các test chạy xanh nhưng branch chỉ 70%. Gemini nhận thêm báo cáo JaCoCo, đề xuất test cho ngày âm, hạng thành viên rỗng và nhánh VIP còn thiếu. Sau khi bổ sung, branch của lượt triển khai đạt 100%. Người thực hiện kiểm tra input, expected result và assertion trước khi chấp nhận test.
-->

---

# Review pull request cùng CI

<div class="ai-review-evidence">
  <img class="shot" src="/ai-pr-review-comment.png" alt="GitHub Actions bot đăng kết quả Gemini review trên pull request" />
  <div>
    <b>Comment hợp nhất hai nguồn bằng chứng</b>
    <span>JUnit và JaCoCo báo số đo thực tế; Gemini nhận xét phần diff được gửi.</span>
    <b>Vai trò tư vấn</b>
    <span>Nhận xét AI không thay required checks, không tự sinh, sửa hoặc merge test.</span>
  </div>
</div>

<!--
Ảnh là comment do GitHub Actions bot đăng trên pull request. Phần đầu lấy từ các job CI: 49 test pass, line 76/83 và branch 24/24. Phần sau là nhận xét Gemini về diff.
Trong lượt này Gemini không nêu finding. Điều đó không chứng nhận code hoàn toàn đúng; AI chỉ review phần diff đã gửi và không thay thế JUnit, coverage gate hay review của con người.
-->

---
class: video
---

# <span class="vtag">Video E</span> Demo 4 tính năng AI

<div class="vbody">
<a class="play" href="https://youtu.be/fLtNeE-MSw4" target="_blank"><carbon-play-filled-alt class="icon" /><b>Video E</b><span>09:15</span><small>Ngô Gia An</small><u>youtu.be/fLtNeE-MSw4</u></a>
<div class="tl">
  <div><time>00:00</time><em>Sinh test</em><span>Đọc module và sinh Unit Test nháp từ source</span></div>
  <div><time>01:30</time><em>Coverage</em><span>Đọc coverage gap và bổ sung test còn thiếu</span></div>
  <div><time>03:45</time><em>PR review</em><span>Review diff test và đăng nhận xét trên pull request</span></div>
  <div><time>05:30</time><em>Dữ liệu biên</em><span>Sinh và đối chứng bộ test case với bộ người lập</span></div>
</div>
</div>

<!--
Video E chỉ minh họa bốn tính năng AI của nhóm: sinh test từ source, bổ sung theo coverage, review pull request, và sinh rồi đối chứng dữ liệu biên.
-->

---

# Kết luận

<div class="conclusion-list">
  <ul>
    <li><b>Unit Test:</b> cần dữ liệu phù hợp và assertion cụ thể.</li>
    <li><b>Coverage và quality gate:</b> giúp phát hiện và chặn phần mã bị bỏ sót.</li>
    <li><b>GitHub Actions:</b> tự động kiểm tra mỗi thay đổi trong quy trình CI/CD.</li>
    <li><b>AI:</b> hỗ trợ đề xuất test, nhưng con người vẫn cần review kết quả.</li>
  </ul>
</div>

<div class="answer">Test xanh và coverage 100% <b>vẫn chưa đủ</b> để kết luận chương trình đúng.</div>

<!--
Kết luận: Unit Test cần test case và assertion tốt; coverage và gate tìm phần bị bỏ sót; GitHub Actions tự động hóa; AI chỉ đề xuất và không thay review của con người.
-->

---
layout: cover
class: text-left
---

<div class="flex items-center gap-3 mb-6 text-blue-700">
  <carbon-book class="text-4xl" aria-hidden="true" />
  <span class="kicker">Phần 5 / 5</span>
</div>

# Case study thư viện, Lab &amp; Q&amp;A

Tính phí trả sách trễ, thực hành mutation testing và hỏi đáp.

---

# Case study: phí trả sách trễ

<div class="case">
<div>

| Trường hợp | Quy tắc |
|---|---|
| Thường | **2.000đ** / ngày trễ |
| VIP | Miễn 2 ngày đầu, rồi **1.000đ** / ngày |
| Mọi hạng | Tối đa **50.000đ** |
| Ngày âm / hạng rỗng | **Bị từ chối** |

</div>
<img src="/library-books.jpg" alt="Kệ sách thư viện" />
</div>

<!--
Ứng dụng quản lý thư viện; demo tập trung vào lớp FineCalculator tính phí trả sách trễ.
Lớp này có nhiều nhánh và giá trị biên rõ ràng: hạng thành viên, thời gian miễn phí của VIP, mức trần 50.000đ, và hai loại dữ liệu không hợp lệ.
-->

---
class: video
---

# <span class="vtag">Video C</span> Case study & 7 kịch bản HTTP

<div class="vbody">
<a class="play" href="https://youtu.be/Wco_4852snM" target="_blank"><carbon-play-filled-alt class="icon" /><b>Video C</b><span>04:30</span><small>Nguyễn Lê Thế Vinh</small><u>youtu.be/Wco_4852snM</u></a>
<div class="tl">
  <div><time>00:00</time><em>Setup</em><span>Chạy JAR trên OpenJDK 25, dữ liệu mẫu H2 in-memory</span></div>
  <div><time>01:00</time><em>Demo</em><span>7 request curl: 201, 409 UNAVAILABLE, 404, 409 UNPAID_FINE</span></div>
  <div><time>03:30</time><em>Đối chiếu</em><span><code>LoanFlowEdgeCaseTest</code> khớp 100% kết quả HTTP thực tế</span></div>
</div>
</div>

<!--
Video C chạy ứng dụng thư viện thật và gửi 7 request HTTP, sau đó đối chiếu với test tự động LoanFlowEdgeCaseTest.
-->

---

# Lab: Coverage & Mutation Testing · 30 phút

<div class="steps">
  <div><b>1</b>Use this template, clone về, <code>./mvnw clean verify</code></div>
  <div><b>2</b>Bài 1: điền giá trị biên vào <code>fine-cases.csv</code></div>
  <div><b>3</b>Bài 2: viết test Mockito để qua gate 100% branch</div>
  <div><b>4</b>Chạy PIT, tìm lỗi cài sẵn, nộp <code>REPORT.md</code></div>
</div>

| Bài | Học được |
|---|---|
| **1** | Phân tích giá trị biên, test data-driven bằng CSV |
| **2** | Đọc báo cáo JaCoCo, mock, coverage gate, mutation testing |

<p class="note">Repo: <b>github.com/tzin1401/seminar-lab-nhom09</b> · cần JDK 17+ · lab bắt đầu ở trạng thái <b>đỏ</b>, push lên thì CI chạy lại</p>

<!--
Lab dùng lại FineCalculator và LoanService của case study, bỏ Spring Boot để chỉ cần JDK 17 trở lên là chạy được.
Bài 1: thay 8 dấu ? trong CSV bằng số tiền tính tay theo đặc tả (24/25/26 ngày NORMAL; 2/3/51/52/53 ngày VIP).
Bài 2: gate ban đầu báo 0.66 (4/6 nhánh); viết 2 test LIMIT_REACHED và UNPAID_FINE cho đủ 100%.
Nộp: link repo tạo từ template, REPORT.md đã điền, tab Actions có dấu xanh.
-->

---

# Lab · Gate xanh nhưng vẫn còn lỗi

<div class="vs">
  <div><span>Test <code>count = 4</code> · branch 100%, gate xanh</span><code>if (count > 3) → LIMIT_REACHED</code><p class="bad">✕ PIT 8/9: mutant <code>></code> → <code>>=</code> sống sót</p></div>
  <div><span>Test đúng biên <code>count = 3</code></span><code>if (count >= 3) → LIMIT_REACHED</code><p class="good">✓ Test đỏ, lộ lỗi; sửa xong thì PIT 9/9</p></div>
</div>

<div class="answer">Đặc tả: <b>đang mượn 3 cuốn thì không được mượn thêm</b>. Code cài sẵn lỗi <b>&gt; 3</b>; test ở giá trị 2 và 4 vẫn phủ đủ nhánh nhưng không chạm biên 3. Coverage cho biết code <b>đã chạy</b>, PIT cho biết test <b>có kiểm đúng không</b>.</div>

<!--
Đây là điểm nhấn của lab. Phần lớn học viên sẽ viết test với count = 4: build xanh, coverage 100%. Khi chữa bài, hỏi cả lớp "vậy là hết lỗi chưa?", sau đó chạy PIT.
PIT đổi > thành >=; với count 2 và 4 hai phiên bản cho cùng kết quả nên mutant sống sót. Thêm test count = 3 thì test đỏ; đối chiếu đặc tả thấy lỗi ở code, sửa thành >= 3, PIT diệt 9/9 mutant.
Đáp án nằm trên nhánh dap-an trong repo lab ở máy Vinh, không đưa lên GitHub.
-->

---
layout: center
class: text-center
---

# Hỏi đáp

Cảm ơn thầy cô và các bạn đã lắng nghe

<!--
Câu hỏi dự kiến:
- Có nên đặt coverage 100%? Không nhất thiết; ngưỡng dựa trên mức quan trọng và khả năng kiểm thử của từng phần.
- Coverage cao thay review test được không? Không; vẫn phải kiểm tra dữ liệu, assertion và liên hệ với yêu cầu.
- Vì sao gate chỉ cho FineCalculator? Lớp nhiều quy tắc, giá trị biên rõ; gate theo lớp giúp tập trung vào code nghiệp vụ quan trọng.
- Công cụ sinh test thay người viết test được không? Chưa; nó tạo input và tăng coverage, nhưng con người xác định kết quả đúng và kiểm tra assertion.
-->

---
class: refs
---

# Tài liệu tham khảo

- Pizzorno & Berger, *CoverUp: Effective High Coverage Test Generation for Python*, FSE 2025 — doi.org/10.1145/3729398
- Lukasczyk, Kroiß & Fraser, *An empirical study of automated unit test generation for Python*, EMSE 2023 — doi.org/10.1007/s10664-022-10248-w
- JUnit User Guide — docs.junit.org
- JaCoCo Documentation — jacoco.org/jacoco/trunk/doc
- CORE2023 (FSE) · CORE2020 (Empirical Software Engineering) — portal.core.edu.au
- GitHub Actions: Java with Maven — docs.github.com/actions
