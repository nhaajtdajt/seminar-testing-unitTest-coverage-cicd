# Báo cáo chi tiết seminar — cập nhật đến Tuần 06

**Nhóm:** Group09. **Phạm vi:** tổng hợp nội dung seminar và minh chứng tích lũy; báo cáo tiến độ theo tuần nằm ở `BangCongViec.md` và `evidence/tuan-06/README.md`. **Cập nhật tài liệu:** 23/10/2026. Tài liệu được biên tập với Codex hỗ trợ và cần nhóm review trước khi trình bày.

**Thành viên:** TV1: Phạm Quang Vinh (23120202); TV2: Nguyễn Bảo An (23120207); TV3: Trương Nhật Đạt (23120231); TV4: Nguyễn Lê Thế Vinh (23120190); TV5: Ngô Gia An (23120205)

## 1. Mục tiêu và phạm vi

Nhóm em tìm hiểu chuỗi Unit Test → Code Coverage → CI/CD trên một ứng dụng quản lý thư viện. Người học cần viết được test cho logic có điều kiện, đọc được phần mã chưa được phủ và hiểu cách đưa test/coverage vào pipeline kiểm tra trước khi tích hợp mã.

Case study gồm tính phí trả sách trễ, mượn sách qua ba repository và API `POST /api/loans`. Dữ liệu nằm trong H2 in-memory qua Spring Data JPA (dữ liệu mẫu trong `data.sql`), nên mọi người chạy lại được mà không cần cài database. Công nghệ theo thiết kế gốc: Java 25, Spring Boot 4.1.1, JUnit Jupiter 6. Cấu hình CI thực hiện kiểm thử và đóng gói, chưa triển khai lên môi trường sử dụng thật.

## 2. Unit Test

Unit test kiểm tra một đơn vị hành vi với đầu vào và đầu ra xác định. Cấu trúc AAA gồm chuẩn bị dữ liệu (Arrange), thực hiện hành vi (Act), kiểm kết quả (Assert). Nguyên tắc FIRST hướng tới test nhanh, độc lập, lặp lại được, tự xác nhận kết quả và được viết đúng thời điểm.

Với `FineCalculator`, dùng đối tượng thật vì lớp chỉ chứa logic. Với `LoanService`, dùng mock cho ba repository để tập trung vào quyết định nghiệp vụ. Stub cung cấp phản hồi từ phụ thuộc; mock/verify kiểm tra cách tương tác. `Clock.fixed` loại bỏ phụ thuộc giờ máy. Không dùng mock chính đối tượng đang cần kiểm logic.

`@ParameterizedTest` + CSV giúp chạy cùng quy tắc với nhiều dữ liệu. Bộ tham chiếu có 15 ca hợp lệ và hai test dữ liệu sai, gồm biên gia hạn, mức trần và số ngày cực lớn. `LoanServiceTest` kiểm 6 tình huống và xác nhận nhánh bị từ chối không ghi phiếu. Kiểm thử tầng web xác nhận mã HTTP/validation; integration test kiểm các thành phần thật (controller, service, repository trên H2 in-memory) phối hợp với nhau.

Bốn vòng TDD được tái hiện với test mới fail trước, sau đó sửa logic để toàn bộ test đã thêm pass. Nguồn và log từng vòng được giữ riêng. Đây là bài thực hành hiện tại, chưa có commit lịch sử của 5 thành viên.

## 3. Code Coverage và chất lượng test

Line coverage đo số dòng thực thi; branch coverage đo các hướng rẽ trong mã đã được chạy. Một dòng có thể chứa nhiều nhánh; vì vậy chỉ xem màu xanh ở dòng là chưa đủ. JaCoCo thu dữ liệu thực thi và tạo HTML cho người đọc, XML/CSV cho xử lý tự động.

Trên riêng `FineCalculator`, bộ baseline 1 test phủ 5/10 nhánh (50%); bộ đầy đủ phủ 10/10 nhánh (100%). Gate dùng `jacoco:check` yêu cầu ít nhất 90% branch cho lớp này. Chạy baseline và bật gate làm Maven fail; bộ đầy đủ giữ nguyên gate thì pass. Các con số này không phải độ phủ 100% của toàn ứng dụng.

