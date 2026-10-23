# Minh chứng Tuần 06

Các minh chứng mới của Tuần 06 được tách riêng khỏi `evidence/tuan-05/`, vốn giữ các lượt chạy tích lũy/kỳ trước.

## Source và kiểm thử

- [Lượt `clean verify` thành công](source-verify/run.json): JDK 25.0.2, 33/33 test, 0 failure/error/skipped. Bắt đầu 2026-10-23 10:01:33 UTC (17:01:33 +07).
- [Log](source-verify/output.log) và [Surefire reports](source-verify/surefire-reports/).
- [JaCoCo HTML](source-verify/site/jacoco/index.html), [XML](source-verify/site/jacoco/jacoco.xml): instruction 429/455 (94%), branch 18/18 (100%), line 69/76 (90,8%).
- [HTTP smoke trên JAR Java 25](http-smoke-java25/results.json): 5/5 tình huống đạt status mong đợi.

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
