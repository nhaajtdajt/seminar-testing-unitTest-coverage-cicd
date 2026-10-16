# Báo cáo tuần thực hành 04 — Seminar Unit Test · Code Coverage · CI/CD

**Nhóm:** Nhóm 09 (Group09)

**Thành viên:** TV1: Nguyễn Bảo An (23120207); TV2: Phạm Quang Vinh (23120202); TV3: Trương Nhật Đạt (23120231); TV4: Nguyễn Lê Thế Vinh (23120190); TV5: Ngô Gia An (23120205)

**Tuần báo cáo:** Tuần thực hành **04**, theo xác nhận của nhóm. **Khoảng thời gian tuần học:** 12/10/2026 – 16/10/2026 (Thứ Hai đến Thứ Sáu).

**Tiến độ:** Nhóm đã thực hiện một phần công việc dự kiến cho Tuần 05 ngay trong Tuần 04. Các kết quả đã có được ghi nhận trong báo cáo Tuần 04; phần còn thiếu tiếp tục theo kế hoạch Tuần 05.

**Tên gói nộp:** `Group09-04.zip`. WeekID tính theo tuần thực hành.

**Ngày thực hiện đợt bổ sung và chạy minh chứng:** 16/10/2026. **Người phụ trách tổng hợp:** Nguyễn Bảo An (23120207) — Nhóm trưởng. **Xác nhận nội dung:** Nhóm rà soát trước khi nộp.

> Bản báo cáo này tổng hợp sản phẩm hiện có và phần triển khai bổ sung với Codex hỗ trợ ở Tuần thực hành 04, bao gồm phần làm trước theo kế hoạch Tuần 05. TV1–TV5 dưới đây là vai trò phụ trách rà soát/nhận bàn giao. Nhóm cần xác nhận người thực hiện thực tế trước khi nộp; các file do trợ lý chuẩn bị không tự chứng minh đóng góp cá nhân. Các kết quả chạy được ghi theo thời điểm trong log; chưa có báo cáo riêng của những tuần trước thì không tự ghi lùi ngày.

Các đường dẫn `evidence/tuan-05/` giữ tên thư mục đã dùng khi triển khai theo kế hoạch Tuần 05. Thời điểm thực hiện nằm trong metadata/log; nhãn thư mục này không phải WeekID của bài nộp. Báo cáo và gói nộp hiện tại dùng WeekID **04**.

## 1. Mục tiêu tuần

Hoàn thiện Unit Test và Coverage theo kế hoạch Tuần 04, đồng thời thực hiện sớm các phần tích hợp dự kiến cho Tuần 05: case study chạy được; test/coverage có minh chứng; pipeline CI có cấu hình; demo AI có đầu vào/đầu ra và phép đo; có bản nháp slide, báo cáo và hướng dẫn demo.

## 2. Kết quả chung có minh chứng

