# Thiết kế Seminar: Unit Test · Code Coverage · CI/CD

- **Môn học:** Software Testing — FIT@HCMUS
- **Nhóm:** 5 thành viên
- **Ngày lập:** 2026-10-01
- **Nguồn yêu cầu:** [require.md](../../../require.md)
- **Giai đoạn hiện tại:** Gặp mặt Tuần 2–3 — trình bày nội dung dự kiến để GV góp ý

---

## 1. Mục tiêu

Xây dựng một bài seminar giúp sinh viên **chưa biết gì** về unit test, code coverage và
CI/CD có thể hiểu và tự làm được ở mức cơ bản, đồng thời thể hiện rõ công sức làm việc
nhiều tuần của 5 thành viên.

**Thành công nghĩa là:**

1. Một người trong lớp đọc slide + làm bài tập áp dụng là viết được unit test có ý nghĩa,
   đọc được báo cáo coverage, và dựng được pipeline CI tối thiểu cho project Java của họ.
2. GV thấy được **quá trình làm**, không chỉ kết quả: commit tăng dần, issue được gán
   người, log pipeline chạy thật, coverage trước/sau.
3. Không mất điểm ở 4 mốc trừ điểm của đề (−1đ / −3đ / −4đ).

## 2. Hai yêu cầu dễ mất điểm nhất (thiết kế phải chống lại)

**(a) "Chỉ show kết quả, không thể hiện các bước làm rõ ràng cụ thể sẽ không được điểm cao"**
→ Mọi demo phải để lại dấu vết kiểm chứng được: commit history, run log của CI, báo cáo
JaCoCo của *hai* thời điểm (trước và sau khi bổ sung test). Không dùng ảnh chụp kết quả
cuối làm bằng chứng duy nhất.

**(b) "Chỉ rõ những trường hợp công cụ có điểm yếu, không giải quyết tốt mục tiêu"**
→ Đây là mục bắt buộc cho từng công cụ, và phải chứng minh bằng ví dụ chạy thật. Các điểm
yếu sẽ demo:

| Công cụ | Điểm yếu được chứng minh bằng code chạy thật |
|---|---|
| JUnit + Mockito | Mock quá sâu → test pass nhưng hệ thống sai (test xác nhận mock, không xác nhận hành vi); không mock được `static`/`final` mà không thêm `mockito-inline`; test xanh nhưng thiếu assertion |
| JaCoCo | 100% line coverage với test **không có assertion** nào → coverage ≠ chất lượng; nhánh trong lambda/switch pattern đếm không như trực giác; không phát hiện test thiếu kiểm chứng (phải dùng mutation testing mới lộ ra) |
| GitHub Actions | Khó debug local (phải push mới biết sai); giới hạn phút miễn phí với repo private; vendor lock-in cú pháp YAML; cache phụ thuộc dễ gây "pass trên máy tôi, fail trên CI" |

## 3. Quyết định kỹ thuật đã chốt

| Hạng mục | Chốt | Lý do |
|---|---|---|
| JDK | **Java 25 LTS** (đã cài: 25.0.2) | Khớp máy nhóm, không cần cài thêm; JaCoCo 0.8.15 hỗ trợ chính thức Java 25 |
| Build | **Maven 3.9.16** (đã cài) | — |
| Framework | **Spring Boot 4.1.1** | Nhánh hỗ trợ Java 25 ổn định; quản lý sẵn Jupiter/Mockito/AssertJ nên không phải tự pin version |
| Unit test | **JUnit Jupiter 6.0.3** + **Mockito 5.23.0** + **AssertJ 3.27.7** (Spring Boot 4.1.1 quản lý) | — |
| Coverage | **JaCoCo 0.8.15** | Chuẩn de-facto cho Maven; có `check` goal để làm coverage gate |
| CI/CD | **GitHub Actions** | Chạy thật trên cloud, log public làm minh chứng, dễ quay video |
| Mutation testing | **PIT 1.30.0** — chỉ dùng để *chứng minh điểm yếu của JaCoCo*, không phải công cụ chính | — |
| Database | **H2 in-memory 2.4.240** cho gói này | Nhẹ, không cần Docker, CI chạy nhanh. Postgres + Testcontainers để dành Gói 4 ("luồng xử lý phức tạp") |
| Slide | **HTML/CSS tự viết, không CDN** | Nền trắng chữ đen chữ to theo đề; **không phụ thuộc mạng** khi trình bày (reveal.js qua CDN sẽ trắng trang nếu phòng học mất mạng) |
| Báo cáo | **LaTeX `.tex`, giao file nguồn, không build PDF** | Theo yêu cầu của nhóm |
| Nguồn sự thật | **Markdown trong `docs/`** | Slide và `.tex` dẫn xuất từ đây; review theo commit chính là minh chứng quá trình |
| Quản lý việc | **GitHub Projects + Issues** | Minh chứng phân công tự sinh (issue gán người ↔ commit/PR) |

