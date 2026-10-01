# Kế hoạch triển khai — Gói gặp mặt Tuần 2–3

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Có đủ tài liệu đề xuất + một slice case study chạy được (test xanh, báo cáo JaCoCo, workflow CI) để trình bày nội dung dự kiến cho GV ở buổi gặp mặt Tuần 2–3, không bị đánh giá "chuẩn bị sơ sài" (−1đ).

**Architecture:** Markdown trong `docs/` là nguồn sự thật; slide HTML và báo cáo `.tex` dẫn xuất từ đó. Case study là một Maven project độc lập trong `case-study/`, tách theo nghiệp vụ (`fine/`, `loan/`) chứ không theo tầng kỹ thuật. Một script Node (`scripts/check-repo.mjs`) đóng vai "test" cho phần tài liệu: kiểm link chết, kiểm heading bắt buộc, và quét secret lỡ commit.

**Tech Stack:** Java 25 LTS · Maven 3.9.16 · Spring Boot 4.1.1 · JUnit Jupiter 6.0.3 · Mockito 5.23.0 · AssertJ 3.27.7 · H2 2.4.240 · JaCoCo 0.8.15 · PIT 1.30.0 · GitHub Actions · Node 22 (chỉ cho script kiểm tra)

**Spec:** [docs/superpowers/specs/2026-10-01-seminar-unittest-coverage-cicd-design.md](../specs/2026-10-01-seminar-unittest-coverage-cicd-design.md)

## Global Constraints

- **GitHub:** mọi hành động chạm GitHub (`git push`, lệnh `gh`, tạo/đổi repo, bật Actions, tạo GitHub Projects) phải hỏi chủ repo trước **từng lần**. `git commit` local không cần hỏi. Các bước có nhãn **[GATE: GITHUB]** không được chạy mà chưa có câu đồng ý.
- **API key AI:** không bao giờ nằm trong repo, slide, video, hay chat. Chỉ qua GitHub Secrets hoặc biến môi trường.
- **Không dùng lại** 5 file tài liệu ở commit `52ec671`. Nội dung xây mới hoàn toàn.
- **Phiên bản đã chốt, không tự đổi:** Spring Boot `4.1.1`, Java `25`, JaCoCo `0.8.15`, PIT `1.30.0` + `pitest-junit5-plugin 1.2.3`, `actions/checkout@v7`, `actions/setup-java@v6`, `actions/upload-artifact@v7`.
- **Spring Boot 4 khác Boot 3 ở 1 chỗ sẽ gặp:** `@MockBean` đã bị **xoá**. Dùng `@MockitoBean` (`org.springframework.test.context.bean.override.mockito.MockitoBean`).
- **Chạy Maven không dùng `cd`:** luôn `mvn -f case-study/pom.xml ...` từ gốc repo.
- **Slide không được phụ thuộc CDN/mạng.** Nền trắng, chữ đen, cỡ chữ thân bài ≥ 24px.
- **So sánh BigDecimal trong test:** dùng `isEqualByComparingTo`, không dùng `isEqualTo` (khác scale → `equals` sai).
- **Tiếng Việt** cho toàn bộ tài liệu, comment code, và tên test (`@DisplayName`).

## Review Focus

Năm trường hợp spec hàm ý nhưng không task nào tự nhiên kiểm tới. Mỗi dòng đã được gắn một test vào task sở hữu code đó:

1. `FineCalculator.calculate(-1, tier)` — ngày trễ âm phải ném `IllegalArgumentException`, tuyệt đối không trả phí âm. → test ở Task 8.
2. `FineCalculator.calculate(5, null)` — `tier` null phải ném `IllegalArgumentException` với thông báo rõ, không để `NullPointerException` lọt ra. → test ở Task 8.
3. `FineCalculator.calculate(Integer.MAX_VALUE, STANDARD)` — ngày trễ cực lớn phải trả đúng `MAX_FINE`, không tràn số, không ném. → test ở Task 8.
4. `LoanService.borrow()` khi `Member` lấy từ DB có `tier == null` (dữ liệu xấu) — phải báo lỗi nghiệp vụ rõ ràng, không `NullPointerException`. → test ở Task 10.
5. `POST /api/loans` với body thiếu `memberId` — phải trả **400** kèm tên field sai, không trả 500. → test ở Task 11.

---

## Task 1: Khung repo + script kiểm tra tài liệu

**Files:**
- Create: `.gitignore`
- Create: `scripts/check-repo.mjs`
- Create: `README.md`

**Interfaces:**
- Consumes: không có (task đầu tiên).
- Produces: `node scripts/check-repo.mjs` — exit code `0` nếu mọi kiểm tra đạt, `1` nếu có lỗi, in từng lỗi ra stderr. Mọi task sau đều chạy lệnh này trước khi commit. Script đọc mọi file `.md` trong repo (bỏ `node_modules`, `target`, `.git`).

- [ ] **Step 1: Viết script kiểm tra (đây là "test" của phần tài liệu)**

Create `scripts/check-repo.mjs`:

```javascript
// Kiểm tra sức khoẻ repo seminar. Chạy: node scripts/check-repo.mjs
// Quy tắc 1 — link chết: mọi link markdown trỏ tới file nội bộ phải tồn tại.
// Quy tắc 2 — secret: không được có API key lọt vào repo.
import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, dirname, resolve, relative, sep } from 'node:path';

const ROOT = resolve(import.meta.dirname, '..');
const SKIP_DIRS = new Set(['.git', 'node_modules', 'target', '.idea']);
const errors = [];

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (SKIP_DIRS.has(name)) continue;
    const full = join(dir, name);
    if (statSync(full).isDirectory()) walk(full, out);
    else out.push(full);
  }
  return out;
}

const allFiles = walk(ROOT);
const mdFiles = allFiles.filter((f) => f.endsWith('.md'));

// --- Quy tắc 1: link chết ---
const LINK = /\[[^\]]*\]\(([^)\s]+)\)/g;
for (const file of mdFiles) {
  const text = readFileSync(file, 'utf8');
  for (const m of text.matchAll(LINK)) {
    const target = m[1];
    if (/^(https?:|mailto:|#)/.test(target)) continue;
    const path = resolve(dirname(file), decodeURIComponent(target.split('#')[0]));
    if (!existsSync(path)) {
      errors.push(`LINK CHET: ${relative(ROOT, file)} -> ${target}`);
    }
  }
}

// --- Quy tắc 2: secret lọt vào repo ---
const SECRETS = [
  { name: 'Anthropic API key', re: /sk-ant-[A-Za-z0-9_-]{20,}/ },
  { name: 'OpenAI API key', re: /sk-(?:proj-)?[A-Za-z0-9]{32,}/ },
  { name: 'GitHub token', re: /gh[pousr]_[A-Za-z0-9]{36,}/ },
];
const TEXT_EXT = /\.(md|java|xml|yml|yaml|html|css|tex|mjs|js|json|properties|txt|csv)$/;
for (const file of allFiles.filter((f) => TEXT_EXT.test(f))) {
  if (file.endsWith(`scripts${sep}check-repo.mjs`)) continue; // chính file này chứa pattern
  const text = readFileSync(file, 'utf8');
  for (const { name, re } of SECRETS) {
    if (re.test(text)) errors.push(`SECRET (${name}): ${relative(ROOT, file)}`);
  }
}

if (errors.length > 0) {
  console.error(`\n${errors.length} loi:\n`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
}
console.log(`OK: ${mdFiles.length} file markdown, khong co link chet, khong co secret.`);
```

- [ ] **Step 2: Chạy script với một README cố tình sai để chắc nó bắt được lỗi**

Create `README.md` (bản tạm, cố tình có 1 link chết):

```markdown
# Seminar: Unit Test · Code Coverage · CI/CD

Xem [đề bài](require.md) và [outline](docs/01-outline-unit-test.md).
```

Run: `node scripts/check-repo.mjs`

Expected: FAIL, exit code 1, in `LINK CHET: README.md -> docs/01-outline-unit-test.md`

- [ ] **Step 3: Viết `.gitignore`**

Create `.gitignore`:

```gitignore
# Build
target/
*.class
case-study.zip

# IDE
.idea/
*.iml
.vscode/
.settings/
.classpath
.project

# Node (chỉ dùng cho scripts/)
node_modules/

# LaTeX build
*.aux
*.log
*.out
*.toc
*.synctex.gz
*.fls
*.fdb_latexmk
report/main.pdf

# Bí mật — không bao giờ commit
.env
.env.*
*.pem
secrets/
```

- [ ] **Step 4: Sửa README thành bản thật (chỉ link tới file đã tồn tại)**

Create `README.md`:

```markdown
# Seminar: Unit Test · Code Coverage · CI/CD

- **Môn:** Software Testing — FIT@HCMUS
- **Nhóm:** 5 thành viên
- **Giai đoạn:** Gặp mặt Tuần 2–3 — trình bày nội dung dự kiến

## Tài liệu

| File | Nội dung |
|---|---|
| [require.md](require.md) | Đề bài của GV (không sửa) |
| [Thiết kế seminar](docs/superpowers/specs/2026-10-01-seminar-unittest-coverage-cicd-design.md) | Quyết định kỹ thuật, phạm vi, roadmap 7 gói |
| [Kế hoạch gói gặp mặt](docs/superpowers/plans/2026-10-01-goi-gap-mat-tuan-2-3.md) | Kế hoạch triển khai gói hiện tại |

## Kiểm tra repo

```bash
node scripts/check-repo.mjs
```

Script kiểm: link markdown chết, và API key lỡ bị commit.
```

- [ ] **Step 5: Chạy lại script để chắc nó xanh**

Run: `node scripts/check-repo.mjs`

Expected: PASS — `OK: N file markdown, khong co link chet, khong co secret.`

- [ ] **Step 6: Commit**

```bash
git add .gitignore README.md scripts/check-repo.mjs docs/superpowers
git commit -m "chore: khung repo, script kiem tra tai lieu, spec va ke hoach"
```

---

## Task 2: Outline chi tiết 3 trụ

**Files:**
- Create: `docs/01-outline-unit-test.md`
- Create: `docs/02-outline-code-coverage.md`
- Create: `docs/03-outline-cicd.md`
- Modify: `scripts/check-repo.mjs` (thêm quy tắc heading bắt buộc)
- Modify: `README.md` (thêm link 3 outline)

**Interfaces:**
- Consumes: `node scripts/check-repo.mjs` từ Task 1.
- Produces: quy tắc 3 trong script — mỗi file `docs/0[1-3]-outline-*.md` phải có đủ 4 heading cấp 2: `## Lý thuyết & thuật ngữ`, `## Công cụ`, `## Demo dự kiến`, `## Điểm yếu của công cụ`. Các task sau không được xoá heading này.

- [ ] **Step 1: Thêm quy tắc heading bắt buộc vào script (viết test trước)**

Trong `scripts/check-repo.mjs`, chèn đoạn sau ngay trước block `if (errors.length > 0)`:

```javascript
// --- Quy tắc 3: heading bắt buộc trong outline ---
const REQUIRED_OUTLINE_HEADINGS = [
  '## Lý thuyết & thuật ngữ',
  '## Công cụ',
  '## Demo dự kiến',
  '## Điểm yếu của công cụ',
];
for (const file of mdFiles.filter((f) => /docs[\\/]0[1-3]-outline-.*\.md$/.test(f))) {
  const text = readFileSync(file, 'utf8');
  for (const heading of REQUIRED_OUTLINE_HEADINGS) {
    if (!text.includes(heading)) {
      errors.push(`THIEU HEADING: ${relative(ROOT, file)} -> "${heading}"`);
    }
  }
}
```

