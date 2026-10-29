# Paper: nguồn, kết quả và cách chạy lại

Ngô Gia An (23120205), Codex hỗ trợ thực nghiệm và tổng hợp, cập nhật 29/10/2026.
Danh mục DOI, phiên bản và nguồn kiểm hạng: [papers.json](papers.json).
Output cần trình bày: [chỉ mục evidence](../evidence/tuan-06/papers/README.md).

## 1. Hai bài được chọn

| Bài | Xuất bản / hạng venue đã kiểm | Source tác giả |
|---|---|---|
| CoverUp: Effective High Coverage Test Generation for Python — Pizzorno, Berger | FSE 2025 / PACMSE, [DOI 10.1145/3729398](https://doi.org/10.1145/3729398); FSE A*, CORE2023 | [Tool](https://github.com/plasma-umass/coverup), [artifact](https://github.com/plasma-umass/coverup-eval) |
| An empirical study of automated unit test generation for Python — Lukasczyk, Kroiß, Fraser | Empirical Software Engineering 2023, 28:36, [DOI 10.1007/s10664-022-10248-w](https://doi.org/10.1007/s10664-022-10248-w); A, CORE2020 journal ranking | [Pynguin](https://github.com/se2p/pynguin), [artifact và notebook gốc](https://doi.org/10.5281/zenodo.6838658) |

Hai bài xuất bản trong 2021–2026. Đã kiểm trên [CORE conference portal](https://portal.core.edu.au/conf-ranks/?by=all&search=&source=CORE2023) và [CORE journal portal](https://portal.core.edu.au/jnl-ranks/?search=Empirical+Software+Engineering&by=all&source=CORE2020). Đây là hạng venue; bảng journal dừng cập nhật năm 2020, không nhận là hạng mới năm 2026 của từng paper.

## 2. Phương pháp và kết quả

CoverUp dùng coverage để chọn đoạn source, gọi LLM sinh pytest rồi chạy/đo/sửa theo phản hồi. Lượt mới dùng Gemini **3.6 Flash**, khác GPT-4o của kết quả công bố. Pynguin dùng tìm kiếm tiến hóa DynaMOSA, type hints và thực thi để sinh test; lượt này **không gọi Gemini hoặc LLM**. Dùng trực tiếp tool và mã phân tích của tác giả, không tự implement lại thuật toán.

| Thí nghiệm đã chạy | Kết quả | Giới hạn |
|---|---|---|
| CoverUp: script `compare.py` gốc trên dữ liệu MT | 163 module; overall line+branch 89,0% vs MuTAP 76,8%, khớp abstract đã làm tròn 89% vs 77% | Phân tích dữ liệu công bố |
| CoverUp: Gia An tự sinh test mới trên benchmark f003 | Thêm 2 hàm; cả bộ 3 pass; line 8/8, branch 4/4, bằng reference cùng module | Một module, khác model/baseline/versions/budget |
| CoverUp: sinh trên `scripts/coverage_gaps.py` của nhóm | Thêm 6 hàm, tổng 7 pass; line 11/39 → 38/39, branch 2/16 → 15/16; kết hợp 23,6% → 96,4% | Còn entrypoint `__main__`; source Python, không phải JUnit Java |
| Pynguin: chạy nguyên numeric cells notebook tác giả | 134 module sau lọc, 40.200 dòng dữ liệu, 30 lượt/config/module; cả 8 cột `describe()` của 10 cấu hình khớp output gốc trong 1e-6; DynaMOSA-TypeHints median 80,72% | Không chạy mới 40.200 thí nghiệm |
| Pynguin 0.25.2: benchmark `codetiming._timers`, DYNAMOSA 600s, seed 23120205 | Coverage nội bộ 81,48%, bằng median 30 lượt công bố cùng module/config; pytest **10 pass, 5 xfail**; SlipCover target line 42/42, branch 4/4 | Một seed; metric bytecode khác metric source SlipCover. Reference module lấy trước bộ lọc completeness, không thuộc 134 module so toàn cấu hình |
| Pynguin: source nhóm, 60s/lượt | 0.25.2: 1 xfail, không gọi source. 0.48.0: 1 xfail, kết hợp 20%. 0.48.0 có seed XML: 2 pass nhưng không assertion, kết hợp 23,6%, bằng smoke baseline | Kết quả yếu trên module filesystem/XML này; không kết luận mọi module đều yếu. Bản 0.48.0 là thử thích nghi riêng |

`xfail` là lỗi dự kiến được tool đánh dấu, **không tính là test pass**. Coverage nội bộ Pynguin tính cả nhánh bytecode, không đối chiếu trực tiếp 81,48% với 100% SlipCover hoặc JaCoCo. Cả hai tool được thử trên script Python thật của nhóm; không dịch LoanService sang Python. Các lượt mới trên source nhóm và Pynguin do Codex chạy theo ủy quyền Gia An; f003 do Gia An tự chạy.

## 3. Chạy lại phân tích dữ liệu công bố

Đặt artifact/venv ngoài repo. Không commit bản sao benchmark, dependency dump, API key hoặc full model log.

### CoverUp

```bash
git clone https://github.com/plasma-umass/coverup-eval.git /tmp/coverup-eval
git -C /tmp/coverup-eval checkout f3173196b90181974b0b684600ffde42ac36672c
python3 -m venv /tmp/paper-analysis
/tmp/paper-analysis/bin/pip install -r research/requirements-analysis.lock.txt
python3 scripts/paper_experiments.py coverup-reanalyse /tmp/coverup-eval \
  --python /tmp/paper-analysis/bin/python --output /tmp/paper-reanalysis
```

Expected: script gốc phân tích 163 module, 89,0% vs 76,8%. Output phải là thư mục mới.

### Pynguin

Tải [artifact Zenodo](https://zenodo.org/records/6838658), giải nén `emse2022-experiments/` vào `/tmp/pynguin-artifact/`. ZIP khoảng 1,4 GB; chỉ cần `data/{results.csv.xz,results-assertions.csv.xz,loc_data.csv,types.csv,types_per_project.csv}`, `notebooks/project-analysis.ipynb` và project `projects/codetiming/`. Phiên này dùng HTTP range để lấy riêng các thành phần đó, không đưa vào Git.

```bash
/tmp/paper-analysis/bin/pip install -r research/pynguin/requirements-analysis.txt
/tmp/paper-analysis/bin/python research/pynguin/reanalyse.py \
  /tmp/pynguin-artifact/emse2022-experiments > /tmp/pynguin-analysis.json
```

Expected: `matches_author_stored_describe_output: true`, `retained_modules: 134`, `retained_rows: 40200`. Wrapper thực thi nguyên cell số học của notebook; chỉ thêm serialize/check output. Chạy notebook từ artifact có hash trong evidence; các cell plot/TeX và mutation RQ3 không chạy ở đây.

## 4. Chạy mới tool tác giả

### CoverUp + Gemini

[Bài thực hành từng bước](../docs/thuc-hanh/ThucHanh_App_Paper.md) có baseline XML, đọc key từ `.env.gemini`, lệnh sinh test và đo trước/sau. Python 3.12, CoverUp 0.6.0; cài `research/requirements-coverup.lock.txt`. Lượt mới dùng quota và không bảo đảm số test/coverage giống output đã lưu.

### Pynguin gốc trên benchmark

Pynguin **0.25.2 cần Python 3.10**; pin `bytecode==0.13.0` để tương thích instrumentation của phiên bản này.

```bash
python3.10 -m venv /tmp/pynguin025
/tmp/pynguin025/bin/pip install -r research/pynguin/requirements-original.txt
GA_PY_PROJECT=/tmp/pynguin-artifact/emse2022-experiments/projects/codetiming
GA_PY_RUN="$(mktemp -d /tmp/pynguin-run.XXXXXX)"
PYNGUIN_DANGER_AWARE=1 /tmp/pynguin025/bin/pynguin \
  --project-path "$GA_PY_PROJECT" --module-name codetiming._timers \
  --output-path "$GA_PY_RUN/generated" --report-dir "$GA_PY_RUN/report" \
  --algorithm DYNAMOSA --maximum-search-time 600 --seed 23120205 \
  --assertion-generation SIMPLE --statistics-backend CSV
cd "$GA_PY_PROJECT"
PYTHONPATH="$GA_PY_PROJECT" PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /tmp/pynguin025/bin/python -m slipcover --branch --source codetiming \
  --json --out "$GA_PY_RUN/coverage.json" -m pytest -q \
  --junitxml "$GA_PY_RUN/junit.xml" "$GA_PY_RUN/generated"
```

Expected của **lượt đã lưu**: CSV 0,8148148, pytest 10 pass/5 xfail; đọc riêng `coverage.json → files → codetiming/_timers.py`. Seed cố định vẫn có thể khác do môi trường/thời gian tìm kiếm. `PYNGUIN_DANGER_AWARE` là xác nhận của tool vì nó thực thi source; dùng project đã chọn trong môi trường tạm.

### Pynguin trên source nhóm

Tạo thư mục tạm có `scripts/coverage_gaps.py` nguyên vẹn. Đổi `--project-path` sang thư mục này, `--module-name scripts.coverage_gaps`, ngân sách 60s. Lượt 0.25.2 kết thúc mã 120 và xuất một test xfail không gọi source.

Để thử khả năng thích nghi, tạo venv Python 3.12 khác, cài `research/pynguin/requirements-current.txt`, thêm `--subprocess True --filesystem-isolation True`. Bản có seed thêm `--initial-population-seeding True --initial-population-data <seed-tests>`; [seed và XML](../evidence/tuan-06/papers/pynguin-group-2026-10-29/seeded/) được lưu cùng output. Test xuất ra chứa đường dẫn XML tạm gốc; khi replay ở thư mục mới, thay đường dẫn **trên bản sao test replay**, giữ nguyên output lưu trữ.

Đo pytest/SlipCover với source `scripts`. Đọc assertion và xfail, không chỉ exit code. Không tự đồng bộ test paper vào suite chính: lượt có seed chỉ gọi hàm, chưa giữ assertion của baseline.

## 5. Phạm vi hoàn thành và bàn giao

Đã có cho mỗi paper: nguồn/hạng, chạy lại phân tích công bố, sinh test mới trên một benchmark gốc, thử trên source nhóm và đối chiếu kết quả/giới hạn. Evidence chỉ giữ test sinh, số đo, JUnit và output cuối cần kiểm; đã bỏ trial cũ và log lỗi khởi tạo.

Đây là **tái hiện có giới hạn**, không phải chạy lại toàn bộ benchmark, 30 seed/config hay mutation experiment. Không nhận các lượt Codex chạy là từng thành viên tự chạy. Gia An phụ trách tổng hợp/review; thành viên khác xác nhận riêng phần họ thực sự thực hiện. Video, hợp nhất slide/HTML và trình bày với GV làm sau theo yêu cầu.
