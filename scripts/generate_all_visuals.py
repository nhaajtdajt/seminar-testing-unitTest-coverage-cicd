#!/usr/bin/env python3
"""Generate all missing monochrome SVG diagrams so every slide has a dedicated visual."""
import os

DIAGRAMS_DIR = 'slides/images/diagrams'
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

def save_svg(filename, content):
    path = os.path.join(DIAGRAMS_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f'Generated {path}')

# 1. roadmap-goals.svg (Slide 3)
save_svg('roadmap-goals.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340" width="100%" height="100%">
  <g transform="translate(10, 10)">
    <!-- Box 1 -->
    <rect x="0" y="0" width="280" height="150" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="280" height="34" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="15" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">1. VIẾT UNIT TEST CHUẨN</text>
    <text x="15" y="62" font-family="system-ui, sans-serif" font-size="12" fill="#333333">• Cấu trúc AAA, nguyên lý FIRST</text>
    <text x="15" y="87" font-family="system-ui, sans-serif" font-size="12" fill="#333333">• Parameterized test dữ liệu biên</text>
    <text x="15" y="112" font-family="system-ui, sans-serif" font-size="12" fill="#333333">• Dùng Mockito verify hành vi</text>
    <text x="15" y="134" font-family="monospace" font-size="11" font-weight="700" fill="#111111">Mục tiêu: Độc lập, phản hồi mili-giây</text>

    <!-- Box 2 -->
    <rect x="300" y="0" width="280" height="150" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="300" y="0" width="280" height="34" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="315" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">2. ĐO ĐỘ PHỦ &amp; PIT</text>
    <text x="315" y="62" font-family="system-ui, sans-serif" font-size="12" fill="#333333">• Phân tích Line vs Branch JaCoCo</text>
    <text x="315" y="87" font-family="system-ui, sans-serif" font-size="12" fill="#333333">• Thoát bẫy '100% độ phủ danh nghĩa'</text>
    <text x="315" y="112" font-family="system-ui, sans-serif" font-size="12" fill="#333333">• Mutation Testing diệt 10/11 mutant</text>
    <text x="315" y="134" font-family="monospace" font-size="11" font-weight="700" fill="#111111">Mục tiêu: Đánh giá chất lượng assertion</text>

    <!-- Box 3 -->
    <rect x="0" y="170" width="280" height="150" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="0" y="0" width="280" height="34" rx="6" transform="translate(0, 170)" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="15" y="193" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">3. CHỐT CHẶN CI TỰ ĐỘNG</text>
    <text x="15" y="232" font-family="system-ui, sans-serif" font-size="12" fill="#333333">• Pipeline 3 job: test → gate → package</text>
    <text x="15" y="257" font-family="system-ui, sans-serif" font-size="12" fill="#333333">• Gate branch ≥ 90% chặn PR hỏng</text>
    <text x="15" y="282" font-family="system-ui, sans-serif" font-size="12" fill="#333333">• Required checks bảo vệ master</text>
    <text x="15" y="304" font-family="monospace" font-size="11" font-weight="700" fill="#111111">Mục tiêu: Fail-fast, an toàn phát hành</text>

    <!-- Box 4 -->
    <rect x="300" y="170" width="280" height="150" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect x="300" y="0" width="280" height="34" rx="6" transform="translate(0, 170)" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="315" y="193" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">4. ĐÁNH GIÁ KIỂM THỬ AI</text>
    <text x="315" y="232" font-family="system-ui, sans-serif" font-size="12" fill="#333333">• Gemini 3.6 đọc gap &amp; sinh test</text>
    <text x="315" y="257" font-family="system-ui, sans-serif" font-size="12" fill="#333333">• Quy trình Review chặn ảo giác test</text>
    <text x="315" y="282" font-family="system-ui, sans-serif" font-size="12" fill="#333333">• Tái hiện CoverUp &amp; Pynguin paper</text>
    <text x="315" y="304" font-family="monospace" font-size="11" font-weight="700" fill="#111111">Mục tiêu: Thực nghiệm &amp; phản biện</text>
  </g>
</svg>''')

# 2. aaa-pattern.svg (Slide 5)
save_svg('aaa-pattern.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 300" width="100%" height="100%">
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#111111"/>
    </marker>
  </defs>
  <!-- Step 1 -->
  <g transform="translate(20, 20)">
    <rect width="560" height="70" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect width="130" height="70" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="65" y="42" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="14" fill="#111111">ARRANGE</text>
    <text x="150" y="32" font-family="monospace" font-size="12" fill="#111111">var calc = new FineCalculator();</text>
    <text x="150" y="52" font-family="system-ui, sans-serif" font-size="11" fill="#555555">Chuẩn bị đối tượng &amp; dữ liệu đầu vào (VIP trễ 3 ngày)</text>
  </g>

  <line x1="300" y1="95" x2="300" y2="115" stroke="#111111" stroke-width="2" marker-end="url(#arr)"/>

  <!-- Step 2 -->
  <g transform="translate(20, 115)">
    <rect width="560" height="70" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect width="130" height="70" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="65" y="42" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="14" fill="#111111">ACT</text>
    <text x="150" y="32" font-family="monospace" font-size="12" fill="#111111">var amount = calc.calculate(3, MemberTier.VIP);</text>
    <text x="150" y="52" font-family="system-ui, sans-serif" font-size="11" fill="#555555">Thực thi duy nhất một hành vi nghiệp vụ cần kiểm chứng</text>
  </g>

  <line x1="300" y1="190" x2="300" y2="210" stroke="#111111" stroke-width="2" marker-end="url(#arr)"/>

  <!-- Step 3 -->
  <g transform="translate(20, 210)">
    <rect width="560" height="70" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect width="130" height="70" rx="6" fill="#111111" stroke="#111111" stroke-width="2"/>
    <text x="65" y="42" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="14" fill="#ffffff">ASSERT</text>
    <text x="150" y="32" font-family="monospace" font-size="12" fill="#111111">assertThat(amount).isEqualByComparingTo("1000");</text>
    <text x="150" y="52" font-family="system-ui, sans-serif" font-size="11" fill="#555555">So sánh chính xác giá trị tiền tệ (tránh bẫy scale BigDecimal)</text>
  </g>
</svg>''')

