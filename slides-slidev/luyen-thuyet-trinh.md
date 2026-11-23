# Luyện thuyết trình · Phần 1 — Unit Testing

## Slide 3 · Phần 1 — Unit Testing

- Em xin chào thầy cô và các bạn. Giả sử một cửa hàng miễn phí giao hàng cho **đơn từ 200.000 đồng**. Sau khi sửa hàm tính phí, em sẽ thử ngay một đơn đúng 200.000 đồng. Theo quy định, phí giao hàng phải bằng **0 đồng**.
- Đây là một **unit test**, hay kiểm thử đơn vị. Ta kiểm tra riêng một hàm, một lớp hoặc một nhóm đối tượng cùng đảm nhiệm một trách nhiệm. Với đầu vào đã chuẩn bị, ta gọi hành vi cần kiểm tra rồi đối chiếu kết quả với yêu cầu.
- Vẫn với đơn hàng ấy, nếu ta đặt hàng qua ứng dụng và theo dõi đến màn hình xác nhận, **phạm vi kiểm thử** đã rộng hơn. Phạm vi và mục tiêu đó giúp ta phân biệt các mức kiểm thử.

## Slide 4 · Unit testing và test level

- Để xác định mức kiểm thử, ta cần biết **đối tượng đang được kiểm tra** và điều ta muốn xác minh. Đối tượng này được gọi là **SUT**, viết tắt của *system under test*.
- Ở mức **unit**, còn gọi là *component testing*, ta kiểm tra hành vi của một thành phần trong điều kiện cô lập. Nếu thành phần cần dữ liệu bên ngoài, ta có thể thay nguồn dữ liệu để tạo đúng tình huống cần thử.
- Ở mức **integration**, ta kiểm tra cách các thành phần giao tiếp với nhau, chẳng hạn một bên có truyền đúng dữ liệu mà bên kia cần hay không.
- Ở mức **system**, ta kiểm tra hành vi của toàn hệ thống theo đặc tả. Đến mức **acceptance**, người nghiệm thu đối chiếu sản phẩm với nhu cầu nghiệp vụ và tiêu chí chấp nhận.
- Sơ đồ sử dụng cách chia bốn mức. Trong **CTFL 4.0.1**, mức tích hợp được tách chi tiết hơn thành tích hợp giữa các thành phần và tích hợp giữa các hệ thống.

## Slide 5 · Phí giao hàng ở bốn test level

- Mời các bạn theo dõi cùng một quy định qua bốn ô trên slide. Ở mức **unit**, ta truyền 200.000 đồng vào hàm tính phí và kiểm tra giá trị trả về bằng 0.
- Ở mức **integration**, ta kiểm tra xem phần thanh toán có gửi đúng tổng tiền cho hàm và sử dụng đúng mức phí nhận về hay không.
- Ở mức **system**, ta đặt đơn qua ứng dụng, sau đó đối chiếu số tiền lúc thanh toán với số tiền trên màn hình xác nhận.
- Ở mức **acceptance**, chủ cửa hàng có thể nghiệm thu bằng hai đơn chỉ chênh nhau một đồng. Đơn **199.999 đồng** vẫn phải thu phí, còn đơn 200.000 đồng phải được miễn.

## Slide 6 · Đặc điểm của một unit test tốt

- Trở lại phép thử đầu tiên. Nếu thấy tên “miễn phí khi đơn đúng ngưỡng” trong báo cáo lỗi, ta biết ngay **tình huống và kết quả mong đợi**. Một unit test nên tập trung vào **một hành vi**. Hành vi đó có thể cần nhiều phép kiểm tra nếu nó tạo ra nhiều kết quả quan sát được.
- **Tính độc lập** thể hiện ở việc test có thể chạy riêng hoặc theo bất kỳ thứ tự nào. Chẳng hạn, nếu test cần một đơn hàng do test trước tạo sẵn, nó có thể đạt khi chạy cả bộ nhưng thất bại khi chạy riêng.
- **Tính lặp lại** nghĩa là cùng mã nguồn và cùng điều kiện kiểm thử phải cho cùng kết quả.
- Test **chạy nhanh** giúp ta kiểm tra lại sau mỗi lần sửa mã. Việc chạy lại các test để phát hiện thay đổi làm hỏng hành vi từng hoạt động đúng được gọi là **kiểm thử hồi quy**.

