# Nội dung thuyết trình: Unit Test, Code Coverage và CI/CD

Thời lượng dự kiến: 30 phút, gồm phần trình bày, demo ngắn và research paper.

Đây là lời thuyết trình đầy đủ. Khi làm slide, chỉ lấy tiêu đề, ý chính, sơ đồ và số liệu cần thiết.

## 1. Giới thiệu

> Một cửa hàng online miễn phí giao hàng từ 200.000 đồng. Sau khi sửa code, mình thử đơn 250.000 đồng và thấy phí bằng 0. Nếu khách mua đúng 200.000 đồng thì sao? Một lần thử thành công cho mình biết được bao nhiêu về các trường hợp còn lại?

Trong quá trình phát triển phần mềm, một thay đổi nhỏ cũng có thể làm hỏng chức năng đang hoạt động. Kiểm tra thủ công sau mỗi lần sửa vừa tốn thời gian, vừa khó lặp lại. Unit Test giúp biến những kiểm tra đó thành các test case có thể chạy tự động.

Nhưng khi toàn bộ test đều xanh, chúng ta vẫn chưa biết bộ test đã đi qua hết các nhánh xử lý hay chưa. Code Coverage giúp trả lời câu hỏi này. Từ số liệu coverage, nhóm có thể tạo coverage gate để build thất bại nếu độ phủ thấp hơn ngưỡng yêu cầu.

Bài trình bày tập trung vào Unit Test, Code Coverage và coverage gate trong CI/CD. Ba công cụ được sử dụng là JUnit, JaCoCo và GitHub Actions.

Câu hỏi chính của bài là:

> Test xanh và coverage đạt 100% có chắc chương trình đã đúng không?

## 2. Unit Test

### 2.1. Unit Test là gì?

Unit Test kiểm tra một phần nhỏ của chương trình, thường là một hàm, phương thức hoặc lớp có trách nhiệm rõ ràng. Mỗi test tập trung vào một hành vi và so sánh kết quả thực tế với kết quả mong đợi.

Phạm vi test cần đủ nhỏ để khi thất bại, người phát triển có thể tìm nguyên nhân nhanh. Một test phải khởi động toàn bộ ứng dụng, gọi nhiều dịch vụ và dùng cơ sở dữ liệu thật thường không còn là Unit Test thuần túy.

Unit Test kiểm tra tốt logic cục bộ nhưng không thay thế integration test. Integration test vẫn cần thiết để xác nhận các thành phần thật kết nối đúng với nhau.

Trong ví dụ cửa hàng, khi gọi riêng hàm tính phí giao hàng, hàm đó là SUT (System Under Test), tức phần được kiểm thử. Nếu muốn kiểm tra trang thanh toán có nhận đúng phí và lưu đúng tổng tiền, có thể dùng integration test để chạy các thành phần đó cùng nhau.

### 2.2. Unit Test mang lại lợi ích gì?

Unit Test giúp phát hiện lỗi sớm. Khi một thay đổi làm sai hành vi đã được kiểm tra, test báo lỗi ngay trong quá trình phát triển.

Bộ test cũng giúp việc sửa code an toàn hơn. Lập trình viên có thể thay đổi cách cài đặt bên trong rồi chạy lại test để kiểm tra các hành vi cũ.

Tên test, dữ liệu và assertion còn mô tả chương trình phải xử lý một tình huống như thế nào. Khi một test nhỏ thất bại, phạm vi tìm lỗi thường hẹp hơn so với kiểm thử toàn hệ thống.

### 2.3. Arrange, Act, Assert

Một Unit Test thường có ba bước:

1. Arrange: chuẩn bị đối tượng, dữ liệu và các thành phần mà đối tượng cần sử dụng (dependency).
2. Act: thực hiện hành vi cần kiểm tra.
3. Assert: so sánh kết quả thực tế với kết quả mong đợi.

Assertion quyết định test có phát hiện được sai lệch hay không. Ví dụ, kiểm tra kết quả "không rỗng" chưa đủ nếu yêu cầu là phải trả về chính xác 6.000 đồng. Assertion cần bám vào kết quả nghiệp vụ cụ thể.