**Lưu ý thuật ngữ:** Đề và tài liệu phổ thông gọi là "JUnit 5". Chúng ta chạy **Jupiter 6.0.3**
(phiên bản Spring Boot 4.1.1 quản lý). Các API dùng trong seminar (`@Test`, `@ParameterizedTest`,
`@CsvSource`, `@MethodSource`, `@Nested`, `@DisplayName`) giống nhau giữa Jupiter 5 và 6.
Báo cáo sẽ có một hộp ghi chú nói rõ điều này để người đọc không bị lẫn khi tra tài liệu.

## 4. Case study

**Domain: Quản lý thư viện — nghiệp vụ cho mượn sách.** Chọn domain này vì nó cho đủ ba thứ
cần thiết mà vẫn đủ nhỏ để lên slide:

- `FineCalculator` — logic thuần, nhiều nhánh điều kiện (số ngày trễ × hạng thành viên).
  Dùng để demo **branch coverage** và **data-driven test** (`@ParameterizedTest`).
- `LoanService` — nghiệp vụ phối hợp nhiều repository. Dùng để demo **Mockito**
  (stub, `verify`, `ArgumentCaptor`) và sự khác nhau giữa unit test và integration test.
- `LoanController` — REST endpoint. Dùng để demo `@WebMvcTest` và tầng ngoài cùng của pipeline.

**Các nhánh nghiệp vụ của `LoanService.borrow()`** (đây là nguồn của branch coverage):
sách không tồn tại · sách đang được mượn · thành viên không tồn tại · thành viên vượt hạn
mức mượn · thành viên còn phí trễ chưa trả · mượn thành công.

## 5. Diễn giải dòng 22 của đề — **cần GV xác nhận**

Đề yêu cầu mỗi công cụ có đủ **Record and Playback · Data driven · Checkpoints**. Đây là
khung của công cụ automation UI (Selenium IDE, Katalon), không map tự nhiên vào unit test /
coverage / CI-CD. Nhóm đề xuất diễn giải tương đương sau và sẽ hỏi GV ở buổi gặp mặt:

| Thuật ngữ trong đề | Tương đương trong chủ đề này | Demo cụ thể |
|---|---|---|
| **Record and Playback** | Sinh test tự động thay vì gõ tay | IDE generate test skeleton; **AI sinh test JUnit từ class** (đo coverage trước/sau); "playback" = chạy lại bộ test đã sinh trong CI |
| **Data driven** | Một test, nhiều bộ dữ liệu | `@ParameterizedTest` + `@CsvSource` / `@MethodSource` / `@CsvFileSource` đọc CSV ngoài; **AI sinh bộ dữ liệu biên** |
| **Checkpoints** | Điểm kiểm chứng làm fail build | `assertThat` (AssertJ), `verify()` / `ArgumentCaptor` (Mockito), **`jacoco:check` fail build khi branch coverage tụt dưới ngưỡng**, quality gate trong workflow |

## 6. Phần AI (4 demo, phải tái sử dụng được)

Yêu cầu của đề: *"có khả năng tổng quát hóa, tái sử dụng"* → mỗi demo AI không chỉ là một
lần chat, mà là **một tài sản dùng lại được**: prompt template có tham số, hoặc script.

| # | Demo | Tài sản để lại | Đo bằng gì |
|---|---|---|---|
| AI-1 | Sinh unit test từ source class | Prompt template + checklist review | Coverage trước/sau; **số test AI sinh ra bị sai phải sửa tay** (số này là phần trung thực nhất của báo cáo) |
| AI-2 | Đọc báo cáo JaCoCo → chỉ ra nhánh chưa phủ → sinh test còn thiếu | Script trích XML JaCoCo thành prompt | Branch coverage trước/sau |
| AI-3 | AI review Pull Request trong pipeline | GitHub Actions job (API key đọc từ **GitHub Secrets**, không hard-code) | Số vấn đề thật / số báo động giả trên 1 PR có lỗi cài sẵn |
| AI-4 | Sinh bộ test data biên cho `@ParameterizedTest` | Prompt template + file CSV sinh ra | So với bộ ca kiểm thử người viết: trùng bao nhiêu, bỏ sót gì |

