package vn.edu.seminar.fine;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

@Tag("baseline")
class FineCalculatorBaselineTest {
    @Test void motNgayTreThongThuong() {
        assertThat(new FineCalculator().calculate(1, MemberTier.NORMAL)).isEqualByComparingTo("2000");
    }
}