Với đơn đúng 200.000 đồng, Arrange là chuẩn bị tổng tiền 200.000 đồng, Act là gọi hàm tính phí giao hàng, Assert là kiểm tra phí trả về bằng 0. Nếu hàm trả nhầm 20.000 đồng, phép so sánh với 0 sẽ làm test thất bại.

### 2.4. Một Unit Test tốt cần gì?

Một Unit Test tốt nên:

- Kiểm tra một hành vi rõ ràng.
- Chạy nhanh và có thể chạy lại nhiều lần.
- Không phụ thuộc vào thứ tự của test khác.
- Cho cùng kết quả với cùng code và dữ liệu.
- Có tên mô tả tình huống và kết quả mong đợi.
- Thất bại khi quy tắc nghiệp vụ bị làm sai.

Test có thể chứa nhiều assertion nếu chúng cùng kiểm tra một kết quả. Chẳng hạn, sau khi tạo phiếu mượn, test có thể kiểm tra mã sách, mã thành viên và thời điểm mượn.

### 2.5. Chọn test case

Test case nên xuất phát từ yêu cầu, điều kiện và giới hạn của chức năng. Các nhóm chính gồm:

- Trường hợp hoạt động bình thường.
- Giá trị biên.
- Dữ liệu không hợp lệ.
- Trường hợp rỗng hoặc không tồn tại.
- Trường hợp đạt hoặc vượt giới hạn.

Nếu một quy tắc thay đổi tại giá trị 25, nên kiểm tra 24, 25 và 26. Ba giá trị này đại diện cho ngay trước, tại và sau ranh giới. Chúng dễ phát hiện lỗi dùng sai toán tử so sánh.

> Đơn dưới 200.000 đồng trả phí cố định 20.000 đồng. Nếu muốn kiểm tra đúng chỗ bắt đầu miễn phí, mình sẽ chọn những đơn nào?

| Tình huống | Tổng tiền | Phí mong đợi |
|---|---:|---:|
| Ngay dưới ngưỡng | 199.999 đồng | 20.000 đồng |
| Đúng ngưỡng | 200.000 đồng | 0 đồng |
| Ngay trên ngưỡng | 200.001 đồng | 0 đồng |

Ca đúng ngưỡng phân biệt được điều kiện “từ 200.000 đồng” với “trên 200.000 đồng”.

Khi nhiều test có cùng cách thực hiện và chỉ khác dữ liệu, có thể dùng data-driven testing. Một test được chạy nhiều lần với các bộ đầu vào và kết quả mong đợi khác nhau. Cách này giảm code lặp và giúp các giá trị biên dễ quan sát hơn.

### 2.6. Mock

Một service thường cần repository hoặc dịch vụ khác để hoạt động. Các thành phần đó được gọi là dependency. Mock thay dependency thật bằng một đối tượng do test kiểm soát. Nhờ vậy, test có thể tạo đúng tình huống cần kiểm tra mà không truy cập cơ sở dữ liệu thật.

> Muốn kiểm tra chức năng đặt hàng khi sản phẩm hết hàng, mình có phải sửa tồn kho thật về 0 mỗi lần chạy test không?

Trong Java, có thể dùng Mockito để tạo đối tượng quản lý kho giả và cho nó trả về số lượng 0. Sau đó gọi chức năng đặt hàng với yêu cầu mua một sản phẩm. Test cần kiểm tra chức năng báo hết hàng và chưa gọi thao tác lưu đơn. Dữ liệu tồn kho do test chủ động chuẩn bị.

Mock có giới hạn. Nếu đối tượng giả hoạt động khác hệ thống thật, Unit Test vẫn có thể xanh trong khi ứng dụng lỗi. Các luồng quan trọng cần thêm integration test để kiểm tra sự phối hợp giữa các thành phần.

## 3. Công cụ JUnit

JUnit là framework dùng để viết và chạy test trong Java. Nó giúp test runner tìm test case, thực hiện từng test và ghi nhận kết quả thành công hoặc thất bại.

JUnit cung cấp assertion để so sánh kết quả thực tế với kết quả mong đợi. Nó cũng hỗ trợ parameterized test, cho phép cùng một test chạy với nhiều dòng dữ liệu, chẳng hạn dữ liệu đọc từ CSV.