# 3. first-principles.svg (Slide 6)
save_svg('first-principles.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 300" width="100%" height="100%">
  <!-- F.I.R.S.T Cards -->
  <g transform="translate(10, 15)">
    <g transform="translate(0, 0)">
      <rect width="112" height="110" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
      <rect width="112" height="30" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
      <text x="56" y="21" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="14" fill="#111111">F · FAST</text>
      <text x="10" y="55" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• &lt; 0.05s/test</text>
      <text x="10" y="75" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Không chờ I/O</text>
      <text x="10" y="95" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Phản hồi tức thì</text>
    </g>
    <g transform="translate(122, 0)">
      <rect width="112" height="110" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
      <rect width="112" height="30" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
      <text x="56" y="21" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="14" fill="#111111">I · INDEP.</text>
      <text x="10" y="55" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Độc lập hoàn toàn</text>
      <text x="10" y="75" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Thứ tự chạy</text>
      <text x="10" y="95" font-family="system-ui, sans-serif" font-size="10" fill="#333333">  không ảnh hưởng</text>
    </g>
    <g transform="translate(244, 0)">
      <rect width="112" height="110" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
      <rect width="112" height="30" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
      <text x="56" y="21" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="14" fill="#111111">R · REPEAT</text>
      <text x="10" y="55" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Clock.fixed()</text>
      <text x="10" y="75" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Chạy 100 lần</text>
      <text x="10" y="95" font-family="system-ui, sans-serif" font-size="10" fill="#333333">  kết quả như một</text>
    </g>
    <g transform="translate(366, 0)">
      <rect width="112" height="110" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
      <rect width="112" height="30" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
      <text x="56" y="21" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="14" fill="#111111">S · SELF-VAL</text>
      <text x="10" y="55" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Tự pass/fail</text>
      <text x="10" y="75" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Không cần người</text>
      <text x="10" y="95" font-family="system-ui, sans-serif" font-size="10" fill="#333333">  đọc log terminal</text>
    </g>
    <g transform="translate(488, 0)">
      <rect width="112" height="110" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
      <rect width="112" height="30" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
      <text x="56" y="21" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="14" fill="#111111">T · TIMELY</text>
      <text x="10" y="55" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Viết cùng mã</text>
      <text x="10" y="75" font-family="system-ui, sans-serif" font-size="10" fill="#333333">  hoặc trước (TDD)</text>
      <text x="10" y="95" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Thiết kế theo test</text>
    </g>
  </g>

  <!-- Hazard Alert Box -->
  <g transform="translate(10, 145)">
    <rect width="600" height="135" rx="6" fill="#fafafa" stroke="#111111" stroke-width="2"/>
    <rect width="600" height="30" rx="6" fill="#111111"/>
    <text x="300" y="20" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#ffffff">⚠ HAI BẪY KIỂM THỬ THƯỜNG GẶP</text>
    <text x="20" y="58" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">1. Assertionless Test:</text>
    <text x="180" y="58" font-family="system-ui, sans-serif" font-size="12" fill="#444444">Chỉ gọi hàm mà không assert → Pass xanh giả tạo, không bắt được lỗi!</text>
    <text x="20" y="88" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">2. Over-mocking:</text>
    <text x="180" y="88" font-family="system-ui, sans-serif" font-size="12" fill="#444444">Mock quá đà khiến test chỉ đang xác nhận lại chính các dòng stub vừa tạo.</text>
    <rect x="20" y="105" width="560" height="22" rx="3" fill="#ffffff" stroke="#111111" stroke-width="1"/>
    <text x="300" y="120" text-anchor="middle" font-family="monospace" font-size="11" font-weight="700" fill="#111111">Khắc phục: Tiêm Clock.fixed() &amp; Kiểm tra assertion bằng PIT Mutation</text>
  </g>
</svg>''')

# 4. surefire-report.svg (Slide 7)
save_svg('surefire-report.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="38" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="24" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Apache Maven Surefire · Báo cáo kết quả kiểm thử</text>
  <rect x="500" y="8" width="80" height="22" rx="3" fill="#111111"/>
  <text x="540" y="23" text-anchor="middle" font-family="monospace" font-size="11" font-weight="700" fill="#ffffff">PASSED</text>

  <!-- Metric row -->
  <g transform="translate(20, 55)">
    <rect width="125" height="75" rx="6" fill="#f8f8f8" stroke="#111111" stroke-width="1.5"/>
    <text x="62" y="28" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#555555">TESTS RUN</text>
    <text x="62" y="58" text-anchor="middle" font-family="monospace" font-weight="700" font-size="24" fill="#111111">49</text>
  </g>
  <g transform="translate(165, 55)">
    <rect width="125" height="75" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <text x="62" y="28" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#555555">FAILURES</text>
    <text x="62" y="58" text-anchor="middle" font-family="monospace" font-weight="700" font-size="24" fill="#111111">0</text>
  </g>
  <g transform="translate(310, 55)">
    <rect width="125" height="75" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <text x="62" y="28" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#555555">ERRORS</text>
    <text x="62" y="58" text-anchor="middle" font-family="monospace" font-weight="700" font-size="24" fill="#111111">0</text>
  </g>
  <g transform="translate(455, 55)">
    <rect width="125" height="75" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <text x="62" y="28" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#555555">SKIPPED</text>
    <text x="62" y="58" text-anchor="middle" font-family="monospace" font-weight="700" font-size="24" fill="#111111">0</text>
  </g>

  <!-- Evolution bar -->
  <g transform="translate(20, 150)">
    <rect width="560" height="50" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <text x="15" y="28" font-family="system-ui, sans-serif" font-weight="600" font-size="12" fill="#111111">Quy mô:</text>
    <text x="75" y="28" font-family="system-ui, sans-serif" font-size="12" fill="#444444">39 core tests ban đầu → 49 tests sau khi tích hợp 10 test Gemini (PR #13)</text>
    <rect x="420" y="14" width="125" height="22" rx="3" fill="#f0f0f0" stroke="#111111" stroke-width="1"/>
    <text x="482" y="29" text-anchor="middle" font-family="monospace" font-size="10" font-weight="700" fill="#111111">100% Pass JVM 25</text>
  </g>

  <!-- Command line -->
  <g transform="translate(20, 215)">
    <rect width="560" height="45" rx="4" fill="#f6f8fa" stroke="#111111" stroke-width="1"/>
    <text x="15" y="27" font-family="monospace" font-size="12" fill="#111111">$ ./mvnw -B -ntp clean test &gt;&gt; BUILD SUCCESS [Exit 0]</text>
  </g>
</svg>''')

