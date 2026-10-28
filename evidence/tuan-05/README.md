# Minh chứng thực hành — bản Java 25

Bản cập nhật dùng Java 25, Spring Boot 4.1.1, Maven Wrapper 3.9.16 và H2 in-memory qua Spring Data JPA. Các file `run.json` ghi lệnh, thời điểm UTC, thời gian chạy và mã thoát; `output.log` giữ đầu ra thực tế. Môi trường được ghi trong Surefire XML và `maven-version.txt`.

| Minh chứng | Nội dung |
|---|---|
| [final](final/run.json) | 33 lượt test pass trên Java 25; FineCalculator đạt 100% branch, gate pass. |
| [baseline](baseline/run.json) | Bộ 1 test, FineCalculator phủ 50% branch; tắt gate để thu báo cáo ban đầu. |
| [gate-fail](gate-fail/run.json) | Bật gate 90% cho bộ thiếu test; Maven exit 1. |
| [coverage-trap](coverage-trap/run.json) | Test bẫy phủ đủ nhánh nhưng không assert tiền của ca hợp lệ. |
| [pit-weak](pit-weak/pit-reports/index.html) | Bộ test yếu: 3/11 mutant bị diệt. |
| [pit-strong](pit-strong/pit-reports/index.html) | Bộ đầy đủ: 10/11 mutant bị diệt. |
| [tdd-replay](tdd-replay/summary.json) | Bốn vòng đỏ–xanh trong bản sao riêng, có source/test/log. |
| [ai-draft-recheck](ai-draft-recheck/run.json) | 3 test AI ban đầu, phủ 70% branch. |
| [ai-improved](ai-improved/run.json) | 6 test sau khi bổ sung theo gap, phủ 100% branch. |
| [ai-data](ai-data/run.json) | 13 ca CSV AI chạy pass. |
| [http-smoke](http-smoke/results.json) | 5 tình huống HTTP trên ứng dụng đóng gói. |
| [workflow-lint](workflow-lint/run.json) | Kiểm tra tĩnh workflow; chưa phải lần chạy GitHub Actions. |
| [benchmark-jacoco](benchmark-jacoco/summary.json) | 3 lượt/cấu hình: trung vị không JaCoCo 9,727s; có JaCoCo 12,754s. |
| [benchmark-cache](benchmark-cache/summary.json) | Đủ **3/3 cặp** kho Maven lạnh/ấm, trung vị 48,412s / 12,539s (`complete: true`). |
| [ai-review-prepared](ai-review-prepared/metadata.json) | Chuẩn bị prompt, `api_called=false`. |

Phép đo cache của bản Java 25 đã đủ 3/3 cặp hợp lệ. Cặp 3 chạy bổ sung lúc 15:00–15:08 UTC ngày 16/10/2026, mất 479,523 giây lạnh và 11,940 giây ấm; hai lượt đều pass 33 test, coverage gate và BUILD SUCCESS. Cặp này dùng IPv4, connect timeout 15 giây, request timeout 120 giây và giới hạn 1.800 giây/lệnh. Hai cặp trước và log được giữ nguyên; [resume-provenance.json](benchmark-cache/resume-provenance.json) lưu dữ liệu ban đầu cùng SHA-256. Điều kiện mạng thay đổi giữa các cặp nên cần đọc cả số đo từng lượt. Các lần thử không hoàn tất (Read timed out, tải Hibernate bị ngắt, hết thời hạn) vẫn nằm trong [benchmark-cache/failed-attempts](benchmark-cache/failed-attempts/) và không tính vào trung vị.

`summary.json` tổng hợp từ XML/JSON của các lượt được chọn. `source-sha256.txt` ghi dấu kiểm source tại thời điểm tổng hợp, không xác nhận hash lịch sử của từng lượt chạy.

Các bước cần thực hiện trên dịch vụ: chạy GitHub Actions/PR đỏ–xanh, bật required checks, chạy Jenkins và gọi API AI khi nhóm có cấu hình. Danh tính và phân công đã được điền theo thông tin nhóm cung cấp; nhóm cần xác nhận đóng góp thực tế. Gói Tuần 04 dùng ảnh minh chứng theo yêu cầu của nhóm.

 Bằng chứng chuẩn trong `final/` được giữ; lượt kiểm lặp `java25-review/`, ảnh kiểm bố cục cũ và bằng chứng của cấu hình Java 21/Boot 3.5 đã được dọn khỏi repo. `case-study/target/` sẽ được tạo lại khi chạy Maven; các báo cáo đã lưu ở đây vẫn mở được sau khi dọn.
