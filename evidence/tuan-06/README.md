# Minh chứng Tuần 06

Các minh chứng mới của Tuần 06 được tách riêng khỏi `evidence/tuan-05/`, vốn giữ các lượt chạy tích lũy/kỳ trước.

## Source và kiểm thử

- [Lượt `clean verify` thành công](source-verify/run.json): JDK 25.0.2, 33/33 test, 0 failure/error/skipped. Bắt đầu 2026-10-23 10:01:33 UTC (17:01:33 +07).
- [Log](source-verify/output.log). Surefire reports đã bỏ khỏi nhánh gọn (còn ở `reportweek04`).
- [JaCoCo HTML](source-verify/site/jacoco/index.html), [XML](source-verify/site/jacoco/jacoco.xml): instruction 429/455 (94%), branch 18/18 (100%), line 69/76 (90,8%).
- [HTTP smoke trên JAR Java 25](http-smoke-java25/results.json): 5/5 tình huống đạt status mong đợi.

## Code Coverage (Trương Nhật Đạt)

- [coverage-types/](coverage-types/): JaCoCo trên `LoanPeriodPolicy`, chạy cộng dồn T1 → T4 (`s1`–`s4`) và bộ phản chứng T2 + T3 (`alt-t2-t3`). Nhánh: 3/6, 5/6, 6/6, 6/6; bộ phản chứng 5/6 nhánh, 6/7 dòng. Mỗi lượt có `run.json`, `output.log` (đã thay đường dẫn máy bằng `<repo>`/`<home>`), `jacoco.csv`/`jacoco.xml`.
- [openclover/](openclover/): OpenClover 4.5.2 chạy trên bản sao `case-study/` (không sửa `pom.xml`, gọi plugin bằng tọa độ đầy đủ). `s1`, `s2`, `s3`, `alt-t2-t3` cùng bộ test với JaCoCo: `LoanPeriodPolicy` đạt 2/4, 4/4, 4/4, 3/4 conditional; `full` là cả bộ 39 test. `time-jacoco-*` / `time-clover-*`: 3 lượt mỗi công cụ, trung vị 46,570 s (JaCoCo `clean verify`) và 43,446 s (OpenClover, tắt JaCoCo). `clover.xml` đã bỏ thuộc tính đường dẫn tệp.
- [coverage-blindspot/](coverage-blindspot/): `FineCalculatorNoCapTest` (assert đủ số tiền, không ca nào chạm trần 50.000 VND). `nocap-jacoco`: 10/10 nhánh, gate 90% pass. `nocap-pit-default`: PIT 10/11 (91%), bằng bộ đầy đủ. `nocap-pit-consts` (`-Dmutators=DEFAULTS,INLINE_CONSTS`): 13/16, mutant `50000 → 50001` sống. `strong-pit-consts`: bộ đầy đủ 15/16, chỉ còn mutant tương đương ở dòng 15.
- [pit-cost/](pit-cost/): chi phí PIT. Một lớp (`FineCalculator`): `test-1..3` chạy `FineCalculatorTest` (trung vị 16,1 s cả Maven, test 0,6 s), `pit-1..3` (trung vị 18,9 s cả Maven, PIT tự báo 4 s, 11 mutant). Toàn project: `test-all` 39 test trong 22,3 s; `all` PIT 84,9 s cả Maven (PIT 75 s: coverage 10 s, mutation 65 s), 46 mutant, diệt 40, 4 không được phủ, 2 sống. Mỗi cấu hình toàn project chỉ chạy 1 lượt.

## Ảnh JaCoCo do người dùng cung cấp

- Tệp: [jacoco-summary-2026-10-23.png](screenshots/jacoco-summary-2026-10-23.png). Timestamp sửa tệp nhận được: 2026-10-23 17:32:21 +07; SHA-256: `746c16203f5801ffaf8fd581c31359f67cfd45107a78492405d382fba95a7a51`.
- Số liệu trong ảnh khớp với XML/HTML của lượt verify thành công lúc 17:01:33 +07.
- Các số liệu trong ảnh khớp với HTML/XML của lượt verify thành công gần nhất đã lưu trong thư mục `source-verify/`.

## Ảnh HTTP API do người dùng cung cấp

- Tệp: [api-http-201-409-2026-10-23.png](screenshots/api-http-201-409-2026-10-23.png). Ảnh cho thấy request `POST /api/loans` gửi trực tiếp tới app local: lần đầu trả `201`, gửi lại cùng sách trả `409` với `BOOK_UNAVAILABLE`.
- Thời gian response trong ảnh: 2026-10-23 11:16:48 GMT (18:16:48 +07). SHA-256: `5f571e4a4a7e955c11ba12f2a0cfa3d16c38af6bdf8d9760e9966be020f497a6`.

## AI-3 Gemini API