| Hạng mục | Kết quả thực tế | Minh chứng |
|---|---|---|
| Case study | Java 25 + Spring Boot 4.1.1; tính phí, mượn sách, REST API; H2 in-memory qua Spring Data JPA | [Mã nguồn](../case-study/), [hướng dẫn](../docs/thuc-hanh/HuongDan_Demo.md) |
| Bộ kiểm thử chuẩn | 33 lượt test, 0 failure, 0 error; gồm 17 tính phí, 6 nghiệp vụ, 5 tầng web, 2 integration, 3 persistence (H2) | [Lượt cuối Java 25](../evidence/tuan-05/final/), [Java 21](../evidence/tuan-05/jdk21/) |
| Coverage trước/sau | Riêng FineCalculator: baseline 50% nhánh → bộ đầy đủ 100%; 100% line ở bộ đầy đủ | [Baseline](../evidence/tuan-05/baseline/site/jacoco/index.html), [bản đầy đủ](../evidence/tuan-05/final/site/jacoco/index.html) |
| Coverage gate | Yêu cầu >=90% nhánh cho FineCalculator; baseline fail, bộ đầy đủ pass | [Log fail](../evidence/tuan-05/gate-fail/output.log), [log pass](../evidence/tuan-05/final/output.log) |
| TDD | 4 vòng đỏ/xanh chạy trong bản sao riêng; có source/test/XML từng vòng | [Replay TDD](../evidence/tuan-05/tdd-replay/summary.json) |
| Test yếu và mutation | Cùng 100% branch: bộ yếu diệt 3/11 mutant; bộ đầy đủ diệt 10/11 | [PIT yếu](../evidence/tuan-05/pit-weak/pit-reports/index.html), [PIT đầy đủ](../evidence/tuan-05/pit-strong/pit-reports/index.html) |
| Luồng HTTP thật | Chạy ứng dụng đóng gói trên cổng loopback ngẫu nhiên; 5/5 tình huống đúng mã HTTP/kết quả | [Kết quả HTTP](../evidence/tuan-05/http-smoke/results.json) |
| CI/CD | Có workflow test → gate → package, JDK 25, cache, artifact; có Jenkinsfile đối chiếu | [Workflow](../.github/workflows/ci.yml), [Jenkinsfile](../Jenkinsfile), [actionlint pass](../evidence/tuan-05/workflow-lint/run.json) |
| AI-1/AI-2 | Bản đầu 3 test pass, phủ 70% nhánh; thêm 3 test từ gap, 6 test pass, phủ 100% | [Bản đầu đã kiểm lại](../evidence/tuan-05/ai-draft-recheck/), [bản bổ sung](../evidence/tuan-05/ai-improved/) |
| AI-3 | Có prompt, client, workflow và review fixture tương tác; chế độ chuẩn bị không gọi API | [Prompt đã chuẩn bị](../evidence/tuan-05/ai-review-prepared/), [review Codex](../ai/results/AI-3-session-review.json) |
| AI-4 | 13/13 ca CSV AI chạy pass; trùng 13/15 ca tham chiếu; chưa có bộ con người độc lập | [CSV](../ai/data/AI-4-boundaries.csv), [log chạy](../evidence/tuan-05/ai-data/output.log) |
| Công cụ phụ trợ | 5 test Python pass; kiểm chế độ không gọi API, phản hồi lỗi, trích gap và đếm review | [Log](../evidence/tuan-05/python-tools/output.log) |
| Slide nháp | 23 trang nền trắng/chữ đen; nội dung đã đồng bộ bản Java 25. Đã mở slide và chụp trang phân công trong trình duyệt | [Slide](../slides/index.html) |

Một mutant còn sống trong bộ đầy đủ đổi `<=` thành `<` tại ngưỡng gia hạn. Tại đúng ngưỡng, cả hai cách vẫn tính ra 0; đây là mutant tương đương theo đặc tả hiện tại. Không tuyên bố mutation score 100%.

Số test là **số lượt thực thi**, gồm các dòng dữ liệu parameterized. Bộ Java 25 và 21 chạy lại cùng bộ chuẩn; không cộng thành 66 ca kiểm thử khác nhau. Phần test bẫy/AI dùng profile riêng và không thuộc bộ chuẩn 33 lượt.

## 3. Phân công 5 thành viên và phần cần xác nhận

