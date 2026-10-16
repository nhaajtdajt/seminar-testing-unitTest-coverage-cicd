package vn.edu.seminar.fine;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;
class TddRoundTest {
@Test void case0() { assertThat(new FineCalculator().calculate(0, MemberTier.NORMAL)).isEqualByComparingTo("0"); }
@Test void case1() { assertThat(new FineCalculator().calculate(3, MemberTier.NORMAL)).isEqualByComparingTo("6000"); }
@Test void case2() { assertThat(new FineCalculator().calculate(3, MemberTier.VIP)).isEqualByComparingTo("1000"); }
}