Ba đơn hàng sát ngưỡng miễn phí có thể trở thành ba dòng CSV. Mỗi dòng gồm tổng tiền và phí mong đợi. JUnit chạy cùng một phép so sánh với từng dòng, nên khi thất bại có thể biết chính xác đầu vào nào gặp lỗi.

Nhóm chọn JUnit vì công cụ tích hợp tốt với Maven và Spring Boot. Trong bài này, JUnit đại diện cho bước viết và chạy Unit Test. Nhóm không đi sâu vào toàn bộ annotation hoặc API của framework.

## 4. Code Coverage

### 4.1. Code Coverage là gì?

Code Coverage cho biết phần code nào đã được thực thi khi chạy bộ test. Coverage trả lời câu hỏi "test đã chạy qua đâu?", nhưng không xác nhận kết quả đã được kiểm tra đúng.

Một dòng code được chạy chỉ chứng minh chương trình đã đi qua dòng đó. Nếu test không có assertion phù hợp, lỗi vẫn có thể bị bỏ sót.

Coverage được tính bằng số đơn vị đã thực thi chia cho tổng số đơn vị đo được, rồi nhân 100%. Đơn vị có thể là dòng, nhánh hoặc phương thức. Ví dụ, chạy 8 trong số 10 dòng có thể thực thi thì line coverage là 80%. Khi trình bày số liệu, cần nói rõ đang đo chỉ số gì và đo trên phạm vi nào.

### 4.2. Line coverage và branch coverage

Line coverage cho biết tỷ lệ dòng code đã được chạy. Chỉ số này giúp tìm các vùng code chưa được test chạm đến.

Branch coverage đo các hướng xử lý của điều kiện. Với một câu lệnh `if`, thường có nhánh đúng và nhánh sai. Nếu test chỉ đi qua một hướng, nhánh còn lại chưa được kiểm tra.

Branch coverage phù hợp với code nghiệp vụ có nhiều điều kiện. Ví dụ, chương trình có thể xử lý khác nhau cho thành viên thường và thành viên VIP, hoặc từ chối dữ liệu không hợp lệ.

Line coverage đếm theo dòng. Statement coverage đếm theo từng câu lệnh. Ví dụ, nếu viết `int discount = 0; if (isVip) discount = 10;` trên cùng một dòng thì test với khách thường vẫn chạy dòng đó để khởi tạo và kiểm tra điều kiện. Câu lệnh gán `discount = 10` chỉ chạy khi khách là VIP.

> Cửa hàng giảm giá 20% khi khách vừa là thành viên vừa có mã giảm giá. Nếu chỉ thử một khách thỏa cả hai điều kiện, mình đã chạy qua mọi dòng. Vậy còn hướng rẽ nào chưa được kiểm tra?

```java
int calculateDiscount(boolean isMember, boolean hasCoupon) {
    int discount = 0;
    if (isMember && hasCoupon) {
        discount = 20;
    }
    return discount;
}
```

| Ca thêm vào bộ test | Là thành viên? | Có mã? | Kết quả mong đợi | Giải thích | Line lũy kế | JaCoCo branch lũy kế |
|---|---|---|---:|---|---:|---:|
| T1 | Có | Có | 20% | Cả hai điều kiện đều đúng. Hàm chạy cả câu gán 20 và câu trả về. | 100% | 2/4 (50%) |
| T2 | Không | Có | 0% | Điều kiện thành viên sai. Java dừng đánh giá trước khi xét mã. | 100% | 3/4 (75%) |
| T3 | Có | Không | 0% | Điều kiện thành viên đúng nên Java xét mã. Hướng mã sai được chạy lần đầu. | 100% | 4/4 (100%) |
| T4 | Không | Không | 0% | Điều kiện thành viên sai. Hàm đi cùng đường với T2. | 100% | 4/4 (100%) |

Java dừng đánh giá `&&` ngay khi điều kiện đầu sai. Đây là short-circuit. JaCoCo đếm bốn hướng ở bytecode của ví dụ, gồm đúng và sai của từng điều kiện khi nó được xét. Nếu đã có T1 và T2, thêm T4 vẫn chưa chạy tới hướng “là thành viên nhưng thiếu mã”. Phải dùng T3 để kiểm tra hướng đó.

Các chỉ số khác trên slide cũng có thể giải thích trên chính hàm này:

