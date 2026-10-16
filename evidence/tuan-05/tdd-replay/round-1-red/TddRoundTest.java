package vn.edu.seminar.fine;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;
class TddRoundTest {
@Test void case0() { assertThat(new FineCalculator().calculate(0, MemberTier.NORMAL)).isEqualByComparingTo("0"); }
}