| Vai trò | Sản phẩm bàn giao để thành viên rà soát | Trạng thái đến lúc chốt | Việc thành viên cần làm tiếp |
|---|---|---|---|
| Nguyễn Bảo An (23120207) — Trưởng nhóm/Unit Test | FineCalculatorTest/CSV, LoanServiceTest, UT-1/2/3, replay TDD và tổng hợp báo cáo | Các test chạy pass tại máy | Tự chạy lại, rà soát assertion/đặc tả, viết phần giải thích và quay demo UT; chốt hồ sơ nộp. |
| Phạm Quang Vinh (23120202) — CI-CD, Build & Benchmark | Kế hoạch build Java 25, bảng công việc, Actions, Jenkinsfile, đo benchmark | Có file và kiểm tra tĩnh; benchmark 3 cặp pass | Cập nhật board, dùng tài khoản có quyền ghi để chạy CI, cấu hình required checks và thu PR đỏ/xanh. |
| Trương Nhật Đạt (23120231) — Coverage | JaCoCo, gate, hai bộ PIT, báo cáo trước/sau và phép đo | Có log/XML/HTML tại máy | Kiểm số liệu, giải thích mutant còn sống; chạy gate trên CI và thu link run. |
| Nguyễn Lê Thế Vinh (23120190) — Case study | Logic, service/repository, controller, integration test và HTTP smoke | Ứng dụng chạy được với H2 in-memory | Tự chạy từ README, xác nhận nghiệp vụ và phạm vi dữ liệu; chuẩn bị dữ liệu cho buổi demo. |
| Ngô Gia An (23120205) — AI/trình bày | 4 prompt, script/gap/CSV/review AI, slide, báo cáo Markdown/LaTeX | Có bản nháp; API AI và nhóm review chưa hoàn tất | Cấu hình API bằng Secrets nếu nhóm dùng; review nội dung AI, hoàn thiện slide/báo cáo và video. |

Bảng việc chi tiết: [BangCongViec.md](../docs/thuc-hanh/BangCongViec.md). Lịch sử Git thật chưa cho phép thống kê đóng góp theo từng thành viên: trước đợt này chỉ có 4 commit tài liệu ngày 01/10/2026 của một tài khoản, kèm các commit mã nguồn mới tạo cục bộ trên `master` ngày 16/10/2026. Mỗi thành viên cần tự commit phần của mình bằng tài khoản của mình thì mới có số liệu đối chiếu.

## 4. Đối chiếu các mốc kế hoạch

Các tuần trong bảng là mốc công việc của kế hoạch. Thời điểm báo cáo hiện tại là Tuần thực hành 04; các phần thuộc mốc Tuần 05 đã có là công việc thực hiện sớm.

| Mốc kế hoạch | Tài liệu/sản phẩm hiện có | Giới hạn xác nhận thời gian |
|---|---|---|
| Tuần 2 | Gói đề xuất, outline, khảo sát, ma trận demo, kế hoạch AI, phân công | Git có commit tài liệu ngày 01/10/2026; chưa đủ cơ sở tự quy đổi ngày này thành tuần học cụ thể hoặc xác nhận đã gặp giảng viên. |
| Tuần 3 | Case study, bộ test ban đầu, cấu hình coverage và CI | Các phần mã/chạy thật được bổ sung trong đợt hiện tại ở Tuần 04; chưa có chứng cứ thực hiện riêng ở Tuần 3. |
| Tuần 4 | Unit test đầy đủ, gate, mutation, AI-1/4 | Có kết quả thực hành và log được tổng hợp trong báo cáo này. |
| Tuần 5 — làm trước | Tích hợp mã, test, coverage, CI config, AI demo tương tác, bản nháp tài liệu | Các sản phẩm đã có được ghi nhận ở Tuần 04; các bước dịch vụ bên ngoài còn thiếu được ghi ở mục 6 và chuyển sang kế hoạch Tuần 05. |

Lịch sử có sẵn: [existing-history.txt](../evidence/tuan-05/existing-history.txt). Nhóm bổ sung biên bản thật nếu đã có, thay vì tạo báo cáo quá khứ với ngày giả định.

## 5. Phép đo tại máy

| Thí nghiệm | Số lượt | Trung vị thời gian |
|---|---|---|
| Build Maven với kho dependency trống (lạnh) | 3 | 48,412 giây |
| Build ngay sau đó với kho đã có dependency (ấm) | 3 | 12,539 giây |
| Verify không bật JaCoCo | 3 | 9,727 giây |
| Verify có JaCoCo/report/gate | 3 | 12,754 giây |

