# ĐỀ XUẤT NỘI DUNG SEMINAR

**Chủ đề:** Unit Test · Code Coverage · CI/CD
**Môn học:** Kiểm thử phần mềm (Software Testing) — FIT@HCMUS
**Nhóm:** 5 thành viên
**Mốc:** Gặp mặt đầu môn học (Tuần 2–3) — trình bày nội dung dự kiến để xin ý kiến GVTH
**Ngày:** 01/10/2026

---

## 1. Nhóm hiểu đề bài như thế nào

Chủ đề gồm ba phần gắn với nhau thành một chuỗi, và nhóm muốn trình bày đúng theo chuỗi đó
thay vì ba bài rời rạc:

> **Unit Test** sinh ra các phép kiểm chứng → **Code Coverage** cho biết phép kiểm chứng đó
> đã chạm tới đâu trong mã nguồn → **CI/CD** bắt buộc cả hai phải chạy ở cổng merge, không
> phụ thuộc việc ai nhớ chạy.

Nhóm xác định **mục tiêu của bài seminar**: một bạn trong lớp chưa từng viết unit test, sau
khi nghe seminar và làm bài tập áp dụng, có thể (a) viết được unit test có ý nghĩa cho project
Java của mình, (b) đọc được báo cáo coverage và biết con số đó nói gì / **không** nói gì,
(c) dựng được một pipeline CI tối thiểu tự chạy test.

Nhóm cũng ghi nhận hai yêu cầu trong đề mà nhóm cho là then chốt khi chấm điểm, và thiết kế
toàn bộ bài làm xoay quanh chúng:

| Yêu cầu trong đề | Nhóm xử lý thế nào |
|---|---|
| *"Chỉ show được kết quả, không thể hiện được các bước làm rõ ràng cụ thể sẽ không được điểm cao"* | Mọi demo đều để lại dấu vết kiểm chứng được: commit history theo từng vòng TDD, log pipeline chạy thật, và **hai** báo cáo coverage ở hai thời điểm trước/sau. Không dùng ảnh chụp kết quả cuối làm bằng chứng duy nhất. |
| *"Chỉ rõ những trường hợp công cụ có điểm yếu, không giải quyết tốt mục tiêu đặt ra"* | Mỗi công cụ có một mục riêng về điểm yếu, và mỗi điểm yếu phải được chứng minh bằng code chạy thật trong repo của nhóm, không chỉ nói lý thuyết. |

---

## 2. Nội dung lý thuyết dự kiến

### Phần 1 — Unit Test

| Mục | Nội dung | Minh chứng kèm theo |
|---|---|---|
| 1.1 | Unit test là gì; "unit" là gì; vị trí trong kim tự tháp kiểm thử | Bảng đo thời gian chạy thật trên case study của nhóm |
| 1.2 | Nguyên tắc FIRST (Fast, Independent, Repeatable, Self-validating, Timely) | Mỗi nguyên tắc ghép với một ví dụ **vi phạm** lấy từ code thật |
| 1.3 | Cấu trúc AAA (Arrange – Act – Assert) | Trích trực tiếp từ test của nhóm |
| 1.4 | Test Double: Dummy, Stub, Spy, Mock, Fake — phân biệt 5 loại | Ví dụ Mockito cho từng loại |
| 1.5 | Nên test cái gì, không nên test cái gì | Đối chiếu với báo cáo coverage: chỗ nào **cố ý** để trống và vì sao |
| 1.6 | Quan hệ với TDD: vòng đỏ – xanh – refactor | Chính commit history của nhóm là minh chứng |

### Phần 2 — Code Coverage