**Ràng buộc:** API key của nhóm **không được xuất hiện trong repo, slide, video, hay chat**.
Demo AI-3 đọc key từ GitHub Secrets; bản chạy local đọc từ biến môi trường. Nếu chưa cấu
hình được Secrets, AI-3 có bản chạy local (script + ảnh chụp output) làm dự phòng.

## 7. Phạm vi gói này: Gặp mặt Tuần 2–3

Đây là **gói 1 trong 7**. Mục tiêu: có đủ thứ để GV góp ý và chỉnh hướng *trước khi* nhóm
đầu tư nhiều tuần, và không bị đánh giá "chuẩn bị sơ sài" (−1đ).

**Trong phạm vi:**

1. Văn bản **đề xuất nội dung dự kiến** cho GV đọc.
2. **Outline chi tiết** cả 3 trụ (mục lục tới cấp mục con, kèm điều sẽ nói ở mỗi mục).
3. **Bảng khảo sát & so sánh công cụ** (bản dự kiến, các trục so sánh đã chốt).
4. **Ma trận 9 demo** (3 công cụ × 3 kịch bản) — mô tả từng demo làm gì, đo gì.
5. **Kế hoạch 4 demo AI.**
6. **Mapping dòng 22** + danh sách **câu hỏi cho GV.**
7. **Phân công 5 thành viên** + quy ước sử dụng AI của nhóm.
8. **Slice case study chạy được**: `FineCalculator` + `LoanService` + `LoanController`,
   có unit test, có báo cáo JaCoCo, có workflow GitHub Actions — để GV thấy kế hoạch là thật
   chứ không phải hứa.
9. **Khung slide HTML** cho buổi gặp mặt + **khung báo cáo `.tex`**.

**Ngoài phạm vi (để dành các gói sau):** nội dung lý thuyết đầy đủ cho slide chính thức;
Postgres + Testcontainers; 4 demo AI triển khai thật; video; bài tập áp dụng; bản báo cáo
hoàn chỉnh; Jenkins đối chiếu.

## 8. Cấu trúc file

```
seminar/
├── README.md                        Điểm vào: trạng thái, link mọi tài liệu
├── require.md                       Đề bài (không sửa)
├── docs/
│   ├── 00-de-xuat-noi-dung.md       ★ Văn bản GV đọc ở buổi gặp mặt
│   ├── 01-outline-unit-test.md
│   ├── 02-outline-code-coverage.md
│   ├── 03-outline-cicd.md
│   ├── 04-khao-sat-so-sanh-cong-cu.md
│   ├── 05-ma-tran-demo.md
│   ├── 06-ke-hoach-ai.md
│   ├── 07-phan-cong-nhom.md
│   ├── 08-cau-hoi-cho-gv.md
│   ├── 09-quy-uoc-su-dung-ai.md
│   └── superpowers/{specs,plans}/
├── case-study/                      Maven project
│   ├── pom.xml
│   └── src/
│       ├── main/java/vn/edu/hcmus/fit/library/
│       │   ├── LibraryApplication.java
│       │   ├── domain/{Book,Member,Loan,MemberTier}.java
│       │   ├── fine/FineCalculator.java
│       │   ├── loan/{LoanService,LoanController,BorrowRequest,BorrowResult}.java
│       │   ├── repo/{BookRepository,MemberRepository,LoanRepository}.java
│       │   └── error/BorrowException.java
│       ├── main/resources/application.yml
│       └── test/java/.../{FineCalculatorTest,LoanServiceTest,LoanControllerTest}.java
├── slides/
│   ├── index.html                   Slide buổi gặp mặt (nền trắng, chữ đen, chữ to)
│   └── slides.css
├── report/
│   ├── main.tex
│   ├── refs.bib
│   └── sections/*.tex
└── .github/workflows/ci.yml
```

**Nguyên tắc tách file:** mỗi file `docs/` phục vụ một mục đích trình bày duy nhất và một
người chịu trách nhiệm → 5 thành viên làm song song không tranh chấp file. Code tách theo
*nghiệp vụ* (`fine/`, `loan/`), không tách theo tầng kỹ thuật.

## 9. Phân công 5 thành viên

Tên thật do nhóm điền; vai trò và ranh giới file đã chốt để không tranh chấp:

| Vai | Phụ trách | File sở hữu |
|---|---|---|
| TV1 — Trưởng nhóm / CI-CD | GitHub Actions, GitHub Projects, tổng hợp đề xuất | `.github/workflows/`, `docs/00`, `docs/03`, `docs/07` |
| TV2 — Unit Test | JUnit + Mockito, lý thuyết unit test | `docs/01`, `LoanServiceTest.java` |
| TV3 — Coverage | JaCoCo, mutation testing, chứng minh coverage ≠ chất lượng | `docs/02`, cấu hình JaCoCo trong `pom.xml` |
| TV4 — Case study | Code nghiệp vụ, `FineCalculator`, controller | `case-study/src/main/**`, `FineCalculatorTest`, `LoanControllerTest` |
| TV5 — AI & trình bày | 4 demo AI, slide HTML, báo cáo `.tex` | `docs/06`, `slides/`, `report/` |

Bảng khảo sát/so sánh công cụ (`docs/04`) và ma trận demo (`docs/05`) là việc chung, mỗi
người viết phần công cụ mình phụ trách.

## 10. Ràng buộc

- **GitHub:** mọi hành động chạm tới GitHub (tạo/đổi repo, `git push`, lệnh `gh`, bật
  Actions, tạo GitHub Projects) phải được chủ repo đồng ý trước từng lần. Commit local
  không cần hỏi.
- **API key AI:** không bao giờ nằm trong repo, slide, video. Chỉ qua GitHub Secrets hoặc
  biến môi trường.
- **Trình bày:** slide nền trắng chữ đen chữ to; không phụ thuộc CDN/mạng.
- **Chính chủ:** video do nhóm tự quay và tự thuyết minh. AI được dùng nhưng nhóm phải
  review và chịu trách nhiệm; `docs/09` ghi rõ dùng AI ở đâu và review thế nào.
- **Không dùng lại** 5 file tài liệu ở commit `52ec671` — nội dung xây mới hoàn toàn.

## 11. Rủi ro

| Rủi ro | Xử lý |
|---|---|
| Spring Boot 4.1.1 / Jupiter 6 mới, tài liệu trên mạng phần lớn viết cho Boot 3 / JUnit 5 | Hộp ghi chú trong báo cáo; API dùng trong seminar giống nhau. Nếu vướng thật, hạ xuống Java 21 + Spring Boot 3.5.x (phải cài thêm JDK 21) |
| GV không đồng ý cách diễn giải dòng 22 | Đã đưa thành câu hỏi riêng trong `docs/08`, hỏi ngay buổi gặp mặt — trước khi đầu tư làm demo |
| Phút GitHub Actions miễn phí cạn | Repo public → Actions miễn phí không giới hạn. Nếu phải để private thì chạy `act` local, hoặc giới hạn trigger |
| 7 deliverable quá nhiều, trễ Tuần 6 (−3đ) | Chia 7 gói, mỗi gói có kế hoạch riêng và cho ra sản phẩm chạy được; gói gặp mặt làm trước để GV chỉnh hướng sớm |

## 12. Roadmap các gói sau

| Gói | Nội dung | Phụ thuộc |
|---|---|---|
| 1 | **Gói gặp mặt Tuần 2–3** (gói này) | — |
| 2 | Case study đầy đủ + bộ unit test hoàn chỉnh (đủ 3 kịch bản demo) | Gói 1 |
| 3 | JaCoCo đầy đủ + coverage gate + chứng minh coverage ≠ chất lượng (PIT) | Gói 2 |
| 4 | Pipeline GitHub Actions 3 cấp độ + Postgres/Testcontainers + bảng so sánh Jenkins | Gói 2, 3 |
| 5 | 4 demo AI triển khai thật, đo được | Gói 2, 3, 4 |
| 6 | Nội dung lý thuyết đầy đủ → slide HTML chính thức + báo cáo `.tex` + bài tập áp dụng | Gói 2–5 |
| 7 | Kịch bản video + quay + GitHub Projects + bảng minh chứng phân công | Gói 6 |

## 13. Câu hỏi cho GV ở buổi gặp mặt

1. Cách diễn giải **Record&Playback / Data driven / Checkpoints** ở mục 5 có được chấp nhận không?
2. "Ít nhất 2–3 công cụ" — 3 công cụ chính demo sâu + bảng so sánh alternatives có đủ không,
   hay cần 2 công cụ cho *mỗi* trụ?
3. Phần AI: 4 demo như mục 6 có đúng kỳ vọng "tổng quát hóa, tái sử dụng" không?
4. Bài tập áp dụng: bao nhiêu bài, mức độ nào là phù hợp?
5. Minh chứng phân công: GitHub Issues + commit có được tính là minh chứng hợp lệ không?
6. Tuần 6 nộp bài là ngày nào cụ thể, nộp qua kênh nào?
