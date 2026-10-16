package vn.edu.seminar.fine;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

/** AI-2: generated from AI-2-gaps.json plus source; reviewed by Codex, pending team review. */
@Tag("ai-gaps")
class FineCalculatorAiGapsTest {
    private final FineCalculator calculator = new FineCalculator();
    @Test void nhanNullBiTuChoi() {
        assertThatIllegalArgumentException().isThrownBy(() -> calculator.calculate(1, null));
    }
    @Test void ngayAmBiTuChoi() {
        assertThatIllegalArgumentException().isThrownBy(() -> calculator.calculate(-1, MemberTier.NORMAL));
    }
    @Test void vipSauNguongGiaHan() {
        assertThat(calculator.calculate(3, MemberTier.VIP)).isEqualByComparingTo("1000");
    }
}
