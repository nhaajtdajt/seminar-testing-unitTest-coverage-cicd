#!/usr/bin/env python3
"""Generate crisp, minimalist, monochrome SVG diagrams for the seminar slides."""
import os

DIAGRAMS_DIR = 'slides/images/diagrams'
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

def save_svg(filename, content):
    path = os.path.join(DIAGRAMS_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f'Generated {path}')

# 1. three-layers.svg
save_svg('three-layers.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 240" width="100%" height="100%">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#111111"/>
    </marker>
  </defs>
  <!-- Layer 1 -->
  <g transform="translate(20, 20)">
    <rect width="220" height="200" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="220" height="40" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="110" y="26" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="15" fill="#111111">LỚP 1 · UNIT TEST</text>
    <text x="20" y="70" font-family="system-ui, sans-serif" font-weight="600" font-size="13" fill="#111111">• JUnit 5 + Mockito</text>
    <text x="20" y="95" font-family="system-ui, sans-serif" font-size="12" fill="#444444">• Kiểm đúng logic nghiệp vụ</text>
    <text x="20" y="120" font-family="system-ui, sans-serif" font-size="12" fill="#444444">• Dữ liệu biên: VIP, trần 50k</text>
    <text x="20" y="145" font-family="system-ui, sans-serif" font-size="12" fill="#444444">• Mock cô lập phụ thuộc</text>
    <rect x="20" y="165" width="180" height="24" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <text x="110" y="181" text-anchor="middle" font-family="monospace" font-size="11" fill="#111111">Tốc độ: &lt; 0.05s / test</text>
  </g>
  <!-- Arrow 1 to 2 -->
  <line x1="245" y1="120" x2="285" y2="120" stroke="#111111" stroke-width="2.5" marker-end="url(#arrow)"/>
  <!-- Layer 2 -->
  <g transform="translate(290, 20)">
    <rect width="220" height="200" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="220" height="40" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="110" y="26" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="15" fill="#111111">LỚP 2 · COVERAGE GATE</text>
    <text x="20" y="70" font-family="system-ui, sans-serif" font-weight="600" font-size="13" fill="#111111">• JaCoCo + PIT Mutation</text>
    <text x="20" y="95" font-family="system-ui, sans-serif" font-size="12" fill="#444444">• Branch coverage ≥ 90%</text>
    <text x="20" y="120" font-family="system-ui, sans-serif" font-size="12" fill="#444444">• Phát hiện nhánh bị bỏ quên</text>
    <text x="20" y="145" font-family="system-ui, sans-serif" font-size="12" fill="#444444">• Diệt 10/11 mutant kiểm thử</text>
    <rect x="20" y="165" width="180" height="24" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <text x="110" y="181" text-anchor="middle" font-family="monospace" font-size="11" fill="#111111">Ngưỡng: 90% Branch Gate</text>
  </g>
  <!-- Arrow 2 to 3 -->
  <line x1="515" y1="120" x2="555" y2="120" stroke="#111111" stroke-width="2.5" marker-end="url(#arrow)"/>
  <!-- Layer 3 -->
  <g transform="translate(560, 20)">
    <rect width="220" height="200" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="220" height="40" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="110" y="26" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="15" fill="#111111">LỚP 3 · CI/CD PIPELINE</text>
    <text x="20" y="70" font-family="system-ui, sans-serif" font-weight="600" font-size="13" fill="#111111">• GitHub Actions [JDK 25]</text>
    <text x="20" y="95" font-family="system-ui, sans-serif" font-size="12" fill="#444444">• Tự động chạy khi mở PR</text>
    <text x="20" y="120" font-family="system-ui, sans-serif" font-size="12" fill="#444444">• Required checks chặn lỗi</text>
    <text x="20" y="145" font-family="system-ui, sans-serif" font-size="12" fill="#444444">• Đóng gói artifact JAR</text>
    <rect x="20" y="165" width="180" height="24" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <text x="110" y="181" text-anchor="middle" font-family="monospace" font-size="11" fill="#111111">Pipeline: Chặn PR hỏng</text>
  </g>
</svg>''')

# 2. test-pyramid.svg
save_svg('test-pyramid.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 320" width="100%" height="100%">
  <!-- Smoke / E2E Level -->
  <polygon points="325,30 230,110 420,110" fill="#ffffff" stroke="#111111" stroke-width="2.5"/>
  <text x="325" y="75" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">HTTP Smoke Test</text>
  <text x="325" y="95" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#555555">JAR thật · 5 tình huống · H2 DB</text>

  <!-- Integration / Slice Level -->
  <polygon points="220,120 140,200 510,200 430,120" fill="#ffffff" stroke="#111111" stroke-width="2.5"/>
  <text x="325" y="155" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="14" fill="#111111">Integration &amp; Web Slice Tests</text>
  <text x="325" y="175" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#555555">MockMvc · Spring Data JPA · Controller ↔ Service</text>

  <!-- Unit Test Level -->
  <polygon points="130,210 30,300 620,300 520,210" fill="#f8f8f8" stroke="#111111" stroke-width="2.5"/>
  <text x="325" y="248" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="16" fill="#111111">Unit Tests (Core Suite)</text>
  <text x="325" y="272" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" fill="#333333">FineCalculatorTest · LoanServiceTest · @CsvFileSource · Mockito verify()</text>
  <text x="325" y="290" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#666666">Chạy trong milli-giây · Độc lập · Không phụ thuộc I/O</text>

  <!-- Side labels -->
  <line x1="580" y1="290" x2="580" y2="40" stroke="#111111" stroke-width="1.5" stroke-dasharray="4"/>
  <text x="590" y="50" font-family="system-ui, sans-serif" font-size="11" fill="#111111">Chậm hơn</text>
  <text x="590" y="285" font-family="system-ui, sans-serif" font-size="11" fill="#111111">Nhanh nhất</text>
</svg>''')

