# Paper: nguồn, kết quả và cách chạy lại

Ngô Gia An (23120205), AI hỗ trợ: Codex, 28/10/2026. Danh mục máy đọc được: [papers.json](papers.json). Không tự viết lại thuật toán của paper.

## Hai bài được chọn

| Bài | Xuất bản / hạng hội nghị | Source tác giả | Áp dụng cho nhóm |
|---|---|---|---|
| P1 — CoverUp (Pizzorno, Berger, 2025) | [FSE 2025 Research Papers](https://conf.researchr.org/details/fse-2025/fse-2025-research-papers/112/CoverUp-Effective-High-Coverage-Test-Generation-for-Python), DOI 10.1145/3729398 | [coverup-eval](https://github.com/plasma-umass/coverup-eval), [tool](https://github.com/plasma-umass/coverup) | Python: dùng `scripts/coverage_gaps.py` thật của repo, không dịch LoanService sang Python |
| P2 — ChatUniTest (Chen và cộng sự, 2024) | [FSE 2024 Demonstrations](https://2024.esec-fse.org/details/fse-2024-demonstrations/6/ChatUniTest-A-Framework-for-LLM-based-Test-Generation), DOI 10.1145/3663529.3663801 | [nhánh python gốc](https://github.com/ZJU-ACES-ISE/ChatUniTest/tree/python), [plugin Java của tác giả](https://github.com/ZJU-ACES-ISE/chatunitest-maven-plugin) | Java: `LoanService#borrow`, so với suite hiện tại |

Đã kiểm trực tiếp [CORE2023](https://portal.core.edu.au/conf-ranks/?by=all&search=&source=CORE2023): FSE A*. Đây là hạng của **venue**; không gán hạng A* cho từng bài. P2 thuộc demo track, cần nhóm xác nhận GV chấp nhận track này. Khoảng năm 2024–2025 nằm trong yêu cầu 2021–2026. Năm 2023 trên preprint ChatUniTest không phải năm xuất bản proceedings.

## Ý chính để đưa lên slide

**P1.** CoverUp dùng coverage hiện có để chọn phần mã cần test, đưa ngữ cảnh vào prompt rồi chạy test mới. Nếu test lỗi hoặc không tăng coverage, công cụ gửi phản hồi để sửa. Điểm phù hợp với seminar là vòng đo → sinh → kiểm lại; phạm vi của tool là Python regression testing, không phải tự suy ra đúng đặc tả. [Paper, bản v4](https://arxiv.org/html/2403.16218v4).

**P2.** ChatUniTest tổ chức ngữ cảnh của phương thức Java và vòng generation–validation–repair. Nhóm cần theo dõi test sinh ra có biên dịch được, chạy được và có assertion đúng hay không. Dùng plugin hiện nay để thử case study phải ghi riêng với môi trường bài báo năm 2024. [Nguồn công bố](https://2024.esec-fse.org/details/fse-2024-demonstrations/6/ChatUniTest-A-Framework-for-LLM-based-Test-Generation), [hướng dẫn tác giả](https://github.com/ZJU-ACES-ISE/ChatUniTest).

## Kết quả thực sự đã có

| Thí nghiệm | Kết quả | Được phép kết luận |
|---|---|---|
| P1: chạy nguyên `scripts/compare.py` trên dữ liệu MT công bố, 163 module | CoverUp overall line 89,2%; branch 88,7%; line+branch 89,0%. MuTAP `gpt4o_zero`: 78,0%; 74,5%; 76,8% | Tái hiện **bước phân tích dữ liệu công bố**, khớp số 89% vs 77% đã làm tròn ở abstract v4. Không phải sinh lại tất cả test bằng LLM |
| P1: chạy tool gốc trên source Python nhóm với `--dry-run` | Xem `evidence/gia-an/papers/coverup-group-dry*/run.json` và log | Chỉ kiểm môi trường/coverage/chuẩn bị prompt. Không có model output hay kết quả test mới |
| P2: kiểm điều kiện chạy artifact gốc | Chưa có config, API key, thư viện và môi trường MySQL/grammar gốc | Chưa chạy tái lập P2; không điền coverage/số test giả |
| P2: plugin tác giả 2.1.1 parse bản sao case study | 20 class, 28 method; build success, endpoint localhost không có model | Thử tương thích parser hiện tại, chưa sinh test và chưa tái lập thí nghiệm gốc |
| AI-5: Codex tương tác trên LoanService | 2 → 10 test; 3/6 → 6/6 branch | Đây là demo AI của nhóm, **không** thay cho thí nghiệm của P2 |

File log, lệnh, revision và giới hạn: [evidence paper](../evidence/gia-an/papers/). Dùng dependencies phân tích hiện tại đã khóa trong `requirements-analysis.lock.txt`; khác pins cũ của tác giả nên không coi đây là tái lập nguyên môi trường. Script/dữ liệu MT dùng trong phép so được kiểm không sửa; checkout macOS báo một tên file CM khác biệt do hoa/thường, không nằm trong dữ liệu MT đã dùng.

## Chạy lại P1 không gọi model

Chọn thư mục ngoài repo cho artifact và môi trường. Artifact đầy đủ có thể chiếm nhiều GB; không chép nó vào source nộp.

```bash
git clone https://github.com/plasma-umass/coverup-eval.git /tmp/coverup-eval
git -C /tmp/coverup-eval checkout f3173196b90181974b0b684600ffde42ac36672c
python3 -m venv /tmp/paper-analysis
/tmp/paper-analysis/bin/pip install -r research/requirements-analysis.lock.txt
python3 scripts/paper_experiments.py coverup-reanalyse /tmp/coverup-eval \
  --python /tmp/paper-analysis/bin/python --output /tmp/paper-reanalysis
```

Lệnh này dùng trực tiếp script gốc, không dùng submodule CodaMosa. Muốn thử dry-run trên source nhóm, dùng **Python 3.12**, tạo venv rồi cài `research/requirements-coverup.lock.txt`:

```bash
python3 scripts/paper_experiments.py coverup-dry-run \
  --python /tmp/coverup-env/bin/python --output /tmp/coverup-group-check
```

Runner tạo bản sao tạm cô lập gồm source `coverage_gaps.py` và một smoke test, giữ smoke test trong `inputs/` rồi dọn bản sao. Tool có thể cần mạng lần đầu để tải tokenizer; sentinel trong dry-run không phải API key. Khi cần sinh test thật, trên bản sao đó bỏ `--dry-run`, chọn model đang truy cập được, giới hạn `--max-concurrency 1 --max-attempts 1`, giữ output model/test/coverage và ghi chi phí thật. Chưa thực hiện bước gọi model trong phiên này.

## P2: artifact gốc và lần thử hiện tại

Artifact gốc cần MySQL, Java grammar native, Python dependencies cũ, model/API. Làm theo README ở revision trong `papers.json`; chạy `python run.py` tại `src/` sau khi thiết lập config riêng. Chưa có các điều kiện đó ở máy hiện tại; [preflight](../evidence/gia-an/papers/chatunitest-preflight/run.json) lưu trạng thái. Không thay thuật toán bằng code tự viết hoặc response model giả để nhận là tái lập.

Đã chuẩn bị [plugin fragment](chatunitest/pom.fragment.xml) cho **bản sao** case study. Không sửa `pom.xml` chính bằng plugin này. Chèn plugin vào `<build><plugins>` của bản sao; chọn `CHATUNITEST_MODEL` và key bằng biến môi trường, không lưu giá trị vào repo/video. Fragment đặt endpoint chính thức rõ ràng vì source plugin hiện tại mặc định dùng một proxy bên thứ ba. Lệnh thử sau khi có môi trường:

```bash
# Chạy trong thư mục case-study BẢN SAO, sau khi chèn plugin fragment.
./mvnw -B -ntp -DskipTests package
./mvnw -B -ntp io.github.zju-aces-ise:chatunitest-maven-plugin:2.1.1:method \
  '-DselectMethod=vn.edu.seminar.loan.LoanService#borrow'
```

Bước `package` và `:parse` đã chạy được trên bản sao Java 25: **20 class, 28 method**. Bước `:method` và test sinh ra trên JUnit 6 vẫn **chưa kiểm chứng**. Tạo bản sao bằng `python3 research/chatunitest/prepare_trial.py /tmp/chatunitest-case` trước khi thử. Giữ lỗi compile/parser/assertion nếu gặp, sau đó đánh giá khả năng tương thích. Không dùng `prune` để xóa test lỗi rồi báo tất cả thành công. Chỉ chép test được review vào nguồn chính bằng commit riêng. Dùng fixture AI-5 hiện tại để giải thích workflow trong khi chờ thí nghiệm P2 thật.

## Phân chia lượt chạy và tiêu chí hoàn tất

Đề xuất để Gia An điều phối, chưa xác nhận người khác đã nhận/chạy: Gia An giữ P1 và tổng hợp; Bảo An chạy P2 Java; Thế Vinh thử môi trường sạch và dữ liệu; Đạt review coverage/mutation; Quang Vinh review khả năng đưa lệnh vào CI. Mỗi người lưu lệnh, ngày, revision, model, seed/tham số, số test build/pass, coverage và giới hạn rồi commit bằng tài khoản thật.

P1 còn thiếu sinh test mới trên benchmark và trên source nhóm. P2 còn thiếu chạy artifact gốc, thí nghiệm LoanService và kết quả định lượng. Chỉ đánh dấu mục paper hoàn thành sau các bước này; việc xác nhận track/hạng với GV nằm trong việc điều phối của trưởng nhóm.