- [ ] **Step 2: Chạy script để chắc nó fail vì chưa có file outline nào**

Run: `node scripts/check-repo.mjs`

Expected: PASS (chưa có file `docs/0X-outline-*.md` nào nên quy tắc 3 chưa áp). Đây là kết quả đúng — quy tắc chỉ kích hoạt khi file xuất hiện. Bước 3 sẽ tạo file thiếu heading để thấy nó fail.

- [ ] **Step 3: Tạo `docs/01-outline-unit-test.md` chỉ với heading đầu để xác nhận script bắt lỗi**

Create `docs/01-outline-unit-test.md`:

```markdown
# Outline — Unit Test

## Lý thuyết & thuật ngữ
```

Run: `node scripts/check-repo.mjs`

Expected: FAIL, exit 1, in 3 dòng `THIEU HEADING` cho `## Công cụ`, `## Demo dự kiến`, `## Điểm yếu của công cụ`.

- [ ] **Step 4: Viết đủ nội dung `docs/01-outline-unit-test.md`**

Create `docs/01-outline-unit-test.md`:

```markdown
# Outline — Unit Test

> Phụ trách: **TV2**. Đây là outline *dự kiến* trình GV ở buổi gặp mặt Tuần 2–3,
> chưa phải nội dung slide hoàn chỉnh. Mỗi mục ghi rõ sẽ nói gì và chứng minh bằng gì.

## Lý thuyết & thuật ngữ

| Mục | Sẽ trình bày điều gì | Chứng minh bằng |
|---|---|---|
| 1.1 Unit test là gì, "unit" là gì | Phân biệt unit / integration / E2E qua kim tự tháp kiểm thử; vì sao unit test rẻ nhất và chạy nhiều nhất | Bảng so sánh thời gian chạy đo thật trên case study |
| 1.2 Nguyên tắc FIRST | Fast · Independent · Repeatable · Self-validating · Timely | Mỗi chữ ghép với một ví dụ *vi phạm* lấy từ code thật |
| 1.3 Cấu trúc AAA | Arrange – Act – Assert, và vì sao tách 3 khối giúp đọc test như đọc tài liệu | Trích `LoanServiceTest` |
| 1.4 Test Double | Dummy · Stub · Spy · Mock · Fake — 5 loại khác nhau ra sao | Bảng + ví dụ Mockito cho từng loại |
| 1.5 Test nào nên viết, test nào không | Logic nhiều nhánh thì test; getter/setter, framework code thì không | Đối chiếu với báo cáo coverage: chỗ nào cố ý để trống và vì sao |
| 1.6 Quan hệ với TDD | Vòng đỏ–xanh–refactor | Chính commit history của `FineCalculator` trong repo này |

**Thuật ngữ cần chốt cách dịch:** test fixture · test double · stub · mock · spy ·
assertion · parameterized test · flaky test · test smell.

## Công cụ

**Công cụ chính: JUnit Jupiter + Mockito + AssertJ.**

| Thành phần | Vai trò | Phiên bản dùng |
|---|---|---|
| JUnit Jupiter | Khung chạy test, annotation, lifecycle | 6.0.3 (Spring Boot 4.1.1 quản lý) |
| Mockito | Tạo test double cho dependency | 5.23.0 |
| AssertJ | Assertion đọc được như câu tiếng Anh | 3.27.7 |

**Lưu ý thuật ngữ bắt buộc nói trên slide:** tài liệu phổ thông gọi "JUnit 5"; chúng ta
chạy Jupiter **6**. Các API dùng trong seminar (`@Test`, `@ParameterizedTest`, `@CsvSource`,
`@MethodSource`, `@Nested`, `@DisplayName`, `@Tag`) giống nhau giữa 5 và 6 — nói rõ để
người trong lớp không bị lẫn khi tra tài liệu.

**Khảo sát alternatives** (chi tiết ở [docs/04](04-khao-sat-so-sanh-cong-cu.md)):
TestNG · Spock (Groovy) · Hamcrest (assertion) · EasyMock / JMockit (mocking).

## Demo dự kiến

| Mã | Kịch bản | Nội dung | Mức tự động |
|---|---|---|---|
| UT-1 | **Cài đặt** | Thêm `spring-boot-starter-test` vào `pom.xml`, chạy `mvn test` lần đầu, đọc output Surefire, mở `target/surefire-reports` | Fully automated |
| UT-2 | **Chức năng cơ bản** | Viết `FineCalculatorTest` theo vòng TDD đỏ–xanh–refactor; AAA; `@DisplayName` tiếng Việt; `@ParameterizedTest` + `@CsvFileSource` đọc dữ liệu từ CSV ngoài (phần **Data driven**) | Fully automated |
| UT-3 | **Luồng phức tạp** | `LoanServiceTest`: 6 nhánh nghiệp vụ, `@Mock` 3 repository, `when/thenReturn`, `verify`, `verify(never())`, `ArgumentCaptor` bắt `Loan` được lưu, `Clock.fixed` để test không phụ thuộc thời gian thật (phần **Checkpoints**) | Fully automated |

## Điểm yếu của công cụ

Mỗi điểm yếu phải demo bằng code chạy thật, không chỉ nói lý thuyết.

| Điểm yếu | Cách chứng minh |
|---|---|
| Mock quá sâu → test xanh nhưng hệ thống sai | Viết `LoanServiceTest` bản mock cả `FineCalculator`, sửa công thức tính phí cho sai → test vẫn xanh. So với bản dùng `FineCalculator` thật → test đỏ ngay |
| Test không có assertion vẫn được tính là "pass" | Test gọi method rồi không assert gì; Surefire báo xanh. Đây cũng là đầu vào cho demo coverage ở [docs/02](02-outline-code-coverage.md) |
| Mockito không mock được `static` / `final` mặc định | Thử mock `LocalDate.now()` → thất bại; giải thích vì sao phải inject `Clock` thay vì thêm `mockito-inline` |
| `@InjectMocks` im lặng khi thiếu dependency | Cố tình thiếu 1 mock → lỗi `NullPointerException` khó đọc; giải thích vì sao nhóm chọn khởi tạo bằng constructor tường minh trong `@BeforeEach` |
| Unit test không bắt được lỗi tích hợp | Test unit xanh toàn bộ nhưng query dẫn xuất của Spring Data sai tên field → chỉ `@DataJpaTest` mới lộ ra |
```

- [ ] **Step 5: Chạy script — phải xanh cho file 01**

Run: `node scripts/check-repo.mjs`

Expected: PASS (file `01` đã đủ 4 heading; file `02`, `03` chưa tồn tại nên chưa bị kiểm).

- [ ] **Step 6: Viết `docs/02-outline-code-coverage.md`**

Create `docs/02-outline-code-coverage.md`:

```markdown
# Outline — Code Coverage

> Phụ trách: **TV3**. Outline dự kiến cho buổi gặp mặt Tuần 2–3.

## Lý thuyết & thuật ngữ

| Mục | Sẽ trình bày điều gì | Chứng minh bằng |
|---|---|---|
| 2.1 Coverage là gì, đo cái gì | Coverage đo *code được chạy qua*, không đo *code được kiểm chứng* — đây là câu quan trọng nhất của cả phần này | Demo 100% coverage với 0 assertion |
| 2.2 Các loại coverage | Line · Statement · Branch · Method · Class · Condition / MC-DC | Bảng + đoạn `if (a && b)` minh hoạ line 100% nhưng branch 50% |
| 2.3 Line vs Branch trên code thật | Lấy đúng `FineCalculator.calculate()`: một test phủ hết *dòng* nhưng chỉ phủ một nửa *nhánh* | Hai báo cáo JaCoCo cạnh nhau |
| 2.4 Đọc báo cáo JaCoCo | Ý nghĩa màu xanh / vàng / đỏ, cột `Missed Branches`, cột `Cxty` (cyclomatic complexity) | Ảnh chụp `target/site/jacoco/index.html` của repo này |
| 2.5 Ngưỡng coverage hợp lý | Vì sao "100% coverage" là mục tiêu sai; chốt ngưỡng theo lớp quan trọng thay vì theo toàn project | Cấu hình `jacoco:check` thật trong `pom.xml` |
| 2.6 Mutation testing — thước đo thật của chất lượng test | Mutant · killed · survived · mutation score; vì sao nó bắt được điều coverage không bắt được | Báo cáo PIT trên `FineCalculator` |

**Thuật ngữ cần chốt cách dịch:** độ phủ dòng · độ phủ nhánh · độ phủ điều kiện ·
coverage gate · mutation testing · mutant sống/bị diệt.

## Công cụ

**Công cụ chính: JaCoCo 0.8.15** (Java Code Coverage) — chuẩn de-facto cho Maven.

| Chức năng | Goal Maven | Dùng để làm gì |
|---|---|---|
| Gắn agent đo lúc chạy test | `jacoco:prepare-agent` | Instrument bytecode on-the-fly |
| Sinh báo cáo HTML/XML/CSV | `jacoco:report` | Người đọc + để AI đọc XML (demo AI-2) |
| Gate chặn build | `jacoco:check` | Fail build khi branch coverage tụt dưới ngưỡng |

**Nguyên lý hoạt động (phải nói được trên slide):** JaCoCo không sửa source. Nó chạy như
một *Java agent*, chèn bộ đếm (probe) vào bytecode khi class được nạp, ghi kết quả ra
`target/jacoco.exec` dạng nhị phân, rồi `report` ghép file đó với bytecode + source để
tô màu. Vì làm việc trên bytecode, nó cần phiên bản hỗ trợ đúng class file version —
đó là lý do phải dùng 0.8.15 cho Java 25.

**Công cụ bổ trợ: PIT 1.30.0** — chỉ dùng để chứng minh điểm yếu của JaCoCo, không phải
công cụ chính của seminar.

**Khảo sát alternatives** (chi tiết ở [docs/04](04-khao-sat-so-sanh-cong-cu.md)):
Cobertura · OpenClover · IntelliJ IDEA coverage · SonarQube (tổng hợp, không tự đo).

## Demo dự kiến

| Mã | Kịch bản | Nội dung | Mức tự động |
|---|---|---|---|
| CC-1 | **Cài đặt** | Thêm plugin JaCoCo vào `pom.xml`, chạy `mvn verify`, mở `target/site/jacoco/index.html`, giải thích từng cột | Fully automated |
| CC-2 | **Chức năng cơ bản** | Chạy coverage với *một* test → xem số; thêm test cho nhánh còn đỏ → xem số tăng. Lưu **cả hai** báo cáo làm minh chứng trước/sau | Fully automated |
| CC-3 | **Luồng phức tạp** | Bật `jacoco:check` làm coverage gate ở ngưỡng branch 90% cho `FineCalculator`; cố tình xoá một test → `mvn verify` **fail**; khôi phục → xanh. Gắn gate này vào GitHub Actions | Fully automated |

## Điểm yếu của công cụ

| Điểm yếu | Cách chứng minh |
|---|---|
| **Coverage ≠ chất lượng test** | Test `@Tag("antipattern")` gọi `calculate()` đủ mọi nhánh mà **không có assertion nào** → JaCoCo báo 100% branch. Chạy `mvn -Pcoverage-trap verify` để thấy con số, so với báo cáo PIT: nhiều mutant *sống* |
| Không phát hiện assertion yếu | PIT đổi `>` thành `>=` trong `FineCalculator` → bộ test vẫn xanh → mutant sống. JaCoCo không nói gì về chuyện này |
| Nhánh trong lambda / switch pattern đếm khó hiểu | Viết lại một đoạn bằng `stream().filter()` → JaCoCo báo thiếu nhánh ở dòng trông như chỉ có một nhánh; giải thích bytecode sinh ra |
| Code sinh tự động làm loãng số liệu | Lombok / record / class `LibraryApplication` làm tụt tỉ lệ → phải cấu hình `<excludes>`; cho thấy số liệu đổi hẳn sau khi loại trừ |
| Số coverage toàn project vô nghĩa khi gộp | So sánh: toàn project ~70% nhưng `FineCalculator` 100% và `LoanService` 45% → gate theo *lớp* thay vì theo *project* |
```

