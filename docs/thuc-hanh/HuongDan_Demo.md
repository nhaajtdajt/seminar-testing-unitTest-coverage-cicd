# Hướng dẫn chạy và kịch bản demo — gói tuần 06

## 1. Môi trường và đặc tả

Chạy các lệnh từ thư mục gốc repository. Dùng JDK 25 và Python 3.10+. Maven không cần cài sẵn: mọi lệnh gọi `case-study/mvnw`, wrapper tự tải Maven 3.9.16. POM theo đúng thiết kế gốc: Spring Boot 4.1.1, JaCoCo 0.8.15, PIT 1.30.0 và pitest-junit5-plugin 1.2.3; JUnit Jupiter 6.0.3, Mockito 5.23.0, AssertJ 3.27.7 và H2 2.4.240 do Spring Boot quản lý. Xem phiên bản bằng `case-study/mvnw -f case-study/pom.xml dependency:list`. Lưu ý Spring Boot 4 đã tách module: `@WebMvcTest`/`@AutoConfigureMockMvc` nằm ở `org.springframework.boot.webmvc.test.autoconfigure`, `@DataJpaTest` ở `org.springframework.boot.data.jpa.test.autoconfigure`; nhiều tài liệu trên mạng vẫn viết theo Boot 3.

Tính phí (VND): NORMAL không gia hạn, 2.000/ngày; VIP gia hạn 2 ngày, 1.000/ngày sau gia hạn; mức trần 50.000. Ngày âm hoặc hạng null bị từ chối. Tính bằng `long` trước khi tạo `BigDecimal` để không tràn số với `Integer.MAX_VALUE` ngày.

Mượn sách: sách tồn tại và còn rảnh; thành viên tồn tại; đang mượn ít hơn 3 sách; không còn phí chưa trả. Thành công lưu phiếu và đánh dấu sách bận. Thời gian lấy qua `Clock` để test dùng được giờ cố định. Dữ liệu nằm trong H2 in-memory (Spring Data JPA), không phải cơ sở dữ liệu lưu bền hay cấu hình transaction cho triển khai nhiều máy.

## 2. UT-1 — Cài đặt và chạy test

```bash
case-study/mvnw -B -ntp -f case-study/pom.xml clean test
```

Mở `case-study/target/surefire-reports`. Giải thích Tests, Failures, Errors, Skipped. `FineCalculatorTest` là unit test logic thuần; `LoanServiceTest` dùng mock repository; `LoanControllerTest` là kiểm thử tầng web; `LoanFlowTest` là integration test qua controller, service và repository thật trên H2 in-memory.

## 3. UT-2 — TDD và data driven

`FineCalculatorTest` nạp `src/test/resources/fine-cases.csv` bằng `@CsvFileSource`. Đối chiếu các dòng 24/25/26 ngày NORMAL và 51/52/53 ngày VIP với mức trần. Mỗi dòng CSV tạo một lượt kiểm thử, không phải một file test riêng.

Bốn vòng TDD đã được tái hiện tại `evidence/tuan-05/tdd-replay`: 0 ngày → NORMAL 3 ngày → VIP 3 ngày → chạm trần. Mỗi vòng có source, test, Surefire XML và log đỏ/xanh. Script `python3 scripts/tdd_replay.py` chạy trong thư mục tạm và không sửa case study chính. Script từ chối ghi đè minh chứng đã có; muốn chạy lại, dùng bản sao repository và một thư mục evidence mới. Đây là bài thực hành tái hiện TDD ở hiện tại; không phải commit lịch sử của thành viên trong các tuần trước.

## 4. UT-3 — Mockito và 6 tình huống mượn sách

```bash
case-study/mvnw -B -ntp -f case-study/pom.xml -Dtest=LoanServiceTest test
```

Đọc lần lượt: BOOK_NOT_FOUND, BOOK_UNAVAILABLE, MEMBER_NOT_FOUND, LIMIT_REACHED, UNPAID_FINE, thành công. Chỉ stub dữ liệu cần cho nhánh đang chạy; kiểm `never()`/`verifyNoInteractions` để bảo đảm nhánh lỗi không ghi dữ liệu. `ArgumentCaptor` kiểm phiếu thực sự có đúng mã sách, thành viên và giờ cố định.

Mock có thể che lỗi ở chỗ kết nối các thành phần; vì vậy `LoanFlowTest` chạy thêm với service/repository thật. Mockito 5 dùng inline mock maker mặc định, hỗ trợ mock final/static; nhận định cần thêm `mockito-inline` trong một số tài liệu đề xuất cũ cần được sửa theo phiên bản. Không mock chính lớp tính phí khi mục tiêu là kiểm logic tính phí.