| Mục | Nội dung | Minh chứng kèm theo |
|---|---|---|
| 2.1 | Coverage đo *mã được chạy qua*, **không** đo *mã được kiểm chứng* | Demo 100% độ phủ với 0 assertion |
| 2.2 | Các loại coverage: Line, Statement, Branch, Method, Class, Condition | Đoạn `if (a && b)` minh hoạ line 100% nhưng branch 50% |
| 2.3 | Line vs Branch trên code thật | Hai báo cáo JaCoCo đặt cạnh nhau |
| 2.4 | Cách đọc báo cáo JaCoCo (cột Missed Branches, Cxty) | Ảnh chụp báo cáo của chính repo nhóm |
| 2.5 | Ngưỡng coverage hợp lý; vì sao "100%" là mục tiêu sai | Cấu hình coverage gate thật trong `pom.xml` |
| 2.6 | Mutation testing — thước đo chất lượng test mà coverage không đo được | Báo cáo PIT: mutant *sống* dù coverage 100% |

### Phần 3 — CI/CD

| Mục | Nội dung | Minh chứng kèm theo |
|---|---|---|
| 3.1 | Vì sao cần CI: vấn đề "chạy được trên máy tôi", integration hell | Một Pull Request fail thật rồi được sửa |
| 3.2 | Phân biệt CI / Continuous Delivery / Continuous Deployment | Chỉ rõ pipeline của nhóm dừng ở mức nào và vì sao |
| 3.3 | Cấu trúc pipeline: checkout → build → test → coverage gate → package | Chính file workflow của nhóm |
| 3.4 | Thuật ngữ GitHub Actions: workflow, job, step, runner, action, trigger, matrix, cache, artifact, secret | Đối chiếu từng thuật ngữ với dòng YAML tương ứng |
| 3.5 | Vì sao hai phần trước chỉ có giá trị khi được CI **bắt buộc** chạy | Demo coverage gate chặn merge |

---

## 3. Công cụ và case study

### Case study dùng xuyên suốt

Một ứng dụng **quản lý thư viện** (Java + Spring Boot REST API), nghiệp vụ *cho mượn sách*.
Nhóm chọn nghiệp vụ này vì nó cung cấp đủ ba loại tình huống cần thiết mà vẫn đủ nhỏ để trình bày:

- **`FineCalculator`** — tính phí trả sách trễ. Logic thuần, nhiều nhánh điều kiện
  (số ngày trễ × hạng thành viên × mức phí trần) → dùng để demo **branch coverage** và
  **data-driven test**.
- **`LoanService.borrow()`** — nghiệp vụ phối hợp nhiều repository, có 6 nhánh: sách không
  tồn tại · sách đang được mượn · thành viên không tồn tại · vượt hạn mức mượn · còn phí trễ
  chưa trả · mượn thành công → dùng để demo **Mockito** và phân biệt unit test với integration test.
- **`LoanController`** — `POST /api/loans` → dùng để demo kiểm thử tầng web và pipeline đầy đủ.

### Công cụ

Nhóm chọn **3 công cụ chính để demo sâu** (mỗi trụ một công cụ, mỗi công cụ đủ 3 kịch bản
demo như đề yêu cầu), kèm **khảo sát và so sánh các công cụ thay thế**:

| Trụ | Công cụ demo sâu | Các công cụ sẽ khảo sát & so sánh |
|---|---|---|
| Unit Test | **JUnit Jupiter + Mockito + AssertJ** | TestNG, Spock, JUnit 4; EasyMock, JMockit; Hamcrest |
| Code Coverage | **JaCoCo** | Cobertura, OpenClover, coverage của IntelliJ IDEA; thêm **PIT** (mutation testing) để chứng minh điểm yếu của coverage |
| CI/CD | **GitHub Actions** | Jenkins, GitLab CI, CircleCI |

Việc so sánh sẽ theo **7 trục thống nhất** cho cả ba trụ, để các bảng đọc ngang được:
*khả năng · độ dễ cài đặt · tích hợp Maven/IDE · hiệu năng · tài liệu & cộng đồng ·
giá & giấy phép · điểm yếu đã tự kiểm chứng.*

Nhóm tự quy định: ô nào nhóm **chưa tự kiểm** thì ghi rõ *"chưa kiểm"*, không điền theo cảm giác.

### Môi trường kỹ thuật