- **Decision coverage** nhìn kết quả của cả câu `if`. T1 cho kết quả đúng, T2 cho kết quả sai, nên T1 và T2 đã đạt 100% decision coverage.
- **Condition coverage** nhìn từng điều kiện con đã được đánh giá đúng và sai chưa. Cần đến T3 để có lần đầu điều kiện mã được đánh giá là sai.
- **MC/DC** kiểm tra ảnh hưởng riêng của từng điều kiện. So T1 với T2 để đổi tư cách thành viên trong khi giữ dữ liệu có mã, rồi so T1 với T3 để đổi trạng thái mã trong khi vẫn giữ khách là thành viên.
- **Path coverage** nhìn các đường thực thi. Nếu chỉ xét vào hay bỏ qua thân `if` như trên slide, T1 và T2 đã đủ hai hướng. Nếu phân biệt cả đường đánh giá short-circuit, T3 mới đi đường thứ ba.
- **Method coverage** ghi nhận phương thức đã chạy. Chỉ T1 đã gọi được phương thức tính giảm giá.

### 4.3. Coverage gap

Coverage gap là dòng hoặc nhánh chưa được bộ test thực thi. Sau khi thấy gap trên báo cáo, người viết test cần quay lại yêu cầu để xác định tình huống nào tạo ra nhánh đó và kết quả đúng là gì.

Không nên thêm test chỉ để làm dòng code chuyển sang màu xanh. Test mới phải kiểm tra một hành vi có ý nghĩa bằng assertion cụ thể.

Với nhánh khách là thành viên nhưng thiếu mã, một test hoàn chỉnh phải vừa đưa hàm đi vào đúng hướng đó, vừa kiểm tra mức giảm bằng 0%. Nếu hàm áp nhầm 20%, test phải thất bại.

### 4.4. Giới hạn của coverage

Coverage cao không chứng minh rằng:

- Assertion đã đúng.
- Mọi giá trị biên đã được kiểm tra.
- Các thành phần tích hợp đúng với nhau.
- Chương trình không còn lỗi.

Hai bộ test có thể đạt cùng coverage nhưng khả năng phát hiện lỗi khác nhau. Coverage là thước đo về phạm vi code đã chạy, không phải điểm chất lượng tổng hợp.

## 5. Công cụ JaCoCo

JaCoCo là công cụ đo Code Coverage cho Java. Khi test chạy, JaCoCo ghi nhận phần code được thực thi và tạo báo cáo.

Trong bài này, nhóm quan tâm hai chỉ số chính là line coverage và branch coverage. Báo cáo HTML dùng màu sắc để chỉ ra dòng đã chạy, chưa chạy hoặc mới được phủ một phần.

Khi chỉ vào báo cáo, có thể giải thích xanh là đã phủ, đỏ là chưa phủ, vàng là phủ một phần. Ở dòng có điều kiện, xem số nhánh đã phủ để xác định hướng còn thiếu rồi quay về bảng test case tìm dữ liệu tương ứng.

JaCoCo còn cho phép đặt ngưỡng coverage. Nếu kết quả thấp hơn ngưỡng, build bị đánh dấu thất bại. Khả năng này được dùng để tạo coverage gate.

## 6. Coverage gate

Coverage gate là điều kiện tự động kiểm tra coverage có đạt ngưỡng hay không:

```text
Coverage đạt ngưỡng       → build tiếp tục
Coverage không đạt ngưỡng → build thất bại
```

Gate giúp phát hiện khi một thay đổi thêm nhánh mới nhưng không bổ sung test, hoặc khi test quan trọng bị xóa.

> Giả sử bộ test đều xanh, nhưng branch coverage của phần tính ưu đãi chỉ còn 85%, trong khi ngưỡng tối thiểu là 90%. Build sẽ xanh hay đỏ?

Build đỏ vì gate đo độ phủ. JUnit báo xanh vì các ca hiện có đều đạt kết quả mong đợi. Khi giải thích gate, nêu rõ ba thứ: chỉ số được đo, phạm vi áp dụng và ngưỡng tối thiểu.

Không có một ngưỡng phù hợp cho mọi dự án. Ngưỡng cần dựa trên mức độ quan trọng và khả năng kiểm thử của code. Đặt 100% cho toàn dự án có thể khiến nhóm viết test để đạt con số thay vì kiểm tra hành vi cần thiết.

