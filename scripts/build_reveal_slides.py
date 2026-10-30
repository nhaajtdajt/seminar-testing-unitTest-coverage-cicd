#!/usr/bin/env python3
"""Build modern, high-contrast, black-and-white Reveal.js slides.
Optimized for:
- 100% compliance with seminar requirements (covers all 5 demo videos A, B, C, D, E + table)
- Perfectly balanced layout: bold typography (readable in bright presentation halls), zero void/empty space
- Every slide features rich technical bullets, a takeaway anchor card, and a dedicated SVG diagram/screenshot
- Link placeholders for video URLs to be updated once uploaded to YouTube
- Rich speaker notes for presenters
"""
import os
import html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLIDES_HTML = os.path.join(ROOT, 'slides', 'index.html')

slides_data = [
    # 1. BÌA
    {
        "stage": "TỔNG QUAN",
        "title": "Một lần mượn sách, ba lớp kiểm chứng",
        "layout": "hero",
        "bullets": [
            "<strong>Mô hình 3 lớp kiểm chứng:</strong> Unit Test → Coverage Gate → CI/CD Pipeline.",
            "<strong>Case study thực chiến:</strong> Quản lý mượn sách &amp; chính sách phạt trễ hạn thư viện.",
            "<strong>Seminar Kiểm thử phần mềm · Nhóm 09</strong> · Cập nhật báo cáo Tuần 06."
        ],
        "takeaway": "Trả lời câu hỏi cốt lõi: 'Test chạy xanh và Coverage 100% đã chắc chắn mã nguồn không còn lỗi?'",
        "diagram": "images/diagrams/three-layers.svg",
        "logos": ["openjdk.svg", "junit5.svg", "githubactions.svg", "apachemaven.svg", "googlegemini.svg"],
        "notes": "Bảo An: Chào thầy và các bạn. Hôm nay Nhóm 09 xin trình bày đề tài 'Một lần mượn sách, ba lớp kiểm chứng'. Bài thuyết trình giải quyết trọn vẹn câu hỏi: Làm thế nào để đảm bảo chất lượng phần mềm từ Unit Test độc lập, chốt chặn độ phủ đến pipeline CI/CD và ứng dụng AI."
    },
    # 2. THÀNH VIÊN
    {
        "stage": "NHÓM THỰC HIỆN",
        "title": "Thành viên & Phân công trách nhiệm",
        "layout": "team",
        "members": [
            {"name": "Nguyễn Bảo An", "mssv": "23120207", "role": "Unit Test Core", "task": "JUnit 5, Mockito, Parameterized Tests, AAA Pattern & Video A."},
            {"name": "Phạm Quang Vinh", "mssv": "23120202", "role": "CI/CD & Benchmark", "task": "GitHub Actions, Build JDK 25, Đo cache Maven & Video D."},
            {"name": "Trương Nhật Đạt", "mssv": "23120231", "role": "Code Coverage", "task": "JaCoCo 90% branch gate, PIT Mutation Testing & Video B."},
            {"name": "Nguyễn Lê Thế Vinh", "mssv": "23120190", "role": "Case Study & REST", "task": "Spring Data JPA, H2 database, HTTP smoke test & Video C."},
            {"name": "Ngô Gia An", "mssv": "23120205", "role": "Trưởng nhóm & AI/Paper", "task": "Gemini sinh test, tái hiện CoverUp, Pynguin & Video E."}
        ],
        "notes": "Bảo An: Nhóm gồm 5 thành viên phụ trách 5 mảng chuyên môn khép kín, mỗi thành viên chịu trách nhiệm độc lập một mảng kỹ thuật và tự quay một video demo minh chứng."
    },
    # 3. MỤC TIÊU
    {
        "stage": "MỤC TIÊU",
        "title": "4 Trụ cột người học sẽ thực hành",
        "layout": "split",
        "bullets": [
            "<strong>1. Viết Unit Test chuẩn:</strong> Cấu trúc AAA, nguyên lý FIRST và kỹ thuật quét dữ liệu biên.",
            "<strong>2. Đo lường bản chất:</strong> Phân biệt Line vs Branch; nhận diện bẫy độ phủ bằng PIT Mutation.",
            "<strong>3. Chốt chặn CI tự động:</strong> Cấu hình Gate làm fail build ngay khi Branch &lt; 90% trên GitHub Actions.",
            "<strong>4. Đánh giá kiểm thử AI:</strong> Dùng Gemini 3.6 tìm gap, sinh test và đối chứng kết quả bằng oracle."
        ],
        "takeaway": "Mục tiêu: Giúp người học tự xây dựng được hệ thống kiểm thử tự động, không chạy theo số liệu hình thức.",
        "diagram": "images/diagrams/roadmap-goals.svg",
        "notes": "Bảo An: Seminar đi từ lý thuyết đến thực hành: viết test, đo độ phủ thật, cấu hình pipeline và đánh giá AI có phản biện."
    },
    # 4. CASE STUDY
    {
        "stage": "CASE STUDY",
        "title": "Nghiệp vụ tính phí phạt & mượn sách",
        "layout": "split",
        "bullets": [
            "<strong>Hạng NORMAL:</strong> Đơn giá 2.000 VND/ngày; không có ngày gia hạn; mức trần tối đa 50.000 VND.",
            "<strong>Hạng VIP:</strong> Miễn phí 2 ngày đầu, sau đó 1.000 VND/ngày; mức trần tối đa 50.000 VND.",
            "<strong>Quy tắc mượn sách:</strong> Tối đa 3 cuốn/thành viên, không nợ phí phạt cũ, sách đang sẵn có.",
            "<strong>Dữ liệu:</strong> H2 in-memory sạch, nạp tự động lúc khởi động và reset khi restart."
        ],
        "takeaway": "Ranh giới kiểm thử: 0, 1, 2 ngày; chạm trần 25 ngày (NORMAL) và 52 ngày (VIP); ngày âm ném ngoại lệ.",
        "diagram": "images/diagrams/domain-rules.svg",
        "notes": "Thế Vinh: Case study có quy tắc tính phí và điều kiện mượn sách rõ ràng, làm nền tảng kiểm thử xuyên suốt cả seminar."
    },
    # 5. VIDEO C SUMMARY (NEW)
    {
        "stage": "VIDEO DEMO C",
        "title": "Video C: Chạy ứng dụng & 7 Kịch bản HTTP Smoke Test",
        "layout": "split",
        "bullets": [
            "<strong>Người thực hiện:</strong> Nguyễn Lê Thế Vinh (23120190) · <strong>Thời lượng:</strong> 3 – 5 phút.",
            "<strong>00:00 - Setup:</strong> Khởi chạy JAR thật trên JDK 25, kiểm tra dữ liệu mẫu H2 in-memory.",
            "<strong>01:00 - Demo 7 request:</strong> Chạy <code>scripts/demo_case_study.sh</code>: 201 Created, 409 UNAVAILABLE, 404 NOT_FOUND, 409 UNPAID_FINE.",
            "<strong>03:30 - Đối chiếu test:</strong> Chạy <code>LoanFlowEdgeCaseTest</code> chứng minh HTTP curl khớp 100% với test tự động."
        ],
        "takeaway": "Trạng thái: Đã quay xong video · Link YouTube: [Sẽ bổ sung URL sau] · Mã lệnh: scripts/demo_case_study.sh",
        "diagram": "images/diagrams/video-c-timeline.svg",
        "notes": "Thế Vinh: Video C demo trực quan ứng dụng Spring Boot chạy thật, gửi 7 request curl kiểm thử các mã trạng thái HTTP."
    },
    # 6. AAA PATTERN
    {
        "stage": "UNIT TEST",
        "title": "Cấu trúc Arrange → Act → Assert (AAA)",
        "layout": "split",
        "bullets": [
            "<strong>Arrange:</strong> Khởi tạo đối tượng &amp; thiết lập dữ liệu giả định (Khách VIP trễ 3 ngày).",
            "<strong>Act:</strong> Kích hoạt duy nhất phương thức nghiệp vụ cần kiểm thử (<code>calculate</code>).",
            "<strong>Assert:</strong> So sánh kết quả thực tế với giá trị kỳ vọng (1.000 VND).",
            "<strong>Lưu ý BigDecimal:</strong> Bắt buộc dùng <code>isEqualByComparingTo</code> để không bị lỗi so sánh scale."
        ],
        "takeaway": "Quy tắc vàng: Mỗi ca test chỉ tập trung kiểm chứng duy nhất một hành vi nghiệp vụ độc lập.",
        "diagram": "images/diagrams/aaa-pattern.svg",
        "code": "var calculator = new FineCalculator();\nvar amount = calculator.calculate(3, MemberTier.VIP);\nassertThat(amount).isEqualByComparingTo(\"1000\");",
        "notes": "Bảo An: AAA là mẫu chuẩn của unit test. Tuyệt đối không dùng isEqualTo của BigDecimal vì '1000' và '1000.00' sẽ bị coi là khác nhau."
    },
    # 7. FIRST PRINCIPLES
    {
        "stage": "UNIT TEST",
        "title": "Nguyên lý F.I.R.S.T & Bẫy kiểm thử",
        "layout": "split",
        "bullets": [
            "<strong>F - Fast &amp; I - Independent:</strong> Chạy milli-giây, độc lập thứ tự thực thi.",
            "<strong>R - Repeatable:</strong> Tiêm <code>Clock.fixed</code> giữ thời gian bất biến, không phụ thuộc ngày giờ hệ thống.",
            "<strong>S - Self-validating &amp; T - Timely:</strong> Tự động pass/fail; viết đồng thời với mã nguồn.",
            "<strong>2 Bẫy phổ biến:</strong> Test thiếu assert (vẫn xanh vô nghĩa) và Mock quá đà (chỉ test lại stub)."
        ],
        "takeaway": "Giải pháp: Tiêm Clock giả lập và luôn kiểm tra chất lượng câu lệnh assert bằng Mutation Testing.",
        "diagram": "images/diagrams/first-principles.svg",
        "notes": "Bảo An: Hai bẫy nguy hiểm nhất: viết test gọi hàm nhưng quên assert, và mock tràn lan khiến test không kiểm tra logic thật."
    },
    # 8. UT-1 SUREFIRE
    {
        "stage": "UNIT TEST",
        "title": "UT-1: Chạy kiểm thử & Đọc báo cáo Surefire",
        "layout": "split",
        "bullets": [
            "<strong>Lệnh thực thi:</strong> <code>./mvnw -B -ntp clean test</code> (cờ batch mode tối ưu cho CI/terminal).",
            "<strong>Quy mô bộ test:</strong> 39 tests core ban đầu → <strong>49 tests</strong> sau khi tích hợp AI (PR #13).",
            "<strong>Surefire metrics:</strong> Phân biệt rõ Failure (sai assertion logic) vs Error (sập ngoại lệ JVM).",
            "<strong>Tương thích:</strong> Đã chạy pass 100% trên cả JDK 25 mới nhất và JDK 21 LTS."
        ],
        "takeaway": "Kết quả: 49/49 tests passed, 0 failures, 0 errors, thời gian thực thi toàn bộ suite dưới 1.5 giây.",
        "diagram": "images/diagrams/surefire-report.svg",
        "notes": "Bảo An: Sử dụng cờ -B -ntp giúp log sạch trên terminal và CI. Báo cáo Surefire lưu tại target/surefire-reports."
    },
    # 9. UT-2 PARAMETERIZED & TDD
    {
        "stage": "UNIT TEST",
        "title": "UT-2: Parameterized Test (@CsvFileSource) & TDD",
        "layout": "split",
        "bullets": [
            "<strong>@CsvFileSource:</strong> Tách dữ liệu ra file ngoài, kiểm tra quét ranh giới 24, 25, 26 ngày trễ.",
            "<strong>4 Vòng TDD đỏ – xanh:</strong>",
            "• Vòng 1: Tính phí phạt cơ bản theo ngày trễ.",
            "• Vòng 2: Áp dụng mức trần tối đa 50.000 VND.",
            "• Vòng 3: Bổ sung chính sách miễn 2 ngày đầu cho khách VIP.",
            "• Vòng 4: Xử lý ngoại lệ dữ liệu biên (ngày âm &amp; null)."
        ],
        "takeaway": "Giá trị: 1 hàm test tự động sinh 15 ca kiểm thử bao quát toàn bộ ranh giới, lưu vết log từng vòng TDD.",
        "diagram": "images/diagrams/tdd-cycle.svg",
        "code": "daysLate,tier,expected\n24,NORMAL,48000\n25,NORMAL,50000\n26,NORMAL,50000",
        "notes": "Bảo An: Parameterized test giúp một hàm test kiểm tra được hàng chục bộ dữ liệu biên. Bốn vòng TDD đều được lưu vết mã nguồn và log từng bước."
    },
    # 10. UT-3 LOAN SERVICE & MOCKITO
    {
        "stage": "UNIT TEST",
        "title": "UT-3: Sáu tình huống mượn sách & Mockito",
        "layout": "split",
        "bullets": [
            "<strong>5 Ca ngoại lệ:</strong> Sách ảo, sách đang mượn, thành viên ảo, mượn quá 3 cuốn, còn nợ phí phạt.",
            "<strong>1 Ca thành công:</strong> Đủ điều kiện và lưu phiếu mượn hợp lệ xuống cơ sở dữ liệu.",
            "<strong>Kỹ thuật Mockito chuyên sâu:</strong>",
            "• <code>verify(loanRepo, never()).save(...)</code>: Chặn rò rỉ dữ liệu khi gặp lỗi.",
            "• <code>ArgumentCaptor</code>: Bắt và kiểm tra chi tiết trạng thái phiếu mượn được lưu."
        ],
        "takeaway": "Tác dụng: Cô lập hoàn toàn LoanService khỏi I/O và DB, thời gian chạy toàn bộ 6 ca dưới 0.15s.",
        "diagram": "images/diagrams/loan-verification.svg",
        "notes": "Bảo An: LoanService có 6 nhánh logic. Điểm then chốt là kiểm tra verify(never()).save() để chứng minh hệ thống không bao giờ ghi dữ liệu sai xuống DB."
    },
    # 11. TEST PYRAMID
    {
        "stage": "UNIT TEST",
        "title": "Mock kiểm được đến đâu? Kim tự tháp test",
        "layout": "split",
        "bullets": [
            "<strong>Unit Test (Đáy tháp):</strong> Mock cô lập, phản hồi milli-giây, tập trung kiểm quyết định nghiệp vụ.",
            "<strong>Web Slice Test:</strong> Dùng <code>@WebMvcTest</code> kiểm tra HTTP status và validation với service giả lập.",
            "<strong>Integration &amp; Smoke Test (Đỉnh tháp):</strong> Nối DB H2 thật; chạy JAR hoàn chỉnh với 5 kịch bản curl.",
            "<strong>Bài học:</strong> Unit test chạy nhanh và rẻ; Integration test chứng minh các mảnh ghép chạy thật."
        ],
        "takeaway": "Chiến lược: Kết hợp hài hòa các tầng kiểm thử để vừa có tốc độ phản hồi nhanh, vừa có độ tin cậy thực tế.",
        "diagram": "images/diagrams/test-pyramid.svg",
        "notes": "Bảo An: Mock rất nhanh nhưng không thể thay thế integration test. Kim tự tháp kiểm thử giúp cân bằng chi phí và độ tin cậy thực tế."
    },
    # 12. VIDEO A SUMMARY (NEW)
    {
        "stage": "VIDEO DEMO A",
        "title": "Video A: Unit Test với JUnit 5 & Mockito (5–7 phút)",
        "layout": "split",
        "bullets": [
            "<strong>Người thực hiện:</strong> Nguyễn Bảo An (23120207) · <strong>Thời lượng:</strong> 5 – 7 phút.",
            "<strong>00:00 - Setup:</strong> Cấu trúc project Java 25, Maven Wrapper, thư viện JUnit 5 và Mockito 5.",
            "<strong>01:00 - AAA &amp; Surefire:</strong> Quy tắc AAA, chạy FineCalculatorTest, đọc báo cáo XML.",
            "<strong>02:15 - Data-driven:</strong> Tách file CSV, chạy 15 ca biên tự động với @ParameterizedTest.",
            "<strong>03:45 - Mockito:</strong> Cô lập repo, verify(never) ca lỗi và ArgumentCaptor ca thành công.",
            "<strong>05:15 - Anti-patterns:</strong> Mổ xẻ Train Wreck Mocking và Self-fulfilling Prophecy."
        ],
        "takeaway": "Trạng thái: Đã quay xong video · Link YouTube: [Sẽ bổ sung URL sau] · Mã lệnh: ./mvnw test",
        "diagram": "images/diagrams/video-a-timeline.svg",
        "notes": "Bảo An: Video A trình diễn toàn bộ thao tác viết Unit Test chuẩn, chạy Surefire, kiểm thử tham số hóa và chỉ ra các bẫy anti-pattern."
    },
    # 13. LINE VS BRANCH
    {
        "stage": "CODE COVERAGE",
        "title": "Line Coverage vs. Branch Coverage",
        "layout": "split",
        "bullets": [
            "<strong>Line Coverage:</strong> Đếm số dòng đã chạy; dễ ngộ nhận khi dòng chứa toán tử điều kiện (<code>? :</code>, <code>&amp;&amp;</code>).",
            "<strong>Branch Coverage:</strong> Đếm trọn vẹn cả 2 hướng True và False của mọi ngã rẽ logic.",
            "<strong>Nghịch lý:</strong> Đạt 100% Line Coverage vẫn có thể bỏ sót 50% nhánh điều kiện biên!",
            "<strong>Định dạng JaCoCo:</strong> HTML trực quan cho lập trình viên; XML cho CI Gate phân tích tự động."
        ],
        "takeaway": "Kết luận: Line Coverage chỉ là điều kiện cần; Branch Coverage mới phản ánh độ bao quát thực tế.",
        "diagram": "images/diagrams/line-vs-branch.svg",
        "notes": "Nhật Đạt: Slide này làm rõ lý do tại sao nhóm chọn Branch Coverage làm Gate. Một dòng chứa toán tử ba ngôi chỉ cần chạy 1 ca là đạt 100% dòng nhưng thực chất bỏ sót 50% nhánh."
    },
    # 14. CC-1/2 BEFORE & AFTER
    {
        "stage": "CODE COVERAGE",
        "title": "CC-1/2: Quy trình Đo trước → Bổ sung → Đo lại",
        "layout": "split",
        "bullets": [
            "<strong>Baseline ban đầu:</strong> FineCalculator chỉ đạt <strong>50% branch</strong> (thiếu ca ngày âm, ca chạm trần).",
            "<strong>Bổ sung &amp; Đo lại:</strong> Viết thêm các ca kiểm thử biên → vươn lên <strong>100% branch</strong>.",
            "<strong>Lệnh thực thi:</strong>",
            "• Đo baseline: <code>./mvnw -f case-study/pom.xml -Pbaseline clean verify</code>",
            "• Đo đầy đủ: <code>./mvnw -f case-study/pom.xml clean verify</code>"
        ],
        "takeaway": "Minh chứng: Ảnh chụp báo cáo JaCoCo HTML thật trích xuất từ thư mục evidence chứng minh độ phủ 100%.",
        "image": "images/evidence/jacoco-summary-2026-10-23.png",
        "notes": "Nhật Đạt: Nhóm đo lường bằng profile baseline riêng. Hình ảnh bên phải là ảnh chụp thật từ thư mục evidence chứng minh độ phủ nhánh đạt 100%."
    },
    # 15. CC-3 GATE CONFIG
    {
        "stage": "CODE COVERAGE",
        "title": "CC-3: Cấu hình Gate chặn bản thiếu test",
        "layout": "split",
        "bullets": [
            "<strong>Quy tắc Gate:</strong> Cấu hình <code>BRANCH COVEREDRATIO &gt;= 0.90</code> cho FineCalculator.",
            "<strong>Cơ chế Fail-Fast:</strong> Nếu tỷ lệ &lt; 90%, JaCoCo ngắt lệnh và trả về <strong>Exit Code 1</strong>.",
            "<strong>Thực nghiệm Gate:</strong>",
            "<code>./mvnw -f case-study/pom.xml -Pbaseline -Dcoverage.gate.skip=false clean verify</code>",
            "• Kết quả: Văng lỗi <code>BUILD FAILURE</code> ngay lập tức vì 50% &lt; 90%."
        ],
        "takeaway": "Ý nghĩa: Gate ngăn chặn triệt để tình trạng lập trình viên đẩy mã nguồn thiếu test lên kho chung.",
        "diagram": "images/diagrams/gate-failure.svg",
        "code": "<limit>\n  <counter>BRANCH</counter>\n  <value>COVEREDRATIO</value>\n  <minimum>0.90</minimum>\n</limit>",
        "notes": "Nhật Đạt: Gate phải có răng - tức là phải có khả năng làm sập build. Khi chạy với profile baseline thiếu test, Maven dừng ngay ở Exit code 1."
    },
    # 16. MUTATION TESTING
    {
        "stage": "CODE COVERAGE",
        "title": "100% Branch vẫn lọt lỗi: Mutation Testing",
        "layout": "split",
        "bullets": [
            "<strong>Thử nghiệm bẫy:</strong> Bộ test đi đủ nhánh nhưng cố tình bỏ assert tiền phạt → JaCoCo vẫn báo <strong>100% Branch</strong>!",
            "<strong>Giải pháp PIT Mutation:</strong> Tự động cấy lỗi đột biến (đổi toán tử, return 0).",
            "<strong>Kết quả thực nghiệm:</strong>",
            "• Bộ test yếu (bẫy): Chỉ diệt được <strong>3/11 mutant</strong> (chỉ bắt được ca văng ngoại lệ).",
            "• Bộ test chuẩn của nhóm: Diệt được <strong>10/11 mutant</strong> (mutant còn sống là tương đương)."
        ],
        "takeaway": "Bài học: Coverage chỉ đo mã được chạy; PIT Mutation Testing mới đo lường chất lượng câu lệnh assert.",
        "diagram": "images/diagrams/mutation-flow.svg",
        "notes": "Nhật Đạt: Đây là điểm nhấn quan trọng nhất của phần Coverage. PIT Mutation Testing chứng minh con số 100% độ phủ chưa nói lên chất lượng nếu câu lệnh assert bị yếu."
    },
    # 17. VIDEO B SUMMARY (NEW)
    {
        "stage": "VIDEO DEMO B",
        "title": "Video B: Code Coverage & PIT Mutation Testing (8–9 phút)",
        "layout": "split",
        "bullets": [
            "<strong>Người thực hiện:</strong> Trương Nhật Đạt (23120231) · <strong>Thời lượng:</strong> 8 – 9 phút.",
            "<strong>00:00 - Setup:</strong> Cấu hình plugin JaCoCo agent và PIT trong <code>pom.xml</code>.",
            "<strong>01:00 - 6 Loại coverage:</strong> Minh họa trên <code>LoanPeriodPolicy</code> (Statement, Decision, MC/DC).",
            "<strong>03:00 - Trước / Sau:</strong> So sánh baseline 50% vs Bộ đầy đủ 100% Branch Coverage.",
            "<strong>04:00 - Gate &amp; PIT:</strong> Demo Gate văng Exit 1, test bẫy 100% branch nhưng PIT chỉ diệt 3/11 mutant.",
            "<strong>06:00 - Hạn chế:</strong> Quyết định ẩn trong <code>Math.min()</code>, mutant tương đương và chi phí thời gian."
        ],
        "takeaway": "Trạng thái: Đã quay xong video · Link YouTube: [Sẽ bổ sung URL sau] · Lệnh: clean verify, pitest:mutationCoverage",
        "diagram": "images/diagrams/video-b-timeline.svg",
        "notes": "Nhật Đạt: Video B quay đủ 5 phân đoạn chuẩn: setup, 6 loại coverage, trước/sau, gate fail, bẫy PIT và các điểm yếu thực tế."
    },
    # 18. CI / CD LEVELS
    {
        "stage": "CI/CD",
        "title": "CI, Continuous Delivery, Continuous Deployment",
        "layout": "split",
        "bullets": [
            "<strong>Continuous Integration (CI):</strong> Mỗi lần push/PR, tự động build JDK 25 và chạy test. Phát hiện lỗi ngay.",
            "<strong>Continuous Delivery:</strong> Sau CI, tự động đóng gói Artifact (JAR) sẵn sàng phát hành; triển khai do người duyệt.",
            "<strong>Continuous Deployment:</strong> Tự động đẩy thẳng lên server chạy thật không cần người duyệt.",
            "<strong>Nguyên lý:</strong> Càng lên mức tự động hóa cao, càng đòi hỏi bộ test và gate tin cậy tuyệt đối."
        ],
        "takeaway": "Phân cấp: CI bảo vệ mã nguồn → Delivery bảo vệ bản dựng → Deployment bảo vệ môi trường vận hành.",
        "diagram": "images/diagrams/ci-cd-levels.svg",
        "notes": "Quang Vinh: 3 khái niệm này đại diện cho 3 cấp độ tự động hóa tăng dần, đòi hỏi bộ test và gate ngày càng khắt khe."
    },
    # 19. TEAM SCOPE
    {
        "stage": "CI/CD",
        "title": "Phạm vi CI/CD nhóm triển khai thực tế",
        "layout": "split",
        "bullets": [
            "<strong>CI · HOÀN THÀNH 100%:</strong> Tự chạy test JDK 25 và kiểm tra Branch Gate ≥ 90% trên mọi Pull Request.",
            "<strong>Continuous Delivery · ĐẠT MỨC ARTIFACT:</strong> Tự đóng gói JAR, đính kèm báo cáo Surefire &amp; JaCoCo.",
            "<strong>Continuous Deployment · KHÔNG THỰC HIỆN:</strong> Đề tài tập trung kiểm thử phần mềm, không triển khai server.",
            "<strong>Mở rộng:</strong> Nếu cần deploy, bổ sung job deploy sau package với điều kiện nhánh master + approval."
        ],
        "takeaway": "Cam kết: Ghi nhận trung thực phạm vi thực hiện, không phóng đại những nội dung không thuộc đề tài.",
        "diagram": "images/diagrams/team-scope.svg",
        "notes": "Quang Vinh: Nhóm xác định rõ ranh giới: hoàn thành xuất sắc CI và Delivery ở mức tạo artifact JAR, không làm deployment vì không thuộc phạm vi môn học."
    },
    # 20. PIPELINE FLOW
    {
        "stage": "CI/CD",
        "title": "Từ lệnh tại máy đến GitHub Actions Pipeline",
        "layout": "split",
        "bullets": [
            "<strong>3 Job độc lập:</strong> <code>test</code> → <code>coverage-gate</code> → <code>package</code>.",
            "<strong>Ràng buộc <code>needs</code>:</strong> Job trước bị FAIL thì job sau tuyệt đối không được thực thi.",
            "<strong>Bảo vệ chất lượng:</strong> Mã thiếu test hoặc hỏng logic không bao giờ được đóng gói thành file JAR.",
            "<strong>Môi trường:</strong> Runner <code>ubuntu-latest</code> cấp phát bởi GitHub, cài đặt Temurin OpenJDK 25."
        ],
        "takeaway": "Triết lý: Fail-Fast (thất bại sớm) giúp tiết kiệm tài nguyên máy chủ và phản hồi lỗi tức thì cho lập trình viên.",
        "diagram": "images/diagrams/ci-pipeline.svg",
        "notes": "Quang Vinh: Pipeline được module hóa thành 3 job nối nhau bằng needs. Fail ở đâu thì dừng ngay ở đó (fail-fast)."
    },
    # 21. REAL RUNS EVIDENCE
    {
        "stage": "CI/CD",
        "title": "CI-1/2/3: Minh chứng thực nghiệm trên GitHub",
        "layout": "split",
        "bullets": [
            "<strong>PR #1 (Xanh):</strong> Khởi tạo CI, cả 3 job chạy thành công trọn vẹn.",
            "<strong>PR #2 (Đỏ):</strong> Cố tình xóa test → Job test xanh nhưng coverage-gate đỏ → package bị hủy.",
            "<strong>PR #2 (Khôi phục):</strong> Bổ sung test đầy đủ → Toàn bộ pipeline xanh trở lại.",
            "<strong>PR #6 vào master:</strong> Trạng thái <strong>BLOCKED</strong> hoàn toàn do required checks bảo vệ!"
        ],
        "takeaway": "Chứng cứ: Minh chứng thật tại repo, lệnh gh pr merge bị từ chối thẳng thừng khi gate không đạt yêu cầu.",
        "diagram": "images/diagrams/pr-checks-blocked.svg",
        "notes": "Quang Vinh: Hình ảnh bên phải mô phỏng chính xác giao diện PR #6 trên GitHub khi bị required checks chặn đứng vì vi phạm gate."
    },
    # 22. WORKFLOW YAML
    {
        "stage": "CI/CD",
        "title": "Cấu trúc .github/workflows/ci.yml",
        "layout": "split",
        "bullets": [
            "<strong>Trigger:</strong> Kích hoạt khi có <code>pull_request</code> hoặc <code>push</code> vào master / seminar-core.",
            "<strong>Maven Cache:</strong> Dùng <code>actions/cache@v4</code> cache <code>~/.m2</code> theo hash của <code>pom.xml</code>.",
            "<strong>Step Summary:</strong> Xuất kết quả kiểm thử trực tiếp lên giao diện GitHub Action Markdown.",
            "<strong>Cơ chế needs:</strong> Khai báo tường minh <code>needs: [test]</code> và <code>needs: [coverage-gate]</code>."
        ],
        "takeaway": "Tối ưu: Cache dependency giúp rút ngắn thời gian chạy từ 48 giây xuống chỉ còn 12 giây trên máy chủ.",
        "diagram": "images/diagrams/github-workflow-structure.svg",
        "code": "name: Seminar CI\non: [pull_request, push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps: [checkout, setup-java, test]\n  coverage-gate:\n    needs: test\n    runs-on: ubuntu-latest\n    steps: [clean verify gate]\n  package:\n    needs: coverage-gate\n    runs-on: ubuntu-latest\n    steps: [package JAR]",
        "notes": "Quang Vinh: Cấu trúc workflow YAML ngắn gọn, tận dụng cache để tăng tốc build và hiển thị kết quả trực quan trên Step Summary."
    },
    # 23. GREEN TEST RED GATE
    {
        "stage": "CI/CD",
        "title": "Khi test xanh mà PR vẫn bị chặn",
        "layout": "split",
        "bullets": [
            "<strong>Thực nghiệm:</strong> Xóa <code>FineCalculatorTest</code> → 21 test LoanService vẫn pass 100%!",
            "<strong>Job 1 (test):</strong> Báo xanh hoàn toàn vì không có ca kiểm thử nào bị lỗi assertion.",
            "<strong>Job 2 (gate):</strong> Báo đỏ lập tức vì branch rơi về 0.00 &lt; 0.90 → Chặn đứng PR!",
            "<strong>Kết luận:</strong> Chỉ dựa vào test xanh là không đủ; bắt buộc phải có Coverage Gate trên CI."
        ],
        "takeaway": "Bài học: Test xanh chỉ chứng minh ca có sẵn không lỗi; Gate chứng minh mã mới không bị bỏ quên kiểm thử.",
        "diagram": "images/diagrams/green-test-red-gate.svg",
        "notes": "Quang Vinh: Đây là bài học thực tế đắt giá nhất: test pass là chưa đủ, phải có gate để phát hiện các đoạn mã mới bị bỏ quên kiểm thử."
    },
    # 24. CI WEAKNESSES
    {
        "stage": "CI/CD",
        "title": "Những điểm yếu thực tế khi vận hành CI",
        "layout": "split",
        "bullets": [
            "<strong>Cache Miss nhạy cảm:</strong> Sửa 1 dòng comment pom.xml làm đổi hash key → Tải lại từ đầu (48s vs 12s).",
            "<strong>Trùng lặp test suite:</strong> Job gate phải thực thi lại toàn bộ test suite lần 2 gây lãng phí tài nguyên.",
            "<strong>Dao động thời gian runner:</strong> Cùng 1 bước, thời gian runner dao động từ 29s đến 70s.",
            "<strong>Required check làm kẹt PR:</strong> PR vào master bị kẹt nếu workflow chưa khai báo trigger (PR #4)."
        ],
        "takeaway": "Kinh nghiệm: Hiểu rõ hạn chế giúp nhóm tối ưu thời gian chạy pipeline và xử lý sự cố kẹt PR kịp thời.",
        "diagram": "images/diagrams/ci-weaknesses.svg",
        "notes": "Quang Vinh: Nhóm thẳng thắn chỉ ra các điểm yếu thực tế: cache miss rất nhạy cảm và thời gian chạy trên cloud runner luôn có độ trễ dao động."
    },
    # 25. VIDEO D SUMMARY
    {
        "stage": "VIDEO DEMO D",
        "title": "Video D: CI/CD với GitHub Actions (8–9 phút)",
        "layout": "split",
        "bullets": [
            "<strong>Người thực hiện:</strong> Phạm Quang Vinh (23120202) · <strong>Thời lượng:</strong> 8 – 9 phút.",
            "<strong>00:00 - Setup:</strong> Phân tích file ci.yml, trigger, runner ubuntu-latest và Temurin JDK 25.",
            "<strong>01:00 - Khái niệm:</strong> Minh họa luồng CI/CD, cơ chế needs và plugin jacoco:check.",
            "<strong>02:15 - Demo đơn giản:</strong> Kích hoạt run xanh, đọc log Surefire, tải artifact JAR và cache.",
            "<strong>04:00 - Demo phức tạp:</strong> Mở PR đỏ bị gate chặn, PR vào master bị BLOCKED không cho merge.",
            "<strong>06:30 - Mổ xẻ sự cố:</strong> Cache miss khi đổi pom.xml, runner jitter và cách cứu PR kẹt."
        ],
        "takeaway": "Trạng thái: Đã quay xong video · Link YouTube: [Sẽ bổ sung URL sau] · File: .github/workflows/ci.yml",
        "diagram": "images/diagrams/video-d-timeline.svg",
        "notes": "Quang Vinh: Video demo D được chia mốc thời gian rõ ràng từ lý thuyết cơ bản đến các tình huống thực nghiệm lỗi nâng cao."
    },
    # 26. BENCHMARK MAVEN
    {
        "stage": "THỰC NGHIỆM",
        "title": "Thời gian đo tại máy: Cold Cache vs. Warm Cache",
        "layout": "split",
        "bullets": [
            "<strong>Kho Maven Lạnh (Cold):</strong> Xóa sạch ~/.m2 → Trung vị thời gian build: <strong>48.412 giây</strong>.",
            "<strong>Kho Maven Ấm (Warm):</strong> Giữ nguyên dependency → Trung vị thời gian build: <strong>12.539 giây</strong>.",
            "<strong>Hiệu quả:</strong> Cache giúp <strong>tiết kiệm 74% thời gian</strong> chạy pipeline của lập trình viên!",
            "<strong>Chi phí JaCoCo:</strong> Overhead kiểm tra độ phủ tăng khoảng 31% (9.7s lên 12.7s)."
        ],
        "takeaway": "Số liệu: Đo đạc 3 cặp chuẩn xác trên Java 25 tại máy cục bộ bằng script scripts/benchmark_maven.py.",
        "diagram": "images/diagrams/benchmark-chart.svg",
        "notes": "Quang Vinh: Số liệu đo 3 cặp tại máy chứng minh cache dependency giúp tiết kiệm tới gần 3/4 thời gian chờ đợi trên mỗi lần lập trình viên push mã."
    },
    # 27. AI-1/2 GEMINI
    {
        "stage": "AI TRONG KIỂM THỬ",
        "title": "AI-1/2: Gemini sinh test, Review rồi mới Apply",
        "layout": "split",
        "bullets": [
            "<strong>Context động:</strong> Runner tự đọc mã nguồn và gap; tuyệt đối không hard-code prompt.",
            "<strong>AI-1 &amp; AI-2:</strong> Gemini 3.6 sinh 7 test ban đầu + 3 test bổ sung lấp lỗ hổng độ phủ.",
            "<strong>Review &amp; Apply:</strong> Con người duyệt cú pháp và chạy thử nghiệm trên JVM thật.",
            "<strong>Kết quả:</strong> <strong>49/49 test pass</strong>; LoanService đạt tuyệt đối <strong>100% Branch Coverage</strong>."
        ],
        "takeaway": "Nguyên tắc: Không tin tưởng mù quáng vào AI; mọi ca test sinh ra đều phải được kiểm chứng qua oracle.",
        "diagram": "images/diagrams/ai-workflow.svg",
        "notes": "Gia An: Quy trình kết hợp AI có kiểm soát: AI sinh test nháp, con người review chặn ảo giác, chạy thử trên JVM thật rồi mới apply vào repo."
    },
    # 28. AI-3 BOT REVIEW
    {
        "stage": "AI TRONG KIỂM THỬ",
        "title": "AI-3: Review PR tự động song song với CI",
        "layout": "split",
        "bullets": [
            "<strong>Bot tự động:</strong> Phân tích riêng git diff của các file test khi mở Pull Request.",
            "<strong>Đánh giá độc lập:</strong> Nhận xét về chất lượng assertion, độ bao quát dữ liệu biên và nguy cơ flaky.",
            "<strong>Thực tế PR #13:</strong> Bot nhận xét tích cực, 0 finding tiêu cực, cả 6 job CI đều xanh.",
            "<strong>Nguyên tắc vàng:</strong> AI chỉ đóng vai trò tham vấn; không thay quyền quyết định của con người."
        ],
        "takeaway": "Cơ chế: AI Review chạy song song chứ không thay thế Required Checks của CI pipeline.",
        "diagram": "images/diagrams/pr-bot-comment.svg",
        "notes": "Gia An: AI Review chạy song song chứ không thay thế CI. Cho dù AI khen đẹp nhưng nếu Coverage Gate đỏ thì PR vẫn bị chặn."
    },
    # 29. AI-4 COMPARISON
    {
        "stage": "AI TRONG KIỂM THỬ",
        "title": "AI-4: Bộ test Người viết & AI bổ sung nhau",
        "layout": "split",
        "bullets": [
            "<strong>Bộ Người viết (Gia An):</strong> 23 ca từ đặc tả (16 ca hợp lệ, 7 ca lỗi) → <strong>Branch 10/10</strong>.",
            "<strong>Bộ AI sinh (Gemini):</strong> 13 ca độc lập → Tập trung ca hợp lệ &amp; <code>Integer.MAX_VALUE</code>.",
            "<strong>11 Đầu vào chung:</strong> Kết quả hoàn toàn trùng khớp (<strong>0 disagreement</strong>).",
            "<strong>Kết luận:</strong> Người nắm sâu logic nghiệp vụ; AI hỗ trợ phát hiện các giá trị biên cực đại."
        ],
        "takeaway": "Ý nghĩa: Người và AI cộng tác bổ trợ cho nhau thay vì loại trừ hay thay thế nhau.",
        "diagram": "images/diagrams/human-vs-ai.svg",
        "notes": "Gia An: Đây là thực nghiệm rất thú vị. Hai bộ test có 11 ca trùng nhau và cho kết quả giống hệt. Người giỏi ca nghiệp vụ, AI giỏi nghĩ ra số siêu to."
    },
    # 30. PAPER COVERUP
    {
        "stage": "NGHIÊN CỨU PAPER",
        "title": "Paper 1 · CoverUp: Coverage dẫn đường cho LLM",
        "layout": "split",
        "bullets": [
            "<strong>Bài báo:</strong> FSE 2025 (Hội nghị Công nghệ Phần mềm Quốc tế Hạng A*).",
            "<strong>Ý tưởng cốt lõi:</strong> Dùng báo cáo lỗ hổng độ phủ (Coverage Gaps) để làm prompt dẫn đường cho LLM.",
            "<strong>Tái hiện dữ liệu gốc:</strong> Phân tích 163 module đạt overall <strong>89.0%</strong> (vượt MuTAP 76.8%).",
            "<strong>Thực nghiệm nhóm:</strong> Trên benchmark f003 đạt 100% branch; trên source nhóm tăng từ <strong>23.6% lên 96.4%</strong>."
        ],
        "takeaway": "Đóng góp: Chứng minh hiệu quả vượt trội khi kết hợp tri thức LLM với phản hồi đo lường độ phủ động.",
        "diagram": "images/diagrams/coverup-flow.svg",
        "notes": "Gia An: CoverUp chứng minh hướng đi đúng đắn: dùng coverage report chỉ điểm cho LLM biết chỗ nào đang hở để sinh test nhắm trúng đích."
    },
    # 31. PAPER PYNGUIN
    {
        "stage": "NGHIÊN CỨU PAPER",
        "title": "Paper 2 · Pynguin: Sinh test bằng tìm kiếm tiến hóa",
        "layout": "split",
        "bullets": [
            "<strong>Bài báo:</strong> EMSE 2023 (Tạp chí quốc tế Hạng A) · Thuật toán tiến hóa DynaMOSA (không dùng LLM).",
            "<strong>Tái hiện dữ liệu công bố:</strong> 134 module, 40.200 dòng dữ liệu khớp 100% số liệu tác giả.",
            "<strong>Chạy mới:</strong> Benchmark <code>codetiming._timers</code> đạt coverage 81.48%, 10 pass, 5 xfail.",
            "<strong>Hạn chế chí mạng:</strong> Trên source nhóm, Pynguin sinh test chỉ gọi hàm mà <strong>thiếu assertion</strong>!"
        ],
        "takeaway": "So sánh: Pynguin chỉ tối ưu độ phủ toán học; CoverUp có LLM hiểu ngữ nghĩa để sinh assertion kiểm đúng/sai.",
        "diagram": "images/diagrams/papers-comparison.svg",
        "notes": "Gia An: Pynguin đại diện cho trường phái tìm kiếm tiến hóa. Nhược điểm chí mạng là nó chỉ cố gọi hàm để tăng coverage chứ không hiểu ngữ nghĩa để viết assertion kiểm đúng sai."
    },
    # 32. VIDEO E SUMMARY
    {
        "stage": "VIDEO DEMO E",
        "title": "Video E: AI Gemini & Tái hiện Paper (8–10 phút)",
        "layout": "split",
        "bullets": [
            "<strong>Người thực hiện:</strong> Ngô Gia An (23120205) · <strong>Thời lượng:</strong> 8 – 10 phút.",
            "<strong>GA-01/02:</strong> Setup Gemini client, AI-1 sinh test LoanService và AI-2 bổ sung test lấp gap.",
            "<strong>GA-03/04:</strong> Bot AI comment tự động trên PR; demo ca oracle sai để chỉ ra giới hạn của test xanh.",
            "<strong>GA-05:</strong> So sánh trực tiếp bộ test 23 ca của người viết với bộ test do Gemini sinh.",
            "<strong>GA-06/07:</strong> Tái hiện thực nghiệm bài báo CoverUp (FSE'25) và Pynguin (EMSE'23)."
        ],
        "takeaway": "Trạng thái: Đã quay xong video · Link YouTube: [Sẽ bổ sung URL sau] · Script: scripts/run_ai_demo.py",
        "diagram": "images/diagrams/video-e-timeline.svg",
        "notes": "Gia An: Video demo E phân bổ 7 phần từ thao tác code, review PR, đối chứng đến tái hiện bài báo khoa học."
    },
    # 33. ALL VIDEOS SUMMARY TABLE (NEW)
    {
        "stage": "TỔNG HỢP VIDEO",
        "title": "Danh mục 5 Video Demo của nhóm (Yêu cầu GV)",
        "layout": "split",
        "bullets": [
            "<strong>Video A (Unit Test):</strong> Bảo An · 5–7 phút · AAA, Parameterized CSV, Mockito, Anti-patterns.",
            "<strong>Video B (Coverage &amp; PIT):</strong> Nhật Đạt · 8–9 phút · 6 loại coverage, Gate fail, Bẫy PIT.",
            "<strong>Video C (REST &amp; Smoke):</strong> Thế Vinh · 3–5 phút · Chạy JAR, 7 kịch bản HTTP, mã lỗi 201/409/404.",
            "<strong>Video D (CI/CD Actions):</strong> Quang Vinh · 8–9 phút · 3 jobs needs, PR đỏ/xanh, PR BLOCKED.",
            "<strong>Video E (AI &amp; Paper):</strong> Gia An · 8–10 phút · Gemini test gen, đối chứng, CoverUp &amp; Pynguin."
        ],
        "takeaway": "Cam kết: Tất cả 5 video đã được các thành viên quay hoàn tất; URL YouTube sẽ được đính kèm vào link nộp bài.",
        "diagram": "images/diagrams/all-videos-table.svg",
        "notes": "Bảo An: Đây là bảng tổng hợp cả 5 video demo độc lập của nhóm, đáp ứng đầy đủ yêu cầu bắt buộc của giảng viên."
    },
    # 34. EXERCISES
    {
        "stage": "THỰC HÀNH",
        "title": "3 Bài tập thực hành dành cho người tham gia",
        "layout": "split",
        "bullets": [
            "<strong>Bài 1 (Dễ · Unit Test):</strong> Thêm hạng <code>STUDENT</code> (giảm 50% phạt, trần 30k) và viết Parameterized test.",
            "<strong>Bài 2 (Trung bình · Coverage &amp; PIT):</strong> Cố tình xóa 1 assertion tiền; so sánh JaCoCo (vẫn 100%) vs PIT Mutation (mutant sống).",
            "<strong>Bài 3 (Nâng cao · CI/CD):</strong> Tích hợp CI vào fork, mở PR thiếu nhánh kiểm thử để quan sát Gate chặn merge."
        ],
        "takeaway": "Tài liệu kèm theo: Mã nguồn khung tại case-study/ và hướng dẫn từng bước tại docs/thuc-hanh/HuongDan_Demo.md.",
        "diagram": "images/diagrams/exercises.svg",
        "notes": "Thế Vinh: Nhóm chuẩn bị 3 bài tập từ dễ đến khó để các bạn sinh viên sau buổi seminar có thể tự thực hành trên máy."
    },
    # 35. DELIVERABLES
    {
        "stage": "TỔNG KẾT",
        "title": "7 Đầu ra hoàn chỉnh trong gói nộp Tuần 06",
        "layout": "split",
        "bullets": [
            "<strong>1. Slide &amp; Báo cáo:</strong> Slide Reveal.js monochrome + Báo cáo LaTeX tại <code>report/main.tex</code>.",
            "<strong>2. Video Demo:</strong> Đầy đủ 5 video (A, B, C, D, E) quay trên màn hình ứng dụng thật.",
            "<strong>3. Mã nguồn &amp; Minh chứng:</strong> Unit test, script AI runner, benchmark và minh chứng tại <code>evidence/</code>.",
            "<strong>4. Quản lý nhóm:</strong> Bảng phân công <code>PhanCong_NhiemVu.md</code>, Git commit log thật &amp; Khai báo AI."
        ],
        "takeaway": "Nghiệm thu: Gói nộp Tuần 06 đạt &gt;90% khối lượng đề tài, đầy đủ minh chứng thực nghiệm có thể tái hiện.",
        "diagram": "images/diagrams/deliverables.svg",
        "notes": "Bảo An: Toàn bộ 7 hạng mục đầu ra đều được nhóm đóng gói chỉn chu, minh bạch và sẵn sàng nộp cho giảng viên."
    },
    # 36. Q&A
    {
        "stage": "TÀI LIỆU",
        "title": "Nguồn tham khảo & Hỏi đáp (Q&A)",
        "layout": "split",
        "bullets": [
            "<strong>Tài nguyên dự án:</strong> <code>README.md</code>, <code>docs/thuc-hanh/</code>, <code>evidence/tuan-06/</code>.",
            "<strong>Tài liệu kỹ thuật:</strong> JUnit 5, Mockito, JaCoCo, PIT, GitHub Actions, Gemini API.",
            "<strong>Nghiên cứu khoa học:</strong> Paper CoverUp (FSE 2025) &amp; Pynguin (EMSE 2023).",
            "<strong>Cảm ơn quý thầy cô và các bạn!</strong> Nhóm 09 sẵn sàng giải đáp mọi thắc mắc."
        ],
        "takeaway": "Thông tin liên hệ: Nhóm 09 · Môn Kiểm thử phần mềm · FIT - Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM.",
        "diagram": "images/diagrams/qa-resources.svg",
        "notes": "Bảo An: Nhóm 09 xin chân thành cảm ơn thầy và các bạn đã lắng nghe. Bây giờ là thời gian dành cho phần hỏi đáp (Q&A)."
    }
]

