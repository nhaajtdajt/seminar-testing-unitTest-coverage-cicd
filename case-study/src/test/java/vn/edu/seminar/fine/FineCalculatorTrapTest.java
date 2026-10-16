package vn.edu.seminar.fine;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertThrows;

/** Deliberately weak example: valid amounts are never asserted. Excluded from normal runs. */
@Tag("antipattern")
class FineCalculatorTrapTest {
    @Test void chayMoiNhanhNhungKhongKiemTraTien() {
        FineCalculator calculator = new FineCalculator();
        for (MemberTier tier : MemberTier.values()) {
            for (int days : new int[]{0, 1, 2, 3, 24, 25, 26, 52, 53, Integer.MAX_VALUE}) {
                calculator.calculate(days, tier);
            }
        }
        assertThrows(IllegalArgumentException.class, () -> calculator.calculate(-1, MemberTier.NORMAL));
        assertThrows(IllegalArgumentException.class, () -> calculator.calculate(1, null));
    }
}