Trong case study, nhóm đặt branch coverage của `FineCalculator` tối thiểu 90%. Gate chỉ áp dụng cho lớp có quy tắc nghiệp vụ rõ ràng, không áp cùng một tỷ lệ cho mọi lớp.

Gate cũng không biết assertion có đúng hay không. Nó phải được kết hợp với review code, review test case và hiểu biết về nghiệp vụ.

## 7. CI/CD và GitHub Actions

Continuous Integration, hay CI, là cách tích hợp thay đổi thường xuyên và chạy kiểm tra tự động. Khi có push hoặc pull request, hệ thống build dự án, chạy test và báo kết quả.

Continuous Delivery đưa quy trình đến bước tạo sản phẩm có thể phát hành. Continuous Deployment tự triển khai sản phẩm lên môi trường chạy thật. Dự án của nhóm dừng ở Continuous Delivery: pipeline kiểm tra và đóng gói ứng dụng nhưng chưa tự triển khai.

GitHub Actions là công cụ tự động hóa tích hợp với GitHub. Trong dự án, nó thực hiện quy trình sau:

```text
Pull request
    ↓
JUnit chạy Unit Test
    ↓
JaCoCo đo coverage và kiểm tra gate
    ↓
GitHub Actions báo kết quả
```

Nếu test lỗi hoặc coverage không đạt, pull request có trạng thái đỏ. Sau khi người phát triển sửa và push lại, workflow tự chạy lại.

> Sau khi mở pull request, JUnit xanh và coverage gate đỏ. Pipeline có tiếp tục đóng gói không?

Trong pipeline demo, job `package` phụ thuộc vào `coverage-gate`, nên nó bị bỏ qua khi gate thất bại. Khi test và gate cùng đạt, job đóng gói tạo file JAR. Nếu gate được đặt làm required check, kết quả đỏ cũng chặn hợp nhất pull request.

Ba công cụ có vai trò khác nhau:

1. JUnit viết và chạy test.
2. JaCoCo đo phần code đã chạy.
3. GitHub Actions tự động hóa toàn bộ quy trình.

## 8. Case study và demo

### 8.1. Case study

Nhóm sử dụng ứng dụng quản lý thư viện. Phần demo tập trung vào chức năng tính phí trả sách trễ:

- Thành viên thường trả 2.000 đồng cho mỗi ngày trễ.
- Thành viên VIP được miễn hai ngày đầu, sau đó trả 1.000 đồng mỗi ngày.
- Phí tối đa là 50.000 đồng.
- Số ngày âm hoặc hạng thành viên rỗng phải bị từ chối.

### 8.2. Demo

Demo gồm bốn bước và nên hoàn thành trong khoảng bốn phút.

1. Mở bộ test baseline. Bộ này chỉ kiểm tra thành viên thường trễ một ngày. Test chạy xanh nhưng còn thiếu nhiều tình huống.
2. Chạy baseline với coverage gate 90%. Test vẫn xanh nhưng build đỏ vì coverage không đạt ngưỡng.
3. Mở báo cáo JaCoCo và chỉ ra các nhánh chưa được chạy.
4. Chạy bộ test đầy đủ. Bộ này có dữ liệu cho thành viên VIP, giá trị biên và dữ liệu không hợp lệ. Coverage đạt ngưỡng và build chuyển sang xanh.

Hai lệnh dùng trong demo:

```bash
# Baseline: test xanh nhưng gate thất bại.
case-study/mvnw -B -ntp -f case-study/pom.xml -Pbaseline -Dcoverage.gate.skip=false clean verify

# Bộ đầy đủ: test và gate đều thành công.
case-study/mvnw -B -ntp -f case-study/pom.xml clean verify
```

Nên mở sẵn code và hai báo cáo trước, sau. Nếu Maven chạy chậm, dùng video quay sẵn để không làm gián đoạn bài trình bày.

*Khi chiếu demo, chỉ vào trạng thái test xanh và gate đỏ trước. Cho lớp dự đoán bước đóng gói, rồi mở lượt xanh để đối chiếu.*

## 9. Research paper và demo tích hợp AI

Phần này trả lời câu hỏi: nếu coverage cho thấy còn nhánh chưa được kiểm tra, AI có thể đề xuất test bổ sung hay không?

