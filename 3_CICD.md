# Phần 3 — CI/CD & Jenkins
### Tài liệu chuẩn bị seminar · Môn Kiểm thử phần mềm

> **Vị trí trong chuỗi seminar:** Đây là mắt xích **thứ ba và cuối cùng**: [Unit Test](1_UnitTest.md) → [Code Coverage](2_CodeCoverage.md) **→ CI/CD**. Nếu Unit Test là *lưới an toàn* và Coverage là *đèn soi lỗ thủng*, thì CI/CD là *cánh tay robot tự động kéo lưới ra kiểm tra mỗi khi có người đổi code* — không cần ai nhắc.

---

## Mục lục
1. [Vì sao cần CI/CD](#1-vì-sao-cần-cicd)
2. [CI, Continuous Delivery, Continuous Deployment](#2-ci-continuous-delivery-continuous-deployment)
3. [Cấu trúc một pipeline](#3-cấu-trúc-một-pipeline)
4. [Lợi ích của CI/CD](#4-lợi-ích-của-cicd)
5. [Jenkins là gì](#5-jenkins-là-gì)
6. [Kiến trúc Controller – Agent](#6-kiến-trúc-controller--agent)
7. [Freestyle vs Pipeline · Jenkinsfile](#7-freestyle-vs-pipeline--jenkinsfile)
8. [Ví dụ Jenkinsfile ghép cả ba chủ đề](#8-ví-dụ-jenkinsfile-ghép-cả-ba-chủ-đề)
9. [So sánh Jenkins với nền tảng khác](#9-so-sánh-jenkins-với-nền-tảng-khác)
10. [Best practices & cạm bẫy](#10-best-practices--cạm-bẫy)
11. [Thuật ngữ & câu hỏi ôn tập](#11-thuật-ngữ--câu-hỏi-ôn-tập)

---

## 1. Vì sao cần CI/CD

Giả sử nhóm đã có [unit test](1_UnitTest.md) và đo [coverage](2_CodeCoverage.md). Nhưng nếu **lần nào cũng phải chạy bằng tay**, sớm muộn sẽ có ngày quên — và một bug lọt ra production. Ngoài ra còn vấn đề kinh điển *"máy tôi chạy được mà"* (works on my machine): code chạy ổn ở máy này nhưng hỏng ở máy khác do khác môi trường.

**CI/CD** ra đời để tự động hóa toàn bộ: mỗi khi có người đổi code, hệ thống **tự động** build, chạy test, đo coverage, và (nếu đạt chuẩn) đưa sản phẩm tới người dùng — nhất quán, lặp lại được, ít lỗi do con người.

---

## 2. CI, Continuous Delivery, Continuous Deployment

Ba khái niệm rất hay bị nhầm:

| Thuật ngữ | Tên đầy đủ | Bản chất |
|-----------|-----------|---------|
| **CI** | Continuous **Integration** (Tích hợp liên tục) | Mỗi lần push code → **tự động build + chạy test** để phát hiện lỗi/xung đột tích hợp sớm. Khuyến khích merge thường xuyên (≥ 1 lần/ngày). |
| **CD** | Continuous **Delivery** (Phân phối liên tục) | Mở rộng CI: sau khi pass, sản phẩm luôn ở trạng thái **sẵn sàng phát hành**. Việc đưa lên production là **bước thủ công** (người bấm nút). |
| **CD** | Continuous **Deployment** (Triển khai liên tục) | Như Delivery nhưng bước lên production cũng **tự động hoàn toàn**, không cần người can thiệp (với điều kiện mọi test pass). |

```
 Continuous Integration │ Continuous Delivery  │ Continuous Deployment
 ───────────────────────┼──────────────────────┼──────────────────────
  Build + Test tự động  │ + đóng gói sẵn sàng   │ + tự động release
                        │   (người BẤM NÚT      │   thẳng lên production
                        │    để deploy)         │   (máy tự làm)
```

> **Khác biệt mấu chốt giữa hai chữ "CD":** Continuous **Delivery** luôn *sẵn sàng* deploy nhưng *con người bấm nút*; Continuous **Deployment** *tự động* deploy luôn. Khác nhau đúng **một bước phê duyệt của con người**.

---

## 3. Cấu trúc một pipeline

Pipeline là chuỗi các **stage (giai đoạn)** chạy tuần tự; mỗi stage chỉ chạy nếu stage trước thành công:

```
 Push code
    │
    ▼
┌────────┐ ┌───────┐ ┌──────┐ ┌──────────┐ ┌─────────────┐ ┌────────┐
│Checkout│►│ Build │►│ Test │►│ Coverage │►│Quality Gate │►│ Deploy │
└────────┘ └───────┘ └──────┘ └──────────┘ └─────────────┘ └────────┘
  lấy code   biên     chạy      đo độ phủ    PASS mới đi tiếp  đưa lên
  mới nhất   dịch   unit test                FAIL thì DỪNG     server
```

- **Checkout:** lấy mã nguồn mới nhất từ Git.
- **Build:** biên dịch, phân giải phụ thuộc.
- **Test:** chạy [unit test](1_UnitTest.md) (và các loại test khác).
- **Coverage:** đo [độ phủ](2_CodeCoverage.md), xuất báo cáo.
- **Quality Gate:** điểm quyết định — nếu test fail hoặc coverage dưới ngưỡng → pipeline **fail**, không cho đi tiếp.
- **Deploy:** triển khai lên môi trường (staging/production).

> **Đây là nơi cả ba chủ đề seminar gặp nhau:** Unit Test và Coverage trở thành **hai trạm gác chất lượng (quality gate)** tự động bên trong pipeline.

---

## 4. Lợi ích của CI/CD

- **Phát hiện lỗi sớm:** sai ở commit nào lộ ra ngay commit đó, chi phí sửa thấp.
- **Giảm "works on my machine":** mọi thứ build/test trên môi trường chuẩn, nhất quán của CI.
- **Phát hành nhanh & an toàn:** quy trình tự động, lặp lại được, giảm lỗi thao tác tay.
- **Tăng tự tin khi refactor/thay đổi:** luôn có lưới kiểm thử tự động chạy phía sau.

---

## 5. Jenkins là gì

**Jenkins** là một **máy chủ tự động hóa (automation server) mã nguồn mở**, viết bằng Java. Nó có nguồn gốc từ dự án Hudson (Sun Microsystems) và tách ra thành Jenkins năm 2011. Đây là một trong những công cụ CI/CD lâu đời và được dùng rộng rãi nhất.

Đặc điểm nổi bật:
- **Hệ sinh thái plugin rất lớn** (hơn 1.800 plugin): tích hợp Git, Maven/Gradle, Docker, JaCoCo, Slack, cloud… Gần như mọi công cụ đều có plugin kết nối.
- **Tự host (self-hosted):** cài trên máy chủ riêng, kiểm soát toàn bộ — phù hợp doanh nghiệp, môi trường on-premise, yêu cầu bảo mật nội bộ.
- **Rất linh hoạt:** tùy biến được gần như mọi quy trình; đổi lại cần công cài đặt và bảo trì.

> Hiểu đơn giản: Jenkins là **"người công nhân không bao giờ ngủ"** — bạn giao cho nó bản hướng dẫn (Jenkinsfile), mỗi khi có code mới nó tự động làm theo: build, test, đo coverage, deploy.

---

## 6. Kiến trúc Controller – Agent

Jenkins hoạt động theo mô hình phân tán:

```
        ┌─────────────────┐
        │   CONTROLLER    │  "bộ não": lập lịch, quản lý job,
        │   (Jenkins)     │   giao diện web, lưu kết quả
        └────────┬────────┘
                 │ giao việc
       ┌─────────┼─────────┐
       ▼         ▼         ▼
   ┌───────┐ ┌───────┐ ┌───────┐
   │Agent 1│ │Agent 2│ │Agent 3│  "cánh tay": nơi THỰC SỰ
   │ Linux │ │Windows│ │ macOS │   chạy build/test
   └───────┘ └───────┘ └───────┘
```

- **Controller** (trước gọi là "master"): bộ não trung tâm — lập lịch, quản lý cấu hình & job, cung cấp giao diện web, lưu kết quả. Controller *điều phối*, không nên là nơi chạy build nặng.
- **Agent (node):** máy thực thi — nơi job thực sự chạy build/test.

Lợi ích: **chạy song song** nhiều job; **kiểm thử đa môi trường** (Linux/Windows/macOS, nhiều phiên bản runtime) cùng lúc; **dễ mở rộng** bằng cách thêm agent.

---

## 7. Freestyle vs Pipeline · Jenkinsfile

Hai cách định nghĩa công việc trong Jenkins:

- **Freestyle job:** cấu hình qua giao diện web bằng cách bấm chọn. Dễ bắt đầu nhưng **khó version control** và khó tái lập.
- **Pipeline (khuyến nghị hiện đại):** mô tả toàn bộ quy trình bằng mã trong một file tên **`Jenkinsfile`** đặt ngay trong kho mã nguồn → gọi là **Pipeline as Code**.

**Ưu điểm của Pipeline as Code:**
- Pipeline được **version control** cùng với code (xem lịch sử, review như code).
- Tái lập được, dễ chia sẻ và khôi phục.
- Hai cú pháp: **Declarative** (cấu trúc rõ ràng — khuyến nghị cho đa số) và **Scripted** (linh hoạt theo kiểu lập trình Groovy).

**Các khái niệm trong Jenkinsfile:**
- **`pipeline`** — khối bao ngoài toàn bộ.
- **`agent`** — chỉ định nơi chạy (agent nào).
- **`stage`** — một giai đoạn có tên (Build, Test, Deploy…); hiển thị thành ô riêng trên giao diện.
- **`steps`** — các hành động cụ thể bên trong stage.
- **`post`** — hành động chạy *sau* pipeline tùy kết quả (`always`, `success`, `failure`, `unstable`); thường dùng lưu báo cáo & gửi thông báo.

---

## 8. Ví dụ Jenkinsfile ghép cả ba chủ đề

Đây là ví dụ "chốt hạ" — một `Jenkinsfile` cho dự án Java/Maven thể hiện trọn vẹn Unit Test + Coverage + CI/CD trong một mạch:

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps { checkout scm }                     // lấy code mới nhất từ Git
        }

        stage('Build') {
            steps { sh 'mvn -B compile' }              // biên dịch
        }

        stage('Unit Test') {
            steps { sh 'mvn test' }                    // (1) chạy UNIT TEST (JUnit)
            post {
                always { junit 'target/surefire-reports/*.xml' }  // hiển thị kết quả test
            }
        }

        stage('Coverage') {
            steps { sh 'mvn jacoco:report' }           // (2) sinh báo cáo COVERAGE (JaCoCo)
            post {
                always {
                    jacoco(changeBuildStatus: true,    // đặt ngưỡng làm QUALITY GATE
                           minimumBranchCoverage: '70')// branch < 70% → build FAIL
                }
            }
        }

        stage('Deploy') {
            when { branch 'main' }                     // chỉ deploy nhánh main
            steps { sh './deploy.sh' }                 // (3) TRIỂN KHAI
        }
    }

    post {
        success { echo 'Pipeline xanh — code đạt chuẩn để merge/deploy' }
        failure { echo 'Pipeline đỏ — có test fail hoặc coverage dưới ngưỡng' }
    }
}
```

**Đọc theo mạch ba chủ đề:**
1. **[Unit Test](1_UnitTest.md)** (`stage Unit Test`) — lưới kiểm thử chạy tự động mỗi lần có code mới.
2. **[Coverage](2_CodeCoverage.md)** (`stage Coverage`, `minimumBranchCoverage: '70'`) — coverage thành **quality gate**: tụt dưới 70% branch là build fail, chặn luôn.
3. **CI/CD** (toàn bộ pipeline + `Deploy`) — Jenkins tự động vận hành cả dây chuyền mỗi lần push; chỉ khi tất cả pass, code mới lên `main`/được triển khai.

→ Một file, kể trọn câu chuyện: **code → test → đo coverage → gác cổng chất lượng → triển khai**, hoàn toàn tự động.

---

## 9. So sánh Jenkins với nền tảng khác

| Tiêu chí | **Jenkins** | **GitHub Actions** | **GitLab CI** |
|----------|-------------|--------------------|--------------|
| Mô hình | Tự host (self-hosted) | SaaS, gắn với GitHub | Tích hợp sẵn trong GitLab |
| Cấu hình | Jenkinsfile (Groovy) | YAML (`.github/workflows`) | YAML (`.gitlab-ci.yml`) |
| Điểm mạnh | Cực linh hoạt, plugin phong phú, tự chủ hạ tầng | Khởi động nhanh, không cần server, hợp dự án nhỏ/vừa | Liền mạch với repo GitLab, DevOps trọn gói |
| Đánh đổi | Cần cài đặt & bảo trì | Phụ thuộc GitHub, ít kiểm soát hạ tầng | Gắn chặt hệ sinh thái GitLab |

→ **Chọn Jenkins** khi cần tùy biến cao, tự chủ hạ tầng, môi trường on-premise/doanh nghiệp. **Chọn GitHub Actions/GitLab CI** khi muốn khởi động nhanh, dự án nhỏ/vừa, đã dùng sẵn GitHub/GitLab.

---

## 10. Best practices & cạm bẫy

### Thực hành tốt
- Dùng **Pipeline as Code** (Jenkinsfile trong repo) để version control quy trình.
- Thiết kế pipeline **fail fast**: xếp bước nhanh ([unit test](1_UnitTest.md)) trước bước chậm (integration, E2E, deploy) → lỗi lộ sớm, tiết kiệm thời gian.
- Đặt [coverage](2_CodeCoverage.md) làm **quality gate** với ngưỡng rõ ràng.
- Tự động **thông báo** kết quả (Slack/email) để cả nhóm biết ngay khi pipeline đỏ.
- Giữ pipeline **nhanh**; cân nhắc chạy song song trên nhiều agent.

### Cạm bẫy thường gặp
- **Pipeline quá chậm** → lập trình viên nản, tìm cách bỏ qua.
- **"Xanh giả":** tắt/bỏ qua test fail cho pipeline pass nhanh → vô hiệu hóa toàn bộ ý nghĩa quality gate.
- **Chạy build nặng ngay trên Controller** → nghẽn hệ thống; nên đẩy sang Agent.
- **Để lộ secret** (mật khẩu, token) trong Jenkinsfile → phải dùng cơ chế quản lý credential của Jenkins.

---

## 11. Thuật ngữ & câu hỏi ôn tập

### Thuật ngữ
| Thuật ngữ | Nghĩa ngắn |
|-----------|-----------|
| CI | Continuous Integration: tự động build + test mỗi lần push |
| Continuous Delivery | Luôn sẵn sàng phát hành; deploy là bước thủ công |
| Continuous Deployment | Deploy lên production hoàn toàn tự động |
| Pipeline | Chuỗi các stage tự động từ code tới triển khai |
| Stage / Step | Giai đoạn có tên / hành động cụ thể trong stage |
| Quality gate | Điều kiện chất lượng bắt buộc vượt qua để đi tiếp |
| Jenkins | Automation server mã nguồn mở cho CI/CD |
| Controller / Agent | Bộ não điều phối / máy thực thi job |
| Jenkinsfile | File mô tả pipeline (Pipeline as Code) |
| Declarative / Scripted | Hai cú pháp viết Jenkinsfile |

### Câu hỏi ôn tập
1. Phân biệt CI, Continuous Delivery và Continuous Deployment.
2. Kể các stage điển hình của một pipeline và vai trò từng stage.
3. Quality gate là gì? Unit Test và Coverage đóng vai trò quality gate thế nào?
4. Jenkins là gì? Mô tả vai trò Controller và Agent.
5. Pipeline as Code (Jenkinsfile) là gì và vì sao tốt hơn cấu hình qua giao diện?
6. So sánh Jenkins với GitHub Actions — khi nào chọn cái nào?
7. "Fail fast" trong thiết kế pipeline nghĩa là gì và vì sao quan trọng?

### Tài liệu tham khảo
- Jenkins User Handbook & Pipeline Syntax — jenkins.io/doc
- Martin Fowler — *ContinuousIntegration*, *ContinuousDelivery* (martinfowler.com)
- Jez Humble & David Farley — *Continuous Delivery* (sách kinh điển)

---
*Phần trước ← [Phần 2 — Code Coverage](2_CodeCoverage.md) · Quay lại [Phần 1 — Unit Test](1_UnitTest.md)*
