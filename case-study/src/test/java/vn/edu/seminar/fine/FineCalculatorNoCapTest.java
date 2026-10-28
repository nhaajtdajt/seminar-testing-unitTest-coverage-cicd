package vn.edu.seminar.fine;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

/**
 * Deliberately incomplete: every amount is asserted and every branch is covered,
 * but no case reaches the 50,000 VND cap hidden inside Math.min. Excluded from normal runs.
 */
@Tag("antipattern")
class FineCalculatorNoCapTest {
    private final FineCalculator calculator = new FineCalculator();

    @Test void duNhanhNhungKhongChamTran() {
        assertThat(calculator.calculate(0, MemberTier.NORMAL)).isEqualByComparingTo("0");
        assertThat(calculator.calculate(1, MemberTier.NORMAL)).isEqualByComparingTo("2000");
        assertThat(calculator.calculate(2, MemberTier.VIP)).isEqualByComparingTo("0");
        assertThat(calculator.calculate(3, MemberTier.VIP)).isEqualByComparingTo("1000");
        assertThatIllegalArgumentException().isThrownBy(() -> calculator.calculate(-1, MemberTier.NORMAL));
        assertThatIllegalArgumentException().isThrownBy(() -> calculator.calculate(1, null));
    }
}
