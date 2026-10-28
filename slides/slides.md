# Seminar: Unit Test - Code Coverage - CI/CD

## 1. Một lần mượn sách, ba lớp kiểm chứng

Tổng quan

- Unit Test → Code Coverage → CI/CD
- Seminar Kiểm thử phần mềm · Nhóm 09
- Cập nhật 28/10/2026 · phần Gia An (23120205)

---

## 2. Thành viên và phân công

Nhóm thực hiện

- Nguyễn Bảo An · 23120207: Unit Test, JUnit/Mockito.
- Phạm Quang Vinh · 23120202: CI/CD, Build Java 25 & Benchmark.
- Trương Nhật Đạt · 23120231: Code Coverage, JaCoCo, coverage gate và mutation testing.
- Nguyễn Lê Thế Vinh · 23120190: Case study, REST API, persistence và demo tích hợp.
- Ngô Gia An · 23120205: AI, paper, hợp nhất slide/báo cáo, trưởng nhóm.

---

## 3. Người học sẽ thực hành gì?

Tổng quan

- Viết test kiểm đúng hành vi và dữ liệu biên.
- Đọc báo cáo để tìm mã chưa được chạy qua.
- Dùng gate để làm fail build khi không đạt yêu cầu.
- Review test do AI sinh bằng kết quả chạy thật.

---

## 4. Tính phí và mượn sách

Case study

- NORMAL: 2.000 VND/ngày; VIP: gia hạn 2 ngày, sau đó 1.000 VND/ngày.
- Mức trần 50.000 VND; ngày âm và hạng null bị từ chối.
- Mượn sách: kiểm sách, thành viên, hạn mức 3 sách và phí chưa trả.
- Dữ liệu trong H2 in-memory (Spring Data JPA); restart để đặt lại trạng thái.

---

## 5. Arrange → Act → Assert

Unit Test

- Kiểm giá trị cụ thể; so tiền không phụ thuộc scale.
- Logic thuần dùng đối tượng thật.

```text
// Đầu vào: VIP trễ 3 ngày
var calculator = new FineCalculator();
var amount = calculator.calculate(3, MemberTier.VIP);
assertThat(amount).isEqualByComparingTo("1000");
```

---

## 6. Test nhanh, độc lập, lặp lại được

Unit Test

- FIRST: Fast, Independent, Repeatable, Self-validating, Timely.
- Clock.fixed giữ thời gian test ổn định.
- Một test không có assertion vẫn có thể pass.
- Test mock quá mức có thể xác nhận lại điều đã stub.

---

## 7. UT-1: chạy và đọc kết quả

Unit Test

- 39 lượt trong bộ chuẩn hiện tại: 18 tính phí, 7 LoanService, 4 LoanPeriodPolicy, 5 web, 2 integration, 3 persistence.
- JDK 25.0.5: 0 failure/error; coverage gate pass.
- GA-01: setup Maven Wrapper + agent Mockito; các suite AI chạy bằng profile riêng.

```text
case-study/mvnw -B -ntp -f case-study/pom.xml clean test
```

---

## 8. UT-2: một test, nhiều bộ dữ liệu

Unit Test

- @CsvFileSource đọc dữ liệu từ CSV ngoài mã test.
- Kiểm trước / đúng / sau ngưỡng.
- Bốn vòng TDD đỏ–xanh được tái hiện; có source và log từng vòng.

```text
daysLate,tier,expected
24,NORMAL,48000
25,NORMAL,50000
26,NORMAL,50000
```

---

## 9. UT-3: sáu tình huống mượn sách

Unit Test

- Sách không tồn tại; sách đang được mượn.
- Thành viên không tồn tại; đạt hạn mức 3 sách.
- Còn phí chưa trả; mượn thành công.
- verify(never()) kiểm nhánh lỗi không lưu phiếu.
- ArgumentCaptor kiểm phiếu đã lưu, không chỉ kiểm giá trị trả về.
- UT-3 hiện có thêm 1 ca thành viên mới; video do Bảo An phụ trách, chờ URL.

---

## 10. Mock kiểm được đến đâu?

Unit Test

- Unit test tách phụ thuộc để kiểm quyết định nghiệp vụ.
- Web slice kiểm HTTP và validation với service được mock.
- Integration test nối controller → service → repository thật trên H2 in-memory.
- HTTP smoke khởi động JAR và kiểm 5 tình huống thật.

---

## 11. Dòng được chạy và nhánh được chạy

Code Coverage

- Line coverage đếm dòng thực thi.
- Branch coverage đếm hướng rẽ trong mã.
- Một dòng có thể chứa nhiều nhánh.
- JaCoCo cung cấp HTML để đọc, XML để phân tích tự động.

---

## 12. CC-1/2: đo trước, bổ sung, đo lại

Code Coverage

