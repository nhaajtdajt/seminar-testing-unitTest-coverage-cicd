# Seminar: Unit Test · Code Coverage · CI/CD

Case study quản lý thư viện (nghiệp vụ cho mượn sách) dùng chung cho cả ba phần: unit test, code coverage và pipeline CI.

Nhánh `master` chỉ chứa **mã nguồn, test, cấu hình build/CI và công cụ chạy**. Tài liệu nằm ở các nhánh riêng:

| Nhánh | Nội dung |
|---|---|
| [`reportweek04`](../../tree/reportweek04) | Báo cáo, slide, bằng chứng chạy và công cụ dựng tài liệu của Tuần thực hành 04 |
| [`noplan01`](../../tree/noplan01) | Gói đề xuất nộp lần 1 (`nop-lan-1/`), đặc tả thiết kế gốc, kế hoạch và đề bài (`require.md`) |

## Yêu cầu

- JDK 25 và Python 3.10+ (cho các script).
- Không cần cài Maven: `case-study/mvnw` tự tải Maven 3.9.16.
- Công nghệ: Java 25, Spring Boot 4.1.1, JUnit Jupiter 6.0.3, Mockito 5.23.0, AssertJ 3.27.7, H2 2.4.240, JaCoCo 0.8.15, PIT 1.30.0.

## Build và test

```bash
case-study/mvnw -B -ntp -f case-study/pom.xml clean verify
```

Lệnh trên chạy bộ test chuẩn (33 lượt) và coverage gate (branch ≥ 90% cho `FineCalculator`).

| Profile | Dùng để |
|---|---|
| `-Pbaseline` | Chỉ một test, dùng cho demo độ phủ trước khi bổ sung test |
| `-Pbaseline -Dcoverage.gate.skip=false` | Chứng minh gate chặn build khi thiếu test (kỳ vọng exit 1) |
| `-Pcoverage-trap` | Test phủ đủ nhánh nhưng không kiểm giá trị |
| `-Pai-draft`, `-Pai-improved`, `-Pai-data` | Các bộ test do AI sinh |

Mutation testing: `case-study/mvnw -f case-study/pom.xml test-compile org.pitest:pitest-maven:mutationCoverage`.

## Chạy ứng dụng

```bash
java -jar case-study/target/library-case-study-0.1.0.jar --server.port=8081
curl -i http://localhost:8081/api/loans -H 'Content-Type: application/json' -d '{"bookId":1,"memberId":1}'
```

Lần đầu trả 201, mượn lại sách 1 trả 409. Dữ liệu nằm trong H2 in-memory (dữ liệu mẫu trong `data.sql`) nên mất khi tắt ứng dụng.

## CI

- `.github/workflows/ci.yml`: `test` (JDK 25) → `coverage-gate` → `package`.
- `.github/workflows/ai-review.yml`: nhận xét test trên PR, chỉ gọi API khi cấu hình `GEMINI_API_KEY` và `AI_MODEL`.
- `Jenkinsfile`: cùng ba bước, chỉ để so sánh cú pháp.

Hiện hai workflow chỉ chạy tay (`workflow_dispatch`); bỏ dấu `#` ở trigger `push`/`pull_request` để bật tự động.

## Script

`scripts/` gồm công cụ ghi lại lượt chạy (`record_run.py`), TDD replay, HTTP smoke test, benchmark Maven, trích khoảng trống coverage cho AI và test của các công cụ đó (`python3 -m unittest discover -s scripts/tests`).
