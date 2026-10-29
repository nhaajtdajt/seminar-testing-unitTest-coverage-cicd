# Điểm yếu và hạn chế của CI quan sát được trên GitHub Actions

Tất cả số liệu lấy từ các lần chạy thật của workflow `Seminar CI` ngày 28–29/10/2026 (API `actions/runs/<id>/jobs`, log từng job). Số giây là thời gian của **bước Maven** do runner `ubuntu-latest` đo, mỗi tình huống chỉ **một lượt**, nên chỉ dùng để quan sát, không phải benchmark.

| Run | Tình huống | `test`: `clean test` | `coverage-gate`: `clean verify` |
|---|---|---|---|
| [40722865221](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40722865221) | PR #1, lần đầu (chưa có cache) | 40 s | 26 s |
| [40723239123](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40723239123) | PR #2 đỏ (xóa test) | 70 s | 27 s (fail) |
| [40723623913](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40723623913) | PR #2 xanh lại | 29 s | 24 s |
| [40725917834](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40725917834) | PR #6 đỏ vào master | 29 s | 47 s (fail) |
| [40810447672](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40810447672) | PR #9, sửa `pom.xml` (cache miss) | 35 s | 26 s |

## 1. Cache Maven bị vô hiệu khi `pom.xml` đổi (CI-2)
- `setup-java` đặt khóa cache bằng hash của `case-study/pom.xml` (`cache-dependency-path`).
- PR #9 chỉ thêm **một dòng comment** vào `pom.xml`. Log job `test` ghi `maven cache is not found`, rồi lưu cache mới với khóa `setup-java-Linux-x64-maven-5d775ae4...` (khác khóa cũ `cf9a78f3...`). Hai job sau (`coverage-gate`, `package`) restore được cache mới.
- Ảnh hưởng đo được rất nhỏ: bước Maven của `test` 35 s so với 29 s khi cache khớp. Dependency của dự án chỉ khoảng 59 MB và runner có mạng nhanh. **Chênh lệch này nhỏ hơn dao động giữa các lượt** (cùng code, cùng cache khớp nhưng 29 s và 70 s ở hai run khác nhau), nên không kết luận được mức tăng tốc từ cache trên dự án này.
- Bài học: khóa cache gắn với một file nên thay đổi nhỏ cũng làm miss; dự án lớn hơn (nhiều dependency) mới thấy rõ chi phí.

## 2. `coverage-gate` chạy lại toàn bộ test
- `test` chạy `clean test`, `coverage-gate` chạy `clean verify` (test + JaCoCo + gate), nên bộ test chạy **hai lần** mỗi pipeline.
- Hệ quả: tốn thời gian runner. Đổi lại, hai job tách bạch "test fail" khỏi "thiếu coverage" và PR đỏ cho thấy ngay lỗi nằm ở bước nào.
- Phương án nếu cần nhanh: gộp thành một job `verify` hoặc dùng cache build/artifact.

## 3. Thời gian runner dao động lớn
- Cùng một bước `clean test` có các lượt 29 s, 29 s, 35 s, 40 s và 70 s. Nguyên nhân (runner bị chia sẻ, mạng, khởi động JVM) không được xác định.
- Vì vậy nhóm không dùng thời gian CI làm bằng chứng về tốc độ; muốn so sánh phải đo nhiều lượt và lấy trung vị (như `benchmark-jacoco` ở máy).

## 4. Required check có thể làm PR bị kẹt (CI-3)
- Khi chủ repo bật required status checks cho `master`, workflow trên `master` vẫn tắt trigger `pull_request`, nên PR vào `master` **không có check nào chạy** và không thể merge.
- Chỉ sửa được bằng một PR đưa trigger vào `master` ([PR #4](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/4)). Thứ tự đúng: bật trigger trước, bật quy tắc bảo vệ sau.

## 5. Bảo vệ nhánh chỉ có hiệu lực ở nhánh được cấu hình
- PR đỏ #6 vào `master` bị `BLOCKED`; PR đỏ #5 vào `seminar-core` ở trạng thái `UNSTABLE` và vẫn merge được vì nhánh này chưa có quy tắc.

## 6. Coverage gate chỉ kiểm cái được cấu hình
- Gate kiểm branch coverage của một lớp (`FineCalculator`) ≥ 90%. Test bẫy 100% branch vẫn pass gate mà không kiểm số tiền (xem báo cáo mục 3.4). PIT chưa đưa vào CI vì chậm.

## Chưa làm
- **Lộ secret trong log** và **flaky test**: chưa dựng demo nên không kết luận. Nếu làm, dùng giá trị giả, không dùng API key thật.