Nhóm chọn hai paper có source hoặc artifact công khai và xuất bản trong giai đoạn 2021 đến 2026. Hai paper đều nghiên cứu việc sinh test tự động nhưng sử dụng hai cách tiếp cận khác nhau.

### 9.1. CoverUp

"CoverUp: Effective High Coverage Test Generation for Python" của Pizzorno và Berger được công bố tại FSE 2025. CoverUp sử dụng mô hình ngôn ngữ để sinh Unit Test cho Python.

Quy trình của CoverUp gồm các bước:

```text
Chạy bộ test hiện tại
        ↓
Tìm phần source chưa được phủ
        ↓
Gửi source liên quan cho mô hình
        ↓
Sinh test, chạy lại và đo coverage
```

Coverage được dùng làm phản hồi. Nếu test còn lỗi hoặc vẫn thiếu nhánh, công cụ tiếp tục bổ sung theo kết quả vừa nhận được.

Khi nhóm thử CoverUp trên source Python của dự án, line coverage tăng từ 11 trên 39 lên 38 trên 39; branch coverage tăng từ 2 trên 16 lên 15 trên 16. Kết quả cho thấy coverage có thể giúp mô hình tập trung vào đúng phần code còn thiếu.

### 9.2. Pynguin

Paper "An empirical study of automated unit test generation for Python" của Lukasczyk, Kroiß và Fraser được công bố năm 2023. Công cụ được nghiên cứu là Pynguin.

Pynguin không dùng mô hình ngôn ngữ. Công cụ sử dụng thuật toán tìm kiếm, thông tin kiểu dữ liệu và kết quả thực thi để tạo input và test.

Khi chạy trên một module benchmark, nhóm ghi nhận coverage nội bộ 81,48%, với 10 test pass và 5 test `xfail`. Khi thử trên source có filesystem và XML, công cụ tạo được ít test hữu ích và thiếu assertion có ý nghĩa.

Pynguin được dùng để đối chiếu với CoverUp: một bên dùng mô hình ngôn ngữ, một bên dùng thuật toán tìm kiếm. Cả hai đều gặp khó khăn trong việc xác định kết quả đúng cần kiểm tra.

> Có thể lấy 81,48% của Pynguin so thẳng với số CoverUp đo trên một module khác không?

81,48% là coverage nội bộ trên module benchmark `codetiming._timers`. Để so trong phạm vi bài trình bày, đặt hai lượt chạy trên cùng module đọc XML của nhóm cạnh nhau: Pynguin giữ mức 23,6%, CoverUp tăng từ 23,6% lên 96,4% theo chỉ số gộp line và branch. Kết quả phản ánh một module và cấu hình thử cụ thể. Với CoverUp, một dòng và một nhánh còn thiếu nằm ở đường chạy khi gọi file từ dòng lệnh. Các test import module để gọi hàm nên không đi vào đường đó.

### 9.3. Quy trình AI của nhóm

Từ ý tưởng dùng coverage làm phản hồi, nhóm xây dựng một quy trình tương tự cho case study Java:

```text
Source code và yêu cầu
          ↓
AI-1 sinh test nháp
          ↓
JUnit chạy test
          ↓
JaCoCo tìm coverage gap
          ↓
AI-2 đề xuất test bổ sung
          ↓
Con người review rồi mới áp dụng
```

Đây là quy trình riêng của nhóm, không phải bản cài đặt lại CoverUp cho Java. Điểm được kế thừa là dùng coverage gap để cung cấp phản hồi cụ thể cho AI.

### 9.4. Demo AI

Demo sử dụng `FineCalculator` và được quay sẵn để tránh phụ thuộc mạng hoặc hạn mức API.

1. Cung cấp source và quy tắc tính phí cho AI-1.
2. AI-1 sinh ba test nháp. Các test chạy thành công nhưng branch coverage chỉ đạt 70%.
3. AI-2 nhận source, bộ test và báo cáo JaCoCo. Công cụ đề xuất thêm test cho ngày âm, hạng thành viên rỗng và nhánh VIP còn thiếu.
4. Sau khi bổ sung, các test chạy thành công và branch coverage của lượt demo đạt 100%.
5. Người thực hiện đọc lại input, expected result và assertion trước khi chấp nhận test.

