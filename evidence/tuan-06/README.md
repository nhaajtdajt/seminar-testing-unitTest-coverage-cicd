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

## Phần chưa có minh chứng trong tuần

- Video/kịch bản/ảnh demo hiện nằm ngoài checklist nộp tuần 6 theo chỉ đạo mới nhất; không tính là mục thiếu. Ảnh JaCoCo và app/API vẫn được giữ tùy chọn.
- Run GitHub Actions/Jenkins không thuộc checklist tuần 6; đó là trạng thái scope toàn dự án. Gemini API thật đã chạy và đối chiếu fixture đạt 4/4; kết quả lưu trong `ai-review/`.
