# Khảo sát & so sánh công cụ

**Thực hiện:** việc chung cả nhóm — mỗi thành viên khảo sát công cụ thuộc phần mình phụ trách,
TV1 ghép lại.

> Đề yêu cầu *"khảo sát các công cụ liên quan"* và *"so sánh, đánh giá các công cụ ở nhiều
> khía cạnh khác nhau"*. Nhóm chốt **7 trục** và dùng thống nhất cho cả ba trụ, để các bảng
> đọc ngang được với nhau.
>
> **Quy ước trung thực của nhóm:** ô nào nhóm **chưa tự kiểm chứng** thì ghi rõ *"(chưa kiểm)"*,
> không điền theo cảm tính hay theo tài liệu quảng cáo. Các ô này sẽ được điền dần khi nhóm
> thực sự chạy, trước mốc nộp Tuần 6.

---

## 7 trục so sánh

| Trục | Nghĩa là gì | Nhóm sẽ đo / đánh giá bằng cách nào |
|---|---|---|
| **T1 — Khả năng** | Công cụ làm được những gì cho mục tiêu kiểm thử của trụ đó | Đối chiếu tài liệu chính thức |
| **T2 — Độ dễ cài đặt** | Bao nhiêu bước từ project trắng tới lần chạy đầu thành công | **Đếm số bước thật** khi nhóm tự làm, ghi lại |
| **T3 — Tích hợp Maven / IDE** | Có plugin Maven chính thức không; IDE hiển thị được kết quả không | Thử thật, chụp màn hình |
| **T4 — Hiệu năng** | Thêm bao nhiêu thời gian vào một lần `mvn verify` | **Đo bằng giây**, cùng máy, cùng case study, chạy 3 lần lấy trung vị |
| **T5 — Tài liệu & cộng đồng** | Tra cứu có dễ không; gặp lỗi lạ có người trả lời không | Mức độ đầy đủ của tài liệu chính thức; ngày commit gần nhất của dự án |
| **T6 — Giá & giấy phép** | Miễn phí tới đâu, giấy phép loại gì | Trang giá chính thức / file LICENSE |
| **T7 — Điểm yếu đã kiểm chứng** | Trường hợp nhóm **tự gặp** công cụ làm không tốt | Code chạy thật trong repository của nhóm |

---

## 1. Trụ Unit Test

### 1.1 Khung chạy test

| | **JUnit Jupiter** *(chọn)* | TestNG | Spock | JUnit 4 |
|---|---|---|---|---|
| T1 Khả năng | Vòng đời đầy đủ, `@ParameterizedTest`, `@Nested`, `@Tag`, mô hình extension mở rộng được | Mạnh về nhóm test và quan hệ phụ thuộc giữa test, có data provider | Cú pháp BDD rất gọn, tích hợp sẵn khả năng mock | Thiếu parameterized test tiện dụng |
| T2 Dễ cài | 1 dependency, có sẵn trong gói test của Spring Boot | Thêm dependency + cấu hình Surefire | Phải thêm Groovy vào quy trình build | 1 dependency |
| T3 Maven/IDE | Mặc định của Spring Boot; IDE hỗ trợ tốt nhất | Hỗ trợ tốt | Cần plugin Groovy | Tốt |
| T4 Hiệu năng | *(chưa kiểm — đo ở tuần 3)* | *(chưa kiểm)* | *(chưa kiểm)* | *(chưa kiểm)* |
| T5 Tài liệu | Rất nhiều | Nhiều | Ít hơn, giới hạn trong cộng đồng Groovy | Rất nhiều nhưng phần lớn đã lỗi thời |
| T6 Giá | Mã nguồn mở, miễn phí (EPL) | Mã nguồn mở, miễn phí (Apache 2.0) | Mã nguồn mở, miễn phí (Apache 2.0) | Mã nguồn mở, miễn phí |
| T7 Điểm yếu | Test không có assertion vẫn được tính là pass | Mô hình nhóm test dễ bị lạm dụng thành các test phụ thuộc lẫn nhau (vi phạm chữ I của FIRST) | Phải học thêm một ngôn ngữ | Không nên dùng cho dự án mới |