- Gọi API thật bằng `gemini-3.6-flash`; request đầu nhận HTTP 503 và retry thành công.
- Kết quả có 4 findings trên `ai/fixtures/review.diff`. Codex đã đối chiếu từng finding với diff và source liên quan; cả 4 đều phù hợp với fixture. Đây là fixture mẫu, không khẳng định toàn bộ repository có các lỗi đó hay thay cho review độc lập của nhóm.
- [Metadata](ai-review/metadata.json), [prompt](ai-review/prompt.md), [review JSON](ai-review/review.json). API key không được lưu.
- [Đối chiếu fixture](ai-review/evaluation.json): 4 true positives, 0 false positives, 0 false negatives. Kết quả này chỉ đo độ khớp với fixture seed, không phải benchmark độc lập.

## Source verify ngày 28/10 và sau tích hợp core

- [Snapshot 28/10](source-verify-2026-10-28/run.json): 39 test chuẩn, không failure/error/skipped, gate pass; JDK 25.0.5. Lượt 33 test ở `source-verify/` phía trên là snapshot 23/10, giữ nguyên.
- [Lượt sau tích hợp core và chuẩn hóa 29/10](source-verify-2026-10-29/run.json): 39/39 test pass, 0 failure/error/skipped, coverage gate pass; log và `site/jacoco/jacoco.xml` nằm cùng lượt. Không ghi đè snapshot trước.

## AI-4 — Đối chứng dữ liệu biên (Ngô Gia An)

[Chỉ mục, nguồn và kết quả](ai-4/README.md): Gia An cung cấp 23 ca + notes; Codex khóa ở commit `0e58f5f` trước so sánh và chạy Java. Bộ người dùng 23/23 pass, FineCalculator branch 10/10; CSV AI 13/13 pass, branch 8/10. Có 11 đầu vào chung, cả 11 khớp kỳ vọng. Độc lập dựa trên tuyên bố trong notes, không do hash tự chứng minh.

- `ai-4/human/`, `ai-4/ai/`: `run.json`, `output.log`, `site/jacoco/jacoco.xml` của mỗi lượt.
- [comparison.json](ai-4/comparison.json): số ca trùng/thiếu/thêm và kỳ vọng khác nhau.
- `ai-4/tooling/`: snapshot synthetic kiểm công cụ trước khi nhận dữ liệu thật; không dùng làm bộ người viết.

## AI-5 — Tái sử dụng trên LoanService (Ngô Gia An)

[Chỉ mục và lệnh](ai-loan/README.md): nháp 2 test, branch 3/6 → bổ sung 10 test, branch 6/6; fixture sai fail đúng một assertion; PIT 9/9 KILLED. Lượt lỗi quyền và HTTP 502 giữ riêng. Đây là demo Codex tương tác, không phải output Gemini/paper; chưa có xác nhận người tự review/chạy lại.

## Paper — Artifact tác giả (Ngô Gia An điều phối)

[Chỉ mục kết quả và giới hạn](papers/README.md): CoverUp replay phân tích MT 163 module (overall line+branch 89,0% vs 76,8%), dry-run source Python nhóm; ChatUniTest plugin parse 20 class/28 method. [Lượt Gia An tự chạy CoverUp + Gemini trên benchmark f003](papers/coverup-f003-gemini-2026-10-29/README.md): sinh hai hàm test, xác minh offline cả bộ 3/3 pass; line 5/8 → 8/8, branch 1/4 → 4/4, khớp số đo tác giả của đúng module. Khác model/baseline/môi trường; chưa tái lập đầy đủ benchmark hoặc generation trên source nhóm. Source/revision/cách chạy: `research/`.

## Quy ước lưu minh chứng

- Cùng cấu trúc theo tuần/chủ đề với Coverage/CI: `evidence/tuan-06/<chu-de>/<luot>/`.
- Lượt local có `run.json` và `output.log`; báo cáo Java ở `site/jacoco/` hoặc `pit-reports/`. Phân tích không chạy Maven có JSON kết quả riêng; GitHub evidence giữ link run/PR.
- Ngày 29/10 chỉ chuyển vị trí 46 tệp evidence từ `evidence/gia-an/`; nội dung gốc không đổi. Đường dẫn cũ nằm bên trong metadata/log phản ánh thời điểm chạy, không sửa lại lịch sử hoặc số liệu. Markdown và lệnh tái hiện dùng đường dẫn mới.
- Dataset đã khóa `ai/human/frozen/`, CSV/notes gốc và receipt giữ nguyên. Chuyển nơi lưu không phải chạy lại thí nghiệm.

## Phần còn chờ

- Gia An tự đọc, chạy lại và xác nhận khai báo AI; reviewer chéo chưa xác nhận.
- Paper đã có generation thật trên một module CoverUp (f003); còn mở rộng benchmark, thử trên source nhóm và generation/tái lập ChatUniTest.
- Video là yêu cầu seminar, chưa có file video/URL/timestamp thật; script/ảnh không thay cho video.
- Phần slide/HTML Gia An hoãn đến cuối theo yêu cầu ngày 29/10, dùng nguyên nguồn core. Chưa xuất lại PDF riêng.
- CI GitHub và required checks có evidence ở `github-actions/`; trạng thái quyền/nhánh là snapshot, không tự suy ra cấu hình live hôm nay. Nhóm đã bỏ Jenkins.
