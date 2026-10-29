# CoverUp + Gemini — source nhóm (29/10/2026)

## 1. Phạm vi

Codex chạy theo ủy quyền Ngô Gia An (23120205), trên bản sao nguyên vẹn `scripts/coverage_gaps.py`.
Không sửa source hoặc test chuẩn của nhóm.

## 2. Cấu hình

CoverUp 0.6.0 + Gemini 3.6 Flash; một smoke test XML rỗng, tối đa hai vòng mỗi segment,
một segment đồng thời, repeat-tests=1. Lệnh, source hash và phiên bản tại [run.json](run.json).

## 3. Kết quả

| Chỉ số | Baseline | Sau |
|---|---:|---:|
| Tests | 1 | 7 |
| Line | 11/39 | 38/39 |
| Branch | 2/16 | 15/16 |
| Line + branch | 23,6% | 96,4% |

Hai file mới chứa sáu hàm test; 7 pass, không fail/error/skip. G=2, F=0, U=0, R=2.
Test kiểm XML missed lines/branches, source lookup và CLI stdout/output file.

## 4. Output giữ lại

`generated/` có test sinh ra; `before.json`, `after.json`, `junit.xml`, `output.log`
và `run.json` là các output cần đối chiếu. Không lưu full prompt/model response hoặc bản sao project.

## 5. Giới hạn

Còn thiếu dòng 44 và nhánh 43→44 (entrypoint `__main__`); không hạ gate để đạt 100%.
Tool được thử trên script Python của nhóm, không nhận là sinh JUnit cho ứng dụng Java.
Assertion dựa trên implementation cần người review; số tiền tool ước tính không phải hóa đơn.

## 6. Tái hiện

Theo [research/README.md](../../../../research/README.md). Không cần copy test vào source chính;
đây là thực nghiệm paper, không thay suite đã commit của nhóm.