## 5. CC-1/CC-2 — Đọc coverage và so trước/sau

```bash
case-study/mvnw -B -ntp -f case-study/pom.xml -Pbaseline clean verify
# Lưu target/site/jacoco sang thư mục riêng trước khi chạy lần tiếp theo.
case-study/mvnw -B -ntp -f case-study/pom.xml clean verify
```

Mở `target/site/jacoco/index.html`; chọn `FineCalculator`. Cột Branch khác cột Line. Bộ baseline chỉ kiểm 1 ca; bộ đầy đủ kiểm dữ liệu biên và ngoại lệ. Bản baseline chủ động tắt gate để thu báo cáo ban đầu, không dùng cấu hình đó để đánh giá chất lượng bản nộp.

Minh chứng đã lưu riêng ở `evidence/tuan-05/baseline/site/jacoco` và `evidence/tuan-05/final/site/jacoco`, tránh lần chạy sau ghi đè lần trước.

### CC-0 — Các loại coverage trên `LoanPeriodPolicy`

Chạy cộng dồn từng test T1–T4, mỗi lượt mở `target/site/jacoco/vn.edu.seminar.loan/LoanPeriodPolicy.java.html` để xem dòng xanh/vàng và số nhánh:

```bash
case-study/mvnw -B -ntp -f case-study/pom.xml clean verify -Dcoverage.gate.skip=true "-Dtest=LoanPeriodPolicyTest#t1*"
case-study/mvnw -B -ntp -f case-study/pom.xml clean verify -Dcoverage.gate.skip=true "-Dtest=LoanPeriodPolicyTest#t1*+t2*"
case-study/mvnw -B -ntp -f case-study/pom.xml clean verify -Dcoverage.gate.skip=true "-Dtest=LoanPeriodPolicyTest#t1*+t2*+t3*"
# Phản chứng condition ≠ decision: chỉ T2 + T3
case-study/mvnw -B -ntp -f case-study/pom.xml clean verify -Dcoverage.gate.skip=true "-Dtest=LoanPeriodPolicyTest#t2*+t3*"
```

Kỳ vọng nhánh JaCoCo: 3/6 → 5/6 → 6/6; bộ T2 + T3 cho 5/6 nhánh và dòng `days += 7` màu đỏ. Bảng giải thích ở `BaoCao_ChiTiet.md` mục 3.1; số đo đã lưu ở `evidence/tuan-06/coverage-types/`.

### CC-0b — Đối chiếu với OpenClover

Không cần sửa `pom.xml`; gọi plugin bằng tọa độ đầy đủ. Nên chạy trên một bản sao của `case-study/` để thư mục `target/` của OpenClover không lẫn với JaCoCo:

```bash
case-study/mvnw -B -ntp -f case-study/pom.xml clean org.openclover:clover-maven-plugin:4.5.2:setup test org.openclover:clover-maven-plugin:4.5.2:clover -Djacoco.skip=true -Dcoverage.gate.skip=true "-Dtest=LoanPeriodPolicyTest#t1*+t2*"
```

Mở `case-study/target/site/clover/index.html`: `LoanPeriodPolicy` báo 4/4 conditional (100%), trong khi JaCoCo cùng bộ test báo 5/6 nhánh. So sánh chi tiết ở `BaoCao_ChiTiet.md` mục 5.2.

## 6. CC-3 — Gate đỏ rồi xanh

```bash
# Kỳ vọng exit 1: chỉ chạy baseline nhưng bật lại gate 90%.
case-study/mvnw -B -ntp -f case-study/pom.xml -Pbaseline -Dcoverage.gate.skip=false clean verify
# Kỳ vọng exit 0: bộ test đầy đủ, giữ nguyên gate.
case-study/mvnw -B -ntp -f case-study/pom.xml clean verify
```

Đọc dòng `Rule violated` trong log đỏ và `All coverage checks have been met` trong log xanh. Gate áp dụng **branch coverage của FineCalculator >=90%**, không phải ngưỡng chung cho cả ứng dụng. Log tại máy chưa chứng minh GitHub chặn merge; cần cấu hình required status check trên repo có quyền quản trị.

## 7. Coverage cao nhưng test yếu — PIT

```bash
case-study/mvnw -B -ntp -f case-study/pom.xml -Pcoverage-trap clean verify
case-study/mvnw -B -ntp -f case-study/pom.xml -Pcoverage-trap test-compile org.pitest:pitest-maven:mutationCoverage
# Lưu target/pit-reports trước khi chạy đối chiếu.
case-study/mvnw -B -ntp -f case-study/pom.xml clean verify
case-study/mvnw -B -ntp -f case-study/pom.xml test-compile org.pitest:pitest-maven:mutationCoverage
```

