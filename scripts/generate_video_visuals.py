#!/usr/bin/env python3
"""Generate dedicated monochrome SVG diagrams for Video A, Video B, Video C, and All-Videos summary."""
import os

DIAGRAMS_DIR = 'slides/images/diagrams'
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

def save_svg(filename, content):
    path = os.path.join(DIAGRAMS_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f'Generated {path}')

# 1. video-a-timeline.svg (Video A: Unit Test - Bảo An)
save_svg('video-a-timeline.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 340" width="100%" height="100%">
  <rect width="620" height="340" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="620" height="38" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="24" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Video A: Unit Test với JUnit 5 &amp; Mockito (5–7 phút) · Nguyễn Bảo An</text>

  <!-- Player bar -->
  <g transform="translate(20, 50)">
    <rect width="580" height="36" rx="4" fill="#111111"/>
    <rect x="12" y="14" width="556" height="8" rx="3" fill="#444444"/>
    <rect x="12" y="14" width="280" height="8" rx="3" fill="#ffffff"/>
    <circle cx="292" cy="18" r="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <text x="525" y="28" font-family="monospace" font-size="10" fill="#ffffff">06:45</text>
  </g>

  <!-- 5 Segments -->
  <g transform="translate(20, 98)">
    <g transform="translate(0, 0)">
      <rect width="280" height="68" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[00:00 - 01:00] 1. SETUP MÔI TRƯỜNG</text>
      <text x="12" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Java 25, cấu trúc case-study, Maven Wrapper</text>
      <text x="12" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• pom.xml: spring-boot-starter-test</text>
    </g>
    <g transform="translate(300, 0)">
      <rect width="280" height="68" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[01:00 - 02:15] 2. KHÁI NIỆM &amp; UT-1</text>
      <text x="12" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Quy tắc AAA, chạy FineCalculatorTest</text>
      <text x="12" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Đọc báo cáo Surefire XML (Pass, Fail, Time)</text>
    </g>
    <g transform="translate(0, 78)">
      <rect width="280" height="68" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[02:15 - 03:45] 3. DATA-DRIVEN (UT-2)</text>
      <text x="12" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• fine-cases.csv quét ranh giới 0, 2, 25 ngày</text>
      <text x="12" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• @ParameterizedTest sinh tự động 15 test</text>
    </g>
    <g transform="translate(300, 78)">
      <rect width="280" height="68" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[03:45 - 05:15] 4. MOCKITO (UT-3)</text>
      <text x="12" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Cô lập 3 repo, test logic mượn LoanService</text>
      <text x="12" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• verify(never()) chặn lỗi, ArgumentCaptor</text>
    </g>
    <g transform="translate(0, 156)">
      <rect width="580" height="65" rx="4" fill="#fafafa" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[05:15 - 06:45] 5. TRƯỜNG HỢP HẠN CHẾ &amp; ANTI-PATTERNS</text>
      <text x="12" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Train Wreck Mocking (vi phạm Demeter) &amp; Self-fulfilling Prophecy (test lại stub)</text>
      <text x="12" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Cảnh báo lạm dụng mock logic thuần và JVM warning khi mock static/final</text>
    </g>
  </g>
</svg>''')

# 2. video-b-timeline.svg (Video B: Coverage & PIT - Nhật Đạt)
save_svg('video-b-timeline.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 340" width="100%" height="100%">
  <rect width="620" height="340" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="620" height="38" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="24" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Video B: Code Coverage &amp; PIT Mutation (8–9 phút) · Trương Nhật Đạt</text>

  <!-- Player bar -->
  <g transform="translate(20, 50)">
    <rect width="580" height="36" rx="4" fill="#111111"/>
    <rect x="12" y="14" width="556" height="8" rx="3" fill="#444444"/>
    <rect x="12" y="14" width="380" height="8" rx="3" fill="#ffffff"/>
    <circle cx="392" cy="18" r="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <text x="525" y="28" font-family="monospace" font-size="10" fill="#ffffff">08:30</text>
  </g>

  <!-- 5 Segments -->
  <g transform="translate(20, 98)">
    <g transform="translate(0, 0)">
      <rect width="280" height="68" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[00:00 - 01:00] 1. SETUP JACOCO &amp; PIT</text>
      <text x="12" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• pom.xml: cấu hình branch gate ≥ 90%</text>
      <text x="12" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• JaCoCo javaagent gắn vào bytecode</text>
    </g>
    <g transform="translate(300, 0)">
      <rect width="280" height="68" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[01:00 - 03:00] 2. CÁC LOẠI COVERAGE</text>
      <text x="12" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• LoanPeriodPolicy: 6 câu lệnh, 2 quyết định</text>
      <text x="12" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Chạy T1→T4: Statement, Decision, MC/DC</text>
    </g>
    <g transform="translate(0, 78)">
      <rect width="280" height="68" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[03:00 - 04:00] 3. DEMO TRƯỚC / SAU</text>
      <text x="12" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Baseline: FineCalculator 5/10 nhánh (50%)</text>
      <text x="12" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Bộ đầy đủ: 10/10 nhánh (100% Branch)</text>
    </g>
    <g transform="translate(300, 78)">
      <rect width="280" height="68" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[04:00 - 06:00] 4. GATE FAIL &amp; PIT</text>
      <text x="12" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Gate đỏ: baseline văng Exit code 1</text>
      <text x="12" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Test bẫy: 100% branch nhưng PIT diệt 3/11</text>
    </g>
    <g transform="translate(0, 156)">
      <rect width="580" height="65" rx="4" fill="#fafafa" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[06:00 - 08:30] 5. TRƯỜNG HỢP CÔNG CỤ KHÔNG XỬ LÝ ĐƯỢC</text>
      <text x="12" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Quyết định ẩn trong thư viện Math.min() lọt qua JaCoCo &amp; PIT mặc định</text>
      <text x="12" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Mutant tương đương (không thể diệt) &amp; Chi phí thời gian PIT (85s vs 22s test)</text>
    </g>
  </g>
</svg>''')

