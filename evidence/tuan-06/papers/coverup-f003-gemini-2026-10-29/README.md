# CoverUp + Gemini — benchmark f003 (29/10/2026)

## 1. Phạm vi và người thực hiện

**Ngô Gia An (23120205)** tự chạy generation và đo trước/sau trong Terminal.
Codex hướng dẫn, thu kết quả, đọc test và chạy một lượt xác minh offline riêng để lưu
JUnit XML. Lượt xác minh không gọi model, không sinh thêm test. Evidence này chỉ lưu
lượt generation thành công.

Target là `below_zero(operations)` của module `f003` trong benchmark MT của tác giả,
không phải source nhóm. Hàm trả `True` nếu tổng tích lũy từng xuống dưới 0.

## 2. Source và cấu hình

- Artifact: [coverup-eval](https://github.com/plasma-umass/coverup-eval), revision
  `f3173196b90181974b0b684600ffde42ac36672c`.
- Source: `MuTAP-benchmarks/f003/f003/__init__.py`; bản trong `inputs/f003/`
  có SHA-256 khớp nguyên bản tác giả, không sửa thuật toán.
- CoverUp 0.6.0, Python 3.12.14, LiteLLM 1.106.5, SlipCover 1.1.0, pytest 8.3.5.
  Phiên bản đầy đủ và dependency snapshot: [environment/](environment/).
- Model: `gemini/gemini-3.6-flash`, prompt mặc định `gpt-v2` của CoverUp.
- Một smoke test ban đầu do Codex cung cấp, Gia An tạo/chạy: `below_zero([]) is False`.
- `max-attempts=1`, `max-concurrency=1`, `max-backoff=4`, `repeat-tests=1`;
  tiến trình gọi tool được giới hạn ngoài 120 giây và đã hoàn thành trước hạn.
- Thời gian generation theo log: 19:39:47–19:39:57 ngày 29/10/2026, múi giờ Việt Nam.

## 3. Kết quả đo

| Chỉ số | Baseline | Sau generation | Tham chiếu tác giả, đúng f003 |
|---|---:|---:|---:|
| Line | 5/8 (62,5%) | 8/8 (100%) | 8/8 (100%) |
| Branch | 1/4 (25%) | 4/4 (100%) | 4/4 (100%) |
| Line + branch kết hợp | 50% | 100% | 100% |

`G=1, F=0, U=0, R=0`: một đề xuất được chấp nhận, tạo một file chứa **hai hàm test**.
Hai hàm mới có sáu assertion, kiểm các trường hợp số dư xuống âm và luôn không âm;
một assertion danh sách rỗng trùng baseline. Lượt xác minh offline chạy cả ba hàm test:
**3 passed, 0 failure, 0 error, 0 skipped**, exit code 0.

`after.json` do Gia An đo, `checkpoint.json.final_coverage` của tool và coverage của
lượt xác minh offline cùng đạt 8/8 dòng, 4/4 nhánh. [comparison.json](comparison.json)
đối chiếu ba nguồn này với dữ liệu tác giả.

Log có hai response model; không dùng số này như số HTTP request tổng hoặc hóa đơn.
CoverUp/LiteLLM ước tính chi phí khoảng **0,005815 USD** (terminal làm tròn khoảng
0,01 USD), không phải số tiền thanh toán được nhà cung cấp xác nhận.

## 4. File minh chứng

| File | Nội dung |
|---|---|
| [run.json](run.json) | Người thực hiện, thời gian, lệnh generation, model, tham số, phạm vi và giới hạn |
| [output.log](output.log) | Log thành công của CoverUp, gồm prompt, response và thông báo lưu test; đã loại đường dẫn cá nhân/key nếu có |
| [api-summary.json](api-summary.json) | Metadata/usage trích từ response, không có key |
| [before.json](before.json), [after.json](after.json), [checkpoint.json](checkpoint.json) | Số đo gốc của lượt người dùng và tool |
| [test_baseline.py](inputs/tests/test_baseline.py), [test_coverup_1.py](inputs/tests/test_coverup_1.py) | Test ban đầu và test Gemini sinh được CoverUp chấp nhận |
| [reference/author-f003.json](reference/author-f003.json) | Coverage f003 công bố tại revision đã pin; chỉ dùng làm tham chiếu |
| [verification/](verification/) | Lượt Codex chạy lại offline: lệnh/exit code, pytest log, JUnit XML và SlipCover JSON |
| [provenance.json](provenance.json), [manifest.json](manifest.json) | Hash đầu vào trước/sau loại thông tin cá nhân và hash gói evidence |

Không có exit status generation được capture trong file gốc, nên `run.json.exit_code`
để `null`, không tự điền 0. Kết quả hoàn thành dựa trên response, test được lưu và
checkpoint; exit code 0 của lượt xác minh offline được capture riêng.

## 5. Giới hạn kết luận

- Đây là **một module benchmark được chạy với Gemini**, chưa tái lập toàn bộ 163 module.
- Model khác cấu hình GPT-4o công bố; baseline bổ sung, tool/dependencies và ngân sách
  vòng lặp cũng khác thí nghiệm gốc. Reference dùng SlipCover 1.0.15, lượt này 1.1.0.
- Không chạy lại bộ test tác giả: cột tham chiếu là số đo tác giả đã công bố.
- Bằng coverage của một module không chứng minh bằng chất lượng test hoặc đúng mọi
  hành vi. Codex đã đọc assertion; chưa thay cho xác nhận review độc lập của người.
- Chưa phải lượt áp dụng tool lên `scripts/coverage_gaps.py` của nhóm.

## 6. Xác minh lại không gọi API

Trong thư mục evidence này, với môi trường CoverUp còn tồn tại:

```bash
GA_CHECK="$(mktemp -d /tmp/ga-f003-recheck.XXXXXX)"
cp -R inputs/f003 inputs/tests "$GA_CHECK/"
cd "$GA_CHECK"
/tmp/seminar-coverup-venv/bin/python -m slipcover \
  --branch --source f003 --json --out coverage.json \
  -m pytest -q --junitxml junit.xml
```

Expected: 3 test pass, 8/8 dòng và 4/4 nhánh. Source và điều kiện generation được giữ
trong gói này; generation mới cần key riêng, dùng quota và không bảo đảm output giống byte.