- [ ] **Step 7: Viết `docs/03-outline-cicd.md`**

Create `docs/03-outline-cicd.md`:

```markdown
# Outline — CI/CD

> Phụ trách: **TV1**. Outline dự kiến cho buổi gặp mặt Tuần 2–3.

## Lý thuyết & thuật ngữ

| Mục | Sẽ trình bày điều gì | Chứng minh bằng |
|---|---|---|
| 3.1 Vì sao cần CI | Vấn đề "pass trên máy tôi"; integration hell khi merge muộn | Dựng một PR fail thật rồi chụp lại |
| 3.2 CI vs Continuous Delivery vs Continuous Deployment | Ba khái niệm hay bị gọi lẫn; ranh giới nằm ở chỗ nào | Sơ đồ + chỉ rõ pipeline của nhóm dừng ở mức nào |
| 3.3 Cấu trúc một pipeline | checkout → build → unit test → coverage gate → package → (deploy) | Chính `.github/workflows/ci.yml` của repo này |
| 3.4 Thuật ngữ GitHub Actions | workflow · job · step · runner · action · trigger · matrix · cache · artifact · secret | Đối chiếu từng từ với dòng tương ứng trong file YAML |
| 3.5 Quan hệ với hai trụ còn lại | Unit test và coverage chỉ có giá trị khi *bắt buộc* chạy ở cổng merge, không phụ thuộc ai nhớ chạy | Demo gate chặn PR |
| 3.6 Nguyên lý hoạt động | Trigger từ event Git → GitHub cấp runner ảo → thực thi step tuần tự → trả exit code → fail job chặn merge | Log run thật |

**Thuật ngữ cần chốt cách dịch:** tích hợp liên tục · pipeline · runner · artifact ·
quality gate · trigger · secret.

## Công cụ

**Công cụ chính: GitHub Actions.**

| Thành phần | Phiên bản chốt |
|---|---|
| `actions/checkout` | `v7` |
| `actions/setup-java` | `v6` (distribution `temurin`, java-version `25`, `cache: maven`) |
| `actions/upload-artifact` | `v7` |

**Khảo sát alternatives** (chi tiết ở [docs/04](04-khao-sat-so-sanh-cong-cu.md)):
Jenkins · GitLab CI · CircleCI · Azure Pipelines.

## Demo dự kiến

| Mã | Kịch bản | Nội dung | Mức tự động |
|---|---|---|---|
| CI-1 | **Cài đặt** | Tạo `.github/workflows/ci.yml` tối thiểu (checkout + setup-java + `mvn -B verify`); xem run đầu tiên; đọc log từng step | Fully automated |
| CI-2 | **Chức năng cơ bản** | Thêm cache Maven (đo thời gian trước/sau), upload báo cáo JaCoCo làm artifact, ghi summary vào `$GITHUB_STEP_SUMMARY` | Fully automated |
| CI-3 | **Luồng phức tạp** | Pipeline nhiều job: `test` → `coverage-gate` → `package`; matrix Java 21 + 25; chặn merge khi coverage gate fail; demo một PR đỏ rồi sửa cho xanh | Fully automated |

## Điểm yếu của công cụ

| Điểm yếu | Cách chứng minh |
|---|---|
| Khó debug local — phải push mới biết sai | Đếm số commit "fix ci" thật trong history của nhóm; giới thiệu `act` và nói rõ nó cũng không mô phỏng đủ |
| Vendor lock-in cú pháp YAML | Đặt cạnh `Jenkinsfile` làm cùng việc → cho thấy không copy được, phải viết lại |
| Giới hạn phút miễn phí với repo private | Chụp trang billing; nói rõ repo public mới miễn phí không giới hạn |
| Cache phụ thuộc gây kết quả không nhất quán | Tạo tình huống cache hỏng → build fail dù code không đổi; cách xử lý bằng cache key có hash `pom.xml` |
| Secret dễ bị lộ qua log | Cố tình `echo` một biến secret → GitHub che thành `***`, nhưng cho thấy cách gián tiếp (base64) vẫn lộ → quy tắc của nhóm về secret |
| Runner mặc định không có môi trường đặc thù | Demo test cần Docker/Postgres: phải khai báo `services:` hoặc Testcontainers → chi phí cấu hình tăng nhanh |
```

- [ ] **Step 8: Thêm link 3 outline vào README**

Trong `README.md`, thêm 3 dòng vào bảng "Tài liệu", ngay sau dòng `require.md`:

```markdown
| [Outline Unit Test](docs/01-outline-unit-test.md) | Lý thuyết, công cụ, 3 demo, điểm yếu — TV2 |
| [Outline Code Coverage](docs/02-outline-code-coverage.md) | Lý thuyết, công cụ, 3 demo, điểm yếu — TV3 |
| [Outline CI/CD](docs/03-outline-cicd.md) | Lý thuyết, công cụ, 3 demo, điểm yếu — TV1 |
```

- [ ] **Step 9: Chạy script — phải xanh toàn bộ**

Run: `node scripts/check-repo.mjs`

Expected: PASS — không `LINK CHET`, không `THIEU HEADING`, không `SECRET`.

- [ ] **Step 10: Commit**

```bash
git add docs/01-outline-unit-test.md docs/02-outline-code-coverage.md docs/03-outline-cicd.md scripts/check-repo.mjs README.md
git commit -m "docs: outline chi tiet 3 tru + quy tac heading bat buoc trong script kiem tra"
```

---

## Task 3: Khảo sát & so sánh công cụ

**Files:**
- Create: `docs/04-khao-sat-so-sanh-cong-cu.md`
- Modify: `README.md` (thêm link)

**Interfaces:**
- Consumes: 3 file outline từ Task 2 (mỗi outline đã trỏ link tới `docs/04`, nên link chết sẽ hết sau task này).
- Produces: 7 trục so sánh chốt cho cả seminar — các gói sau phải dùng đúng 7 trục này, không tự thêm bớt: *Khả năng · Dễ cài đặt · Tích hợp Maven/IDE · Hiệu năng · Tài liệu & cộng đồng · Giá & giấy phép · Điểm yếu đã kiểm chứng*.

- [ ] **Step 1: Viết `docs/04-khao-sat-so-sanh-cong-cu.md`**

Create `docs/04-khao-sat-so-sanh-cong-cu.md`:

```markdown
# Khảo sát & so sánh công cụ

> Việc chung cả nhóm; mỗi người viết phần công cụ mình phụ trách.
> Đề yêu cầu *"so sánh, đánh giá các công cụ ở nhiều khía cạnh khác nhau"* — nhóm chốt
> **7 trục** dưới đây và dùng thống nhất cho cả 3 trụ, để bảng so sánh có thể đọc ngang.

## 7 trục so sánh

| Trục | Nghĩa là gì | Đo/đánh giá bằng cách nào |
|---|---|---|
| T1 — Khả năng | Công cụ làm được những gì cho mục tiêu testing của trụ đó | Đối chiếu tài liệu chính thức, không nghe quảng cáo |
| T2 — Dễ cài đặt | Bao nhiêu bước từ project trắng tới lần chạy đầu thành công | **Đếm số bước thật** khi nhóm tự làm, ghi lại |
| T3 — Tích hợp Maven / IDE | Có plugin Maven chính thức? IntelliJ hiển thị được kết quả? | Thử thật, chụp ảnh |
| T4 — Hiệu năng | Thêm bao nhiêu thời gian vào `mvn verify` | **Đo bằng giây** trên cùng máy, cùng case study, chạy 3 lần lấy trung vị |
| T5 — Tài liệu & cộng đồng | Tra cứu dễ không, lỗi lạ có người trả lời không | Số câu hỏi trên StackOverflow + ngày commit cuối trên GitHub |
| T6 — Giá & giấy phép | Miễn phí tới đâu, giấy phép gì | Trang pricing / LICENSE |
| T7 — Điểm yếu đã kiểm chứng | Trường hợp nhóm **tự gặp** công cụ làm không tốt | Code chạy thật trong repo này |

**Quy ước trung thực:** ô nào nhóm **chưa tự kiểm** thì ghi `(chưa kiểm)`, không được điền
theo cảm giác. Đây là yêu cầu "chính chủ" của đề.

## 1. Trụ Unit Test

| | **JUnit Jupiter 6** *(chọn)* | TestNG | Spock | JUnit 4 |
|---|---|---|---|---|
| T1 Khả năng | Lifecycle đầy đủ, `@ParameterizedTest`, `@Nested`, `@Tag`, extension model | Mạnh về group/dependency giữa test, data provider | Cú pháp BDD rất gọn, mock built-in | Cũ, không có parameterized tiện |
| T2 Dễ cài | 1 dependency (`spring-boot-starter-test` có sẵn) | Thêm dependency + cấu hình Surefire | Cần thêm Groovy vào build | 1 dependency |
| T3 Maven/IDE | Mặc định của Spring Boot; IDE hỗ trợ tốt nhất | Hỗ trợ tốt | Cần plugin Groovy | Tốt |
| T4 Hiệu năng | *(đo ở Gói 2)* | (chưa kiểm) | (chưa kiểm) | (chưa kiểm) |
| T5 Tài liệu | Rất nhiều, nhưng **phần lớn viết cho Jupiter 5** | Nhiều | Ít hơn, cộng đồng Groovy | Rất nhiều nhưng lỗi thời |
| T6 Giá | EPL 2.0, miễn phí | Apache 2.0 | Apache 2.0 | EPL 1.0 |
| T7 Điểm yếu | Test không assertion vẫn pass; tài liệu phần lớn là bản 5 | Mô hình group dễ bị lạm dụng thành test phụ thuộc nhau | Phải học Groovy | Không nên dùng cho project mới |

**Chốt:** JUnit Jupiter — vì Spring Boot quản lý sẵn, và vì hệ sinh thái (JaCoCo, PIT, Surefire) mặc định nhắm vào nó.

### Thư viện mocking

| | **Mockito 5** *(chọn)* | EasyMock | JMockit |
|---|---|---|---|
| T1 Khả năng | Stub, verify, `ArgumentCaptor`, `@Spy`; mock `static`/`final` cần `mockito-inline` | Tương đương, API record–replay | Mạnh nhất (mock cả `static`, constructor) |
| T2 Dễ cài | Có sẵn trong `spring-boot-starter-test` | Thêm dependency | Thêm dependency + cấu hình `-javaagent` |
| T5 Tài liệu | Nhiều nhất | Trung bình | Ít, cập nhật chậm |
| T7 Điểm yếu | Không mock `static`/`final` mặc định; dễ bị lạm dụng thành "test mock thay vì test hành vi" | API record–replay khó đọc hơn | Can thiệp sâu vào bytecode, dễ vỡ khi đổi JDK |

### Thư viện assertion

| | **AssertJ** *(chọn)* | JUnit `Assertions` | Hamcrest |
|---|---|---|---|
| T1 | Fluent, gợi ý IDE tốt, assertion chuyên biệt cho collection / `BigDecimal` / exception | Đủ dùng, cơ bản | Matcher ghép được |
| T7 | Thêm 1 dependency; đội ngũ phải quen cú pháp | Thông báo lỗi kém chi tiết hơn | Cú pháp lồng nhau khó đọc |

## 2. Trụ Code Coverage

| | **JaCoCo 0.8.15** *(chọn)* | Cobertura | OpenClover | IntelliJ coverage |
|---|---|---|---|---|
| T1 Khả năng | Line, Branch, Method, Class, Instruction, Cxty; HTML/XML/CSV; có `check` goal làm gate | Line, Branch | Nhiều loại nhất, có cả per-test coverage | Line, Branch (trong IDE) |
| T2 Dễ cài | 1 plugin, 2 execution | 1 plugin | 1 plugin + license key cho bản đầy đủ | Không cần cài |
| T3 Maven/IDE | Plugin Maven chính thức; IntelliJ đọc được `jacoco.exec` | Plugin cũ | Có plugin | Chỉ trong IDE |
| T4 Hiệu năng | *(đo ở Gói 3)* | (chưa kiểm) | (chưa kiểm) | — |
| T5 Tài liệu | Rất nhiều, changelog rõ ràng về hỗ trợ JDK | **Gần như ngừng phát triển** | Trung bình | Tài liệu JetBrains |
| T6 Giá | EPL 2.0, miễn phí | GPL 2.0 | Miễn phí cho open-source, trả phí cho thương mại | Kèm IDE |
| T7 Điểm yếu | Coverage ≠ chất lượng; nhánh lambda đếm khó hiểu; không thấy assertion yếu | Không hỗ trợ JDK mới → **loại** | Giấy phép phức tạp | Không chạy được trong CI |

**Chốt:** JaCoCo. Cobertura bị loại vì không theo kịp JDK mới — đây chính là một kết luận
của phần khảo sát, không phải chi tiết kỹ thuật bỏ qua được.

### Công cụ bổ trợ: mutation testing

| | **PIT 1.30.0** *(chọn, chỉ để chứng minh điểm yếu của coverage)* |
|---|---|
| T1 | Sinh mutant trên bytecode, chạy lại test, báo mutant *sống* / *bị diệt* |
| T4 | Chậm hơn coverage nhiều lần → chỉ chạy cho `fine/` chứ không toàn project |
| T7 | Chậm; mutant "tương đương" gây báo động giả; có thể chưa theo kịp JDK mới nhất |

## 3. Trụ CI/CD

| | **GitHub Actions** *(chọn)* | Jenkins | GitLab CI | CircleCI |
|---|---|---|---|---|
| T1 Khả năng | Workflow YAML, matrix, cache, artifact, secret, môi trường; marketplace action lớn | Mạnh nhất về plugin (1800+), controller–agent, chạy tự host | Tích hợp sẵn GitLab, có container registry | Mạnh về cache & song song |
| T2 Dễ cài | **1 file YAML, không cài gì** | Cài server + plugin + agent (nặng nhất) | 1 file `.gitlab-ci.yml` | 1 file config |
| T3 Maven/IDE | `actions/setup-java` có cache Maven sẵn | Plugin Maven lâu đời | Có template Maven | Có orb |
| T4 Hiệu năng | *(đo ở Gói 4: build lạnh vs có cache)* | Phụ thuộc máy tự host | (chưa kiểm) | (chưa kiểm) |
| T5 Tài liệu | Rất nhiều, nhưng ví dụ cũ hay dùng `@v3`/`@v4` lỗi thời | Rất nhiều, nhiều bài đã cũ | Nhiều | Trung bình |
| T6 Giá | Miễn phí **không giới hạn** cho repo public; repo private có hạn mức phút | Miễn phí nhưng **tốn tiền máy chủ** | Có bản miễn phí giới hạn phút | Có bản miễn phí |
| T7 Điểm yếu | Khó debug local; lock-in YAML; cache hỏng gây build sai | Phải tự bảo trì, tự vá bảo mật; UI cũ | Phải dùng GitLab | Ít dùng ở VN |

**Chốt:** GitHub Actions cho demo chính (vì repo của nhóm đã ở GitHub và log public dùng
làm minh chứng được). Jenkins để **đối chiếu** ở Gói 4 — viết `Jenkinsfile` làm cùng việc
để chứng minh luận điểm vendor lock-in.

## Kết luận khảo sát

1. **Hệ sinh thái quan trọng hơn tính năng lẻ.** JUnit Jupiter được chọn không vì nhiều
   tính năng nhất, mà vì JaCoCo, PIT, Surefire, Spring Boot đều mặc định nhắm vào nó.
2. **Một công cụ ngừng theo kịp JDK là đã chết.** Cobertura bị loại vì lý do này.
3. **"Dễ cài" là một trục thật, không phải chi tiết nhỏ.** Chênh lệch GitHub Actions
   (1 file) và Jenkins (cài server) quyết định luôn việc nhóm 5 người có demo kịp hay không.
4. **Không công cụ nào trong 3 trụ đo được *chất lượng* test.** Phải ghép thêm mutation
   testing — và đây là luận điểm xuyên suốt của bài seminar.
```

- [ ] **Step 2: Thêm link vào README**

Trong `README.md`, thêm dòng vào bảng "Tài liệu" sau dòng Outline CI/CD:

```markdown
| [Khảo sát & so sánh công cụ](docs/04-khao-sat-so-sanh-cong-cu.md) | 7 trục so sánh, bảng so sánh cho cả 3 trụ |
```

- [ ] **Step 3: Chạy script kiểm tra**

Run: `node scripts/check-repo.mjs`

Expected: PASS — các link `docs/04-...` trong 3 file outline (Task 2) giờ đã có đích thật.

- [ ] **Step 4: Commit**

```bash
git add docs/04-khao-sat-so-sanh-cong-cu.md README.md
git commit -m "docs: khao sat va so sanh cong cu theo 7 truc cho ca 3 tru"
```

---

## Task 4: Ma trận 9 demo + câu hỏi cho GV

**Files:**
- Create: `docs/05-ma-tran-demo.md`
- Create: `docs/08-cau-hoi-cho-gv.md`
- Modify: `README.md` (thêm link)

**Interfaces:**
- Consumes: mã demo `UT-1..3`, `CC-1..3`, `CI-1..3` đã đặt tên ở Task 2. Không được đổi mã này.
- Produces: mã demo `AI-1..4` dùng lại ở Task 5; cột "Minh chứng để lại" là hợp đồng với các gói sau — mỗi demo ở gói sau phải sinh đúng minh chứng đã cam kết ở đây.

- [ ] **Step 1: Viết `docs/05-ma-tran-demo.md`**

Create `docs/05-ma-tran-demo.md`:

```markdown
# Ma trận demo

> Đề yêu cầu mỗi công cụ có **ít nhất 3 kịch bản demo**: cài đặt · chức năng cơ bản ·
> luồng xử lý phức tạp. Bảng này là cam kết của nhóm: mỗi demo làm gì, đo gì, và
> **để lại minh chứng gì** — vì đề nói rõ *"chỉ show kết quả, không thể hiện các bước
> làm rõ ràng cụ thể sẽ không được điểm cao"*.

## Case study dùng chung cho mọi demo

Quản lý thư viện — nghiệp vụ cho mượn sách (`case-study/`):

- `FineCalculator` — logic thuần tính phí trả trễ. Nhiều nhánh → dùng cho branch coverage và data-driven.
- `LoanService.borrow()` — 6 nhánh nghiệp vụ: sách không tồn tại · sách đang được mượn ·
  thành viên không tồn tại · vượt hạn mức mượn · còn phí trễ chưa trả · mượn thành công.
- `LoanController` — `POST /api/loans`.

## 9 demo công cụ

| Mã | Công cụ | Kịch bản | Làm gì | Đo gì | Minh chứng để lại | Mức tự động |
|---|---|---|---|---|---|---|
| **UT-1** | JUnit | Cài đặt | Thêm `spring-boot-starter-test`, `mvn test` lần đầu, đọc output Surefire | Số test chạy, thời gian | Log `mvn test`, `target/surefire-reports/` | Fully |
| **UT-2** | JUnit | Cơ bản | TDD `FineCalculator`: đỏ → xanh → refactor; AAA; `@ParameterizedTest` + `@CsvFileSource` | Số ca kiểm thử, số vòng TDD | **Commit history từng vòng đỏ/xanh**, file `fines.csv` | Fully |
| **UT-3** | Mockito | Phức tạp | `LoanServiceTest` 6 nhánh; `@Mock` 3 repository; `verify`, `verify(never())`, `ArgumentCaptor`; `Clock.fixed` | Số nhánh phủ, số `verify` | File test, báo cáo Surefire | Fully |
| **CC-1** | JaCoCo | Cài đặt | Thêm plugin, `mvn verify`, mở `index.html`, giải thích từng cột | — | Ảnh chụp báo cáo, log | Fully |
| **CC-2** | JaCoCo | Cơ bản | Chạy coverage với 1 test → thêm test cho nhánh đỏ → chạy lại | **Branch coverage trước/sau** | **Hai báo cáo HTML (trước & sau)** lưu vào `docs/evidence/` | Fully |
| **CC-3** | JaCoCo | Phức tạp | Bật `jacoco:check` gate branch ≥ 90% cho `FineCalculator`; xoá 1 test → build **fail**; khôi phục → xanh; gắn gate vào CI | Build pass/fail | Log `mvn verify` cả hai trạng thái, run CI đỏ và xanh | Fully |
| **CI-1** | GH Actions | Cài đặt | `ci.yml` tối thiểu; xem run đầu tiên; đọc log từng step | Thời gian run | Link run, ảnh chụp log | Fully |
| **CI-2** | GH Actions | Cơ bản | Thêm cache Maven; upload báo cáo JaCoCo làm artifact; ghi `$GITHUB_STEP_SUMMARY` | **Thời gian build trước/sau cache** | Hai link run, artifact tải được | Fully |
| **CI-3** | GH Actions | Phức tạp | 3 job `test` → `coverage-gate` → `package`; matrix Java 21 + 25; chặn merge khi gate fail; một PR đỏ rồi sửa cho xanh | Job nào fail, vì sao | **Link PR có review đỏ rồi xanh**, log matrix | Fully |

## 4 demo AI

Chi tiết ở `docs/06-ke-hoach-ai.md` (link được thêm vào ở Task 5, sau khi file tồn tại).
Tóm tắt để đặt cạnh 9 demo trên:

| Mã | Làm gì | Đo gì | Minh chứng để lại | Mức tự động |
|---|---|---|---|---|
| **AI-1** | AI sinh unit test từ một class | Coverage trước/sau; **số test AI sinh sai phải sửa tay** | Prompt template, diff test do AI sinh, bảng đối chiếu | Semi (người review) |
| **AI-2** | AI đọc XML JaCoCo → chỉ nhánh chưa phủ → sinh test thiếu | Branch coverage trước/sau | Script, prompt, hai báo cáo | Semi |
| **AI-3** | AI review Pull Request trong pipeline | Số vấn đề thật / báo động giả trên 1 PR có lỗi cài sẵn | Workflow job, ảnh comment trên PR | Fully |
| **AI-4** | AI sinh bộ test data biên cho `@ParameterizedTest` | So bộ AI với bộ người viết: trùng bao nhiêu, bỏ sót gì | Prompt, file CSV, bảng đối chiếu | Semi |

## Ánh xạ sang 3 phần đề bài yêu cầu (dòng 22)

Đề đòi mỗi công cụ có **Record and Playback · Data driven · Checkpoints**. Cách nhóm ánh xạ
(**cần GV xác nhận** — xem [docs/08](08-cau-hoi-cho-gv.md)):

| Phần của đề | Demo tương ứng |
|---|---|
| **Record and Playback** | UT-1 (IDE generate test skeleton) · **AI-1** (AI sinh test = "record") · chạy lại bộ test đã sinh trong CI-1 (= "playback") |
| **Data driven** | UT-2 (`@ParameterizedTest` + `@CsvFileSource` đọc CSV ngoài) · **AI-4** (AI sinh dữ liệu biên) |
| **Checkpoints** | UT-3 (`verify`, `ArgumentCaptor`) · **CC-3** (`jacoco:check` fail build) · CI-3 (quality gate chặn merge) |

## Tổng kết số lượng

- 9 demo công cụ + 4 demo AI = **13 demo**.
- 3 công cụ chính × 3 kịch bản = đủ yêu cầu "ít nhất 3 kịch bản demo mỗi công cụ".
- Mỗi demo đều **fully** hoặc **semi-automated**, đúng yêu cầu dòng 21 của đề.
```