# 5. loan-verification.svg (Slide 9)
save_svg('loan-verification.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 300" width="100%" height="100%">
  <!-- 6 scenarios grid -->
  <rect width="620" height="300" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="620" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">LoanService · 6 Tình huống nghiệp vụ &amp; Mockito Verification</text>

  <g transform="translate(15, 50)">
    <!-- 5 error branches -->
    <rect width="285" height="150" rx="6" fill="#fafafa" stroke="#111111" stroke-width="1.5"/>
    <text x="15" y="24" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">5 NHÁNH NGOẠI LỆ (FAIL-FAST):</text>
    <text x="15" y="48" font-family="system-ui, sans-serif" font-size="11" fill="#333333">1. Sách không tồn tại (BookNotFound)</text>
    <text x="15" y="70" font-family="system-ui, sans-serif" font-size="11" fill="#333333">2. Sách đã bị mượn (AlreadyBorrowed)</text>
    <text x="15" y="92" font-family="system-ui, sans-serif" font-size="11" fill="#333333">3. Thành viên không tồn tại</text>
    <text x="15" y="114" font-family="system-ui, sans-serif" font-size="11" fill="#333333">4. Đạt hạn mức tối đa 3 cuốn</text>
    <text x="15" y="136" font-family="system-ui, sans-serif" font-size="11" fill="#333333">5. Còn nợ phí phạt chưa thanh toán</text>

    <!-- 1 success branch -->
    <g transform="translate(300, 0)">
      <rect width="285" height="150" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="15" y="24" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">1 NHÁNH THÀNH CÔNG:</text>
      <text x="15" y="55" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• Đủ điều kiện mượn sách</text>
      <text x="15" y="80" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• Thiết lập ngày mượn &amp; hạn trả</text>
      <text x="15" y="105" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• Lưu phiếu mượn xuống repository</text>
      <rect x="15" y="120" width="255" height="22" rx="3" fill="#f0f0f0" stroke="#111111" stroke-width="1"/>
      <text x="142" y="135" text-anchor="middle" font-family="monospace" font-size="10" font-weight="700" fill="#111111">Tạo LoanRecord hợp lệ</text>
    </g>
  </g>

  <!-- Mockito code pattern -->
  <g transform="translate(15, 215)">
    <rect width="590" height="70" rx="6" fill="#f6f8fa" stroke="#111111" stroke-width="1.5"/>
    <text x="15" y="25" font-family="monospace" font-weight="700" font-size="12" fill="#111111">verify(loanRepository, never()).save(any());</text>
    <text x="15" y="45" font-family="system-ui, sans-serif" font-size="11" fill="#555555">✓ Chặn rò rỉ dữ liệu: Đảm bảo 5 nhánh ngoại lệ không bao giờ ghi rác xuống database.</text>
    <text x="15" y="60" font-family="system-ui, sans-serif" font-size="11" fill="#555555">✓ ArgumentCaptor: Bắt đối tượng LoanRecord để kiểm tra trạng thái mượn chi tiết.</text>
  </g>
</svg>''')

# 6. line-vs-branch.svg (Slide 11)
save_svg('line-vs-branch.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Phân biệt: Line Coverage vs. Branch Coverage</text>

  <!-- Code snippet example -->
  <g transform="translate(20, 50)">
    <rect width="560" height="60" rx="6" fill="#f6f8fa" stroke="#111111" stroke-width="1.5"/>
    <text x="15" y="26" font-family="monospace" font-size="12" fill="#111111">// Dòng lệnh chứa toán tử ba ngôi (ternary):</text>
    <text x="15" y="46" font-family="monospace" font-weight="700" font-size="13" fill="#111111">return (days &gt; 25) ? MAX_FINE : days * rate;</text>
  </g>

  <!-- Comparison boxes -->
  <g transform="translate(20, 125)">
    <!-- Case 1: Line coverage -->
    <rect width="270" height="135" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <text x="15" y="25" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">NẾU CHỈ TEST CA: days = 30</text>
    <text x="15" y="55" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• Dòng lệnh trên ĐÃ ĐƯỢC CHẠY QUA</text>
    <text x="15" y="80" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• <strong>Line Coverage = 100%</strong> (1/1 dòng)</text>
    <text x="15" y="105" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• Nhánh (days &lt;= 25) bị bỏ quên hoàn toàn!</text>
    <rect x="15" y="112" width="240" height="18" rx="2" fill="#f4f4f4" stroke="#111111" stroke-width="1"/>
    <text x="135" y="125" text-anchor="middle" font-family="monospace" font-size="10" font-weight="700" fill="#111111">Nguy cơ: Lọt lỗi nhánh False</text>

    <!-- Case 2: Branch coverage -->
    <g transform="translate(290, 0)">
      <rect width="270" height="135" rx="6" fill="#fafafa" stroke="#111111" stroke-width="1.5"/>
      <text x="15" y="25" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">JACOCO BRANCH COVERAGE:</text>
      <text x="15" y="55" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• Đếm cả 2 hướng: True và False</text>
      <text x="15" y="80" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• Nếu chỉ test days = 30: <strong>Branch = 50%</strong></text>
      <text x="15" y="105" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• Bắt buộc thêm test days &lt;= 25 → 100%</text>
      <rect x="15" y="112" width="240" height="18" rx="2" fill="#111111"/>
      <text x="135" y="125" text-anchor="middle" font-family="monospace" font-size="10" font-weight="700" fill="#ffffff">Bảo đảm: Phủ trọn mọi ngã rẽ</text>
    </g>
  </g>
</svg>''')

# 7. gate-failure.svg (Slide 13)
save_svg('gate-failure.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Terminal Run · Minh chứng JaCoCo Gate chặn Build</text>
  <rect x="495" y="7" width="90" height="22" rx="3" fill="#111111"/>
  <text x="540" y="22" text-anchor="middle" font-family="monospace" font-size="11" font-weight="700" fill="#ffffff">EXIT CODE 1</text>

  <!-- Terminal window -->
  <g transform="translate(15, 48)">
    <rect width="570" height="215" rx="6" fill="#f6f8fa" stroke="#111111" stroke-width="1.5"/>
    <text x="15" y="25" font-family="monospace" font-size="11" fill="#111111">$ ./mvnw -f case-study/pom.xml -Pbaseline -Dcoverage.gate.skip=false clean verify</text>
    <text x="15" y="48" font-family="monospace" font-size="11" fill="#555555">[INFO] --- jacoco:0.8.12:check (coverage-check) @ library-app ---</text>
    <rect x="15" y="58" width="540" height="32" rx="3" fill="#111111"/>
    <text x="25" y="79" font-family="monospace" font-weight="700" font-size="11" fill="#ffffff">[ERROR] Rule violated for FineCalculator: branches ratio is 0.50, min is 0.90</text>
    <text x="15" y="112" font-family="monospace" font-size="11" fill="#555555">[INFO] ------------------------------------------------------------------------</text>
    <text x="15" y="132" font-family="monospace" font-weight="700" font-size="13" fill="#111111">[INFO] BUILD FAILURE</text>
    <text x="15" y="152" font-family="monospace" font-size="11" fill="#555555">[INFO] Total time:  3.284 s</text>
    <text x="15" y="172" font-family="monospace" font-size="11" fill="#555555">[INFO] Finished at: 2026-10-28T20:15:22+07:00</text>
    <rect x="15" y="185" width="540" height="20" rx="3" fill="#ffffff" stroke="#111111" stroke-width="1"/>
    <text x="285" y="199" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#111111">✓ Chặn thành công: Mã nguồn thiếu test không bao giờ được phép đóng gói</text>
  </g>
</svg>''')

# 8. ci-cd-levels.svg (Slide 15)
save_svg('ci-cd-levels.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 280" width="100%" height="100%">
  <!-- Level 1: CI -->
  <g transform="translate(20, 20)">
    <rect width="580" height="65" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect width="180" height="65" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="90" y="32" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">1. CONTINUOUS</text>
    <text x="90" y="50" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">INTEGRATION (CI)</text>
    <text x="200" y="28" font-family="system-ui, sans-serif" font-size="12" fill="#111111"><strong>Phạm vi:</strong> Commit code → Build JDK 25 → Chạy Unit Test → Coverage Gate.</text>
    <text x="200" y="50" font-family="system-ui, sans-serif" font-size="11" fill="#555555">Phát hiện xung đột &amp; lỗi kiểm thử ngay khi tạo Pull Request.</text>
  </g>

  <!-- Level 2: CD Delivery -->
  <g transform="translate(20, 100)">
    <rect width="580" height="75" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect width="180" height="75" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
    <text x="90" y="37" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">2. CONTINUOUS</text>
    <text x="90" y="55" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">DELIVERY</text>
    <text x="200" y="28" font-family="system-ui, sans-serif" font-size="12" fill="#111111"><strong>Phạm vi:</strong> Sau CI → Đóng gói Artifact (JAR) sẵn sàng phát hành.</text>
    <text x="200" y="48" font-family="system-ui, sans-serif" font-size="11" fill="#555555">Bản dựng luôn trong trạng thái sẵn sàng; việc đẩy lên server do con người bấm duyệt.</text>
    <rect x="200" y="56" width="130" height="15" rx="2" fill="#111111"/>
    <text x="265" y="67" text-anchor="middle" font-family="monospace" font-size="9" fill="#ffffff">MỨC NHÓM ĐẠT TỚI</text>
  </g>

  <!-- Level 3: CD Deployment -->
  <g transform="translate(20, 190)">
    <rect width="580" height="70" rx="6" fill="#fafafa" stroke="#999999" stroke-width="1.5" stroke-dasharray="4"/>
    <rect width="180" height="70" rx="6" fill="#f0f0f0" stroke="#999999" stroke-width="1.5"/>
    <text x="90" y="34" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#777777">3. CONTINUOUS</text>
    <text x="90" y="52" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#777777">DEPLOYMENT</text>
    <text x="200" y="28" font-family="system-ui, sans-serif" font-size="12" fill="#777777"><strong>Phạm vi:</strong> Tự động đẩy thẳng bản build lên máy chủ production.</text>
    <text x="200" y="48" font-family="system-ui, sans-serif" font-size="11" fill="#777777">Không có bước duyệt tay; đòi hỏi bộ test và gate cực kỳ khắt khe.</text>
    <text x="200" y="63" font-family="system-ui, sans-serif" font-size="10" font-style="italic" fill="#999999">(Ngoài phạm vi seminar môn kiểm thử)</text>
  </g>
</svg>''')

