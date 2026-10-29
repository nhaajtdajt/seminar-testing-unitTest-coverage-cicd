# CoverUp + Gemini — f003 (29/10/2026)

## 1. Phạm vi

Ngô Gia An (23120205) tự chạy tool và đo trước/sau; Codex thu kết quả và xác minh offline.
Một module f003 của benchmark tác giả; không sửa source nhóm.

## 2. Cấu hình

CoverUp 0.6.0, Gemini 3.6 Flash; max-attempts=1, max-concurrency=1, repeat-tests=1.
Artifact coverup-eval revision f3173196b90181974b0b684600ffde42ac36672c.
Model, lệnh, hash source, phiên bản và chi phí ước tính nằm trong [run.json](run.json).

## 3. Kết quả

| Chỉ số | Trước | Sau | Tác giả, cùng f003 |
|---|---:|---:|---:|
| Line | 5/8 | 8/8 | 8/8 |
| Branch | 1/4 | 4/4 | 4/4 |
| Kết hợp | 50% | 100% | 100% |

Sinh hai hàm test; cả bộ 3 test pass, không failure/error/skipped. G=1, F=0, U=0, R=0.

## 4. Output giữ lại

[Test sinh ra](generated/test_coverup_1.py), [log xác minh](output.log), [JUnit](junit.xml),
[before](before.json), [after](after.json), [đối chiếu](comparison.json), [metadata](run.json).
Đã bỏ full prompt/response, source copy, dependency dump và báo cáo trùng; không lưu log lỗi.

## 5. Giới hạn

Đổi model, baseline, dependencies và ngân sách so với thực nghiệm gốc; chỉ một module.
Coverage bằng nhau không chứng minh chất lượng test bằng nhau hoặc tái lập cả benchmark.

## 6. Tái hiện

Lấy đúng source tại artifact revision nêu trên, chạy CoverUp với baseline danh sách rỗng,
rồi đo pytest/SlipCover như [research/README.md](../../../../research/README.md).
Generation mới dùng quota và có thể tạo output khác. Số đo ở đây là kết quả đã chạy.