Bộ test bẫy đi qua đủ nhánh nhưng không assert số tiền của trường hợp hợp lệ. Nó vẫn đạt 100% branch. PIT tạo 11 mutation: test yếu diệt 3; bộ đầy đủ diệt 10. Một mutant còn sống đổi `daysLate <= graceDays` thành `<`; tại đúng ngưỡng, cả hai cách vẫn trả 0 nên tương đương theo đặc tả hiện tại. Không sửa test để ép diệt một mutant không đổi hành vi quan sát được.

Kết quả cho thấy coverage cần được kết hợp với assertion có ý nghĩa và dữ liệu biên. Mutation testing hỗ trợ tìm test yếu nhưng có chi phí chạy thêm và cần đọc mutant còn sống.

## 4. CI/CD

CI tự động kiểm tra các thay đổi được tích hợp thường xuyên. Continuous Delivery tạo sản phẩm sẵn sàng phát hành với bước quyết định triển khai; Continuous Deployment tự động đưa thay đổi đạt yêu cầu lên môi trường đích. Bản case study hiện dừng ở kiểm thử và tạo JAR.

Workflow gồm `test` chạy JDK 25, `coverage-gate` phụ thuộc kết quả test, `package` phụ thuộc gate. Cache giữ dependency Maven; artifact lưu test report, coverage và JAR; summary giúp người xem đọc điều kiện gate. Jenkinsfile mô tả cùng thứ tự công việc bằng cú pháp pipeline của Jenkins.

Workflow đã qua actionlint, các lệnh Maven đã chạy tại máy. Tài khoản GitHub đang dùng chỉ có quyền READ trên repo nhóm. Do đó chưa có lần chạy Actions, PR đỏ/xanh hay xác nhận required checks chặn merge. Jenkinsfile chưa được chạy trên Jenkins. Việc upload cấu hình không tự bật quy tắc bảo vệ nhánh; người quản trị cần cấu hình required status checks.

Phép đo JaCoCo trên bản Java 25 có ba lượt/cấu hình: trung vị không bật JaCoCo là 9,727 giây; có JaCoCo/report/gate là 12,754 giây. Phép đo repo Maven lạnh/ấm đã đủ ba cặp hợp lệ trên Java 25, trung vị 48,412/12,539 giây. Cặp bổ sung chạy sau hai cặp đầu, mất 479,523/11,940 giây; dùng kho trống cho lượt lạnh và dùng lại kho đó cho lượt ấm, ưu tiên IPv4 và tăng thời gian chờ tải. Điều kiện mạng thay đổi nên không suy ra mức tăng tốc cố định từ trung vị. Log tải lỗi được giữ riêng và không tính vào số liệu hoàn thành. Phép đo cache dependency tại máy không đồng nhất với thời gian restore cache trên GitHub hoặc Jenkins.

## 5. Khảo sát và lựa chọn công cụ

| Mục tiêu | Công cụ thực hành | Công cụ đối chiếu | Cơ sở nhận xét |
|---|---|---|---|
| Viết/chạy test Java | JUnit Jupiter, Mockito, AssertJ | TestNG, Spock, JUnit 4 | Chọn bộ do Spring Boot quản lý; đã chạy test trong case study. Chưa benchmark các bộ đối chiếu. |
| Đo độ phủ | JaCoCo | Cobertura, OpenClover, coverage IDE | Đã chạy HTML/XML và gate; các công cụ đối chiếu chưa cài/chạy trong đợt này. |
| Kiểm chất lượng assertion | PIT | Đọc test thủ công | Đã chạy cùng lớp với test mạnh/yếu; phải phân tích mutant tương đương. |
| Tự động kiểm tra | GitHub Actions | Jenkins, GitLab CI, CircleCI | Có workflow và Jenkinsfile; mới kiểm tra tĩnh/lệnh tại máy, chưa đo trên dịch vụ. |