# 9. team-scope.svg (Slide 16)
save_svg('team-scope.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Bảng nghiệm thu phạm vi CI/CD của Nhóm 09</text>

  <!-- Row 1: CI -->
  <g transform="translate(20, 50)">
    <rect width="560" height="60" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <circle cx="30" cy="30" r="14" fill="#111111"/>
    <path d="M 23 30 L 28 35 L 37 25" fill="none" stroke="#ffffff" stroke-width="2.5"/>
    <text x="55" y="27" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Continuous Integration (CI) · HOÀN THÀNH 100%</text>
    <text x="55" y="47" font-family="system-ui, sans-serif" font-size="11" fill="#555555">Mỗi PR tự kích hoạt GitHub Actions: JDK 25, 49 tests pass, Branch Gate ≥ 90%.</text>
  </g>

  <!-- Row 2: Delivery -->
  <g transform="translate(20, 120)">
    <rect width="560" height="60" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <circle cx="30" cy="30" r="14" fill="#111111"/>
    <path d="M 23 30 L 28 35 L 37 25" fill="none" stroke="#ffffff" stroke-width="2.5"/>
    <text x="55" y="27" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Continuous Delivery · ĐẠT MỨC ARTIFACT JAR</text>
    <text x="55" y="47" font-family="system-ui, sans-serif" font-size="11" fill="#555555">Job package tạo file JAR executable + upload surefire reports và jacoco HTML.</text>
  </g>

  <!-- Row 3: Deployment -->
  <g transform="translate(20, 190)">
    <rect width="560" height="70" rx="6" fill="#fafafa" stroke="#888888" stroke-width="1.5" stroke-dasharray="4"/>
    <circle cx="30" cy="35" r="14" fill="#f0f0f0" stroke="#888888" stroke-width="1.5"/>
    <path d="M 22 27 L 38 43 M 38 27 L 22 43" stroke="#666666" stroke-width="2"/>
    <text x="55" y="28" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#777777">Continuous Deployment · KHÔNG THỰC HIỆN</text>
    <text x="55" y="48" font-family="system-ui, sans-serif" font-size="11" fill="#777777">Đề tài giới hạn trong phạm vi kiểm thử; không phát hành lên server production.</text>
    <text x="55" y="63" font-family="system-ui, sans-serif" font-size="10" font-style="italic" fill="#999999">Mở rộng: Cần thêm job deploy sau package với điều kiện nhánh master + approval.</text>
  </g>
</svg>''')

# 10. github-workflow-structure.svg (Slide 19)
save_svg('github-workflow-structure.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Cấu trúc phân tầng .github/workflows/ci.yml</text>

  <!-- Flow chart in SVG -->
  <g transform="translate(20, 50)">
    <!-- Triggers -->
    <rect width="160" height="70" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <text x="80" y="25" text-anchor="middle" font-family="monospace" font-weight="700" font-size="12" fill="#111111">on: [pr, push]</text>
    <text x="80" y="45" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#555555">Kích hoạt tự động</text>
    <text x="80" y="60" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#555555">khi đẩy mã</text>

    <!-- Cache box -->
    <g transform="translate(190, 0)">
      <rect width="370" height="70" rx="6" fill="#f6f8fa" stroke="#111111" stroke-width="1.5"/>
      <text x="15" y="24" font-family="monospace" font-weight="700" font-size="11" fill="#111111">actions/cache@v4 (Maven ~/.m2)</text>
      <text x="15" y="44" font-family="monospace" font-size="10" fill="#444444">key: ${{ runner.os }}-m2-${{ hashFiles('**/pom.xml') }}</text>
      <text x="15" y="60" font-family="system-ui, sans-serif" font-size="10" fill="#666666">✓ Giảm 74% thời gian build khi hit cache</text>
    </g>

    <!-- 3 jobs connection -->
    <g transform="translate(0, 90)">
      <rect width="170" height="120" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="85" y="26" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">JOB 1: test</text>
      <text x="12" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Setup JDK 25</text>
      <text x="12" y="72" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• mvn clean test</text>
      <text x="12" y="92" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Upload surefire</text>
      <text x="12" y="108" font-family="monospace" font-size="9" fill="#111111">Exit: 0</text>
    </g>

    <!-- Arrow 1 -->
    <line x1="175" y1="150" x2="200" y2="150" stroke="#111111" stroke-width="2"/>
    <text x="187" y="142" text-anchor="middle" font-family="monospace" font-size="8" fill="#111111">needs</text>

    <!-- Job 2 -->
    <g transform="translate(205, 90)">
      <rect width="170" height="120" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="85" y="26" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">JOB 2: coverage-gate</text>
      <text x="12" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• jaсоco:check</text>
      <text x="12" y="72" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Branch ≥ 90%</text>
      <text x="12" y="92" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• GITHUB_STEP_SUMMARY</text>
      <text x="12" y="108" font-family="monospace" font-size="9" fill="#111111">Fail if &lt; 0.90</text>
    </g>

    <!-- Arrow 2 -->
    <line x1="380" y1="150" x2="405" y2="150" stroke="#111111" stroke-width="2"/>
    <text x="392" y="142" text-anchor="middle" font-family="monospace" font-size="8" fill="#111111">needs</text>

    <!-- Job 3 -->
    <g transform="translate(410, 90)">
      <rect width="150" height="120" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="75" y="26" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">JOB 3: package</text>
      <text x="12" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• mvn package</text>
      <text x="12" y="72" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• -DskipTests</text>
      <text x="12" y="92" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Upload JAR</text>
      <text x="12" y="108" font-family="monospace" font-size="9" fill="#111111">Ready to ship</text>
    </g>
  </g>
</svg>''')