- Riêng FineCalculator: baseline 50% nhánh → bộ đầy đủ 100%.
- Lưu cả hai báo cáo HTML/XML để đối chiếu.

```text
case-study/mvnw -f case-study/pom.xml -Pbaseline clean verify
# Lưu báo cáo trước khi chạy tiếp
case-study/mvnw -f case-study/pom.xml clean verify
```

---

## 13. CC-3: gate phải chặn được bản thiếu test

Code Coverage

- Giữ gate 90% branch cho FineCalculator.
- Khôi phục bộ test đầy đủ: build pass.
- Mới chứng minh gate tại máy; required checks trên GitHub còn cần cấu hình.

```text
case-study/mvnw -f case-study/pom.xml -Pbaseline \
  -Dcoverage.gate.skip=false clean verify
# Kỳ vọng: exit 1, vì 50% < 90%
```

---

## 14. 100% branch vẫn có thể kiểm sai rất ít

Code Coverage

- Test bẫy đi đủ nhánh nhưng bỏ assertion tiền ở ca hợp lệ.
- JaCoCo: cả bộ yếu và bộ đầy đủ đều phủ 100% branch.
- PIT: bộ yếu diệt 3/11 mutation; bộ đầy đủ diệt 10/11.
- Mutant còn sống ở bộ đầy đủ tương đương theo đặc tả ngưỡng trả 0.

---

## 15. Từ lệnh tại máy đến pipeline

CI/CD

- CI kiểm thay đổi được tích hợp thường xuyên.
- Bản hiện tại dừng ở kiểm thử/đóng gói; chưa tự deploy ứng dụng.

```text
test [JDK 25]
        ↓
coverage-gate [branch >= 90%]
        ↓
package [JAR + artifact]
```

---

## 16. CI-1/2/3: workflow và minh chứng

CI/CD

- CI-1: checkout, setup Java, chạy Maven.
- CI-2: cache dependency, upload report và summary.
- CI-3: test → gate → package; workflow hiện chỉ workflow_dispatch.
- Video CI do Quang Vinh phụ trách: cần PR đỏ→xanh và required checks thật; chờ URL.

---

## 17. GitHub Actions và Jenkins

CI/CD

- GitHub Actions dùng YAML và hosted runner.
- Jenkinsfile mô tả cùng thứ tự test → gate → package.
- Mỗi hệ có cú pháp và cách cấp môi trường riêng.
- Jenkinsfile chưa chạy trên Jenkins; chưa kết luận về tốc độ hoặc độ dễ vận hành.

---

## 18. Thời gian đo tại máy

Thực nghiệm

- Kho Maven lạnh/ấm (Java 25): đủ 3 cặp; trung vị 48,412s / 12,539s.
- Ba lượt verify không/có JaCoCo: trung vị 9,727s / 12,754s.
- Cặp 3 chạy bổ sung: 479,523s / 11,940s; điều kiện mạng thay đổi giữa các cặp.
- Không coi là thời gian cache trên GitHub Actions.

---

## 19. AI-1/2: sinh test, đọc gap, kiểm lại

AI

- Bản nháp Codex: 3 test đúng, chỉ phủ 70% nhánh.
- Đọc gap và source: thiếu null, ngày âm, tính phí VIP sau gia hạn.
- Thêm 3 test: bộ 6 test phủ 100% nhánh.
- Prompt và test có thể tái sử dụng; thành viên nhóm cần review lại.

---

## 20. AI-3/4: review và dữ liệu biên

AI

- AI-3 đã gọi live Gemini 3.6 Flash trên diff fixture; kết quả đối chiếu: 4 đúng, 0 thừa, 0 bỏ sót.
- Đây là kiểm tra fixture có lỗi seed, không phải benchmark độc lập hay review toàn bộ repository.
- AI-4: bộ Gia An 23/23 ca pass; CSV AI 13/13 ca pass.
- Có 11 đầu vào chung, cả 11 khớp kỳ vọng; độc lập theo ghi chú Gia An gửi.

---

## 21. Tái sử dụng AI trên LoanService

AI · GA-02/03

- Nháp: 2 test pass, line 14/17, branch 3/6.
- Bổ sung: 10 test pass, line 17/17, branch 6/6.
- PIT: 9/9 mutant bị diệt trong cấu hình đã chạy.
- Video mở gap, assertion/captor và log trước/sau; chờ quay.

[AI-5 và giới hạn](../ai/results/AI-5-loan-review.md)

---

## 22. Một test oracle sai phải làm build đỏ

AI · GA-04

- Fixture cố ý kỳ vọng được mượn khi đang giữ 3 sách.
- Đặc tả chặn từ >=3; test fail đúng 1 assertion.
- Đây là fixture cài sẵn, không phải lỗi ghi nhận từ API.
- Video giải thích lỗi kỳ vọng; không sửa nghiệp vụ để chiều test.

[Kết quả fixture](../evidence/gia-an/loan-mistake/run.json)