`FineCalculatorTrapTest` đi qua các trường hợp hợp lệ mà không assert tiền; chỉ assert hai ngoại lệ. JaCoCo vẫn ghi đủ nhánh. PIT sửa bytecode rồi chạy lại: nhiều thay đổi sai số tiền không bị test yếu phát hiện. So sánh `pit-weak/pit-reports` với `pit-strong/pit-reports`. Test bẫy được gắn tag và loại khỏi lần chạy thông thường.

## 8. CI-1/CI-2/CI-3 — Đọc cấu hình và chạy trên GitHub

`.github/workflows/ci.yml` có ba job: `test` (JDK 25) → `coverage-gate` → `package`. Mỗi job dùng runner mới; không giả định `target/` của job trước còn tồn tại. Cache Maven khớp `pom.xml`; test report, coverage và JAR được upload thành artifact. Jenkinsfile làm ba bước tương ứng trên agent có JDK/Maven sẵn. Pipeline dừng ở kiểm tra/đóng gói, chưa triển khai ứng dụng lên server.

Phần chuẩn bị tại máy đã có. Người có quyền ghi cần đưa workflow lên nhánh riêng của repo, mở PR, bật required status checks và thu link run thực tế. Để demo PR đỏ → xanh: dùng thay đổi tạm làm bộ test tính phí thiếu nhánh, giữ gate 90%; kiểm job gate đỏ, rồi khôi phục test và kiểm xanh. Không giảm ngưỡng gate để làm xanh.

Tài khoản được kiểm trong phiên hiện tại có `viewerPermission=READ`, nên chưa tạo run/PR hoặc thay cấu hình repo. Không có link chạy CI/Jenkins trong minh chứng. `scripts/benchmark_maven.py cache` đo ba cặp Maven repo lạnh/ấm **tại máy**; không phải số đo cache của GitHub Actions.

Script cache dùng một kho dependency trống cho mỗi cặp nên phải tải lại nhiều file từ Maven Central, khác với build thông thường tái sử dụng `~/.m2`. Các lượt lỗi tải được giữ ở `evidence/tuan-05/benchmark-cache/failed-attempts/`. Script hỗ trợ `--resume` để bổ sung cặp còn thiếu và giữ nguyên các cặp đã hoàn thành. Mỗi cặp mới bắt đầu với kho dependency trống; lượt ấm dùng lại đúng kho của lượt lạnh vừa thành công.

```bash
# Chọn JDK 25 như hướng dẫn trong README trước khi chạy.
python3 scripts/benchmark_maven.py cache --resume --timeout-seconds 300
```