## Slide 7 · Test oracle và assertion

- Trong ví dụ giao hàng, căn cứ nào cho phép ta khẳng định phí phải bằng 0? Đó là quy định miễn phí của cửa hàng. Căn cứ dùng để xác định kết quả đúng gọi là **test oracle**. Oracle cũng có thể là bảng quyết định đã thống nhất hoặc ví dụ do người có chuyên môn xác nhận.
- Trên sơ đồ, một phía là **expected result**, kết quả mong đợi suy ra từ oracle. Phía còn lại là **actual result**, kết quả thực tế khi chạy SUT với đầu vào đã chọn.
- **Assertion** là phép kiểm tra xem kết quả thực tế có thỏa điều kiện mong đợi hay không. Nếu dùng chính hàm tính phí để tính cả giá trị mong đợi, cùng một sai sót có thể xuất hiện ở hai phía mà phép so sánh vẫn đạt.

## Slide 8 · Arrange, Act, Assert

- Sau khi xác định kết quả mong đợi, ta có thể viết ca kiểm thử theo cấu trúc **Arrange, Act, Assert**, thường gọi tắt là **AAA**. Có thể đọc ba bước này theo trình tự sau.
- **Arrange** là chuẩn bị đối tượng cần kiểm tra, dữ liệu đầu vào, trạng thái ban đầu và câu trả lời từ các thành phần phụ thuộc nếu cần.
- **Act** là thực hiện hành vi cần kiểm tra. Trong ví dụ này, đó là lời gọi hàm tính phí giao hàng.
- **Assert** là đối chiếu kết quả quan sát được với yêu cầu. Tùy hành vi, ta có thể kiểm tra giá trị trả về, thay đổi trạng thái, ngoại lệ hoặc lời gọi sang một thành phần khác.

## Slide 9 · Một đơn đúng ngưỡng trong JUnit

- Ba dòng JUnit trên slide có thể đọc thành câu “Với đơn 200.000 đồng, khi gọi hàm tính phí, phí giao hàng phải bằng 0 đồng.”
- Ở bước **Arrange**, ta gán tổng tiền cho biến total. Đến bước **Act**, ta gọi shippingFee với tổng tiền đó và lưu kết quả vào biến fee.
- Ở bước **Assert**, ta gọi **assertEquals(0, fee)**. Đối số đầu là số phí mong đợi, đối số sau là số phí thực tế. Ta đã có cách viết một ca test. Vậy ngoài đơn đúng ngưỡng, còn những đầu vào nào đáng thử?

## Slide 10 · Black-box test techniques

- Ta có thể chọn dữ liệu ngay từ đặc tả nghiệp vụ. Đây là **kiểm thử hộp đen**. Bốn kỹ thuật trên slide giúp ta chọn ca thử phù hợp với từng dạng yêu cầu.
- Với **phân vùng tương đương**, ta nhóm các đầu vào cần được xử lý giống nhau rồi chọn đại diện cho từng nhóm. Trong các đơn hợp lệ, nhóm dưới 200.000 đồng phải trả phí, còn nhóm từ 200.000 đồng trở lên được miễn.
- Với **phân tích giá trị biên**, ta thử ngay nơi quy tắc thay đổi. Hai đơn 199.999 và 200.000 đồng chỉ lệch một đồng nhưng phải được xử lý khác nhau. Cặp giá trị này giúp phát hiện lỗi dùng sai dấu so sánh.
- Khi kết quả phụ thuộc vào nhiều điều kiện, ta dùng **bảng quyết định** để ghi từng tổ hợp có ý nghĩa và kết quả tương ứng. Ví dụ, khi xét yêu cầu mượn sách, thư viện cần xét cả tình trạng của sách và việc thành viên có nợ phí hay không.
- Với **kiểm thử chuyển trạng thái**, ta xét cùng một sự kiện ở các trạng thái khác nhau. Mượn lần đầu thành công sẽ chuyển bản sách từ “còn sẵn” sang “đang cho mượn”. Nếu có yêu cầu mượn tiếp chính bản sách ấy, ta kiểm tra yêu cầu bị từ chối và trạng thái sách được giữ nguyên.