# 11. green-test-red-gate.svg (Slide 20)
save_svg('green-test-red-gate.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Nghịch lý: Test xanh hoàn toàn nhưng PR vẫn bị chặn</text>

  <!-- Side-by-side contrast -->
  <g transform="translate(20, 50)">
    <!-- Column 1: Test Job -->
    <rect width="265" height="150" rx="6" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <rect width="265" height="30" rx="6" fill="#f0f0f0" stroke="#111111" stroke-width="2"/>
    <text x="15" y="20" font-family="monospace" font-weight="700" font-size="12" fill="#111111">JOB 1: test (JDK 25)</text>
    <rect x="200" y="5" width="55" height="20" rx="3" fill="#111111"/>
    <text x="227" y="19" text-anchor="middle" font-family="monospace" font-size="10" font-weight="700" fill="#ffffff">PASSED</text>
    <text x="15" y="55" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• Xóa sạch FineCalculatorTest</text>
    <text x="15" y="78" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• 21 test của LoanService chạy</text>
    <text x="15" y="100" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• <strong>Không có ca nào fail!</strong></text>
    <text x="15" y="125" font-family="system-ui, sans-serif" font-weight="600" font-size="11" fill="#111111">✓ Exit code: 0 (Xanh)</text>

    <!-- Column 2: Gate Job -->
    <g transform="translate(295, 0)">
      <rect width="265" height="150" rx="6" fill="#fafafa" stroke="#111111" stroke-width="2"/>
      <rect width="265" height="30" rx="6" fill="#111111"/>
      <text x="15" y="20" font-family="monospace" font-weight="700" font-size="12" fill="#ffffff">JOB 2: coverage-gate</text>
      <rect x="200" y="5" width="55" height="20" rx="3" fill="#ffffff"/>
      <text x="227" y="19" text-anchor="middle" font-family="monospace" font-size="10" font-weight="700" fill="#111111">FAILED</text>
      <text x="15" y="55" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• Đo độ phủ FineCalculator</text>
      <text x="15" y="78" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• Branch Coverage = <strong>0.00%</strong></text>
      <text x="15" y="100" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• Ngưỡng bắt buộc: <strong>90.00%</strong></text>
      <text x="15" y="125" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">✗ Vi phạm rule → FAIL BUILD</text>
    </g>
  </g>

  <!-- Impact banner -->
  <g transform="translate(20, 215)">
    <rect width="560" height="50" rx="6" fill="#111111"/>
    <text x="280" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#ffffff">HẬU QUẢ: Job package BỊ HỦY BỎ · PR #6 BỊ KHÓA MERGE (BLOCKED)</text>
    <text x="280" y="42" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#dddddd">Minh chứng cho thấy: Không có Coverage Gate, code rách vẫn lọt vào production!</text>
  </g>
</svg>''')

# 12. ci-weaknesses.svg (Slide 21)
save_svg('ci-weaknesses.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">4 Điểm yếu &amp; Rủi ro quan sát được trên CI/CD</text>

  <g transform="translate(15, 50)">
    <!-- Box 1 -->
    <rect width="275" height="95" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <text x="15" y="24" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">1. CACHE MISS NHẠY CẢM</text>
    <text x="15" y="46" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Sửa 1 dòng comment trong pom.xml</text>
    <text x="15" y="64" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Hash key đổi → Cache bị bỏ</text>
    <text x="15" y="82" font-family="monospace" font-size="9" font-weight="700" fill="#111111">Tải lại từ đầu: 48s thay vì 12s</text>

    <!-- Box 2 -->
    <g transform="translate(295, 0)">
      <rect width="275" height="95" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="15" y="24" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">2. TRÙNG LẶP TEST SUITE</text>
      <text x="15" y="46" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Job test chạy toàn bộ test</text>
      <text x="15" y="64" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Job coverage-gate chạy lại từ đầu</text>
      <text x="15" y="82" font-family="monospace" font-size="9" font-weight="700" fill="#111111">Overhead gấp đôi thời gian test</text>
    </g>

    <!-- Box 3 -->
    <g transform="translate(0, 110)">
      <rect width="275" height="95" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="15" y="24" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">3. DAO ĐỘNG RUNNER RUNNER</text>
      <text x="15" y="46" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Cùng một bước trên GitHub Runner</text>
      <text x="15" y="64" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Thời gian dao động từ 29s đến 70s</text>
      <text x="15" y="82" font-family="monospace" font-size="9" font-weight="700" fill="#111111">Không thể lấy làm benchmark chuẩn</text>
    </g>

    <!-- Box 4 -->
    <g transform="translate(295, 110)">
      <rect width="275" height="95" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="15" y="24" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">4. KẸT PR DO REQUIRED CHECKS</text>
      <text x="15" y="46" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Bật check trên master nhưng workflow</text>
      <text x="15" y="64" font-family="system-ui, sans-serif" font-size="10" fill="#444444">  chưa có trigger trên master</text>
      <text x="15" y="82" font-family="monospace" font-size="9" font-weight="700" fill="#111111">PR #4 bị treo vĩnh viễn</text>
    </g>
  </g>
</svg>''')