Thời hạn mặc định là 180 giây cho mỗi lệnh Maven; ví dụ trên tăng lên 300 giây. Script đặt connect timeout 15 giây và request timeout 30 giây bằng các khóa `aether.connector.*` phù hợp với Resolver 1.9.x đi kèm Maven 3.9.16 ([tài liệu cấu hình](https://maven.apache.org/resolver-archives/resolver-1.9.27/configuration.html)). Lượt lỗi hoặc hết thời hạn không được tính vào trung vị; khi thất bại giữa cặp, cả cặp phải được chạy lại từ kho trống. Chạy demo test thông thường dùng lệnh `clean verify` ở trên; chỉ chạy benchmark tải lạnh khi cần thu phép đo này.

Khi đường truyền chậm, có thể cho phép mỗi lệnh tối đa 30 phút và tăng thời gian chờ HTTP lên 120 giây. Sau khi chọn JDK 25 như phần đầu hướng dẫn:

```bash
MAVEN_OPTS=-Djava.net.preferIPv4Stack=true python3 scripts/benchmark_maven.py cache --resume --timeout-seconds 1800 --request-timeout-seconds 120
```

Tùy chọn IPv4 chỉ áp dụng cho lệnh này. Các lượt mới ghi thời điểm bắt đầu/kết thúc, thời hạn, lệnh Maven, `java_home` và `ipv4_preferred` trong `measurements.json`; các lượt cũ được giữ nguyên. Số đo ở các thời điểm hoặc cấu hình kết nối khác nhau cần được đọc cùng metadata, không dùng để kết luận mức cải thiện hiệu năng cố định.

## 9. AI-1/AI-2/AI-3/AI-4

- AI-1: prompt `ai/prompts/AI-1-generate-tests.md`; bản nháp `FineCalculatorAiDraftTest` → bản bổ sung `FineCalculatorTest`/CSV. Chạy `-Pai-draft clean verify` để đối chiếu. Bản nháp do Codex sinh trong phiên này; review tại `ai/results/AI-1-review.md` cần nhóm kiểm lại.
- AI-2: `python3 scripts/coverage_gaps.py evidence/tuan-05/ai-draft-recheck/site/jacoco/jacoco.xml --source-root case-study/src/main/java --output /tmp/coverage-gaps.json`; ghép JSON/source vào prompt AI-2. Output chỉ mô tả vị trí/số nhánh bỏ sót, không tự biết chính xác điều kiện true/false. Chạy `case-study/mvnw -f case-study/pom.xml -Pai-improved clean verify` để kiểm riêng bộ 3 test ban đầu + 3 test bổ sung; kết quả thực tế là 70% → 100% branch.
- AI-3: `python3 scripts/ai_review.py --diff ai/fixtures/review.diff --output /tmp/seminar-ai-review` chỉ chuẩn bị prompt. Có `GEMINI_API_KEY` và `AI_MODEL` thì thêm `--live` để gọi API. `.github/workflows/ai-review.yml` có bước tương ứng, lưu kết quả dạng artifact; chưa tự đăng comment lên PR.
- Khi gọi live, client retry tối đa hai lần sau request đầu cho timeout và lỗi HTTP tạm thời (`408`, `429`, `5xx`), với chờ 1 rồi 2 giây. Nếu vẫn lỗi, chưa có `review.json`; chờ API ổn định rồi chạy lại.
- AI-4: CSV do AI sinh tại `ai/data/AI-4-boundaries.csv`; chạy `case-study/mvnw -f case-study/pom.xml -Pai-data clean verify` để nạp 13 ca qua JUnit và calculator thật; đối chiếu với bộ tham chiếu `fine-cases.csv`. Cả hai bộ được chuẩn bị có AI hỗ trợ trong phiên này, nên chưa có số liệu so với bộ do con người viết độc lập.

Script live đã được gọi trong Tuần 06 bằng `gemini-3.6-flash` trên `ai/fixtures/review.diff`; metadata, prompt và response thật nằm ở `evidence/tuan-06/ai-review/`. `evaluation.json` đối chiếu rule/file/dòng với expected fixture và đạt 4 đúng, 0 thừa, 0 bỏ sót; đây không phải benchmark độc lập. Review fixture cũ ở `ai/results/AI-3-session-review.json` là output Codex trong phiên tương tác, không phải phản hồi Gemini. Workflow GitHub AI chưa được xác minh bằng run dịch vụ thật.

## 10. Lỗi thường gặp

Bộ bài tập đi kèm: [BaiTap_Tuan_06.md](BaiTap_Tuan_06.md). Kịch bản quay các phần Unit Test, Coverage và HTTP: [KichBan_QuayVideo_Tuan_06.md](KichBan_QuayVideo_Tuan_06.md). Kịch bản không thay cho video đã quay.

| Hiện tượng | Kiểm tra/cách xử lý |
|---|---|
| Không tìm thấy Java/Maven | Kiểm `java -version` (cần 25) và `case-study/mvnw -v`. Máy chưa có JDK 25 thì cài `openjdk-25-jdk` hoặc đặt `JAVA_HOME` trỏ tới JDK 25; chạy với JDK 21 thì thêm `-Djava.version=21`. |
| Demo thiếu test làm gate đỏ | Với demo baseline để đọc báo cáo dùng `-Pbaseline`; bản đầy đủ giữ gate mặc định. |
| Báo cáo coverage cũ lẫn vào kết quả mới | Dùng `clean verify`, lưu report mỗi lượt vào thư mục riêng. |
| API trả 409 ngay lần mượn thứ hai | Đúng quy tắc sách đã được mượn; restart để reset dữ liệu. |
| Port 8080 bận | Truyền `--server.port=8081`; smoke script dùng cổng ngẫu nhiên. |
| Test tiền fail do scale | Dùng `isEqualByComparingTo`, không dùng `BigDecimal.equals`. |
| Workflow AI xanh nhưng không có review | Đọc metadata/summary: chế độ prepare-only không gọi API. |

Nguồn chính thức: [Spring Boot 4.1 requirements](https://docs.spring.io/spring-boot/4.1/system-requirements.html), [JaCoCo check](https://www.jacoco.org/jacoco/trunk/doc/check-mojo.html), [PIT Maven](https://pitest.org/quickstart/maven/), [PIT JUnit platform plugin](https://github.com/pitest/pitest-junit5-plugin), [GitHub Maven CI](https://docs.github.com/en/actions/tutorials/build-and-test-code/java-with-maven), [Gemini generateContent](https://ai.google.dev/api/generate-content), [Mockito README](https://github.com/mockito/mockito).