Log và từng số đo: [JaCoCo](../evidence/tuan-05/benchmark-jacoco/summary.json), [cache](../evidence/tuan-05/benchmark-cache/summary.json). Phép đo cache đã đủ **3/3 cặp hợp lệ trên Java 25**; trung vị được tính trên cả ba cặp. Các lượt không hoàn tất, lỗi tải và hết thời hạn được giữ trong [failed-attempts](../evidence/tuan-05/benchmark-cache/failed-attempts/) và không tính vào trung vị. Đây là số đo tại máy, có ảnh hưởng của mạng/tải máy và thứ tự chạy; không coi là tốc độ của GitHub Actions hoặc một benchmark hiệu năng tổng quát.

| Cặp đo | Lạnh (giây) | Ấm (giây) | Bắt đầu lượt lạnh (UTC, 16/10/2026) |
|---|---|---|---|
| 1 | 48,412 | 12,539 | 10:25:03 |
| 2 | 46,713 | 13,229 | 10:26:04 |
| 3 | 479,523 | 11,940 | 15:00:15 |

Cặp 3 được bổ sung muộn hơn, dùng IPv4, connect timeout 15 giây, request timeout 120 giây và giới hạn 1.800 giây/lệnh; kho lạnh ban đầu trống, kho ấm dùng lại đúng kho vừa tải. Lượt lạnh cặp 3 mất khoảng 8 phút khi tải dependency, nên cần đọc từng số đo cùng điều kiện mạng, không chỉ nhìn trung vị. Hai cặp cũ và log được giữ nguyên; [resume-provenance.json](../evidence/tuan-05/benchmark-cache/resume-provenance.json) lưu dữ liệu và SHA-256 để đối chiếu.

## 6. Kế hoạch tuần thực hành 05

| Thành viên | Việc cụ thể | Sản phẩm cần chốt |
|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | Commit và đưa source lên repo có quyền, chạy CI/PR đỏ–xanh, bật required checks; đối chiếu và lưu số liệu benchmark đã đủ 3 cặp | Link run/PR, artifact, bảng công việc và benchmark đủ số lượt hợp lệ. |
| Nguyễn Bảo An (TV2, 23120207) | Tự chạy và duyệt UT-1/2/3, rà soát assertion/dữ liệu biên, ghi đóng góp thực tế | Bộ test và hướng dẫn được thành viên xác nhận. |
| Trương Nhật Đạt (TV3, 23120231) | Đối chiếu JaCoCo/PIT, kiểm gate trên CI và ghi kết quả đỏ/xanh | Báo cáo/log và link CI tương ứng. |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Chạy lại case study theo README, kiểm dữ liệu và luồng demo | Hướng dẫn tái hiện, dữ liệu/kịch bản demo đã kiểm tra. |
| Ngô Gia An (TV5, 23120205) | Chạy AI-3 nếu có cấu hình, hoàn thiện bảng đánh giá AI, review bản nháp slide/báo cáo | Kết quả AI có minh chứng, bảng đối chiếu và tài liệu đã review. |

**Tệp đầu mối:** [README](../README.md), [bản thảo báo cáo chi tiết](../docs/thuc-hanh/BaoCao_ChiTiet.md), [slide](../slides/index.html), [LaTeX](../report/main.tex), [hướng dẫn demo](../docs/thuc-hanh/HuongDan_Demo.md), [mục lục minh chứng](../evidence/tuan-05/README.md).

## 7. Phần đã làm trước và phần còn lại của kế hoạch Tuần 05

**Kết quả tại Tuần thực hành 04:** Đã có phần thực hành tại máy và bản nháp tài liệu, bao gồm các hạng mục làm trước của Tuần 05. Các mục chưa có minh chứng tiếp tục được thực hiện ở Tuần 05.