Java 25 (LTS) · Maven 3.9 · Spring Boot 4.1 · JUnit Jupiter 6 · Mockito 5 · AssertJ 3 ·
H2 (database in-memory) · JaCoCo 0.8.15 · PIT 1.30 · GitHub Actions.

> **Một điểm nhóm xin ý kiến:** tài liệu phổ thông trên mạng phần lớn viết cho Spring Boot 3
> và "JUnit 5". Nhóm đang dùng bản mới hơn (Spring Boot 4, Jupiter 6) vì khớp với JDK 25 trên
> máy nhóm; các annotation dùng trong seminar (`@Test`, `@ParameterizedTest`, `@CsvSource`,
> `@Nested`, `@DisplayName`) giống nhau giữa hai bản. Nhóm sẽ ghi chú rõ điểm khác biệt, hoặc
> hạ về Java 21 + Spring Boot 3.5 nếu GVTH thấy nên ưu tiên việc các bạn trong lớp dễ làm theo.

---

## 4. Các demo dự kiến

Đề yêu cầu mỗi công cụ có ít nhất 3 kịch bản: **cài đặt · chức năng cơ bản · luồng xử lý
phức tạp**. Nhóm dự kiến **9 demo công cụ + 4 demo AI**.

### 9 demo công cụ

| Mã | Công cụ | Kịch bản | Nội dung | Số đo / minh chứng để lại |
|---|---|---|---|---|
| UT-1 | JUnit | Cài đặt | Thêm thư viện test, chạy `mvn test` lần đầu, đọc kết quả Surefire | Log, thư mục báo cáo Surefire |
| UT-2 | JUnit | Cơ bản | Viết `FineCalculator` theo TDD: đỏ → xanh → refactor; cấu trúc AAA; test chạy nhiều bộ dữ liệu từ file CSV | **Commit history từng vòng đỏ/xanh** |
| UT-3 | Mockito | Phức tạp | `LoanService` 6 nhánh nghiệp vụ, mock 3 repository, `verify`, `ArgumentCaptor`, dùng `Clock` cố định để test không phụ thuộc thời gian thật | File test + báo cáo Surefire |
| CC-1 | JaCoCo | Cài đặt | Thêm plugin, sinh báo cáo HTML, giải thích từng cột | Ảnh chụp báo cáo |
| CC-2 | JaCoCo | Cơ bản | Đo coverage với 1 test → bổ sung test cho nhánh còn đỏ → đo lại | **Hai báo cáo trước/sau** |
| CC-3 | JaCoCo | Phức tạp | Bật coverage gate (branch ≥ 90% cho `FineCalculator`); xoá 1 test → build **fail**; khôi phục → xanh; gắn gate vào CI | Log cả hai trạng thái |
| CI-1 | GitHub Actions | Cài đặt | Workflow tối thiểu; xem lần chạy đầu tiên; đọc log từng step | Link lần chạy |
| CI-2 | GitHub Actions | Cơ bản | Thêm cache thư viện, tải báo cáo coverage về dạng artifact, ghi summary | **Thời gian build trước/sau khi có cache** |
| CI-3 | GitHub Actions | Phức tạp | Nhiều job nối tiếp; chạy song song trên Java 21 và 25; chặn merge khi coverage gate fail | **Link PR đỏ rồi xanh** |

### Ánh xạ sang 3 phần mà đề yêu cầu — **nhóm xin ý kiến GVTH ở điểm này**

Đề yêu cầu mỗi công cụ có đủ **Record and Playback · Data driven · Checkpoints**. Nhóm hiểu
đây là khung quen thuộc của công cụ kiểm thử tự động giao diện (Selenium IDE, Katalon), không
ánh xạ trực tiếp sang unit test / coverage / CI-CD. Nhóm đề xuất cách hiểu tương đương sau:

| Phần trong đề | Nhóm hiểu là | Demo tương ứng |
|---|---|---|
| **Record and Playback** | Sinh test tự động thay vì gõ tay (IDE tạo khung test, **AI sinh test từ source**), rồi "playback" = chạy lại bộ test đó trong pipeline | UT-1, AI-1, CI-1 |
| **Data driven** | Một test chạy với nhiều bộ dữ liệu: `@ParameterizedTest` đọc dữ liệu từ file CSV bên ngoài | UT-2, AI-4 |
| **Checkpoints** | Các điểm kiểm chứng làm **fail build**: assertion, `verify()` của Mockito, coverage gate, quality gate trong pipeline | UT-3, CC-3, CI-3 |

Nếu GVTH muốn nhóm hiểu theo hướng khác, nhóm xin điều chỉnh ngay ở giai đoạn này, trước khi
đầu tư làm demo.

---

## 5. Áp dụng AI vào chủ đề

Đề yêu cầu demo AI *"có khả năng tổng quát hóa, tái sử dụng"*. Nhóm hiểu điều đó nghĩa là mỗi
demo phải để lại một **tài sản dùng lại được** (prompt template có tham số, hoặc script), chứ
không phải một đoạn hội thoại chụp ảnh lại. Dự kiến 4 demo:

| Mã | Demo | Tài sản để lại | Đo bằng gì |
|---|---|---|---|
| AI-1 | AI sinh unit test từ một class | Prompt template có tham số + **checklist review bắt buộc** | Coverage trước/sau; **số test AI sinh ra bị sai phải sửa tay** |
| AI-2 | AI đọc báo cáo coverage → chỉ ra nhánh chưa phủ → sinh test còn thiếu | Script lọc báo cáo XML thành đầu vào cho AI (chạy được với bất kỳ project Maven nào) | Branch coverage trước/sau; số nhánh AI chỉ đúng / chỉ sai |
| AI-3 | AI tự động nhận xét chất lượng test trên mỗi Pull Request | Một job trong pipeline CI | Trên một PR có lỗi **cài sẵn**: số vấn đề thật / số báo động giả |
| AI-4 | AI sinh bộ dữ liệu biên cho data-driven test | Prompt template + file CSV | So bộ của AI với bộ người tự viết: trùng bao nhiêu, AI tìm thêm gì, **AI bỏ sót gì** |

**Kết luận nhóm muốn lớp mang về** (và sẽ chứng minh bằng số liệu, không nói suông):

| AI làm tốt | AI làm không tốt |
|---|---|
| Sinh khung test nhanh, tiết kiệm thời gian gõ | Quyết định *điều gì đáng kiểm chứng* |
| Liệt kê ca biên mà người hay quên | Hiểu nghiệp vụ thật đằng sau mã nguồn |
| Đọc báo cáo coverage dài và chỉ chỗ thiếu | Biết nhánh nào **cố ý** không test |

→ Vị trí đúng của AI: **tăng tốc bước gõ, không thay thế bước suy nghĩ.**

Nhóm cũng cam kết quy ước sử dụng AI: mọi nội dung AI sinh ra phải qua ba cửa — *chạy được ·
đối chiếu tài liệu chính thức · có thành viên đứng tên commit chịu trách nhiệm*. Riêng các
**con số** (coverage, thời gian build) và **nhận định về điểm yếu công cụ** thì nhóm tự chạy,
tự đo, không dùng AI. Video demo do nhóm tự quay và tự thuyết minh.

---

## 6. Sản phẩm sẽ nộp

| # | Sản phẩm | Hình thức |
|---|---|---|
| 1 | Slide trình bày | HTML, nền trắng chữ đen cỡ lớn, không phụ thuộc mạng khi trình bày |
| 2 | Báo cáo chi tiết | LaTeX → PDF |
| 3 | Video demo | Nhóm tự quay, nền trắng chữ đen, có thuyết minh; đăng YouTube và dẫn link rõ trong slide |
| 4 | Bài tập áp dụng | Kèm gợi ý thực hiện để các bạn trong lớp làm theo |
| 5 | Phân công + minh chứng | GitHub Issues (việc được giao) + commit (việc đã làm) + GitHub Projects (tiến độ theo thời gian) |
| 6 | Source code | Repository GitHub: case study, bộ test, cấu hình coverage, workflow CI |
| 7 | Tài sản AI | Prompt template và script, dùng lại được cho project khác |