Các bảng khảo sát ở gói đề xuất là dữ liệu tham khảo ban đầu, không thay cho kết quả trải nghiệm. Cần kiểm lại tình trạng phát triển, giấy phép, hạn mức và giá tại thời điểm nộp nếu đưa các thông tin đó vào bản chính thức. Mockito 5 đã dùng inline mock maker mặc định; không giữ kết luận cũ rằng mock final/static luôn cần thêm module.

## 6. Áp dụng AI

AI-1 sinh bản nháp 3 test; các test chạy đúng nhưng chỉ phủ 70% nhánh. AI-2 đọc JSON trích từ JaCoCo và source, nhận ra thiếu null, ngày âm, nhánh tính phí VIP; sinh 3 test bổ sung. Profile riêng cho phép đo đúng bộ 3 → 6 test mà không đưa bộ tham chiếu vào kết quả.

AI-3 có prompt và client gọi Gemini qua biến môi trường, cùng workflow lưu artifact. Chế độ chuẩn bị không gọi dịch vụ và ghi `api_called=false`. Trong Tuần 06 đã có một lần gọi live bằng `gemini-3.6-flash` trên diff fixture; sau HTTP 503, retry thành công và lưu 4 findings. Đối chiếu với expected fixture đạt 4 đúng, 0 thừa, 0 bỏ sót. Fixture có lỗi seed nên đây là kiểm tra luồng gọi API, không phải benchmark độc lập hay review toàn diện repository.

AI-4 có 13 dòng dữ liệu hợp lệ, được chạy với calculator thật bằng profile riêng. Bộ tham chiếu có 15 dòng; hai bộ trùng 13 ca, bộ AI không có NORMAL 3 ngày và VIP 0 ngày. Dữ liệu sai null/ngày âm được kiểm riêng bằng JUnit. Hai bộ đều có AI hỗ trợ chuẩn bị, nên cần thành viên nhóm tự viết/rà soát bộ chuẩn để có so sánh con người–AI hợp lệ.

Tất cả nội dung AI cần được review theo checklist: đúng nghiệp vụ, assertion cụ thể, không bịa API, không mock logic thuần, đọc số đo thực tế. Nhóm sẽ bổ sung người xác nhận; chưa quy đóng góp thực tế cho TV1–TV5 từ sản phẩm do trợ lý chuẩn bị.

## 7. Bài tập áp dụng

Bộ bài tập và đáp án gợi ý được chuẩn hóa tại [BaiTap_Tuan_06.md](BaiTap_Tuan_06.md): mở rộng data-driven Unit Test, phân biệt coverage với sức assertion qua PIT, đọc coverage gate trong pipeline, và chọn mức integration phù hợp. Ví dụ `STUDENT` là chính sách giả định riêng của bài tập; không sửa hợp đồng `NORMAL`/`VIP` trong source seminar.

## 8. Gói seminar và trạng thái hoàn thiện

Gói có source, bộ test, log trước/sau, HTML/XML coverage, PIT, replay TDD, script AI, báo cáo chi tiết, slide, bài tập và hướng dẫn tái hiện. Ba video theo từng chủ đề có kịch bản trong `KichBan_QuayVideo_Tuan_06.md`; chưa có video đã quay. Bảng `BangCongViec.md` ghi giới hạn còn lại của GitHub/Jenkins, video và xác nhận của thành viên.

Số đo và đường dẫn: xem [minh chứng](../../evidence/tuan-05/README.md) và [minh chứng Tuần 06](../../evidence/tuan-06/README.md). Hướng dẫn tái hiện: [HuongDan_Demo.md](HuongDan_Demo.md).

Nguồn chính thức dùng đối chiếu: [JUnit guide](https://docs.junit.org/6.0.3/user-guide/), [Mockito](https://github.com/mockito/mockito), [JaCoCo](https://www.jacoco.org/jacoco/trunk/doc/), [PIT Maven](https://pitest.org/quickstart/maven/), [Spring Boot requirements](https://docs.spring.io/spring-boot/4.1/system-requirements.html), [GitHub Maven CI](https://docs.github.com/en/actions/tutorials/build-and-test-code/java-with-maven), [Gemini API](https://ai.google.dev/api/generate-content).