Phần demo chỉ cần cho thấy báo cáo trước, các test được đề xuất và báo cáo sau. Không nên gọi AI trực tiếp trong lúc thuyết trình vì output có thể thay đổi và thời gian phản hồi phụ thuộc vào mạng.

### 9.5. Nhận xét

AI có thể giúp tìm trường hợp còn thiếu và đề xuất test nhanh hơn. Coverage cung cấp phản hồi cụ thể để AI biết phần code nào cần được kiểm tra thêm.

Tuy nhiên, test do AI sinh vẫn có thể sai expected result, dùng assertion yếu hoặc trùng với test hiện tại. Con người phải review theo yêu cầu nghiệp vụ trước khi đưa test vào dự án.

> Nếu AI đề xuất test cho khách thiếu mã giảm giá nhưng lại mong đợi giảm 20%, có nên giữ test chỉ vì coverage tăng không?

Theo quy tắc của cửa hàng, khách thiếu mã được giảm 0%. Cần sửa kết quả mong đợi, chạy lại test và xem JaCoCo có ghi nhận đúng hướng cần phủ hay không.

Kết quả của nhóm là tái hiện có giới hạn. Nhóm không chạy lại toàn bộ benchmark với mọi cấu hình, vì vậy các số liệu chỉ được dùng trong đúng phạm vi từng thí nghiệm.

## 10. Kết luận

Unit Test kiểm tra hành vi của từng phần nhỏ trong chương trình. Một test tốt cần dữ liệu phù hợp và assertion cụ thể.

Code Coverage cho biết bộ test đã chạy qua phần nào của code. Coverage gate dùng số liệu đó để chặn build không đạt ngưỡng. GitHub Actions giúp quy trình này chạy tự động trên mỗi thay đổi.

AI có thể đọc coverage gap và đề xuất test bổ sung, nhưng người thực hiện vẫn phải kiểm tra expected result và assertion.

Câu trả lời cho câu hỏi ban đầu là: test xanh và coverage 100% vẫn chưa đủ để kết luận chương trình đúng. Coverage giúp tìm phần code bị bỏ sót; chất lượng test vẫn phụ thuộc vào test case, assertion và yêu cầu nghiệp vụ.

Quay lại đơn hàng ở đầu bài. Nếu code viết `total > 200_000` thay cho `total >= 200_000`, đơn 150.000 đồng và đơn 250.000 đồng vẫn cho cùng kết quả với cả hai cách viết. Hai hướng đều đã được chạy, nhưng ca đúng 200.000 đồng mới bắt được lỗi. *Có thể dừng sau khi nêu hai đơn hàng để lớp tự đề xuất ca còn thiếu trước khi giải thích.*

## 11. Câu hỏi dự kiến

### Có nên đặt coverage 100% không?

Không nhất thiết. Ngưỡng nên dựa trên mức độ quan trọng và khả năng kiểm thử của từng phần code.

### Coverage cao có thay thế review test không?

Không. Người review vẫn phải kiểm tra dữ liệu, assertion và mối liên hệ giữa test với yêu cầu.

### Vì sao gate chỉ áp dụng cho `FineCalculator`?

Đây là lớp có nhiều quy tắc và giá trị biên rõ ràng. Đặt gate theo lớp giúp nhóm tập trung vào code nghiệp vụ quan trọng.

### Công cụ sinh test có thể thay người viết test không?

Chưa thể. Công cụ có thể tạo input và tăng coverage, nhưng con người vẫn phải xác định kết quả đúng và kiểm tra assertion.

## 12. Tài liệu tham khảo

- JUnit User Guide: <https://docs.junit.org/6.0.3/user-guide/>
- JaCoCo Documentation: <https://www.jacoco.org/jacoco/trunk/doc/>
- GitHub Actions for Java with Maven: <https://docs.github.com/en/actions/tutorials/build-and-test-code/java-with-maven>
- Pizzorno và Berger, "CoverUp: Effective High Coverage Test Generation for Python", FSE 2025: <https://doi.org/10.1145/3729398>
- Lukasczyk, Kroiß và Fraser, "An empirical study of automated unit test generation for Python", Empirical Software Engineering 2023: <https://doi.org/10.1007/s10664-022-10248-w>
