# Minh chứng CI/CD trên GitHub Actions (28/10/2026)

Workflow `Seminar CI` (`.github/workflows/ci.yml`) đã chạy thật trên GitHub, JDK 25, runner `ubuntu-latest`. Ba job nối nhau bằng `needs`: `test` → `coverage-gate` → `package`.

| # | Tình huống | PR / commit | Kết quả | Link run |
|---|---|---|---|---|
| 1 | Bật CI tự động | [PR #1](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/1), `160fd6b` | `test` ✅ · `coverage-gate` ✅ · `package` ✅ | [run 40722865221](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40722865221) |
| 2 | **PR đỏ**: xóa `FineCalculatorTest` | [PR #2](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/2), `ab1d81d` | `test` ✅ · `coverage-gate` ❌ · `package` ⏭ bỏ qua | [run 40723239123](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40723239123) |
| 3 | **PR xanh**: khôi phục test | PR #2, `6f06691` | cả 3 job ✅ | [run 40723623913](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40723623913) |
| 4 | **PR đỏ vào `master` bị chặn** | [PR #6](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/6) | `test` ✅ · `coverage-gate` ❌ · `package` ⏭; trạng thái merge **BLOCKED**, lệnh `gh pr merge` bị từ chối | [run 40725917834](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/actions/runs/40725917834) |

## Điều run #2 chứng minh
- Test vẫn pass (21 test còn lại), nhưng gate chặn: `Rule violated for class vn.edu.seminar.fine.FineCalculator: branches covered ratio is 0.00, but expected minimum is 0.90` rồi `BUILD FAILURE`.
- `package` **không chạy** vì `needs: coverage-gate`: code thiếu test không được đóng gói.
- PR #2 chỉ để minh họa, đã đóng, **không merge**.

## Artifact của run xanh (#3)
`tests-jdk-25` (Surefire, ~27 KB), `coverage` (JaCoCo HTML, ~246 KB), `library-app` (JAR, ~48 MB).

## Giới hạn, ghi trung thực
- **Required status checks đã bật cho `master`** (chủ repo bật; ba check `test (JDK 25)`, `coverage-gate`, `package`). PR #6 đỏ vào `master` có trạng thái `BLOCKED` và `gh pr merge` bị từ chối (không dùng `--admin`). **`seminar-core` chưa bật** (PR đỏ #5 vào đó ở trạng thái `UNSTABLE`, vẫn merge được).
- Trên `master` ban đầu workflow tắt trigger nên PR vào master bị kẹt (không check nào chạy); [PR #4](https://github.com/nhaajtdajt/seminar-testing-unitTest-coverage-cicd/pull/4) đưa trigger sang master.
- Thời gian job (~1,5 phút `test`, ~35 giây `coverage-gate`) là số của runner GitHub tại thời điểm chạy, không so sánh được với số đo ở máy.
- `ai-review.yml` vẫn chỉ chạy tay (cần `GEMINI_API_KEY` dạng secret).
- Không dùng Jenkins; CI/CD chỉ dùng GitHub Actions.