# 13. video-d-timeline.svg (Slide 22)
save_svg('video-d-timeline.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Video D: CI/CD với GitHub Actions (8–9 phút)</text>

  <!-- Player visual -->
  <g transform="translate(20, 50)">
    <rect width="560" height="40" rx="4" fill="#111111"/>
    <!-- Progress bar -->
    <rect x="10" y="16" width="540" height="8" rx="3" fill="#444444"/>
    <rect x="10" y="16" width="320" height="8" rx="3" fill="#ffffff"/>
    <circle cx="330" cy="20" r="7" fill="#ffffff" stroke="#111111" stroke-width="2"/>
    <text x="510" y="32" font-family="monospace" font-size="10" fill="#ffffff">08:45</text>
  </g>

  <!-- Chapters timeline -->
  <g transform="translate(20, 105)">
    <g transform="translate(0, 0)">
      <rect width="265" height="65" rx="4" fill="#f8f8f8" stroke="#111111" stroke-width="1"/>
      <text x="10" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[00:00 - 01:00] SETUP CI</text>
      <text x="10" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• ci.yml, trigger on: pull_request, push</text>
      <text x="10" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Khởi tạo môi trường Temurin JDK 25</text>
    </g>
    <g transform="translate(295, 0)">
      <rect width="265" height="65" rx="4" fill="#f8f8f8" stroke="#111111" stroke-width="1"/>
      <text x="10" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[01:00 - 02:15] KHÁI NIỆM &amp; NEEDS</text>
      <text x="10" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Cơ chế nối 3 job bằng needs</text>
      <text x="10" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Vai trò của jacoco-maven-plugin check</text>
    </g>
    <g transform="translate(0, 75)">
      <rect width="265" height="65" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="10" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[02:15 - 04:00] DEMO ĐƠN GIẢN</text>
      <text x="10" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Run xanh chuẩn, đọc log Surefire</text>
      <text x="10" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Tải artifact JAR &amp; quan sát Maven cache</text>
    </g>
    <g transform="translate(295, 75)">
      <rect width="265" height="65" rx="4" fill="#fafafa" stroke="#111111" stroke-width="1.5"/>
      <text x="10" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[04:00 - 08:45] DEMO PHỨC TẠP</text>
      <text x="10" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• PR đỏ bị đánh rớt; PR vào master BLOCKED</text>
      <text x="10" y="52" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Mổ xẻ 4 điểm yếu quan sát được</text>
    </g>
  </g>
</svg>''')

# 14. pr-bot-comment.svg (Slide 25)
save_svg('pr-bot-comment.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">GitHub Pull Request #13 · Gemini AI Code Review Bot</text>

  <!-- Bot comment bubble -->
  <g transform="translate(20, 50)">
    <rect width="560" height="150" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <rect width="560" height="30" rx="6" fill="#f6f8fa" stroke="#111111" stroke-width="1.5"/>
    <circle cx="20" cy="15" r="7" fill="#111111"/>
    <text x="35" y="19" font-family="monospace" font-weight="700" font-size="11" fill="#111111">gemini-code-reviewer[bot] commented 2 days ago</text>

    <text x="15" y="50" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">### AI Review Summary for Test Suite</text>
    <text x="15" y="72" font-family="system-ui, sans-serif" font-size="11" fill="#333333">✓ <strong>Test assertions:</strong> Tất cả 10 ca test bổ sung đều có assertion chặt chẽ.</text>
    <text x="15" y="92" font-family="system-ui, sans-serif" font-size="11" fill="#333333">✓ <strong>Edge cases:</strong> Đã bao quát ranh giới Integer.MAX_VALUE và null parameters.</text>
    <text x="15" y="112" font-family="system-ui, sans-serif" font-size="11" fill="#333333">✓ <strong>CI Integration:</strong> 6 jobs xanh, 49 tests pass, Line 76/83, Branch 24/24.</text>
    <rect x="15" y="122" width="230" height="18" rx="2" fill="#f0f0f0" stroke="#111111" stroke-width="1"/>
    <text x="130" y="135" text-anchor="middle" font-family="monospace" font-size="10" font-weight="700" fill="#111111">No negative findings detected</text>
  </g>

  <!-- Golden rule -->
  <g transform="translate(20, 215)">
    <rect width="560" height="50" rx="4" fill="#fafafa" stroke="#111111" stroke-width="1"/>
    <text x="15" y="24" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">NGUYÊN TẮC VÀNG VỀ QUYỀN HẠN CỦA AI:</text>
    <text x="15" y="40" font-family="system-ui, sans-serif" font-size="11" fill="#444444">AI chỉ mang tính tham vấn; không tự sửa mã, không tự commit và không thay quyền merge của người.</text>
  </g>
</svg>''')