---

## 7. Phân công nhóm

| Vai | Phụ trách |
|---|---|
| TV1 — Trưởng nhóm / CI-CD | GitHub Actions, GitHub Projects, tổng hợp tài liệu |
| TV2 — Unit Test | Lý thuyết unit test, JUnit + Mockito, test cho `LoanService` |
| TV3 — Code Coverage | JaCoCo, mutation testing, luận điểm "coverage ≠ chất lượng" |
| TV4 — Case study | Mã nghiệp vụ, `FineCalculator`, controller và test tương ứng |
| TV5 — AI & trình bày | 4 demo AI, slide HTML, báo cáo LaTeX |

Mỗi thành viên **sở hữu một tập file riêng** để 5 người làm song song không tranh chấp; cần
sửa file của người khác thì mở issue gán cho chủ file. Quy tắc làm việc: một đầu việc = một
issue = một nhánh = một Pull Request; PR phải xanh CI mới được merge.

---

## 8. Tiến độ dự kiến

| Giai đoạn | Nội dung | Trạng thái |
|---|---|---|
| Tuần 2–3 | Chốt phạm vi, công cụ, case study; đề xuất nội dung này; dựng repo và khung case study chạy được | **Đang trình GVTH** |
| Tuần 3–4 | Case study đầy đủ + bộ unit test (demo UT-1, UT-2, UT-3) | Dự kiến |
| Tuần 4 | Coverage đầy đủ + coverage gate + chứng minh coverage ≠ chất lượng (CC-1→CC-3) | Dự kiến |
| Tuần 5 | Pipeline CI 3 cấp độ + đối chiếu Jenkins (CI-1→CI-3) | Dự kiến |
| Tuần 5 | 4 demo AI, đo số liệu | Dự kiến |
| **Tuần 6** | **Nộp bài chấm điểm:** slide, báo cáo, video, bài tập áp dụng, phân công kèm minh chứng | Dự kiến |
| Trước tuần seminar | Trình bày thử, xin góp ý GVTH | Dự kiến |
| Tuần 12 | Nộp bản hiệu chỉnh cuối môn | Dự kiến |

---

## 9. Những điểm nhóm xin ý kiến GVTH

1. **Cách ánh xạ "Record and Playback / Data driven / Checkpoints"** ở mục 4 có được chấp nhận
   không? Đây là câu quan trọng nhất, vì nếu hiểu sai thì nhóm phải làm lại phần lớn demo.
2. **Số lượng công cụ:** 3 công cụ chính demo sâu + khảo sát/so sánh các công cụ thay thế có
   đủ theo yêu cầu *"ít nhất 2-3 công cụ"*, hay nhóm cần 2 công cụ demo sâu cho **mỗi** trụ?
3. **Phần AI:** 4 demo ở mục 5 có đúng kỳ vọng *"tổng quát hóa, tái sử dụng"* không? Có cần
   thêm hướng nào, ví dụ AI sinh ca kiểm thử từ tài liệu đặc tả thay vì từ mã nguồn?
4. **Bài tập áp dụng:** bao nhiêu bài là phù hợp? Mức độ chỉ viết test cho mã cho sẵn, hay bao
   gồm cả dựng pipeline? Có cần kèm đáp án?
5. **Minh chứng phân công:** GitHub Issues + commit + Projects có được tính là minh chứng hợp
   lệ, hay nhóm cần thêm biên bản họp / bảng công theo tuần?
6. **Phiên bản kỹ thuật:** giữ Java 25 + Spring Boot 4 (mới, khớp máy nhóm) hay hạ về Java 21 +
   Spring Boot 3.5 (tài liệu phổ biến hơn, lớp dễ làm theo)?
7. **Mốc thời gian:** Tuần 6 nộp bài là ngày nào, nộp qua kênh nào? Repo có nên để public
   không (nhóm muốn public để pipeline CI miễn phí không giới hạn và log chạy dùng được làm
   minh chứng)?