# 3. tdd-cycle.svg
save_svg('tdd-cycle.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 240" width="100%" height="100%">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#111111"/>
    </marker>
  </defs>
  <!-- Step 1: Red -->
  <g transform="translate(30, 40)">
    <circle cx="65" cy="65" r="55" fill="#ffffff" stroke="#111111" stroke-width="2.5"/>
    <text x="65" y="60" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="16" fill="#111111">1. RED</text>
    <text x="65" y="80" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#555555">Viết test fail</text>
  </g>
  <path d="M 160 80 Q 200 40 240 80" fill="none" stroke="#111111" stroke-width="2.5" marker-end="url(#arrow)"/>

  <!-- Step 2: Green -->
  <g transform="translate(245, 40)">
    <circle cx="65" cy="65" r="55" fill="#f4f4f4" stroke="#111111" stroke-width="2.5"/>
    <text x="65" y="60" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="16" fill="#111111">2. GREEN</text>
    <text x="65" y="80" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#555555">Code pass test</text>
  </g>
  <path d="M 375 80 Q 415 40 455 80" fill="none" stroke="#111111" stroke-width="2.5" marker-end="url(#arrow)"/>

  <!-- Step 3: Refactor -->
  <g transform="translate(460, 40)">
    <circle cx="65" cy="65" r="55" fill="#ffffff" stroke="#111111" stroke-width="2.5"/>
    <text x="65" y="55" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="15" fill="#111111">3. REFACTOR</text>
    <text x="65" y="75" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#555555">Dọn mã sạch</text>
    <text x="65" y="90" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#777777">Giữ test xanh</text>
  </g>
  <!-- Loop back -->
  <path d="M 485 165 C 380 230 220 230 115 165" fill="none" stroke="#111111" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="300" y="215" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-style="italic" fill="#555555">Lặp lại 4 vòng TDD (FineCalculator)</text>
</svg>''')

# 4. mutation-flow.svg
save_svg('mutation-flow.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 220" width="100%" height="100%">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#111111"/>
    </marker>
  </defs>
  <!-- Source Code -->
  <rect x="20" y="60" width="130" height="90" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <text x="85" y="98" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Mã nguồn gốc</text>
  <text x="85" y="120" text-anchor="middle" font-family="monospace" font-size="11" fill="#555555">days &gt; 25</text>

  <line x1="155" y1="105" x2="195" y2="105" stroke="#111111" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- PIT Mutation Engine -->
  <rect x="200" y="45" width="160" height="120" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="280" y="80" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="14" fill="#111111">PIT Mutator</text>
  <text x="280" y="105" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#444444">Cấy lỗi nhân tạo:</text>
  <text x="280" y="125" text-anchor="middle" font-family="monospace" font-size="11" fill="#111111">&gt; thành &gt;= hoặc &lt;</text>
  <text x="280" y="145" text-anchor="middle" font-family="monospace" font-size="11" fill="#111111">return 0 thay amount</text>

  <line x1="365" y1="105" x2="405" y2="105" stroke="#111111" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Test Suite Runs -->
  <rect x="410" y="45" width="140" height="120" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <text x="480" y="80" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Chạy Test Suite</text>
  <text x="480" y="105" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#555555">Kiểm tra kết quả</text>
  <text x="480" y="125" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#555555">với từng mutant</text>

  <line x1="555" y1="85" x2="595" y2="55" stroke="#111111" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="555" y1="125" x2="595" y2="155" stroke="#111111" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Result 1: Killed -->
  <rect x="600" y="25" width="140" height="60" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <text x="670" y="50" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">TEST FAIL: KILLED</text>
  <text x="670" y="70" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#333333">✓ Bộ test mạnh (10/11)</text>

  <!-- Result 2: Survived -->
  <rect x="600" y="130" width="140" height="60" rx="6" fill="#f8f8f8" stroke="#111111" stroke-width="2"/>
  <text x="670" y="155" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">TEST PASS: SURVIVED</text>
  <text x="670" y="175" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#555555">⚠ Thiếu assertion (3/11)</text>
</svg>''')