**Nhóm chọn JUnit Jupiter** — không phải vì nhiều tính năng nhất, mà vì **cả hệ sinh thái**
(JaCoCo, PIT, Surefire, Spring Boot) đều mặc định nhắm vào nó. Đây là một kết luận nhóm muốn
nhấn mạnh: *chọn công cụ là chọn hệ sinh thái, không chọn tính năng lẻ.*

### 1.2 Thư viện tạo test double

| | **Mockito** *(chọn)* | EasyMock | JMockit |
|---|---|---|---|
| T1 Khả năng | Stub, verify, `ArgumentCaptor`, spy; mock `static`/`final` cần thêm module phụ | Tương đương, API kiểu record–replay | Mạnh nhất: mock được cả `static` và constructor |
| T2 Dễ cài | Có sẵn trong gói test của Spring Boot | Thêm dependency | Thêm dependency + cấu hình tham số JVM |
| T5 Tài liệu | Nhiều nhất trong ba | Trung bình | Ít, cập nhật chậm |
| T7 Điểm yếu | Không mock `static`/`final` mặc định; **rất dễ bị lạm dụng thành test mock thay vì test hành vi** | API record–replay khó đọc hơn | Can thiệp sâu vào bytecode nên dễ hỏng khi đổi phiên bản JDK |

### 1.3 Thư viện assertion

| | **AssertJ** *(chọn)* | Assertions của JUnit | Hamcrest |
|---|---|---|---|
| T1 | Fluent, IDE gợi ý tốt, có assertion chuyên biệt cho collection / số thập phân / ngoại lệ | Đủ dùng ở mức cơ bản | Các matcher ghép được với nhau |
| T7 | Thêm một dependency; cả nhóm phải quen cú pháp | Thông báo lỗi kém chi tiết hơn | Cú pháp lồng nhau khó đọc khi điều kiện phức tạp |

---

## 2. Trụ Code Coverage

| | **JaCoCo** *(chọn)* | Cobertura | OpenClover | Coverage của IntelliJ |
|---|---|---|---|---|
| T1 Khả năng | Line, Branch, Method, Class, Instruction, độ phức tạp; báo cáo HTML/XML/CSV; **có sẵn goal chặn build** | Line, Branch | Nhiều loại nhất, có cả coverage theo từng test | Line, Branch (chỉ trong IDE) |
| T2 Dễ cài | 1 plugin, 2 khai báo execution | 1 plugin | 1 plugin, bản đầy đủ cần khoá bản quyền | Không cần cài |
| T3 Maven/IDE | Plugin Maven chính thức; IDE đọc được file kết quả | Plugin đã cũ | Có plugin | Chỉ trong IDE |
| T4 Hiệu năng | *(chưa kiểm — đo ở tuần 4)* | *(chưa kiểm)* | *(chưa kiểm)* | — |
| T5 Tài liệu | Nhiều; changelog ghi rõ hỗ trợ từng phiên bản JDK | **Gần như ngừng phát triển** | Trung bình | Tài liệu của JetBrains |
| T6 Giá | Mã nguồn mở, miễn phí | Mã nguồn mở (GPL) | Miễn phí cho dự án mã nguồn mở, trả phí cho thương mại | Kèm theo IDE |
| T7 Điểm yếu | Coverage ≠ chất lượng; nhánh trong lambda đếm khó hiểu; không thấy được assertion yếu | **Không theo kịp các phiên bản JDK mới → nhóm loại** | Điều kiện giấy phép phức tạp | **Không chạy được trong pipeline CI** |

