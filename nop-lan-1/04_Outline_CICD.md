# Outline chi tiết — Phần 3: CI/CD

**Phụ trách:** TV1 · **Thời lượng dự kiến khi seminar:** ~25 phút

> Luận điểm xuyên suốt: hai phần trước (unit test, coverage) chỉ có giá trị thật khi được
> **bắt buộc** chạy ở cổng merge. CI/CD là chỗ biến "nên chạy test" thành "không chạy test
> thì không merge được".

---

## 1. Lý thuyết & thuật ngữ

| Mục | Sẽ trình bày điều gì | Chứng minh bằng |
|---|---|---|
| 3.1 Vì sao cần CI | Vấn đề "chạy được trên máy tôi"; integration hell khi merge muộn | Dựng một Pull Request fail thật rồi sửa cho xanh |
| 3.2 CI vs Continuous Delivery vs Continuous Deployment | Ba khái niệm hay bị gọi lẫn; ranh giới nằm ở chỗ nào (ai bấm nút, bấm lúc nào) | Sơ đồ + chỉ rõ pipeline của nhóm **dừng ở mức nào** và vì sao |
| 3.3 Cấu trúc một pipeline | checkout → build → unit test → coverage gate → package → (deploy) | Chính file cấu hình pipeline của nhóm |
| 3.4 Thuật ngữ GitHub Actions | workflow · job · step · runner · action · trigger · matrix · cache · artifact · secret | **Đối chiếu từng thuật ngữ với dòng YAML tương ứng** trên slide |
| 3.5 Quan hệ với hai trụ trước | Test và coverage chỉ có giá trị khi được bắt buộc chạy, không phụ thuộc trí nhớ của người merge | Demo coverage gate chặn merge |
| 3.6 Nguyên lý hoạt động | Sự kiện Git (push / pull request) kích hoạt trigger → nền tảng cấp một máy ảo sạch → thực thi các step tuần tự → trả mã lỗi → job đỏ thì chặn merge | Log một lần chạy thật, đọc từng step |

**Thuật ngữ nhóm sẽ chốt cách dịch:** tích hợp liên tục · chuyển giao liên tục · triển khai
liên tục · pipeline (luồng xử lý) · runner (máy chạy) · artifact (sản phẩm build) ·
quality gate (cổng chất lượng) · trigger (sự kiện kích hoạt) · secret (bí mật cấu hình).

## 2. Công cụ

**Công cụ demo sâu: GitHub Actions.**

Nhóm chọn vì: (a) repository của nhóm đã ở GitHub nên không phát sinh hạ tầng, (b) log của
mỗi lần chạy là **link công khai** nên dùng trực tiếp làm minh chứng nộp bài, (c) cài đặt
chỉ cần thêm một file YAML — phù hợp với thời lượng của một bài seminar.

**Các thành phần sẽ dùng trong demo:** `actions/checkout` (lấy mã nguồn) ·
`actions/setup-java` (cài JDK và bật cache Maven) · `actions/upload-artifact` (tải báo cáo
coverage về) · biến `$GITHUB_STEP_SUMMARY` (ghi tóm tắt kết quả) · `secrets` (lưu khoá API
cho demo AI) · `strategy.matrix` (chạy song song trên nhiều phiên bản JDK).

**Các công cụ sẽ khảo sát và so sánh** (chi tiết ở `05_KhaoSat_SoSanh_CongCu.md`):
Jenkins · GitLab CI · CircleCI · Azure Pipelines.

Riêng **Jenkins**, nhóm sẽ viết một file cấu hình làm **đúng cùng một việc** để đặt cạnh
nhau — đây là cách chứng minh luận điểm "vendor lock-in" bằng bằng chứng thay vì bằng lời.

## 3. Demo dự kiến

| Mã | Kịch bản | Nội dung | Số đo / minh chứng | Mức tự động |
|---|---|---|---|---|
| **CI-1** | **Cài đặt** | Tạo file workflow tối thiểu: lấy mã nguồn, cài JDK, chạy `mvn verify`; xem lần chạy đầu tiên; đọc log từng step | Link lần chạy, thời gian | Fully automated |
| **CI-2** | **Chức năng cơ bản** | Thêm cache thư viện Maven; tải báo cáo coverage về dạng artifact; ghi tóm tắt kết quả vào trang summary của lần chạy | **Thời gian build trước/sau khi bật cache** (đo thật, chạy 3 lần lấy trung vị) | Fully automated |
| **CI-3** | **Luồng xử lý phức tạp** | Pipeline nhiều job nối tiếp: `test` → `coverage-gate` → `package`; chạy song song trên hai phiên bản JDK; bật chặn merge khi gate fail; demo **một Pull Request đỏ rồi sửa cho xanh** | Link PR có trạng thái đỏ → xanh; log chạy song song | Fully automated |

## 4. Điểm yếu của công cụ

| Điểm yếu | Cách nhóm sẽ chứng minh |
|---|---|
| **Khó debug tại máy — phải push mới biết sai** | Đếm **số commit "fix ci" có thật** trong lịch sử repository của nhóm; giới thiệu công cụ chạy workflow tại máy và nói rõ nó cũng không mô phỏng được đủ môi trường |
| **Vendor lock-in cú pháp cấu hình** | Đặt file cấu hình của GitHub Actions và của Jenkins cạnh nhau cho cùng một pipeline → cho thấy không copy được, phải viết lại từ đầu |
| **Giới hạn thời lượng miễn phí với repository riêng tư** | Trình bày chính sách tính phút; nói rõ repository công khai mới miễn phí không giới hạn, và đây là lý do nhóm chọn để repository công khai |
| **Cache hỏng gây kết quả không nhất quán** | Tạo tình huống cache cũ làm build fail dù mã nguồn không đổi; cách phòng bằng khoá cache gắn với mã băm của `pom.xml` |
| **Secret dễ lộ qua log** | Cố tình in một biến secret → nền tảng che thành `***`; nhưng cho thấy cách gián tiếp (mã hoá base64 rồi in) **vẫn lộ** → từ đó rút ra quy tắc xử lý secret của nhóm |
| **Môi trường mặc định không có sẵn thứ dự án cần** | Demo test cần database thật: phải khai báo dịch vụ phụ trợ hoặc dùng container → chi phí cấu hình tăng nhanh so với lời hứa "chỉ một file YAML" |
| **Pipeline xanh không có nghĩa phần mềm đúng** | Pipeline chỉ chạy đúng những gì được khai báo; nếu bộ test yếu thì pipeline xanh vẫn vô nghĩa → nối ngược về luận điểm của Phần 2 |

## 5. Bài tập áp dụng dự kiến cho lớp

| Bài | Yêu cầu | Gợi ý nhóm sẽ kèm theo |
|---|---|---|
| 1 | Viết workflow tối thiểu tự chạy test cho một project Maven cho sẵn | Khung YAML có chú thích từng dòng |
| 2 | Thêm coverage gate vào workflow, chứng minh nó chặn được một commit xấu | Gợi ý cách tạo commit xấu để thử |
| 3 | Bật cache và đo thời gian build trước/sau | Gợi ý cách đo cho công bằng: chạy nhiều lần, lấy trung vị |

*(Số lượng và mức độ bài tập nhóm xin ý kiến thầy/cô — xem `09_CauHoi_Cho_GV.md`.)*