# 5. ci-pipeline.svg
save_svg('ci-pipeline.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 230" width="100%" height="100%">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#111111"/>
    </marker>
  </defs>
  <!-- Trigger Event -->
  <g transform="translate(10, 45)">
    <rect width="130" height="130" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <text x="65" y="45" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="14" fill="#111111">TRIGGER</text>
    <text x="65" y="75" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#444444">• Pull Request</text>
    <text x="65" y="98" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#444444">• Push to master</text>
    <text x="65" y="120" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#444444">• Workflow dispatch</text>
  </g>

  <line x1="145" y1="110" x2="175" y2="110" stroke="#111111" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Job 1: Test -->
  <g transform="translate(180, 25)">
    <rect width="170" height="170" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="170" height="35" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="85" y="23" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">JOB 1: test</text>
    <text x="15" y="60" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• JDK 25 setup</text>
    <text x="15" y="82" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Maven dependencies cache</text>
    <text x="15" y="104" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Run 39 Core Unit Tests</text>
    <text x="15" y="126" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Upload surefire reports</text>
    <rect x="15" y="138" width="140" height="20" rx="3" fill="#ffffff" stroke="#111111" stroke-width="1"/>
    <text x="85" y="152" text-anchor="middle" font-family="monospace" font-size="10" fill="#111111">Output: Exit Code 0</text>
  </g>

  <line x1="355" y1="110" x2="385" y2="110" stroke="#111111" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="370" y="100" text-anchor="middle" font-family="monospace" font-size="9" fill="#555555">needs</text>

  <!-- Job 2: Coverage Gate -->
  <g transform="translate(390, 25)">
    <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="180" height="35" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="90" y="23" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">JOB 2: coverage-gate</text>
    <text x="15" y="60" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• JaCoCo check rule</text>
    <text x="15" y="82" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Ngưỡng: Branch ≥ 90%</text>
    <text x="15" y="104" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Chặn thiếu test: PR #2 FAIL</text>
    <text x="15" y="126" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Step summary báo cáo</text>
    <rect x="15" y="138" width="150" height="20" rx="3" fill="#ffffff" stroke="#111111" stroke-width="1"/>
    <text x="90" y="152" text-anchor="middle" font-family="monospace" font-size="10" fill="#111111">Branch Gate: 0.90</text>
  </g>

  <line x1="575" y1="110" x2="605" y2="110" stroke="#111111" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="590" y="100" text-anchor="middle" font-family="monospace" font-size="9" fill="#555555">needs</text>

  <!-- Job 3: Package -->
  <g transform="translate(610, 25)">
    <rect width="160" height="170" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="160" height="35" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="80" y="23" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">JOB 3: package</text>
    <text x="15" y="60" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Maven package -DskipTests</text>
    <text x="15" y="85" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Đóng gói executable JAR</text>
    <text x="15" y="110" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Upload artifact</text>
    <rect x="15" y="138" width="130" height="20" rx="3" fill="#ffffff" stroke="#111111" stroke-width="1"/>
    <text x="80" y="152" text-anchor="middle" font-family="monospace" font-size="10" fill="#111111">Artifact: Ready</text>
  </g>
</svg>''')

# 6. ai-workflow.svg
save_svg('ai-workflow.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 220" width="100%" height="100%">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#111111"/>
    </marker>
  </defs>
  <!-- Step 1: Prompt Context -->
  <g transform="translate(15, 35)">
    <rect width="155" height="145" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="155" height="32" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="77" y="21" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">1. ĐỌC CONTEXT</text>
    <text x="12" y="55" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Source code nghiệp vụ</text>
    <text x="12" y="75" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Báo cáo JaCoCo gap</text>
    <text x="12" y="95" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Đặc tả mượn/trả sách</text>
    <text x="12" y="115" font-family="system-ui, sans-serif" font-size="11" fill="#555555">• Không hard-code prompt</text>
  </g>

  <line x1="175" y1="105" x2="200" y2="105" stroke="#111111" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Step 2: Gemini Generation -->
  <g transform="translate(205, 35)">
    <rect width="165" height="145" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="165" height="32" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="82" y="21" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">2. GEMINI 3.6 GENERATE</text>
    <text x="12" y="55" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• AI-1: 7 test LoanService</text>
    <text x="12" y="75" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• AI-2: 3 test bổ sung</text>
    <text x="12" y="95" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Dữ liệu biên: MAX_VALUE</text>
    <text x="12" y="115" font-family="system-ui, sans-serif" font-size="11" fill="#555555">• Sinh test candidate nháp</text>
  </g>

  <line x1="375" y1="105" x2="400" y2="105" stroke="#111111" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Step 3: Human Review & Repair -->
  <g transform="translate(405, 35)">
    <rect width="165" height="145" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="165" height="32" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="82" y="21" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">3. REVIEW &amp; REPAIR</text>
    <text x="12" y="55" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Chặn ảo giác assertion</text>
    <text x="12" y="75" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Chạy thử trên Java 25</text>
    <text x="12" y="95" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Đối chiếu oracle kết quả</text>
    <text x="12" y="115" font-family="system-ui, sans-serif" font-size="11" fill="#555555">• Người duyệt trước khi apply</text>
  </g>

  <line x1="575" y1="105" x2="600" y2="105" stroke="#111111" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Step 4: Apply & Merge -->
  <g transform="translate(605, 35)">
    <rect width="140" height="145" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="140" height="32" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="70" y="21" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">4. APPLY &amp; PASS</text>
    <text x="12" y="55" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• PR #13: 49 tests pass</text>
    <text x="12" y="78" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Branch: 24/24 (100%)</text>
    <text x="12" y="100" font-family="system-ui, sans-serif" font-size="11" fill="#111111">• Line: 76/83 (91.6%)</text>
    <text x="12" y="125" font-family="system-ui, sans-serif" font-size="11" fill="#555555">• Merge an toàn</text>
  </g>
</svg>''')