**Nhóm chọn JaCoCo.** Việc Cobertura bị loại vì không theo kịp JDK mới là **một kết luận của
phần khảo sát**, không phải chi tiết kỹ thuật bỏ qua được: với công cụ làm việc trên bytecode,
ngừng cập nhật đồng nghĩa với hết dùng được.

### Công cụ bổ trợ: mutation testing

| | **PIT** *(chọn — chỉ để chứng minh điểm yếu của coverage)* |
|---|---|
| T1 | Sinh "mutant" bằng cách sửa nhỏ bytecode, chạy lại bộ test, báo mutant nào **sống**, mutant nào **bị diệt** |
| T4 | Chậm hơn đo coverage nhiều lần → nhóm chỉ chạy cho một package, không chạy toàn project |
| T7 | Chậm; có "mutant tương đương" gây báo động giả; có thể chưa theo kịp JDK mới nhất |

---

## 3. Trụ CI/CD

| | **GitHub Actions** *(chọn)* | Jenkins | GitLab CI | CircleCI |
|---|---|---|---|---|
| T1 Khả năng | Workflow YAML, chạy song song theo matrix, cache, artifact, secret, môi trường; kho action dựng sẵn rất lớn | Mạnh nhất về hệ plugin; mô hình controller–agent; tự chủ hoàn toàn khi tự vận hành | Tích hợp sẵn trong GitLab, có cả kho container | Mạnh về cache và chạy song song |
| T2 Dễ cài | **1 file YAML, không cài gì thêm** | Phải dựng máy chủ, cài plugin, cấu hình agent — nặng nhất | 1 file cấu hình | 1 file cấu hình |
| T3 Maven/IDE | Có action cài JDK kèm cache Maven sẵn | Plugin Maven lâu đời | Có mẫu dựng sẵn cho Maven | Có gói dựng sẵn |
| T4 Hiệu năng | *(chưa kiểm — đo build lạnh vs có cache ở tuần 5)* | Phụ thuộc máy tự vận hành | *(chưa kiểm)* | *(chưa kiểm)* |
| T5 Tài liệu | Rất nhiều, nhưng **nhiều ví dụ trên mạng dùng phiên bản action đã lỗi thời** | Rất nhiều, nhưng nhiều bài đã cũ | Nhiều | Trung bình |
| T6 Giá | **Miễn phí không giới hạn cho repository công khai**; repository riêng tư có hạn mức phút | Phần mềm miễn phí nhưng **tốn chi phí máy chủ và công bảo trì** | Có bản miễn phí giới hạn | Có bản miễn phí giới hạn |
| T7 Điểm yếu | Khó debug tại máy; lock-in cú pháp; cache hỏng gây kết quả sai lệch | Phải tự bảo trì và tự vá bảo mật; giao diện cũ | Buộc phải dùng GitLab | Ít phổ biến trong nước |

**Nhóm chọn GitHub Actions** cho demo chính, và **viết thêm cấu hình Jenkins làm cùng một
việc để đối chiếu** — đó là cách chứng minh luận điểm vendor lock-in bằng bằng chứng.

---

## 4. Bốn kết luận rút ra từ phần khảo sát

1. **Hệ sinh thái quan trọng hơn tính năng lẻ.** JUnit Jupiter được chọn vì JaCoCo, PIT,
   Surefire và Spring Boot đều mặc định nhắm vào nó, chứ không vì nó nhiều tính năng nhất.
2. **Một công cụ ngừng theo kịp JDK là một công cụ đã chết.** Cobertura bị loại vì lý do này.
3. **"Độ dễ cài đặt" là một trục thật, không phải chi tiết nhỏ.** Khoảng cách giữa
   "một file YAML" và "dựng một máy chủ" quyết định trực tiếp việc một nhóm 5 người có kịp
   hoàn thành demo trong vài tuần hay không.
4. **Không công cụ nào trong cả ba trụ đo được *chất lượng* của bộ test.** Phải ghép thêm
   mutation testing mới thấy được. Đây là luận điểm xuyên suốt của bài seminar.