- [ ] **Step 2: Viết `docs/08-cau-hoi-cho-gv.md`**

Create `docs/08-cau-hoi-cho-gv.md`:

```markdown
# Câu hỏi cho GV — buổi gặp mặt Tuần 2–3

> Thứ tự đã xếp theo mức ảnh hưởng: câu 1–2 nếu trả lời khác đi thì nhóm phải làm lại
> phần lớn kế hoạch, nên hỏi trước.

## 1. Cách ánh xạ "Record and Playback / Data driven / Checkpoints" — **quan trọng nhất**

Dòng 22 của đề yêu cầu mỗi công cụ có đủ 3 phần này. Nhóm hiểu đây là khung của công cụ
automation UI (Selenium IDE, Katalon), không map tự nhiên vào Unit Test / Coverage / CI-CD.
Nhóm đề xuất ánh xạ:

| Phần của đề | Nhóm hiểu là | Demo |
|---|---|---|
| Record and Playback | Sinh test tự động thay vì gõ tay (IDE generate, **AI sinh test**), rồi chạy lại bộ test đó trong CI | UT-1, AI-1, CI-1 |
| Data driven | Một test chạy nhiều bộ dữ liệu: `@ParameterizedTest` + CSV ngoài | UT-2, AI-4 |
| Checkpoints | Điểm kiểm chứng làm **fail build**: assertion, `verify()`, coverage gate, quality gate | UT-3, CC-3, CI-3 |

**Hỏi:** cách hiểu này có được chấp nhận không? Nếu không, thầy/cô muốn nhóm hiểu thế nào?

## 2. Số lượng công cụ

Đề nói *"ít nhất 2-3 công cụ"*. Chủ đề có 3 trụ. Nhóm dự kiến **3 công cụ chính demo sâu**
(JUnit+Mockito, JaCoCo, GitHub Actions) + bảng khảo sát/so sánh các alternatives
(TestNG, Spock, Cobertura, OpenClover, PIT, Jenkins, GitLab CI, CircleCI).

**Hỏi:** như vậy đủ chưa, hay cần **2 công cụ demo sâu cho mỗi trụ** (tổng 6)?

## 3. Phần AI

Đề yêu cầu demo AI *"có khả năng tổng quát hóa, tái sử dụng"*. Nhóm hiểu là mỗi demo AI
phải để lại một **tài sản dùng lại được** (prompt template có tham số, hoặc script), không
chỉ là một lần chat. Dự kiến 4 demo: sinh test · vá lỗ hổng coverage · review PR trong
pipeline · sinh test data biên.

**Hỏi:** 4 demo này có đúng kỳ vọng không? Có cần thêm hướng nào (ví dụ AI sinh test case
từ tài liệu đặc tả thay vì từ code)?

## 4. Bài tập áp dụng

Đề yêu cầu *"tạo ra vài bài tập áp dụng có gợi ý thực hiện"*.

**Hỏi:** bao nhiêu bài là phù hợp? Mức độ: chỉ viết test cho code cho sẵn, hay bao gồm cả
dựng pipeline CI? Có cần đáp án kèm theo không?

## 5. Minh chứng phân công

Nhóm dự định dùng **GitHub Issues + GitHub Projects**, mỗi đầu việc một issue gán người,
commit/PR liên kết tới issue. Bảng tổng hợp sẽ ở `docs/07-phan-cong-nhom.md`.

**Hỏi:** cách này có được tính là minh chứng hợp lệ không, hay thầy/cô cần thêm biên bản
họp nhóm / bảng công theo tuần?

## 6. Mốc thời gian

**Hỏi:**
- Tuần 6 nộp bài chấm điểm là **ngày nào** cụ thể, nộp qua kênh nào (Moodle / email / link GitHub)?
- Buổi trình bày thử trước tuần seminar đặt lịch thế nào?
- Repo có cần để **public** không? (Nhóm muốn để public để GitHub Actions miễn phí không
  giới hạn và log run dùng làm minh chứng được.)

## 7. Phạm vi kỹ thuật

Nhóm chọn Java 25 + Spring Boot 4.1.1 + JUnit Jupiter 6. Tài liệu phổ thông phần lớn viết
cho Spring Boot 3 / JUnit 5.

**Hỏi:** thầy/cô có muốn nhóm hạ xuống phiên bản phổ biến hơn (Java 21 + Spring Boot 3.5)
để các bạn trong lớp dễ làm theo, hay giữ bản mới và ghi chú rõ điểm khác biệt?
```

- [ ] **Step 3: Thêm link vào README**

Trong `README.md`, thêm 2 dòng vào bảng "Tài liệu":

```markdown
| [Ma trận demo](docs/05-ma-tran-demo.md) | 13 demo: làm gì, đo gì, để lại minh chứng gì |
| [Câu hỏi cho GV](docs/08-cau-hoi-cho-gv.md) | 7 câu cần hỏi ở buổi gặp mặt |
```

- [ ] **Step 4: Chạy script kiểm tra**

Run: `node scripts/check-repo.mjs`

Expected: PASS. (`docs/05` cố ý **không** đặt link tới `docs/06-ke-hoach-ai.md` vì file đó
chỉ xuất hiện ở Task 5; Task 5 sẽ thay chữ thường đó thành link thật.)

- [ ] **Step 5: Commit**

```bash
git add docs/05-ma-tran-demo.md docs/08-cau-hoi-cho-gv.md README.md
git commit -m "docs: ma tran 13 demo va danh sach cau hoi cho GV"
```

---

## Task 5: Kế hoạch 4 demo AI + quy ước sử dụng AI

**Files:**
- Create: `docs/06-ke-hoach-ai.md`
- Create: `docs/09-quy-uoc-su-dung-ai.md`
- Modify: `docs/05-ma-tran-demo.md` (đổi chữ thường `docs/06-ke-hoach-ai.md` thành link thật)
- Modify: `README.md` (thêm link)

**Interfaces:**
- Consumes: mã `AI-1..4` từ Task 4.
- Produces: đường dẫn tài sản mà Gói 5 phải tạo đúng tên: `ai/prompts/01-sinh-unit-test.md`,
  `ai/prompts/02-va-lo-hong-coverage.md`, `ai/prompts/04-sinh-test-data.md`,
  `ai/scripts/jacoco-to-prompt.mjs`. Gói này **chỉ lên kế hoạch**, không tạo các file đó.

- [ ] **Step 1: Viết `docs/06-ke-hoach-ai.md`**

Create `docs/06-ke-hoach-ai.md`:

```markdown
# Kế hoạch 4 demo AI

> Phụ trách: **TV5**. Đề yêu cầu *"trình bày khả năng áp dụng AI vào chủ đề testing được
> giao seminar với các demo cụ thể, có khả năng tổng quát hóa, tái sử dụng"*.
>
> Nhóm hiểu **"tái sử dụng"** nghĩa là: mỗi demo phải để lại một **tài sản** (prompt
> template có tham số, hoặc script) mà người khác lấy về dùng cho project của họ được —
> không phải một đoạn chat chụp ảnh lại.

## Nguyên tắc chung

1. **Mỗi demo để lại một tài sản có đường dẫn cố định** (bảng dưới). Tài sản là file trong
   repo, không phải ảnh chụp.
2. **Mỗi demo phải có số đo trước/sau.** AI nói "đã cải thiện" không tính; phải có con số.
3. **Báo cáo số lần AI làm sai.** Đây là phần trung thực nhất và cũng là phần GV khó thấy
   ở nhóm khác: AI sinh 12 test thì bao nhiêu test sai, sai kiểu gì, nhóm sửa thế nào.
4. **Không bao giờ để API key vào repo, slide, hay video.** Key đọc từ GitHub Secrets (trong
   CI) hoặc biến môi trường (chạy local). `scripts/check-repo.mjs` quét secret ở mọi commit.

## AI-1 — Sinh unit test từ source class

| | |
|---|---|
| **Mục tiêu** | Từ một class chưa có test, AI sinh bộ test JUnit + Mockito chạy được |
| **Đầu vào** | Source của `FineCalculator.java` (hoặc `LoanService.java`) |
| **Tài sản để lại** | `ai/prompts/01-sinh-unit-test.md` — prompt template có tham số `{{SOURCE}}`, `{{FRAMEWORK}}`, `{{RANG_BUOC}}` |
| **Đo gì** | Branch coverage trước/sau · số test AI sinh · **số test sai phải sửa tay** · thời gian người bỏ ra |
| **Minh chứng** | Prompt template · diff commit "test do AI sinh (chưa sửa)" → "test sau khi nhóm review" · hai báo cáo JaCoCo |
| **Mức tự động** | Semi-automated — người **bắt buộc** review trước khi commit |

**Cách làm tổng quát hóa được:** prompt template yêu cầu AI (a) liệt kê các nhánh của method
trước khi viết test, (b) viết một test cho mỗi nhánh, (c) dùng `@DisplayName` tiếng Việt,
(d) **không** được mock class chỉ chứa logic thuần. Ràng buộc (d) là bài học nhóm rút ra từ
điểm yếu của Mockito ở [docs/01](01-outline-unit-test.md).

**Checklist review bắt buộc** (đi kèm prompt template):
- [ ] Mỗi test có ít nhất một assertion?
- [ ] Assertion kiểm *giá trị kỳ vọng*, hay chỉ `assertNotNull`?
- [ ] `BigDecimal` so bằng `isEqualByComparingTo`, không phải `isEqualTo`?
- [ ] Có test nào chỉ xác nhận lại mock (tautology) không?
- [ ] Tên test nói được hành vi, hay chỉ `test1`, `test2`?

## AI-2 — Đọc báo cáo JaCoCo, vá lỗ hổng coverage

| | |
|---|---|
| **Mục tiêu** | Biến báo cáo coverage thành việc cụ thể: nhánh nào chưa phủ, test nào còn thiếu |
| **Đầu vào** | `case-study/target/site/jacoco/jacoco.xml` |
| **Tài sản để lại** | `ai/scripts/jacoco-to-prompt.mjs` (trích XML → danh sách nhánh chưa phủ kèm số dòng) + `ai/prompts/02-va-lo-hong-coverage.md` |
| **Đo gì** | Branch coverage trước/sau · số nhánh AI chỉ đúng / chỉ sai |
| **Minh chứng** | Script · output của script · prompt · hai báo cáo JaCoCo |
| **Mức tự động** | Semi-automated |

**Vì sao cần script chứ không dán cả file XML:** `jacoco.xml` của một project thật dài hàng
nghìn dòng, dán hết thì tốn token và AI dễ bỏ sót. Script lọc còn đúng phần `counter`
`type="BRANCH"` có `missed > 0`, kèm tên class, tên method, số dòng. Đây chính là chỗ
"tổng quát hóa": script chạy được với **bất kỳ** project Maven + JaCoCo nào.

## AI-3 — AI review Pull Request trong pipeline

| | |
|---|---|
| **Mục tiêu** | Mỗi PR được tự động nhận xét về *chất lượng test*, không chỉ về code |
| **Đầu vào** | Diff của PR (`git diff origin/master...HEAD`) |
| **Tài sản để lại** | Job `ai-review` trong `.github/workflows/ci.yml` + prompt nhúng trong job |
| **Đo gì** | Trên **một PR có lỗi cài sẵn**: số vấn đề thật AI tìm ra / số báo động giả |
| **Minh chứng** | File workflow · ảnh chụp comment AI trên PR · bảng đối chiếu "AI nói gì vs sự thật" |
| **Mức tự động** | **Fully automated** |

**Bảo mật — ràng buộc cứng:** API key chỉ nằm trong **GitHub Secrets**
(`${{ secrets.AI_API_KEY }}`). Không hard-code, không in ra log, không hiện trong video.
Job dùng `pull_request` trigger của chính repo (không phải fork) để secret khả dụng.

**Phương án dự phòng:** nếu chưa cấu hình được Secrets kịp, chạy bản local
(`ai/scripts/review-diff.mjs` đọc key từ biến môi trường `AI_API_KEY`) và chụp output.
Khi đó demo xuống mức semi-automated, và phải **ghi rõ** trong báo cáo là đã hạ mức.

**Lỗi cài sẵn trong PR mẫu** (để đo chất lượng review): một test không có assertion · một
test mock chính `FineCalculator` rồi assert lại giá trị mock · một `assertEquals` dùng
`BigDecimal.equals` nên sai vì khác scale · một nhánh nghiệp vụ mới thêm mà không có test.

## AI-4 — Sinh bộ test data biên cho `@ParameterizedTest`

| | |
|---|---|
| **Mục tiêu** | AI đề xuất các ca biên mà người viết dễ bỏ sót |
| **Đầu vào** | Đặc tả nghiệp vụ tính phí (bằng tiếng Việt) + signature `calculate(int, MemberTier)` |
| **Tài sản để lại** | `ai/prompts/04-sinh-test-data.md` + `case-study/src/test/resources/fines-ai.csv` |
| **Đo gì** | So bộ AI với bộ người viết: **trùng bao nhiêu ca · AI tìm thêm ca nào · AI bỏ sót ca nào** |
| **Minh chứng** | Prompt · hai file CSV (người viết & AI) · bảng đối chiếu 3 cột |
| **Mức tự động** | Semi-automated |

**Đây là phần khớp trực tiếp yêu cầu "Data driven" của đề** (xem [docs/05](05-ma-tran-demo.md)):
file CSV nạp vào `@CsvFileSource`, một test chạy nhiều bộ dữ liệu.

**Kỳ vọng thật (viết trước để đối chiếu sau, không sửa về sau):** nhóm dự đoán AI sẽ tìm ra
các ca `daysOverdue = 0`, đúng ngưỡng grace, vượt ngưỡng 1 ngày, và giá trị âm; nhưng sẽ
**bỏ sót** ca `Integer.MAX_VALUE` (tràn số) và ca `tier == null`. Ghi dự đoán này ra trước
khi chạy chính là phần "thể hiện công sức tìm hiểu" mà đề đòi.

## Tổng kết: AI thay thế được gì, không thay thế được gì

Đây là kết luận nhóm muốn lớp mang về:

| AI làm tốt | AI làm không tốt |
|---|---|
| Sinh bộ khung test nhanh (tiết kiệm thời gian gõ) | Quyết định *điều gì đáng kiểm chứng* |
| Liệt kê ca biên mà người hay quên | Hiểu nghiệp vụ thật đằng sau code |
| Đọc báo cáo coverage dài và chỉ ra chỗ thiếu | Biết nhánh nào **cố ý** không test |
| Nhắc lỗi phong cách test lặp lại | Tránh tạo test tautology (assert lại mock) |

→ Vị trí đúng của AI trong 3 trụ này: **tăng tốc bước gõ, không thay thế bước suy nghĩ.**
Mọi test do AI sinh đều phải qua checklist review của AI-1 trước khi vào repo.
```

- [ ] **Step 2: Viết `docs/09-quy-uoc-su-dung-ai.md`**

Create `docs/09-quy-uoc-su-dung-ai.md`:

```markdown
# Quy ước sử dụng AI của nhóm

> Đề cho phép dùng AI nhưng yêu cầu: *"nhóm SV cần phải review kết quả AI phát sinh ra,
> đảm bảo nội dung chính xác, rõ ràng, nhận trách nhiệm trên tài liệu phát sinh"*.
> File này là cam kết công khai của nhóm về cách làm điều đó.

## 1. Nhóm dùng AI ở đâu

| Hạng mục | Có dùng AI? | Dùng thế nào |
|---|---|---|
| Nội dung lý thuyết (slide, báo cáo) | Có | Soạn bản nháp và gợi ý cấu trúc; **mọi định nghĩa kỹ thuật đều được đối chiếu với tài liệu chính thức** của JUnit / JaCoCo / GitHub Docs trước khi đưa vào |
| Code case study | Có | Sinh bản nháp; nhóm đọc hiểu từng dòng, chạy test, mới commit |
| Unit test | Có | Demo AI-1, AI-4 — qua checklist review bắt buộc |
| Số đo (coverage, thời gian build) | **Không** | Mọi con số đều do nhóm chạy thật và chụp lại. Không có con số nào do AI phỏng đoán |
| Kết luận & đánh giá công cụ | **Không** | Nhận định về điểm yếu công cụ đều xuất phát từ việc nhóm tự gặp khi làm |
| Video demo | **Không** | Nhóm tự quay, tự thuyết minh |

## 2. Quy tắc review bắt buộc

Mọi nội dung do AI sinh ra phải qua **ba cửa** trước khi vào repo:

1. **Cửa chạy được:** code/test phải `mvn verify` xanh trên máy người review. Tài liệu phải
   `node scripts/check-repo.mjs` xanh.
2. **Cửa đối chiếu nguồn:** mỗi khẳng định kỹ thuật phải chỉ ra được nguồn chính thức
   (tài liệu JUnit, changelog JaCoCo, GitHub Docs). Không có nguồn thì xoá hoặc ghi rõ
   *"nhóm chưa kiểm"*.
3. **Cửa người ký tên:** commit phải do một thành viên cụ thể tạo. Người commit chịu trách
   nhiệm nội dung đó, kể cả khi AI viết.

## 3. Những điều nhóm tự quy định là **không** được làm

- Không dán nguyên output AI vào báo cáo mà chưa đọc lại.
- Không dùng số liệu AI "nhớ" được (ví dụ "JaCoCo nhanh hơn Cobertura 30%") — phải tự đo.
- Không để API key xuất hiện ở bất cứ đâu trong repo, slide, hay video.
- Không trích dẫn tài liệu/clip của người khác làm kết quả nộp (yêu cầu "chính chủ" của đề).

## 4. Ghi nhận AI trong báo cáo cuối

Báo cáo sẽ có một mục riêng ghi: dùng công cụ AI nào, ở bước nào, và **những lần AI làm sai
mà nhóm phát hiện** (kèm ví dụ cụ thể). Phần này không phải để tự phê — nó là bằng chứng
nhóm thực sự review chứ không chỉ sao chép.
```

- [ ] **Step 3: Biến chữ thường trong `docs/05` thành link thật**

Trong `docs/05-ma-tran-demo.md`, thay:

```markdown
Chi tiết ở `docs/06-ke-hoach-ai.md` (link được thêm vào ở Task 5, sau khi file tồn tại).
Tóm tắt để đặt cạnh 9 demo trên:
```

bằng:

```markdown
Chi tiết ở [docs/06](06-ke-hoach-ai.md). Tóm tắt để đặt cạnh 9 demo trên:
```

- [ ] **Step 4: Thêm link vào README**

Trong `README.md`, thêm 2 dòng vào bảng "Tài liệu":

```markdown
| [Kế hoạch demo AI](docs/06-ke-hoach-ai.md) | 4 demo AI, tài sản để lại, cách đo |
| [Quy ước sử dụng AI](docs/09-quy-uoc-su-dung-ai.md) | Nhóm dùng AI ở đâu và review thế nào |
```

- [ ] **Step 5: Chạy script kiểm tra**

Run: `node scripts/check-repo.mjs`

Expected: PASS. Script sẽ đọc `docs/06` có chuỗi `${{ secrets.AI_API_KEY }}` — đây **không**
khớp pattern secret nào (không có key thật) nên không báo lỗi. Nếu báo `SECRET`, nghĩa là
có key thật lọt vào — phải xoá ngay, **không** commit.

- [ ] **Step 6: Commit**

```bash
git add docs/06-ke-hoach-ai.md docs/09-quy-uoc-su-dung-ai.md docs/05-ma-tran-demo.md README.md
git commit -m "docs: ke hoach 4 demo AI va quy uoc su dung AI cua nhom"
```

---

## Task 6: Phân công 5 thành viên

**Files:**
- Create: `docs/07-phan-cong-nhom.md`
- Modify: `README.md` (thêm link)

**Interfaces:**
- Consumes: vai TV1–TV5 và ranh giới file đã chốt ở spec mục 9.
- Produces: bảng ranh giới file sở hữu — Task 7–16 phải tôn trọng (không có hai người sửa cùng một file trong cùng một gói).

- [ ] **Step 1: Viết `docs/07-phan-cong-nhom.md`**

Create `docs/07-phan-cong-nhom.md`:

```markdown
# Phân công nhóm

> Phụ trách: **TV1** (trưởng nhóm). Tên thật do nhóm điền vào cột "Thành viên" trước khi
> gặp GV. Vai trò và **ranh giới file** đã chốt để 5 người làm song song không tranh chấp.

## 1. Vai trò và ranh giới file

| Vai | Thành viên | Phụ trách nội dung | File sở hữu (chỉ người này sửa) |
|---|---|---|---|
| **TV1** — Trưởng nhóm / CI-CD | *(điền tên)* | GitHub Actions, GitHub Projects, tổng hợp đề xuất trình GV | `.github/workflows/**`, `docs/00`, `docs/03`, `docs/07` |
| **TV2** — Unit Test | *(điền tên)* | Lý thuyết unit test, JUnit + Mockito | `docs/01`, `case-study/**/LoanServiceTest.java` |
| **TV3** — Coverage | *(điền tên)* | JaCoCo, mutation testing, luận điểm "coverage ≠ chất lượng" | `docs/02`, phần JaCoCo + PIT trong `case-study/pom.xml` |
| **TV4** — Case study | *(điền tên)* | Code nghiệp vụ, `FineCalculator`, controller | `case-study/src/main/**`, `FineCalculatorTest.java`, `LoanControllerTest.java` |
| **TV5** — AI & trình bày | *(điền tên)* | 4 demo AI, slide HTML, báo cáo LaTeX | `docs/06`, `docs/09`, `slides/**`, `report/**` |

**Việc chung** (mỗi người viết phần công cụ mình phụ trách, TV1 ghép lại):
`docs/04-khao-sat-so-sanh-cong-cu.md` · `docs/05-ma-tran-demo.md` · `docs/08-cau-hoi-cho-gv.md`

## 2. Minh chứng phân công

Đề yêu cầu *"các đợt tính điểm cần thể hiện rõ ràng công việc của các thành viên (kèm minh
chứng)"*. Nhóm dùng ba lớp minh chứng, không phải một:

| Lớp | Minh chứng | Lấy ở đâu |
|---|---|---|
| 1. Việc được giao | **GitHub Issue** cho mỗi đầu việc, gán đúng người, gắn label theo trụ (`unit-test` / `coverage` / `cicd` / `ai` / `trinh-bay`) | Tab Issues |
| 2. Việc đã làm | **Commit** có tên tác giả, nội dung commit dẫn số issue (`#12`) | `git log` |
| 3. Tiến độ theo thời gian | **GitHub Projects** dạng board, cột `Dự kiến` → `Đang làm` → `Chờ review` → `Xong` | Tab Projects |

**Bảng tổng hợp đóng băng theo mốc nộp:** mỗi mốc (Tuần 6, Tuần 12) TV1 chạy
`git shortlog -sn --since=<ngày bắt đầu>` và `gh issue list --assignee <người>`, dán kết quả
vào một mục của file này kèm ngày chốt. Số liệu đóng băng chứ không để người đọc tự tra.

> **Chưa thực hiện ở gói này.** Việc tạo Issues / Projects chạm tới GitHub nên phải được
> chủ repo đồng ý trước; xem *Ràng buộc* trong [kế hoạch gói gặp mặt](superpowers/plans/2026-10-01-goi-gap-mat-tuan-2-3.md).

## 3. Quy tắc làm việc nhóm

1. **Một đầu việc = một issue = một nhánh = một PR.** Không commit trực tiếp lên `master`
   sau khi repo đã bật nhánh bảo vệ.
2. **PR phải xanh CI mới merge.** Coverage gate là một phần của CI → không ai merge được
   code làm tụt coverage của `FineCalculator` dưới 90%.
3. **Không sửa file người khác sở hữu.** Cần sửa thì mở issue gán cho chủ file.
4. **Họp chốt tiến độ mỗi tuần một lần**, TV1 ghi 5 dòng vào issue tương ứng — không cần
   biên bản dài, nhưng phải có dấu vết theo thời gian.
5. **Người commit chịu trách nhiệm nội dung**, kể cả phần do AI sinh (xem
   [quy ước sử dụng AI](09-quy-uoc-su-dung-ai.md)).

## 4. Phân công cho gói gặp mặt Tuần 2–3

| Task trong kế hoạch | Người làm |
|---|---|
| Khung repo, script kiểm tra | TV1 |
| Outline Unit Test | TV2 |
| Outline Code Coverage | TV3 |
| Outline CI/CD | TV1 |
| Khảo sát & so sánh công cụ | Cả nhóm, TV1 ghép |
| Ma trận demo + câu hỏi cho GV | Cả nhóm, TV1 ghép |
| Kế hoạch AI + quy ước AI | TV5 |
| Phân công nhóm | TV1 |
| Case study: skeleton, `FineCalculator`, entity, controller | TV4 |
| Case study: `LoanService` + test Mockito | TV2 |
| JaCoCo + coverage gate + PIT | TV3 |
| GitHub Actions workflow | TV1 |
| Slide HTML + báo cáo `.tex` | TV5 |
| Đề xuất tổng hợp trình GV | TV1 |
```

- [ ] **Step 2: Thêm link vào README**

Trong `README.md`, thêm dòng vào bảng "Tài liệu":

```markdown
| [Phân công nhóm](docs/07-phan-cong-nhom.md) | Vai trò, ranh giới file, 3 lớp minh chứng |
```

- [ ] **Step 3: Chạy script kiểm tra**

Run: `node scripts/check-repo.mjs`

Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add docs/07-phan-cong-nhom.md README.md
git commit -m "docs: phan cong 5 thanh vien, ranh gioi file va 3 lop minh chung"
```

---

## Task 7: Sinh khung case study bằng Spring Initializr

**Files:**
- Create: `case-study/` (toàn bộ, do Initializr sinh: `pom.xml`, `mvnw`, `mvnw.cmd`, `.mvn/`, `src/main/java/vn/edu/hcmus/fit/library/LibraryApplication.java`, `src/main/resources/application.properties`, `src/test/java/vn/edu/hcmus/fit/library/LibraryApplicationTests.java`)

**Interfaces:**
- Consumes: không có.
- Produces: package gốc `vn.edu.hcmus.fit.library`; `pom.xml` kế thừa `spring-boot-starter-parent:4.1.1` với `<java.version>25</java.version>`; các starter `web`, `data-jpa`, `validation`, `h2` (scope `runtime`), `spring-boot-starter-test`. Mọi task sau chạy Maven bằng `mvn -f case-study/pom.xml ...` từ gốc repo.

> **Vì sao sinh bằng Initializr chứ không tự viết `pom.xml`:** Spring Boot 4 đã tách lại
> module so với Boot 3, nên `pom.xml` viết tay theo ký ức rất dễ sai tên artifact.
> Initializr là nguồn chính thức — lấy từ đó rồi kiểm lại bằng `mvn test`.

- [ ] **Step 1: Sinh project từ Spring Initializr**

Run (từ gốc repo):

```bash
curl -sS --max-time 90 https://start.spring.io/starter.zip \
  -d type=maven-project \
  -d language=java \
  -d bootVersion=4.1.1 \
  -d javaVersion=25 \
  -d groupId=vn.edu.hcmus.fit \
  -d artifactId=library \
  -d name=library \
  -d description="Case study seminar Unit Test - Code Coverage - CI/CD" \
  -d packageName=vn.edu.hcmus.fit.library \
  -d dependencies=web,data-jpa,validation,h2 \
  -d baseDir=case-study \
  -o case-study.zip
tar -xf case-study.zip
rm case-study.zip
```

Expected: thư mục `case-study/` xuất hiện với `pom.xml`, `mvnw`, `src/`.

> `tar -xf` dùng bsdtar có sẵn trên Windows 10/11, không cần cài `unzip`.

- [ ] **Step 2: Kiểm phiên bản trong `pom.xml` đúng như đã chốt**

Run:

```bash
grep -E "<(version|java\.version|artifactId)>" case-study/pom.xml | head -20
```

Expected: thấy `<version>4.1.1</version>` (của parent), `<java.version>25</java.version>`,
và các artifactId `spring-boot-starter-web`, `spring-boot-starter-data-jpa`,
`spring-boot-starter-validation`, `h2`, `spring-boot-starter-test`.

Nếu phiên bản parent khác `4.1.1`: **dừng lại**, Initializr đã đổi bản mặc định — báo lại
cho nhóm và cập nhật spec thay vì tự chọn bản khác.

- [ ] **Step 3: Chạy test do Initializr sinh để xác nhận môi trường đúng**

Run: `mvn -f case-study/pom.xml -B test`

Expected: PASS — `LibraryApplicationTests.contextLoads` chạy xanh, `Tests run: 1, Failures: 0`.
Đây là bằng chứng Java 25 + Spring Boot 4.1.1 + H2 khớp nhau trên máy nhóm.

Nếu FAIL vì H2 không tự cấu hình được datasource: thêm vào
`case-study/src/main/resources/application.properties`:

```properties
spring.datasource.url=jdbc:h2:mem:library;DB_CLOSE_DELAY=-1
spring.datasource.driver-class-name=org.h2.Driver
spring.jpa.hibernate.ddl-auto=update
```

rồi chạy lại `mvn -f case-study/pom.xml -B test`.

- [ ] **Step 4: Commit**

```bash
git add case-study
git commit -m "feat: khung case study Spring Boot 4.1.1 + Java 25 sinh tu Spring Initializr"
```

---

## Task 8: `FineCalculator` theo TDD + data-driven test

**Files:**
- Create: `case-study/src/main/java/vn/edu/hcmus/fit/library/domain/MemberTier.java`
- Create: `case-study/src/main/java/vn/edu/hcmus/fit/library/fine/FineCalculator.java`
- Test: `case-study/src/test/java/vn/edu/hcmus/fit/library/fine/FineCalculatorTest.java`
- Create: `case-study/src/test/resources/fines.csv`

**Interfaces:**
- Consumes: package gốc `vn.edu.hcmus.fit.library` từ Task 7.
- Produces:
  - `enum MemberTier { STANDARD, STUDENT, PREMIUM }` với 3 accessor: `BigDecimal fineMultiplier()`, `int borrowLimit()`, `int graceDays()`.
  - `class FineCalculator` (POJO, không annotation Spring) với `BigDecimal calculate(int daysOverdue, MemberTier tier)`, hai hằng `public static final BigDecimal RATE_PER_DAY`, `MAX_FINE`.
  - Task 10 (`LoanService`) nhận `FineCalculator` qua constructor; Task 11 dùng `MemberTier`.

> **Đây là task để demo UT-2 (TDD + Data driven) và CC-2/CC-3 (branch coverage).** Commit
> từng vòng đỏ–xanh riêng biệt — chính commit history là minh chứng "thể hiện các bước làm".

### Vòng TDD 1 — không tính phí trong thời gian gia hạn

- [ ] **Step 1: Viết `MemberTier` (dữ liệu nghiệp vụ, không cần TDD)**

Create `case-study/src/main/java/vn/edu/hcmus/fit/library/domain/MemberTier.java`:

```java
package vn.edu.hcmus.fit.library.domain;

import java.math.BigDecimal;

/**
 * Hạng thành viên. Mỗi hạng quy định hệ số phí trễ, hạn mức số sách được mượn
 * cùng lúc, và số ngày được gia hạn miễn phí trước khi tính phí.
 */
public enum MemberTier {
    STANDARD(new BigDecimal("1.0"), 5, 3),
    STUDENT(new BigDecimal("0.8"), 3, 3),
    PREMIUM(new BigDecimal("0.5"), 10, 6);

    private final BigDecimal fineMultiplier;
    private final int borrowLimit;
    private final int graceDays;

    MemberTier(BigDecimal fineMultiplier, int borrowLimit, int graceDays) {
        this.fineMultiplier = fineMultiplier;
        this.borrowLimit = borrowLimit;
        this.graceDays = graceDays;
    }

    /** Hệ số nhân vào phí cơ bản. */
    public BigDecimal fineMultiplier() {
        return fineMultiplier;
    }

    /** Số sách được mượn cùng lúc tối đa. */
    public int borrowLimit() {
        return borrowLimit;
    }

    /** Số ngày trễ đầu tiên được miễn phí. */
    public int graceDays() {
        return graceDays;
    }
}
```

- [ ] **Step 2: Viết test đầu tiên (chưa có `FineCalculator`)**

Create `case-study/src/test/java/vn/edu/hcmus/fit/library/fine/FineCalculatorTest.java`:

```java
package vn.edu.hcmus.fit.library.fine;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import vn.edu.hcmus.fit.library.domain.MemberTier;

class FineCalculatorTest {

    private final FineCalculator calculator = new FineCalculator();

    @Test
    @DisplayName("Trả trễ trong thời gian gia hạn thì không bị phí")
    void khongTinhPhiTrongThoiGianGiaHan() {
        // Arrange: STANDARD được gia hạn 3 ngày
        int daysOverdue = 3;

        // Act
        BigDecimal fine = calculator.calculate(daysOverdue, MemberTier.STANDARD);

        // Assert — BigDecimal phải so bằng compareTo, không phải equals
        assertThat(fine).isEqualByComparingTo(BigDecimal.ZERO);
    }
}
```

- [ ] **Step 3: Chạy test để chắc nó đỏ**

Run: `mvn -f case-study/pom.xml -B test -Dtest=FineCalculatorTest`

Expected: FAIL khi biên dịch — `cannot find symbol: class FineCalculator`. Đây là màu **đỏ**
đầu tiên của vòng TDD.

- [ ] **Step 4: Viết bản cài đặt tối thiểu cho test này**

Create `case-study/src/main/java/vn/edu/hcmus/fit/library/fine/FineCalculator.java`:

```java
package vn.edu.hcmus.fit.library.fine;