# 7. domain-rules.svg
save_svg('domain-rules.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 230" width="100%" height="100%">
  <!-- Normal tier card -->
  <g transform="translate(20, 20)">
    <rect width="300" height="190" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="300" height="40" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="150" y="26" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="15" fill="#111111">HẠNG NORMAL</text>
    <text x="20" y="70" font-family="system-ui, sans-serif" font-size="13" fill="#111111">• Đơn giá phạt: <tspan font-weight="700">2.000 VND / ngày trễ</tspan></text>
    <text x="20" y="98" font-family="system-ui, sans-serif" font-size="13" fill="#111111">• Miễn giảm gia hạn: <tspan font-weight="700">0 ngày</tspan> (tính từ ngày 1)</text>
    <text x="20" y="126" font-family="system-ui, sans-serif" font-size="13" fill="#111111">• Mức trần phạt: <tspan font-weight="700">50.000 VND</tspan> (từ ngày 25 trở đi)</text>
    <text x="20" y="154" font-family="system-ui, sans-serif" font-size="13" fill="#555555">• Ranh giới biên kiểm thử: 0, 1, 24, 25, 26 ngày</text>
  </g>
  <!-- VIP tier card -->
  <g transform="translate(360, 20)">
    <rect width="300" height="190" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="300" height="40" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="150" y="26" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="15" fill="#111111">HẠNG VIP</text>
    <text x="20" y="70" font-family="system-ui, sans-serif" font-size="13" fill="#111111">• Đơn giá phạt: <tspan font-weight="700">1.000 VND / ngày trễ</tspan></text>
    <text x="20" y="98" font-family="system-ui, sans-serif" font-size="13" fill="#111111">• Miễn giảm gia hạn: <tspan font-weight="700">2 ngày đầu miễn phí</tspan></text>
    <text x="20" y="126" font-family="system-ui, sans-serif" font-size="13" fill="#111111">• Mức trần phạt: <tspan font-weight="700">50.000 VND</tspan> (từ ngày 52 trở đi)</text>
    <text x="20" y="154" font-family="system-ui, sans-serif" font-size="13" fill="#555555">• Ranh giới biên kiểm thử: 0, 1, 2, 3, 51, 52 ngày</text>
  </g>
</svg>''')

# 8. benchmark-chart.svg
save_svg('benchmark-chart.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 220" width="100%" height="100%">
  <!-- Maven Cold Cache vs Warm Cache -->
  <text x="325" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="14" fill="#111111">THỰC NGHIỆM THỜI GIAN CHẠY MAVEN TRÊN JAVA 25</text>

  <!-- Bar 1: Cold Cache -->
  <text x="30" y="70" font-family="system-ui, sans-serif" font-weight="600" font-size="12" fill="#111111">Maven Cold Cache (Chưa cache)</text>
  <rect x="30" y="80" width="484" height="28" rx="4" fill="#111111"/>
  <text x="525" y="99" font-family="monospace" font-weight="700" font-size="13" fill="#111111">48.412s</text>

  <!-- Bar 2: Warm Cache -->
  <text x="30" y="135" font-family="system-ui, sans-serif" font-weight="600" font-size="12" fill="#111111">Maven Warm Cache (Đã cache ~/.m2)</text>
  <rect x="30" y="145" width="125" height="28" rx="4" fill="#555555"/>
  <text x="165" y="164" font-family="monospace" font-weight="700" font-size="13" fill="#111111">12.539s (-74%)</text>

  <line x1="30" y1="190" x2="600" y2="190" stroke="#cccccc" stroke-width="1"/>
  <text x="30" y="208" font-family="system-ui, sans-serif" font-size="11" fill="#666666">Ý nghĩa CI/CD: Cache dependency giúp giảm 74% thời gian chờ đợi trên mỗi lần push mã.</text>
</svg>''')

print("All diagrams generated successfully.")