## Slide 11 · Statement testing

- Khi có mã nguồn, ta có thêm căn cứ để thiết kế test. Cách chọn ca thử dựa trên cấu trúc bên trong chương trình được gọi là **kiểm thử hộp trắng**.
- Với **statement testing**, ta chọn câu lệnh mục tiêu rồi tìm đầu vào khiến chương trình thực thi câu lệnh đó. Chẳng hạn, hàm giảm giá khởi tạo mức giảm bằng 0 và gán lại bằng 10 nếu khách là VIP. Muốn kiểm tra phép gán này, ta chọn khách VIP rồi xác nhận hàm trả về 10.
- **Độ bao phủ câu lệnh** là số câu lệnh đã chạy chia cho tổng số câu lệnh có thể thực thi đang xét. Trong ví dụ này, riêng ca VIP đã chạy qua tất cả câu lệnh. Nhưng nếu khách thường cũng được giảm nhầm, liệu ca VIP có phát hiện được không?

## Slide 12 · Branch testing

- Để trả lời câu hỏi đó, ta cần thêm ca **khách thường**. Khi điều kiện VIP sai, chương trình bỏ qua phép gán 10 và mức giảm phải bằng 0. Kết hợp với ca VIP, ta đã thử cả hai hướng của câu if.
- Chọn đầu vào để đi qua các hướng của luồng điều khiển gọi là **branch testing**. Ngay cả khi mã nguồn không viết else, hướng bỏ qua thân if vẫn là một nhánh. **Độ bao phủ nhánh** bằng số nhánh đã đi qua chia cho tổng số nhánh đang xét.
- Với **điều kiện ghép**, thứ tự đánh giá cũng ảnh hưởng đến đường thực thi. Chẳng hạn, để được giảm giá, khách phải là thành viên và có phiếu. Với phép “và” trong Java, nếu khách chưa là thành viên thì chương trình dừng ở vế đầu.
- Muốn kiểm tra trường hợp vế “có phiếu” thực sự được xét và cho kết quả sai, ta chọn **thành viên không có phiếu**, rồi xác nhận khách không được giảm giá.

## Slide 13 · Error guessing

- Ngoài việc đọc đặc tả và mã nguồn, người kiểm thử còn có thể dựa vào kinh nghiệm. **Error guessing**, hay phỏng đoán lỗi, bắt đầu từ một sai sót có khả năng xảy ra, sau đó chọn đầu vào có thể làm lộ sai sót ấy.
- Ví dụ, quy định “từ 200.000 đồng” đòi hỏi phép so sánh **lớn hơn hoặc bằng**. Giả sử người lập trình chỉ dùng dấu lớn hơn. Thử đơn 100.000 hay 300.000 đồng đều cho cùng kết quả ở hai cách viết.
- Đơn **đúng 200.000 đồng** mới phân biệt được hai cách cài đặt. Ta chọn giá trị đó và kiểm tra phí bằng 0. Giả thuyết ban đầu có thể đến từ kinh nghiệm cá nhân, lịch sử lỗi của dự án hoặc một lỗi lập trình thường gặp.

## Slide 14 · Checklist-based testing

- Để đồng nghiệp cũng nhớ kiểm tra dạng lỗi vừa rồi, nhóm có thể ghi lại câu hỏi “Quy tắc thay đổi ở giá trị nào? Ta đã thử ngay dưới ngưỡng và đúng ngưỡng chưa?”
- Dùng danh sách câu hỏi hoặc điều kiện được đúc kết từ kinh nghiệm để thiết kế test gọi là **checklist-based testing**, tức kiểm thử dựa trên danh sách kiểm tra.
- Với hàm giao hàng, mục **kiểm tra ngưỡng** dẫn đến hai ca cụ thể. Đơn 199.999 đồng vẫn chịu phí, còn đơn 200.000 đồng được miễn. Mỗi ca cần đầu vào và kết quả mong đợi riêng.
- Khi phát hiện một dạng lỗi mới, nhóm có thể **cập nhật checklist** để kinh nghiệm đó được dùng lại trong các lần kiểm thử sau.