# 15. human-vs-ai.svg (Slide 26)
save_svg('human-vs-ai.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">AI-4: Đối chiếu thực nghiệm Bộ Người viết vs. Bộ AI sinh</text>

  <!-- Venn / Matrix layout -->
  <g transform="translate(20, 50)">
    <!-- Column 1: Human -->
    <rect width="180" height="150" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <text x="90" y="24" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">BỘ NGƯỜI VIẾT (Gia An)</text>
    <text x="15" y="52" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• <strong>23 ca test</strong> từ đặc tả</text>
    <text x="15" y="74" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• 16 ca hợp lệ, 7 ca lỗi</text>
    <text x="15" y="96" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• 23/23 pass trên Java</text>
    <text x="15" y="118" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• <strong>Branch: 10/10</strong></text>
    <rect x="15" y="126" width="150" height="16" rx="2" fill="#f0f0f0" stroke="#111111" stroke-width="1"/>
    <text x="90" y="138" text-anchor="middle" font-family="monospace" font-size="9" fill="#111111">Giỏi ca ngoại lệ</text>

    <!-- Column 2: Intersection -->
    <g transform="translate(190, 0)">
      <rect width="180" height="150" rx="6" fill="#111111"/>
      <text x="90" y="24" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#ffffff">11 ĐẦU VÀO CHUNG</text>
      <text x="15" y="52" font-family="system-ui, sans-serif" font-size="11" fill="#ffffff">• 11 ca trùng khớp</text>
      <text x="15" y="74" font-family="system-ui, sans-serif" font-size="11" fill="#ffffff">• <strong>0 disagreement</strong></text>
      <text x="15" y="96" font-family="system-ui, sans-serif" font-size="11" fill="#ffffff">• Cùng kết quả kỳ vọng</text>
      <text x="15" y="118" font-family="system-ui, sans-serif" font-size="11" fill="#ffffff">• Đồng thuận 100%</text>
      <rect x="15" y="126" width="150" height="16" rx="2" fill="#ffffff"/>
      <text x="90" y="138" text-anchor="middle" font-family="monospace" font-size="9" font-weight="700" fill="#111111">Xác thực chéo</text>
    </g>

    <!-- Column 3: AI -->
    <g transform="translate(380, 0)">
      <rect width="180" height="150" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="90" y="24" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">BỘ AI SINH (Gemini)</text>
      <text x="15" y="52" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• <strong>13 ca test</strong> độc lập</text>
      <text x="15" y="74" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• Tập trung ca hợp lệ</text>
      <text x="15" y="96" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• 13/13 pass trên Java</text>
      <text x="15" y="118" font-family="system-ui, sans-serif" font-size="11" fill="#333333">• <strong>Branch: 8/10</strong></text>
      <rect x="15" y="126" width="150" height="16" rx="2" fill="#f0f0f0" stroke="#111111" stroke-width="1"/>
      <text x="90" y="138" text-anchor="middle" font-family="monospace" font-size="9" fill="#111111">Có Integer.MAX_VALUE</text>
    </g>
  </g>

  <!-- Conclusion -->
  <g transform="translate(20, 215)">
    <rect width="560" height="50" rx="4" fill="#f6f8fa" stroke="#111111" stroke-width="1"/>
    <text x="280" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">KẾT LUẬN: KHÔNG THAY THẾ MÀ BỔ TRỢ CHO NHAU</text>
    <text x="280" y="42" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#555555">Người nắm sâu logic miền; AI bổ sung các ca biên cực đại mà người hay bỏ quên.</text>
  </g>
</svg>''')

# 16. coverup-flow.svg (Slide 27)
save_svg('coverup-flow.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">CoverUp (FSE 2025 · CORE A*) · Cơ chế Coverage-Guided LLM</text>

  <!-- Architecture flow -->
  <g transform="translate(20, 50)">
    <rect width="115" height="130" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <text x="57" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">1. ĐO ĐỘ PHỦ</text>
    <text x="10" y="55" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Chạy suite sẵn</text>
    <text x="10" y="75" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Dùng SlipCover</text>
    <text x="10" y="95" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Tìm missing lines</text>

    <!-- Arrow -->
    <line x1="120" y1="115" x2="140" y2="115" stroke="#111111" stroke-width="2"/>

    <g transform="translate(145, 0)">
      <rect width="125" height="130" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="62" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">2. TRÍCH LỖ HỔNG</text>
      <text x="10" y="55" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Trích đoạn code</text>
      <text x="10" y="75" font-family="system-ui, sans-serif" font-size="10" fill="#333333">  chưa được chạy</text>
      <text x="10" y="95" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Tạo prompt hẹp</text>
    </g>

    <line x1="275" y1="115" x2="295" y2="115" stroke="#111111" stroke-width="2"/>

    <g transform="translate(300, 0)">
      <rect width="125" height="130" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="62" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">3. GEMINI SINH</text>
      <text x="10" y="55" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Sinh test nhắm</text>
      <text x="10" y="75" font-family="system-ui, sans-serif" font-size="10" fill="#333333">  trúng missing line</text>
      <text x="10" y="95" font-family="system-ui, sans-serif" font-size="10" fill="#333333">• Viết assertion</text>
    </g>

    <line x1="430" y1="115" x2="450" y2="115" stroke="#111111" stroke-width="2"/>

    <g transform="translate(455, 0)">
      <rect width="105" height="130" rx="6" fill="#111111"/>
      <text x="52" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#ffffff">4. KẾT QUẢ</text>
      <text x="10" y="55" font-family="system-ui, sans-serif" font-size="10" fill="#ffffff">• 163 module:</text>
      <text x="10" y="75" font-family="system-ui, sans-serif" font-size="10" fill="#ffffff">  <strong>89.0%</strong> coverage</text>
      <text x="10" y="95" font-family="system-ui, sans-serif" font-size="10" fill="#ffffff">• Source nhóm:</text>
      <text x="10" y="115" font-family="system-ui, sans-serif" font-size="10" fill="#ffffff">  <strong>23% → 96.4%</strong></text>
    </g>
  </g>

  <!-- Metric highlight -->
  <g transform="translate(20, 200)">
    <rect width="560" height="65" rx="4" fill="#f8f8f8" stroke="#111111" stroke-width="1"/>
    <text x="15" y="26" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">KẾT QUẢ TÁI HIỆN CỦA GIA AN TRÊN BENCHMARK f003 &amp; SOURCE NHÓM:</text>
    <text x="15" y="45" font-family="system-ui, sans-serif" font-size="11" fill="#444444">• Benchmark f003: 3 test pass, Line 8/8 (100%), Branch 4/4 (100%).</text>
    <text x="15" y="58" font-family="system-ui, sans-serif" font-size="11" fill="#444444">• scripts/coverage_gaps.py: 7 test pass, độ phủ tăng từ 23.6% lên 96.4% (Line 38/39, Branch 15/16).</text>
  </g>
</svg>''')

# 17. video-e-timeline.svg (Slide 29)
save_svg('video-e-timeline.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">Video Demo E: Kịch bản AI &amp; Tái hiện Paper (7 Phần)</text>

  <g transform="translate(15, 50)">
    <g transform="translate(0, 0)">
      <rect width="180" height="95" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="10" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[GA-01/02] SINH &amp; FIX</text>
      <text x="10" y="42" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Setup Gemini client</text>
      <text x="10" y="60" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• AI-1 sinh 7 test LoanService</text>
      <text x="10" y="78" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• AI-2 bổ sung 3 test gap</text>
    </g>
    <g transform="translate(195, 0)">
      <rect width="180" height="95" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="10" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[GA-03/04] BOT REVIEW</text>
      <text x="10" y="42" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• AI-3 comment tự động PR</text>
      <text x="10" y="60" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Demo ca oracle assertion sai</text>
      <text x="10" y="78" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Giới hạn của test xanh</text>
    </g>
    <g transform="translate(390, 0)">
      <rect width="180" height="95" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="10" y="20" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[GA-05] ĐỐI CHỨNG</text>
      <text x="10" y="42" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• So 23 ca người viết</text>
      <text x="10" y="60" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• với 13 ca do Gemini sinh</text>
      <text x="10" y="78" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• 11 ca trùng kết quả</text>
    </g>

    <!-- Bottom row -->
    <g transform="translate(0, 110)">
      <rect width="275" height="100" rx="4" fill="#f8f8f8" stroke="#111111" stroke-width="1.5"/>
      <text x="10" y="22" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[GA-06] COVERUP REPLAY</text>
      <text x="10" y="45" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Tái hiện CoverUp trên module f003 (Pass 100%)</text>
      <text x="10" y="65" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Thực nghiệm tăng coverage trên source nhóm</text>
      <text x="10" y="85" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Đánh giá ưu điểm dẫn đường độ phủ</text>
    </g>
    <g transform="translate(295, 110)">
      <rect width="275" height="100" rx="4" fill="#f8f8f8" stroke="#111111" stroke-width="1.5"/>
      <text x="10" y="22" font-family="monospace" font-weight="700" font-size="11" fill="#111111">[GA-07] PYNGUIN REPLAY</text>
      <text x="10" y="45" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Tái hiện 134 module dữ liệu công bố khớp số liệu</text>
      <text x="10" y="65" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Chạy mới benchmark codetiming._timers</text>
      <text x="10" y="85" font-family="system-ui, sans-serif" font-size="10" fill="#444444">• Mổ xẻ trường hợp tool sinh test thiếu assertion</text>
    </g>
  </g>
</svg>''')

# 18. exercises.svg (Slide 30)
save_svg('exercises.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">3 Bài tập thực hành dành cho người tham gia</text>

  <g transform="translate(20, 50)">
    <!-- Task 1 -->
    <rect width="560" height="65" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
    <rect width="90" height="65" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="1.5"/>
    <text x="45" y="30" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">BÀI 1</text>
    <text x="45" y="46" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#555555">DỄ · UT</text>
    <text x="105" y="26" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">Bổ sung hạng thành viên mới: STUDENT</text>
    <text x="105" y="45" font-family="system-ui, sans-serif" font-size="11" fill="#444444">Quy tắc: Giảm 50% tiền phạt so với NORMAL, mức trần 30.000 VND.</text>
    <text x="105" y="58" font-family="system-ui, sans-serif" font-size="10" fill="#666666">Yêu cầu: Thiết kế bảng dữ liệu biên và viết Parameterized Test @CsvFileSource.</text>

    <!-- Task 2 -->
    <g transform="translate(0, 75)">
      <rect width="560" height="65" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <rect width="90" height="65" rx="6" fill="#f4f4f4" stroke="#111111" stroke-width="1.5"/>
      <text x="45" y="30" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">BÀI 2</text>
      <text x="45" y="46" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#555555">TRUNG BÌNH</text>
      <text x="105" y="26" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">Quan sát bẫy Coverage &amp; Mutation Testing</text>
      <text x="105" y="45" font-family="system-ui, sans-serif" font-size="11" fill="#444444">Cố tình xóa 1 assertion kiểm tra tiền trong FineCalculatorTest.</text>
      <text x="105" y="58" font-family="system-ui, sans-serif" font-size="10" fill="#666666">Yêu cầu: Chạy JaCoCo (vẫn 100% branch) rồi chạy PIT Mutation để thấy mutant survived.</text>
    </g>

    <!-- Task 3 -->
    <g transform="translate(0, 150)">
      <rect width="560" height="65" rx="6" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <rect width="90" height="65" rx="6" fill="#111111"/>
      <text x="45" y="30" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#ffffff">BÀI 3</text>
      <text x="45" y="46" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#dddddd">NÂNG CAO</text>
      <text x="105" y="26" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">Kích hoạt Coverage Gate trên GitHub Actions</text>
      <text x="105" y="45" font-family="system-ui, sans-serif" font-size="11" fill="#444444">Fork repo, bật GitHub Actions, mở PR thiếu nhánh kiểm thử.</text>
      <text x="105" y="58" font-family="system-ui, sans-serif" font-size="10" fill="#666666">Yêu cầu: Quan sát Gate chặn build đỏ và PR rơi vào trạng thái BLOCKED.</text>
    </g>
  </g>
</svg>''')