# 3. video-c-timeline.svg (Video C: Case Study HTTP - Thế Vinh)
save_svg('video-c-timeline.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 340" width="100%" height="100%">
  <rect width="620" height="340" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="620" height="38" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="24" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Video C: Ứng dụng Quản lý Thư viện &amp; HTTP Smoke Test (3–5 phút) · Nguyễn Lê Thế Vinh</text>

  <!-- Player bar -->
  <g transform="translate(20, 50)">
    <rect width="580" height="36" rx="4" fill="#111111"/>
    <rect x="12" y="14" width="556" height="8" rx="3" fill="#444444"/>
    <rect x="12" y="14" width="220" height="8" rx="3" fill="#ffffff"/>
    <circle cx="232" cy="18" r="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <text x="525" y="28" font-family="monospace" font-size="10" fill="#ffffff">04:30</text>
  </g>

  <!-- 4 Segments -->
  <g transform="translate(20, 98)">
    <g transform="translate(0, 0)">
      <rect width="280" height="95" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[00:00 - 01:00] 1. KHỞI CHẠY JAR</text>
      <text x="12" y="42" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Khởi chạy JAR thật trên JDK 25</text>
      <text x="12" y="60" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Nạp dữ liệu hạt giống (seed data)</text>
      <text x="12" y="78" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Cơ sở dữ liệu H2 in-memory sạch</text>
    </g>
    <g transform="translate(300, 0)">
      <rect width="280" height="95" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[01:00 - 02:30] 2. 7 KỊCH BẢN HTTP</text>
      <text x="12" y="42" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Chạy demo_case_study.sh tuần tự</text>
      <text x="12" y="60" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Mượn hợp lệ: HTTP 201 Created</text>
      <text x="12" y="78" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Mượn lại sách đó: 409 UNAVAILABLE</text>
    </g>
    <g transform="translate(0, 105)">
      <rect width="280" height="110" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[02:30 - 03:30] 3. CÁC TÌNH HUỐNG LỖI</text>
      <text x="12" y="42" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• 404 BOOK_NOT_FOUND (sách ảo)</text>
      <text x="12" y="60" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• 404 MEMBER_NOT_FOUND (khách ảo)</text>
      <text x="12" y="78" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• 409 UNPAID_FINE (chưa trả phí)</text>
      <text x="12" y="96" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Kiểm tra response JSON chuẩn</text>
    </g>
    <g transform="translate(300, 105)">
      <rect width="280" height="110" rx="4" fill="#fafafa" stroke="#111111" stroke-width="1.5"/>
      <text x="12" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[03:30 - 04:30] 4. ĐỐI CHIẾU VỚI TEST</text>
      <text x="12" y="42" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Chạy LoanFlowEdgeCaseTest</text>
      <text x="12" y="60" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Chứng minh kịch bản HTTP curl khớp</text>
      <text x="12" y="78" font-family="system-ui, sans-serif" font-size="10" fill="#444444">  hoàn toàn với test tích hợp tự động</text>
      <text x="12" y="96" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Dữ liệu reset sạch khi restart</text>
    </g>
  </g>
</svg>''')

# 4. all-videos-table.svg (Tổng hợp 5 video)
save_svg('all-videos-table.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 340" width="100%" height="100%">
  <rect width="640" height="340" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="640" height="38" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="24" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Danh mục 5 Video Demo Bắt Buộc của Nhóm 09 (Yêu cầu GV)</text>

  <!-- Table header -->
  <g transform="translate(15, 48)">
    <rect width="610" height="28" fill="#111111"/>
    <text x="15" y="18" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#ffffff">VIDEO</text>
    <text x="80" y="18" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#ffffff">CHỦ ĐỀ</text>
    <text x="240" y="18" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#ffffff">NGƯỜI QUAY</text>
    <text x="380" y="18" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#ffffff">THỜI LƯỢNG</text>
    <text x="490" y="18" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#ffffff">TRỌNG TÂM DEMO</text>
  </g>

  <!-- Row 1: Video A -->
  <g transform="translate(15, 78)">
    <rect width="610" height="46" fill="#ffffff" stroke="#eeeeee" stroke-width="1"/>
    <text x="15" y="27" font-family="monospace" font-weight="700" font-size="12" fill="#111111">Video A</text>
    <text x="80" y="20" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">Unit Test Core</text>
    <text x="80" y="36" font-family="system-ui, sans-serif" font-size="10" fill="#555555">JUnit 5, Mockito</text>
    <text x="240" y="27" font-family="system-ui, sans-serif" font-size="11" fill="#111111">Bảo An (23120207)</text>
    <text x="380" y="27" font-family="monospace" font-size="11" fill="#111111">5 – 7 phút</text>
    <text x="490" y="20" font-family="system-ui, sans-serif" font-size="10" fill="#111111">AAA, Data-driven CSV,</text>
    <text x="490" y="35" font-family="system-ui, sans-serif" font-size="10" fill="#555555">verify(never), Anti-patterns</text>
  </g>

  <!-- Row 2: Video C -->
  <g transform="translate(15, 126)">
    <rect width="610" height="46" fill="#fcfcfc" stroke="#eeeeee" stroke-width="1"/>
    <text x="15" y="27" font-family="monospace" font-weight="700" font-size="12" fill="#111111">Video C</text>
    <text x="80" y="20" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">REST &amp; Smoke</text>
    <text x="80" y="36" font-family="system-ui, sans-serif" font-size="10" fill="#555555">Spring Boot, H2</text>
    <text x="240" y="27" font-family="system-ui, sans-serif" font-size="11" fill="#111111">Thế Vinh (23120190)</text>
    <text x="380" y="27" font-family="monospace" font-size="11" fill="#111111">3 – 5 phút</text>
    <text x="490" y="20" font-family="system-ui, sans-serif" font-size="10" fill="#111111">Chạy JAR, 7 kịch bản HTTP,</text>
    <text x="490" y="35" font-family="system-ui, sans-serif" font-size="10" fill="#555555">Mã 201, 409, 404, Edge test</text>
  </g>

  <!-- Row 3: Video B -->
  <g transform="translate(15, 174)">
    <rect width="610" height="46" fill="#ffffff" stroke="#eeeeee" stroke-width="1"/>
    <text x="15" y="27" font-family="monospace" font-weight="700" font-size="12" fill="#111111">Video B</text>
    <text x="80" y="20" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">Coverage &amp; PIT</text>
    <text x="80" y="36" font-family="system-ui, sans-serif" font-size="10" fill="#555555">JaCoCo, PIT</text>
    <text x="240" y="27" font-family="system-ui, sans-serif" font-size="11" fill="#111111">Nhật Đạt (23120231)</text>
    <text x="380" y="27" font-family="monospace" font-size="11" fill="#111111">8 – 9 phút</text>
    <text x="490" y="20" font-family="system-ui, sans-serif" font-size="10" fill="#111111">6 loại coverage, Gate Fail,</text>
    <text x="490" y="35" font-family="system-ui, sans-serif" font-size="10" fill="#555555">Bẫy PIT, mutant tương đương</text>
  </g>

  <!-- Row 4: Video D -->
  <g transform="translate(15, 222)">
    <rect width="610" height="46" fill="#fcfcfc" stroke="#eeeeee" stroke-width="1"/>
    <text x="15" y="27" font-family="monospace" font-weight="700" font-size="12" fill="#111111">Video D</text>
    <text x="80" y="20" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">CI/CD Pipeline</text>
    <text x="80" y="36" font-family="system-ui, sans-serif" font-size="10" fill="#555555">GitHub Actions</text>
    <text x="240" y="27" font-family="system-ui, sans-serif" font-size="11" fill="#111111">Quang Vinh (23120202)</text>
    <text x="380" y="27" font-family="monospace" font-size="11" fill="#111111">8 – 9 phút</text>
    <text x="490" y="20" font-family="system-ui, sans-serif" font-size="10" fill="#111111">3 Jobs needs, PR đỏ/xanh,</text>
    <text x="490" y="35" font-family="system-ui, sans-serif" font-size="10" fill="#555555">PR #6 BLOCKED, Cache miss</text>
  </g>

  <!-- Row 5: Video E -->
  <g transform="translate(15, 270)">
    <rect width="610" height="46" fill="#ffffff" stroke="#eeeeee" stroke-width="1"/>
    <text x="15" y="27" font-family="monospace" font-weight="700" font-size="12" fill="#111111">Video E</text>
    <text x="80" y="20" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">AI &amp; Paper</text>
    <text x="80" y="36" font-family="system-ui, sans-serif" font-size="10" fill="#555555">Gemini, CoverUp</text>
    <text x="240" y="27" font-family="system-ui, sans-serif" font-size="11" fill="#111111">Gia An (23120205)</text>
    <text x="380" y="27" font-family="monospace" font-size="11" fill="#111111">8 – 10 phút</text>
    <text x="490" y="20" font-family="system-ui, sans-serif" font-size="10" fill="#111111">Gemini sinh/sửa test, đối chiếu,</text>
    <text x="490" y="35" font-family="system-ui, sans-serif" font-size="10" fill="#555555">Tái hiện CoverUp &amp; Pynguin</text>
  </g>
</svg>''')

print("All 4 video SVGs generated successfully.")