## Slide 15 · Stub

- Với đơn hàng, ta có thể truyền thẳng số tiền cần thử vào hàm. Còn trong bài toán thư viện, muốn thử hạn mức ba cuốn, ta phải chuẩn bị một dữ liệu mà **LoanService** lấy từ nơi khác.
- Cụ thể, service hỏi repository xem thành viên đang mượn bao nhiêu cuốn. Repository phụ trách truy xuất dữ liệu và là một **dependency**, tức thành phần mà service phụ thuộc vào.
- Để kiểm tra riêng service, ta thay repository thật bằng một đối tượng dùng cho kiểm thử. Tên gọi chung của các đối tượng thay thế này là **test double**.
- Khi đối tượng thay thế cung cấp **câu trả lời định sẵn**, nó đóng vai trò **stub**. Ta cấu hình câu trả lời ở bước Arrange. Đến bước Act, service nhận dữ liệu đó và ta quan sát quyết định cho mượn.

## Slide 16 · Thành viên đã mượn ba cuốn sách

- Có thể đọc dòng Mockito dưới sơ đồ như sau. Khi LoanService hỏi số sách thành viên số 1 đang mượn, repository trả về 3. Trong đoạn mã, **when** xác định lời gọi cần cấu hình, còn **thenReturn** ấn định giá trị trả về.
- Sách vẫn còn sẵn và thành viên không nợ phí. Nhờ stub, ta tạo được tình huống thành viên **đang mượn đúng ba cuốn** mà không cần lập ba phiếu mượn thật trong cơ sở dữ liệu.
- Giả sử service đã trả về mã “đạt hạn mức”. Làm thế nào để kiểm tra rằng nó cũng **không lưu thêm phiếu mượn** trước khi trả về mã đó?

## Slide 17 · Mock

- Để trả lời, ta cần quan sát lời gọi từ service sang repository. **Mock** là test double dùng để xác minh **tương tác** giữa đối tượng đang được kiểm tra và thành phần mà nó gọi.
- Mock ghi nhận phương thức được gọi, đối số và số lần gọi. Sau khi service xử lý xong yêu cầu, ta dùng **verify** của Mockito để đối chiếu các lời gọi đã ghi nhận với hành vi nghiệp vụ yêu cầu.
- Trong ví dụ thư viện, **stub** cung cấp số sách đang mượn để tạo tình huống. Ở vai trò **mock**, đối tượng thay thế cho biết service có yêu cầu repository lưu phiếu hay không.

## Slide 18 · Từ chối mượn và không lưu phiếu

- Với thành viên đang mượn ba cuốn, ta cần kiểm tra hai kết quả. Trước hết, service phải từ chối yêu cầu với mã **LIMIT_REACHED**, nghĩa là thành viên đã đạt hạn mức.
- Tiếp theo, **verify(loans, never()).save(any())** xác nhận repository không nhận lời gọi lưu phiếu nào. Ở đây, save là thao tác lưu, any khớp với bất kỳ phiếu nào và never yêu cầu số lần gọi bằng 0.
- Nếu service gọi save rồi mới trả mã lỗi, phép kiểm tra mã vẫn đạt nhưng **phép kiểm tra tương tác** sẽ thất bại. Cùng một đối tượng loans vừa cung cấp số 3 ở bước chuẩn bị, vừa ghi nhận lời gọi save để ta kiểm tra sau cùng.

## Slide 19 · Framework Unit Test theo ngôn ngữ