# 19. deliverables.svg (Slide 31)
save_svg('deliverables.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>
  <rect width="600" height="36" rx="8" fill="#f4f4f4" stroke="#111111" stroke-width="2"/>
  <text x="20" y="23" font-family="system-ui, sans-serif" font-weight="700" font-size="13" fill="#111111">7 Đầu ra hoàn chỉnh trong gói nộp Tuần 06</text>

  <g transform="translate(20, 50)">
    <g transform="translate(0, 0)">
      <rect width="265" height="45" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="15" y="26" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">1. Slide Trình Chiếu</text>
      <text x="15" y="38" font-family="monospace" font-size="10" fill="#555555">slides/index.html (Reveal.js)</text>
    </g>
    <g transform="translate(295, 0)">
      <rect width="265" height="45" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="15" y="26" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">2. Báo Cáo Tổng Hợp</text>
      <text x="15" y="38" font-family="monospace" font-size="10" fill="#555555">report/main.tex (LaTeX)</text>
    </g>
    <g transform="translate(0, 55)">
      <rect width="265" height="45" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="15" y="26" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">3. Video Demo (D &amp; E)</text>
      <text x="15" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#555555">8-9 phút CI/CD + Demo AI</text>
    </g>
    <g transform="translate(295, 55)">
      <rect width="265" height="45" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="15" y="26" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">4. Mã Nguồn Hoàn Chỉnh</text>
      <text x="15" y="38" font-family="monospace" font-size="10" fill="#555555">case-study/ &amp; scripts/</text>
    </g>
    <g transform="translate(0, 110)">
      <rect width="265" height="45" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="15" y="26" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">5. Bảng Phân Công Nhiệm Vụ</text>
      <text x="15" y="38" font-family="monospace" font-size="10" fill="#555555">PhanCong_NhiemVu.md</text>
    </g>
    <g transform="translate(295, 110)">
      <rect width="265" height="45" rx="4" fill="#ffffff" stroke="#111111" stroke-width="1.5"/>
      <text x="15" y="26" font-family="system-ui, sans-serif" font-weight="700" font-size="11" fill="#111111">6. Git Commit Log Minh Bạch</text>
      <text x="15" y="38" font-family="system-ui, sans-serif" font-size="10" fill="#555555">Lịch sử commit đối chiếu từng tác giả</text>
    </g>
    <g transform="translate(0, 165)">
      <rect width="560" height="45" rx="4" fill="#111111"/>
      <text x="280" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#ffffff">7. TUYÊN BỐ SỬ DỤNG AI (ai-usage-declaration/)</text>
      <text x="280" y="38" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#cccccc">Minh bạch 100% mục đích, prompt, model Gemini và đánh giá phản biện.</text>
    </g>
  </g>
</svg>''')

# 20. qa-resources.svg (Slide 32)
save_svg('qa-resources.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 280" width="100%" height="100%">
  <rect width="600" height="280" rx="8" fill="#ffffff" stroke="#111111" stroke-width="2"/>

  <!-- Top big Q&A Box -->
  <g transform="translate(20, 20)">
    <rect width="560" height="110" rx="6" fill="#111111"/>
    <text x="280" y="48" text-anchor="middle" font-family="Georgia, serif" font-weight="700" font-size="28" fill="#ffffff">Q &amp; A</text>
    <text x="280" y="75" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" fill="#dddddd">Nhóm 09 sẵn sàng giải đáp mọi thắc mắc của thầy và các bạn!</text>
    <text x="280" y="95" text-anchor="middle" font-family="monospace" font-size="11" fill="#aaaaaa">Bảo An · Quang Vinh · Nhật Đạt · Thế Vinh · Gia An</text>
  </g>

  <!-- Bottom resource links -->
  <g transform="translate(20, 145)">
    <rect width="560" height="115" rx="6" fill="#f8f8f8" stroke="#111111" stroke-width="1.5"/>
    <text x="15" y="25" font-family="system-ui, sans-serif" font-weight="700" font-size="12" fill="#111111">TÀI NGUYÊN TÁI HIỆN CỦA DỰ ÁN:</text>
    <text x="15" y="48" font-family="monospace" font-size="11" fill="#111111">• README.md</text>
    <text x="130" y="48" font-family="system-ui, sans-serif" font-size="11" fill="#555555">Tổng quan và hướng dẫn chạy nhanh toàn bộ dự án.</text>
    <text x="15" y="72" font-family="monospace" font-size="11" fill="#111111">• docs/thuc-hanh/</text>
    <text x="130" y="72" font-family="system-ui, sans-serif" font-size="11" fill="#555555">Tài liệu HuongDan_Demo.md kèm script mẫu cho từng demo.</text>
    <text x="15" y="96" font-family="monospace" font-size="11" fill="#111111">• evidence/</text>
    <text x="130" y="96" font-family="system-ui, sans-serif" font-size="11" fill="#555555">Chứng cứ thực tế: file log Surefire, XML/HTML JaCoCo, benchmark.</text>
  </g>
</svg>''')

print("All extra visuals generated successfully.")