| Vai trò | Phần đã có | Phần còn thiếu để chốt kế hoạch |
|---|---|---|
| Phạm Quang Vinh (TV1, 23120202) | Actions, Jenkinsfile, JDK 25, cấu hình cache/artifact | Commit và đưa source lên repo nhóm; run CI thật, PR đỏ → xanh, required checks, tải artifact; chưa có số đo thời gian chạy trên CI (benchmark tại máy đã đủ 3/3 cặp). |
| Nguyễn Bảo An (TV2, 23120207) | Bộ test/CSV, Mockito, hướng dẫn UT-1/2/3, log TDD replay | Thành viên phụ trách review và xác nhận |
| Trương Nhật Đạt (TV3, 23120231) | JaCoCo, gate fail/pass, PIT và giải thích số liệu tại máy | Minh chứng gate đỏ/xanh trên CI của repo nhóm |
| Nguyễn Lê Thế Vinh (TV4, 23120190) | Case study H2/JPA, integration/persistence test, HTTP smoke | Thành viên phụ trách tự chạy lại theo hướng dẫn, xác nhận nghiệp vụ và môi trường demo |
| Ngô Gia An (TV5, 23120205) | AI-1/2/4 có output/test, prompt AI-3, slide/báo cáo nháp | AI-3 chưa gọi API hoặc chạy trên PR thật |

Tại thời điểm kiểm tra, các thư mục source, workflow và báo cáo mới vẫn là file **chưa được Git theo dõi**. Repo đang đăng nhập với quyền READ, nên hiện chưa có cơ sở xác nhận mã thực hành đã được nộp lên repo nhóm. Cần phân công người có quyền ghi thực hiện và ghi nhận tác giả thực tế.

Đã điền tên/MSSV 5 thành viên và phân công theo thông tin nhóm cung cấp. Thông tin còn cần bổ sung: mã nhóm, Git username của các thành viên chưa có trong lịch sử, đóng góp có minh chứng, góp ý giảng viên và biên bản/báo cáo các tuần trước. Repo hiện có báo cáo tổng hợp Tuần thực hành 04; các báo cáo tuần trước cần được bổ sung từ tài liệu thực tế nếu có yêu cầu nộp riêng.

Theo kế hoạch, việc quay video có thuyết minh, chốt bài tập và hoàn thiện bản nộp chính thức thuộc Tuần 6. Nhóm cần ưu tiên hoàn tất CI, AI-3 và minh chứng đóng góp trước mốc đó.

## 8. Dọn gói làm việc

Đã dọn đầu ra build, cache Python, ảnh kiểm tra cũ, lượt verify lặp và bằng chứng Java 21/Boot 3.5 đã được thay thế; bản đề xuất trùng và kế hoạch nội bộ cũ được đưa vào Thùng rác. Gói `nop-lan-1/`, source Java 25, báo cáo/slide hiện tại và các lượt minh chứng phục vụ UT/coverage/AI vẫn được giữ.

Khi dọn, hai cặp benchmark Java 25 hợp lệ đã được đưa về `evidence/tuan-05/benchmark-cache/`; sau đó đã chạy bổ sung thành công cặp thứ 3. Các lượt lỗi giữ riêng trong `failed-attempts/`. Danh sách thao tác và kiểm tra sau dọn: [cleanup.json](../evidence/tuan-05/cleanup.json).

## 9. Minh chứng trực quan và bộ nộp Tuần 04

Đã điền 5 thành viên và phân công theo thông tin nhóm cung cấp. Theo yêu cầu của nhóm, bộ nộp Tuần 04 dùng ảnh minh chứng, không kèm video. Ảnh API được chụp từ trang kiểm tra gửi request thật tới ứng dụng; trang này phục vụ minh chứng, không phải giao diện sản phẩm. Ảnh coverage lấy từ báo cáo của các lượt chạy đã lưu.

- [Minh chứng dạng text](MinhChung_Tuan_04.md) · [Bản HTML có ảnh](MinhChung_Tuan_04.html).
- Gói nộp gồm báo cáo, minh chứng và bản khai báo sử dụng AI. Nhật ký commit chỉ được xuất từ `git log` thật sau khi các thành viên đã tự commit; không tạo thủ công.
- Các thông tin chưa được cung cấp (mã nhóm, Git username còn thiếu, chat log của model khác chỉnh Java 25) được ghi rõ trong chỉ mục hồ sơ để nhóm bổ sung.