- Trong ví dụ vừa rồi, **Mockito** giúp thay thế repository và xác minh tương tác. Để khai báo các ca test, tìm chúng, chạy và nhận kết quả trong dự án Java, nhóm dùng **JUnit**.
- Mỗi hệ sinh thái có các framework kiểm thử riêng. Java có JUnit và TestNG, Python có pytest và unittest, còn JavaScript và TypeScript có Jest và Vitest.
- Với .NET, ta có thể gặp xUnit, NUnit và MSTest. Trong nhóm C và C++, slide giới thiệu GoogleTest và Catch2. Go có sẵn gói testing.
- Trong dự án Spring Boot của nhóm, **JUnit Jupiter** cung cấp annotation và assertion để viết test. Khi chạy qua Maven, **Surefire** chạy test và xuất báo cáo, còn JaCoCo đo phần mã đã được thực thi.

## Slide 20 · JUnit cung cấp những gì?

- Trong một lớp Java có nhiều phương thức, **@Test** đánh dấu phương thức kiểm thử để JUnit nhận diện, chạy và báo kết quả.
- Hai annotation về vòng đời giúp từng ca bắt đầu trong trạng thái đã biết. **@BeforeEach** chạy trước mỗi ca để chuẩn bị dữ liệu. **@AfterEach** chạy sau mỗi ca để dọn dẹp.
- Khi cần so sánh giá trị, ta dùng **assertEquals** với giá trị mong đợi và giá trị thực tế. Khi yêu cầu quy định một thao tác phải phát sinh ngoại lệ, ta dùng **assertThrows**, chỉ rõ loại ngoại lệ mong đợi và thao tác cần thực hiện.
- Nếu nhiều ca cùng kiểm tra một quy tắc và chỉ khác dữ liệu, ta có thể viết **parameterized test**, tức test có tham số. Ví dụ, mỗi dòng CSV chứa hạng thành viên, số ngày trễ và phí mong đợi. JUnit chạy cùng thân test cho từng dòng, nhờ đó ta xác định được bộ dữ liệu nào làm test thất bại.

## Slide 21 · Viết một unit test bằng JUnit

- Mời các bạn đọc tên phương thức trên slide. Quy tắc cần kiểm tra là **thành viên thường trả trễ một ngày phải trả 2.000 đồng**.
- Ba dòng trong thân test tương ứng với ba bước. Ở **Arrange**, ta tạo FineCalculator. Ở **Act**, ta gọi calculate với một ngày trễ và hạng NORMAL. Đến **Assert**, ta dùng assertEquals để so phí thực tế với 2.000 đồng.
- Số tiền mong đợi đến từ **quy định của thư viện**. Vì vậy, ngay cả khi cách tính phí bên trong thay đổi, ca test này vẫn kiểm tra được quy tắc mà người mượn quan tâm.

## Slide 22 · Video A — Unit Test với JUnit 5 và Mockito

- Video A của bạn Nguyễn Bảo An minh họa cách viết và chạy những ca kiểm thử vừa trình bày. Phần đầu hướng dẫn thiết lập Java 25, sử dụng Maven Wrapper, chạy JUnit và đọc **báo cáo Surefire**.
- Tại **02:15**, các bạn có thể theo dõi cách dùng CSV để chạy cùng một thân test với nhiều giá trị biên, gồm trường hợp trả đúng hạn, VIP trễ hai ngày và phí chạm trần 50.000 đồng.
- Tại **03:45**, ví dụ dùng Mockito để cô lập service với ba repository. Các bạn sẽ thấy cách xác minh một lời gọi không xảy ra và dùng **ArgumentCaptor** để kiểm tra đối số thực tế đã truyền.
- Phần cuối chỉ ra hai rủi ro khi dùng mock. Việc cấu hình **nhiều tầng mock** khiến test phụ thuộc sâu vào cách cài đặt. Việc chỉ xác nhận lại **dữ liệu đã cấu hình sẵn** có thể khiến test đạt dù hành vi nghiệp vụ sai.
- Trở lại ví dụ hạn mức, số 3 là dữ liệu ta cung cấp. Điều cần kiểm tra là service **từ chối yêu cầu mượn** và **không lưu thêm phiếu**.