---

## 23. AI-4: đối chứng trước, so sánh sau

AI · GA-05

- Gia An cung cấp 23 ca và ghi chú tuyên bố chỉ dựa trên đặc tả.
- Khóa dữ liệu, hash và commit 0e58f5f trước khi so sánh.
- Java: Gia An 23/23 pass, branch 100%; AI 13/13 pass, branch 80%.
- 11 ca chung khớp; 12 ca chỉ người dùng, 2 chỉ AI. Codex chạy; GA-05 chờ quay.

[Kết quả và giới hạn](../docs/gia-an/AI4_KetQua.md)

[Ghi chú thiết kế gốc](../ai/human/cases-notes.md)

---

## 24. CoverUp: dùng coverage để hướng sinh test

Paper · GA-06

- Pizzorno, Berger · FSE 2025 Research Papers / PACMSE.
- Vòng lặp: đo coverage → chọn gap/ngữ cảnh → LLM → chạy và sửa.
- Tool gốc cho Python; target nhóm là coverage_gaps.py.
- Video mở paper/source/rank và giải thích quy trình.

[Paper v4](https://arxiv.org/html/2403.16218v4)

[Source tác giả](https://github.com/plasma-umass/coverup-eval)

---

## 25. CoverUp: mức tái hiện thực sự đã đạt

Paper · GA-06

- Chạy script tác giả trên 163 module MT: line+branch 89,0%.
- MuTAP gpt4o_zero: 76,8%; khớp số 89% vs 77% làm tròn ở v4.
- Đây là replay phân tích dữ liệu tác giả; không phải sinh lại test.
- Source nhóm đã dry-run thành công; chưa có lượt gọi model mới.

[Log và số liệu](../evidence/gia-an/papers/coverup-mt/run.json)

---

## 26. ChatUniTest: sinh, kiểm tra, sửa test Java

Paper · GA-07

- Chen và cộng sự · FSE 2024 Demonstrations.
- Adaptive focal context và generation–validation–repair.
- Source gốc có công bố; chuẩn bị trial LoanService#borrow.
- Chưa tái lập generation: còn model/API và môi trường gốc; video không được trình bày như đã thành công.

[Nguồn công bố](https://2024.esec-fse.org/details/fse-2024-demonstrations/6/ChatUniTest-A-Framework-for-LLM-based-Test-Generation)

[Kế hoạch thực nghiệm](../research/README.md)

---

## 27. Hạng venue và giới hạn kết luận

Paper · kiểm hạng

- CORE2023: FSE A*; hai bài xuất bản 2024–2025.
- Hạng thuộc hội nghị, không gán trực tiếp cho từng bài.
- ChatUniTest thuộc demo track; nhóm cần xác nhận GV chấp nhận.
- AI-5 Codex của nhóm không thay cho chạy artifact ChatUniTest.

[CORE2023 chính thức](https://portal.core.edu.au/conf-ranks/?by=all&search=&source=CORE2023)

---

## 28. Mỗi phần có video và kết quả cần thấy

Video · toàn nhóm

- Bảo An: UT setup, CSV, mock, giới hạn; Thế Vinh: app/integration.
- Đạt: coverage, gate, công cụ đối chiếu và điểm mù của tool.
- Quang Vinh: CI, cache/artifact, PR đỏ→xanh và lỗi CI.
- Gia An: GA-01..07, AI và paper; tất cả URL/timestamp còn chờ.

[Danh mục và trạng thái từng video](../docs/gia-an/Video_Artifacts.md)

---

## 29. Bài tập cho người nghe

Thực hành

- Thêm hạng STUDENT: viết quy tắc, dữ liệu biên và test.
- Bỏ một assertion tiền: so JaCoCo và PIT trước/sau.
- Đưa Maven vào workflow, tạo PR thiếu nhánh và kiểm gate.
- Gợi ý: giữ nguyên gate; sửa test/logic theo đặc tả.

---

## 30. Video và gói nộp cần hoàn thiện

Video bắt buộc

- Video phải có setup, cơ bản, phức tạp, giới hạn và data driven.
- GA-01..07: artifact đã lập danh mục; chưa quay hoặc đăng YouTube.
- Mỗi video có slide tóm tắt; nếu gộp clip, ghi timestamp thực tế.
- Hạn nộp chờ xác nhận; gửi slide/gặp GV trước hạn 3–4 ngày.

[Danh mục video](../docs/gia-an/Video_Artifacts.md)

[Điều phối](../docs/gia-an/DieuPhoi.md)

---

## 31. Nguồn và cách tái hiện

Tài liệu

- README.md: điểm vào thực hành.
- docs/gia-an/: phạm vi, artifact video và phần còn chờ.
- research/: paper, nguồn hạng, revision và cách thử tool tác giả.
- evidence/gia-an/: log và JSON/XML của các lượt mới ngày 28/10.

---