import java.math.BigDecimal;
import vn.edu.hcmus.fit.library.domain.MemberTier;

/**
 * Tính phí trả sách trễ. Logic thuần, không phụ thuộc Spring — đây là đơn vị
 * dễ unit test nhất trong case study, và là lớp dùng để demo branch coverage.
 */
public class FineCalculator {

    public BigDecimal calculate(int daysOverdue, MemberTier tier) {
        return BigDecimal.ZERO;
    }
}
```

- [ ] **Step 5: Chạy test để chắc nó xanh**

Run: `mvn -f case-study/pom.xml -B test -Dtest=FineCalculatorTest`

Expected: PASS — `Tests run: 1, Failures: 0`.

- [ ] **Step 6: Commit vòng 1**

```bash
git add case-study/src/main/java/vn/edu/hcmus/fit/library/domain/MemberTier.java case-study/src/main/java/vn/edu/hcmus/fit/library/fine/FineCalculator.java case-study/src/test/java/vn/edu/hcmus/fit/library/fine/FineCalculatorTest.java
git commit -m "feat(fine): vong TDD 1 - khong tinh phi trong thoi gian gia han"
```

### Vòng TDD 2 — tính phí theo số ngày và hệ số hạng thành viên

- [ ] **Step 7: Thêm test cho phần tính phí thật**

Trong `FineCalculatorTest.java`, thêm hai test sau vào trong class:

```java
    @Test
    @DisplayName("Quá thời gian gia hạn thì tính 2000d mỗi ngày cho hang STANDARD")
    void tinhPhiTheoNgayChoHangStandard() {
        BigDecimal fine = calculator.calculate(4, MemberTier.STANDARD);

        // 4 ngày trễ - 3 ngày gia hạn = 1 ngày chịu phí; 1 x 2000 x 1.0
        assertThat(fine).isEqualByComparingTo(new BigDecimal("2000"));
    }

    @Test
    @DisplayName("Hang STUDENT duoc giam con 0.8 lan phi co ban")
    void apDungHeSoGiamChoHangStudent() {
        BigDecimal fine = calculator.calculate(5, MemberTier.STUDENT);

        // 5 - 3 = 2 ngày chịu phí; 2 x 2000 x 0.8 = 3200
        assertThat(fine).isEqualByComparingTo(new BigDecimal("3200"));
    }
```

- [ ] **Step 8: Chạy test để chắc nó đỏ**

Run: `mvn -f case-study/pom.xml -B test -Dtest=FineCalculatorTest`

Expected: FAIL — 2 test mới đỏ với `expected: 2000 but was: 0` và `expected: 3200 but was: 0`.
Test của vòng 1 vẫn xanh.

- [ ] **Step 9: Cài đặt công thức tính phí**

Thay toàn bộ nội dung `FineCalculator.java` bằng:

```java
package vn.edu.hcmus.fit.library.fine;

import java.math.BigDecimal;
import vn.edu.hcmus.fit.library.domain.MemberTier;

/**
 * Tính phí trả sách trễ. Logic thuần, không phụ thuộc Spring — đây là đơn vị
 * dễ unit test nhất trong case study, và là lớp dùng để demo branch coverage.
 */
public class FineCalculator {

    /** Phí cơ bản cho mỗi ngày trễ, đơn vị VND. */
    public static final BigDecimal RATE_PER_DAY = new BigDecimal("2000");

    public BigDecimal calculate(int daysOverdue, MemberTier tier) {
        int chargeableDays = daysOverdue - tier.graceDays();
        if (chargeableDays <= 0) {
            return BigDecimal.ZERO;
        }
        return RATE_PER_DAY
                .multiply(BigDecimal.valueOf(chargeableDays))
                .multiply(tier.fineMultiplier());
    }
}
```

- [ ] **Step 10: Chạy test để chắc cả 3 test xanh**

Run: `mvn -f case-study/pom.xml -B test -Dtest=FineCalculatorTest`

Expected: PASS — `Tests run: 3, Failures: 0`.

- [ ] **Step 11: Commit vòng 2**

```bash
git add case-study/src/main/java/vn/edu/hcmus/fit/library/fine/FineCalculator.java case-study/src/test/java/vn/edu/hcmus/fit/library/fine/FineCalculatorTest.java
git commit -m "feat(fine): vong TDD 2 - tinh phi theo so ngay va he so hang thanh vien"
```

### Vòng TDD 3 — mức phí tối đa và đầu vào không hợp lệ

> Ba test dưới đây là **Review Focus 1, 2, 3**: ngày trễ âm, `tier` null, và ngày trễ cực lớn.

- [ ] **Step 12: Thêm test cho mức trần và đầu vào không hợp lệ**

Trong `FineCalculatorTest.java`, thêm import:

```java
import static org.assertj.core.api.Assertions.assertThatThrownBy;
```

và thêm bốn test sau vào trong class:

```java
    @Test
    @DisplayName("Phi khong bao gio vuot muc toi da 100000d")
    void khongVuotMucPhiToiDa() {
        BigDecimal fine = calculator.calculate(100, MemberTier.STANDARD);

        // 97 ngày x 2000 = 194000, nhưng bị chặn ở 100000
        assertThat(fine).isEqualByComparingTo(new BigDecimal("100000"));
    }

    @Test
    @DisplayName("So ngay tre cuc lon van tra ve muc toi da, khong tran so")
    void soNgayTreCucLonKhongTranSo() {
        BigDecimal fine = calculator.calculate(Integer.MAX_VALUE, MemberTier.STANDARD);

        assertThat(fine).isEqualByComparingTo(FineCalculator.MAX_FINE);
    }

    @Test
    @DisplayName("So ngay tre am la du lieu sai, phai nem IllegalArgumentException")
    void soNgayTreAmThiNemLoi() {
        assertThatThrownBy(() -> calculator.calculate(-1, MemberTier.STANDARD))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("daysOverdue");
    }

    @Test
    @DisplayName("Hang thanh vien null phai nem IllegalArgumentException, khong phai NPE")
    void hangThanhVienNullThiNemLoiRoRang() {
        assertThatThrownBy(() -> calculator.calculate(5, null))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("tier");
    }
```

- [ ] **Step 13: Chạy test để chắc nó đỏ**

Run: `mvn -f case-study/pom.xml -B test -Dtest=FineCalculatorTest`

Expected: FAIL — 4 test mới đỏ. Riêng `hangThanhVienNullThiNemLoiRoRang` đỏ vì nhận
`NullPointerException` chứ không phải `IllegalArgumentException` — đúng điều Review Focus 2 lo.

- [ ] **Step 14: Hoàn thiện `FineCalculator`**

Thay toàn bộ nội dung `FineCalculator.java` bằng:

```java
package vn.edu.hcmus.fit.library.fine;

import java.math.BigDecimal;
import vn.edu.hcmus.fit.library.domain.MemberTier;

/**
 * Tính phí trả sách trễ. Logic thuần, không phụ thuộc Spring — đây là đơn vị
 * dễ unit test nhất trong case study, và là lớp dùng để demo branch coverage.
 *
 * <p>Bốn điểm rẽ nhánh trong {@link #calculate(int, MemberTier)} là nguồn của
 * demo branch coverage CC-2 / CC-3: ngày trễ âm, tier null, còn trong thời gian
 * gia hạn, và vượt mức phí tối đa.
 */
public class FineCalculator {

    /** Phí cơ bản cho mỗi ngày trễ, đơn vị VND. */
    public static final BigDecimal RATE_PER_DAY = new BigDecimal("2000");

    /** Mức phí tối đa cho một lượt mượn, đơn vị VND. */
    public static final BigDecimal MAX_FINE = new BigDecimal("100000");

    public BigDecimal calculate(int daysOverdue, MemberTier tier) {
        if (daysOverdue < 0) {
            throw new IllegalArgumentException("daysOverdue khong duoc am: " + daysOverdue);
        }
        if (tier == null) {
            throw new IllegalArgumentException("tier khong duoc null");
        }

        int chargeableDays = daysOverdue - tier.graceDays();
        if (chargeableDays <= 0) {
            return BigDecimal.ZERO;
        }

        BigDecimal fine = RATE_PER_DAY
                .multiply(BigDecimal.valueOf(chargeableDays))
                .multiply(tier.fineMultiplier());

        if (fine.compareTo(MAX_FINE) > 0) {
            return MAX_FINE;
        }
        return fine;
    }
}
```

- [ ] **Step 15: Chạy test để chắc cả 7 test xanh**

Run: `mvn -f case-study/pom.xml -B test -Dtest=FineCalculatorTest`

Expected: PASS — `Tests run: 7, Failures: 0`.

- [ ] **Step 16: Commit vòng 3**

```bash
git add case-study/src/main/java/vn/edu/hcmus/fit/library/fine/FineCalculator.java case-study/src/test/java/vn/edu/hcmus/fit/library/fine/FineCalculatorTest.java
git commit -m "feat(fine): vong TDD 3 - muc phi toi da va kiem tra dau vao khong hop le"
```

### Vòng 4 — chuyển sang data-driven test (phần "Data driven" của đề)

- [ ] **Step 17: Tạo file dữ liệu CSV**

Create `case-study/src/test/resources/fines.csv`:

```csv
daysOverdue,tier,expectedFine
0,STANDARD,0
3,STANDARD,0
4,STANDARD,2000
10,STANDARD,14000
100,STANDARD,100000
3,STUDENT,0
5,STUDENT,3200
6,PREMIUM,0
10,PREMIUM,4000
```

- [ ] **Step 18: Thêm `@ParameterizedTest` đọc CSV**

Trong `FineCalculatorTest.java`, thêm import:

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;
```

và thêm test sau vào trong class:

```java
    @ParameterizedTest(name = "tre {0} ngay, hang {1} -> phi {2}d")
    @CsvFileSource(resources = "/fines.csv", numLinesToSkip = 1)
    @DisplayName("Bang phi tru theo du lieu tu fines.csv (data-driven)")
    void tinhPhiTheoBangDuLieu(int daysOverdue, MemberTier tier, BigDecimal expectedFine) {
        BigDecimal fine = calculator.calculate(daysOverdue, tier);

        assertThat(fine).isEqualByComparingTo(expectedFine);
    }
```

- [ ] **Step 19: Chạy test để chắc 9 dòng CSV đều xanh**

Run: `mvn -f case-study/pom.xml -B test -Dtest=FineCalculatorTest`

Expected: PASS — `Tests run: 16, Failures: 0` (7 test cũ + 9 dòng dữ liệu).

Nếu có dòng đỏ: kiểm lại phép tính trong CSV bằng công thức
`(daysOverdue - graceDays) * 2000 * fineMultiplier`, chặn trên ở `100000`. Grace: STANDARD 3,
STUDENT 3, PREMIUM 6. Hệ số: STANDARD 1.0, STUDENT 0.8, PREMIUM 0.5.

- [ ] **Step 20: Commit vòng 4**

```bash
git add case-study/src/test/resources/fines.csv case-study/src/test/java/vn/edu/hcmus/fit/library/fine/FineCalculatorTest.java
git commit -m "test(fine): data-driven test doc du lieu tu fines.csv"
```

---