def render_html():
    sections = []
    for idx, slide in enumerate(slides_data, 1):
        stage = html.escape(slide["stage"])
        title = html.escape(slide["title"])
        notes = f'<aside class="notes">{html.escape(slide["notes"])}</aside>' if slide.get("notes") else ""

        # Layout 1: Hero title slide
        if slide.get("layout") == "hero":
            bullets_html = "".join(f"<li>{b}</li>" for b in slide["bullets"])
            logos_html = "".join(f'<img src="images/logos/{logo}" alt="logo" class="tech-logo" />' for logo in slide.get("logos", []))
            takeaway_html = f'<div class="takeaway-card"><div class="takeaway-title">CÂU HỎI XUYÊN SUỐT</div><div class="takeaway-content">{html.escape(slide["takeaway"])}</div></div>' if slide.get("takeaway") else ""
            section_html = f'''
      <section class="slide-hero" data-transition="fade">
        <div class="stage-pill">{stage}</div>
        <h1 class="hero-title">{title}</h1>
        <div class="split-container">
          <div class="split-left">
            <ul class="styled-list">{bullets_html}</ul>
            {takeaway_html}
            <div class="logo-strip">{logos_html}</div>
          </div>
          <div class="split-right">
            <div class="visual-box">
              <img src="{slide['diagram']}" alt="Three layers architecture" class="diagram-img" />
            </div>
          </div>
        </div>
        {notes}
      </section>'''
            sections.append(section_html)

        # Layout 2: Team slide
        elif slide.get("layout") == "team":
            members_html = []
            for m in slide["members"]:
                members_html.append(f'''
            <div class="member-card">
              <div class="member-header">
                <span class="member-name">{html.escape(m['name'])}</span>
                <span class="member-mssv">{html.escape(m['mssv'])}</span>
              </div>
              <div class="member-role">{html.escape(m['role'])}</div>
              <div class="member-task">{html.escape(m['task'])}</div>
            </div>''')
            all_members = "".join(members_html)
            section_html = f'''
      <section class="slide-team" data-transition="fade">
        <div class="stage-pill">{stage}</div>
        <h2>{title}</h2>
        <div class="team-grid">{all_members}</div>
        <div class="takeaway-card" style="margin-top: 1.2rem;">
          <div class="takeaway-title">CAM KẾT MINH BẠCH &amp; ĐÓNG GÓP THỰC TẾ</div>
          <div class="takeaway-content">100% thành viên có commit và Pull Request thật trên Git; mỗi người tự quay và thuyết minh video demo công cụ phụ trách.</div>
        </div>
        {notes}
      </section>'''
            sections.append(section_html)

        # Layout 3: Standard Split View (1fr 1fr - Balanced Left and Right)
        else:
            bullets_html = "".join(f"<li>{b}</li>" for b in slide.get("bullets", []))
            code_html = f'<div class="code-wrapper"><pre><code class="language-java">{html.escape(slide["code"])}</code></pre></div>' if slide.get("code") else ""
            takeaway_html = f'<div class="takeaway-card"><div class="takeaway-title">ĐIỂM THEN CHỐT</div><div class="takeaway-content">{html.escape(slide["takeaway"])}</div></div>' if slide.get("takeaway") else ""

            # Right visual column
            if slide.get("diagram"):
                visual_html = f'<div class="visual-box"><img src="{slide["diagram"]}" alt="diagram" class="diagram-img" /></div>'
            elif slide.get("image"):
                visual_html = f'<div class="visual-box"><img src="{slide["image"]}" alt="evidence" class="screenshot-img" /></div>'
            else:
                visual_html = '<div class="visual-box"><img src="images/diagrams/three-layers.svg" alt="fallback visual" class="diagram-img" /></div>'

            section_html = f'''
      <section class="slide-split" data-transition="fade">
        <div class="stage-pill">{stage}</div>
        <h2>{title}</h2>
        <div class="split-container">
          <div class="split-left">
            <ul class="styled-list">{bullets_html}</ul>
            {code_html}
            {takeaway_html}
          </div>
          <div class="split-right">{visual_html}</div>
        </div>
        {notes}
      </section>'''
            sections.append(section_html)

    slides_body = "\n".join(sections)

    full_html = f'''<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Seminar · Unit Test, Coverage, CI/CD · Nhóm 09</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="dist/reset.css">
  <link rel="stylesheet" href="dist/reveal.css">
  <link rel="stylesheet" href="dist/theme/white.css">
  <style>
    /* ============================================================
       HIGH-CONTRAST MONOCHROME THEME · OPTIMIZED FOR BRIGHT HALLS
       - Crisp, large, bold typography
       - Zero empty/sparse space: full, balanced two-column layout
       - 100% offline & strictly black-on-white
       ============================================================ */
    :root {{
      --r-background-color: #ffffff;
      --r-main-color: #111111;
      --r-heading-color: #000000;
      --r-link-color: #111111;
      --r-selection-background-color: #e5e5e5;
      --r-selection-color: #000000;
    }}

    body {{
      background: #ffffff !important;
      color: #111111 !important;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }}

    .reveal {{
      background-color: #ffffff;
      color: #111111;
      font-size: 25px; /* Larger base font for clear readability */
      font-weight: 400;
    }}

    /* Global Slide Container */
    .reveal .slides {{
      text-align: left;
    }}

    .reveal .slides section {{
      padding: 1.5rem 2.8rem !important;
      box-sizing: border-box;
      height: 100% !important;
      max-height: 100% !important;
      overflow: hidden !important;
    }}

    /* Stage Pill / Badge */
    .stage-pill {{
      display: inline-block;
      font-family: Consolas, "JetBrains Mono", monospace;
      font-size: 0.62em;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 4px 10px;
      background: #f0f0f0;
      color: #111111;
      border: 1.5px solid #111111;
      border-radius: 4px;
      margin-bottom: 0.5rem;
    }}

    /* Headings */
    .reveal h1, .reveal h2, .reveal h3 {{
      font-family: Georgia, -apple-system, serif;
      color: #000000;
      font-weight: 700;
      letter-spacing: -0.02em;
      text-transform: none;
      margin: 0 0 0.9rem 0 !important;
      line-height: 1.18;
    }}

    .hero-title {{
      font-size: 2.0em !important;
      max-width: 1100px;
      margin-bottom: 1.1rem !important;
    }}

    .reveal h2 {{
      font-size: 1.52em !important;
      margin-bottom: 0.9rem !important;
    }}

    /* Lists */
    ul.styled-list {{
      list-style-type: none;
      padding-left: 0;
      margin: 0 0 0.6rem 0;
      font-size: 0.94em;
      line-height: 1.52;
    }}

    ul.styled-list li {{
      position: relative;
      padding-left: 1.5rem;
      margin-bottom: 0.65rem;
      color: #222222;
    }}

    ul.styled-list li::before {{
      content: "■";
      position: absolute;
      left: 0;
      top: 1px;
      font-size: 0.65em;
      color: #111111;
    }}

    ul.styled-list strong {{
      color: #000000;
      font-weight: 750;
    }}

    /* Split 2-Column Layout (52% Left, 48% Right) */
    .split-container {{
      display: grid;
      grid-template-columns: 1.08fr 0.92fr;
      gap: 2.2rem;
      align-items: stretch;
      min-height: 520px;
    }}

    .split-left {{
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .split-right {{
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }}

    /* Takeaway Anchor Card (Fills empty vertical space cleanly) */
    .takeaway-card {{
      border: 1.5px solid #111111;
      border-left: 5px solid #111111;
      background: #fafafa;
      padding: 0.7rem 1.1rem;
      border-radius: 4px;
      margin-top: 0.7rem;
      font-size: 0.82em;
      box-shadow: 3px 3px 0px #111111;
      box-sizing: border-box;
    }}

    .takeaway-title {{
      font-family: Consolas, monospace;
      font-weight: 800;
      font-size: 0.85em;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: #111111;
      margin-bottom: 0.25rem;
    }}

    .takeaway-content {{
      color: #333333;
      line-height: 1.42;
    }}

    /* Visual Media Container */
    .visual-box {{
      width: 100%;
      height: 100%;
      min-height: 480px;
      max-height: 540px;
      border: 2px solid #111111;
      border-radius: 8px;
      background: #ffffff;
      padding: 12px;
      box-shadow: 4px 4px 0px #111111;
      box-sizing: border-box;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}

    .diagram-img {{
      width: 100%;
      height: 100%;
      max-height: 500px;
      object-fit: contain;
      display: block;
    }}

    .screenshot-img {{
      width: 100%;
      height: 100%;
      max-height: 500px;
      object-fit: contain;
      display: block;
      border-radius: 4px;
      filter: grayscale(100%) contrast(105%);
    }}

    /* Code Blocks */
    .code-wrapper pre {{
      background: #f6f8fa !important;
      border: 1.5px solid #111111 !important;
      border-radius: 6px !important;
      box-shadow: 3px 3px 0px #111111 !important;
      padding: 0.65rem 0.9rem !important;
      margin: 0.5rem 0 !important;
      font-size: 0.74em !important;
      line-height: 1.4 !important;
      max-height: 200px !important;
      overflow: auto !important;
    }}

    .code-wrapper code {{
      font-family: Consolas, "JetBrains Mono", "DejaVu Sans Mono", monospace !important;
      color: #111111 !important;
    }}

    code {{
      font-family: Consolas, "JetBrains Mono", monospace;
      background: #f0f0f0;
      padding: 2px 5px;
      border-radius: 3px;
      font-size: 0.88em;
      border: 1px solid #d0d0d0;
    }}

    /* Logo Strip */
    .logo-strip {{
      display: flex;
      gap: 1.2rem;
      align-items: center;
      margin-top: 1.0rem;
      padding-top: 0.8rem;
      border-top: 1px solid #ddd;
    }}

    .tech-logo {{
      width: 32px;
      height: 32px;
      filter: grayscale(100%);
      opacity: 0.9;
    }}

    /* Team Slide Grid */
    .team-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.1rem;
      margin-top: 0.8rem;
    }}

    .member-card {{
      background: #ffffff;
      border: 2px solid #111111;
      border-radius: 6px;
      padding: 0.9rem 1.1rem;
      box-shadow: 3px 3px 0px #111111;
      font-size: 0.82em;
    }}

    .member-header {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 0.3rem;
    }}

    .member-name {{
      font-weight: 750;
      font-size: 1.15em;
      color: #000000;
    }}

    .member-mssv {{
      font-family: monospace;
      color: #444444;
      font-weight: 600;
    }}

    .member-role {{
      font-weight: 700;
      color: #111111;
      margin-bottom: 0.4rem;
      font-size: 0.92em;
      background: #f0f0f0;
      display: inline-block;
      padding: 2px 7px;
      border-radius: 3px;
      border: 1px solid #ccc;
    }}

    .member-task {{
      color: #333333;
      line-height: 1.4;
    }}

    /* Progress bar and controls */
    .reveal .progress {{
      color: #111111;
      height: 4px;
    }}
    .reveal .controls {{
      color: #111111;
    }}
    .reveal .slide-number {{
      font-family: monospace;
      color: #111111;
      background-color: transparent;
      font-size: 14px;
      right: 1.5rem;
      bottom: 0.9rem;
    }}

    /* Pinned Header Bar */
    .header-bar {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      display: flex;
      justify-content: space-between;
      padding: 0.6rem 2.8rem;
      font-size: 0.76rem;
      color: #555555;
      border-bottom: 1px solid #d5d5d5;
      background: #ffffff;
      z-index: 10;
    }}
    .header-bar strong {{
      color: #111111;
    }}

    /* Print styles */
    @media print {{
      .header-bar {{ display: none; }}
      .reveal .slides section {{
        page-break-after: always !important;
        height: 100% !important;
      }}
    }}
  </style>
</head>
<body>
  <div class="header-bar">
    <span><strong>Seminar KCPM · Nhóm 09</strong> (Tuần 06)</span>
    <span>Chủ đề: Unit Test → Coverage Gate → CI/CD</span>
  </div>

  <div class="reveal">
    <div class="slides">
{slides_body}
    </div>
  </div>

  <script src="dist/reveal.js"></script>
  <script src="dist/plugin/notes.js"></script>
  <script src="dist/plugin/highlight.js"></script>
  <script>
    Reveal.initialize({{
      width: 1366,
      height: 768,
      margin: 0.05,
      minScale: 0.2,
      maxScale: 1.5,
      hash: true,
      slideNumber: 'c/t',
      progress: true,
      controls: true,
      keyboard: true,
      center: false,
      transition: 'fade',
      transitionSpeed: 'fast',
      plugins: [ RevealHighlight, RevealNotes ]
    }});
  </script>
</body>
</html>'''

    with open(SLIDES_HTML, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Successfully generated {SLIDES_HTML} ({len(slides_data)} slides).")

if __name__ == '__main__':
    render_html()
