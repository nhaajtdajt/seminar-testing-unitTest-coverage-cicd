# Minh chứng paper — output thực nghiệm ngày 29/10/2026

**Phụ trách:** Ngô Gia An (23120205). Gia An tự chạy CoverUp f003; Codex chạy phân tích, xác minh và các lượt bổ sung theo ủy quyền. Nguồn/hạng/phiên bản và lệnh chạy lại: [research](../../../research/README.md), [danh mục](../../../research/papers.json).

## 1. Kết quả cần trình bày

| Lượt | Output thực tế | Minh chứng |
|---|---|---|
| CoverUp: phân tích dữ liệu công bố | 163 module MT; overall line+branch 89,0% vs MuTAP 76,8% | [Metadata](coverup-mt/run.json), [output](coverup-mt/output.log) |
| CoverUp + Gemini 3.6: benchmark f003 | 1 → 3 test pass; line 5/8 → 8/8, branch 1/4 → 4/4, bằng reference đúng module | [Kết quả](coverup-f003-gemini-2026-10-29/README.md), [test sinh](coverup-f003-gemini-2026-10-29/generated/test_coverup_1.py) |
| CoverUp + Gemini 3.6: source nhóm | Thêm 6 hàm; 7 pass; kết hợp 23,6% → 96,4%; line 38/39, branch 15/16 | [Kết quả](coverup-group-gemini-2026-10-29/README.md), [test sinh](coverup-group-gemini-2026-10-29/generated/) |
| Pynguin: notebook dữ liệu công bố | 134 module sau lọc, 40.200 dòng, 30 lượt/config/module; 8 cột thống kê × 10 cấu hình khớp output tác giả; median DynaMOSA-TypeHints 80,72% | [Metadata](pynguin-reanalysis-2026-10-29/run.json), [output](pynguin-reanalysis-2026-10-29/output.log) |
| Pynguin 0.25.2: benchmark codetiming._timers | 600s, seed 23120205; nội bộ 81,48%, bằng median 30 lượt công bố cùng module/config. **10 pass, 5 xfail**; SlipCover target line 42/42, branch 4/4 | [Metadata/đối chiếu](pynguin-benchmark-2026-10-29/run.json), [pytest](pynguin-benchmark-2026-10-29/output.log), [test sinh](pynguin-benchmark-2026-10-29/generated/test_codetiming__timers.py) |
| Pynguin: source nhóm | 0.25.2: 1 xfail, không gọi SUT. 0.48.0 không seed: 1 xfail, 20% kết hợp. Có seed: 2 pass, 23,6%, thiếu assertion và không hơn smoke baseline | [Tổng hợp ba lượt](pynguin-group-2026-10-29/run.json), [test/coverage có seed](pynguin-group-2026-10-29/seeded/) |

## 2. Cách đọc kết quả

- Phân tích dữ liệu công bố khác với chạy mới tool. Mỗi paper đã có cả hai loại kết quả.
- Source nhóm là `scripts/coverage_gaps.py` nguyên vẹn, không phải LoanService hoặc toàn bộ ứng dụng Java.
- Pynguin bytecode coverage, SlipCover source line/branch và JaCoCo Java là các metric khác nhau. 81,48% nội bộ và 100% SlipCover trên cùng benchmark không mâu thuẫn.
- `xfail` là lỗi dự kiến, không tính vào pass. Bản có seed chỉ gọi hàm, chưa có assertion nên chưa đủ làm regression suite.
- Reference `codetiming._timers` lấy từ 30 lượt DynaMOSA-TypeHints công bố trước lọc completeness; module này không nằm trong bảng 134 module đủ mọi cấu hình.

## 3. Phạm vi và lưu trữ

Đã chạy phân tích công bố, một benchmark generation mới và thử source nhóm cho từng paper. Đây là tái hiện có giới hạn; không chạy lại toàn bộ benchmark nhiều seed hoặc mutation RQ3, không khẳng định chất lượng test chỉ từ coverage.

Chỉ giữ test xuất ra, số đo, JUnit/pytest output và metadata cần đối chiếu. Đã bỏ dry-run/log lỗi cũ, full prompt/response, source copy và dependency dump. Source/artifact gốc ở ngoài Git; không thêm test paper vào suite chính của thành viên khác.
