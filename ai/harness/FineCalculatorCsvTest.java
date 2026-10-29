package vn.edu.seminar.fine;

import java.math.BigDecimal;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;
import static org.assertj.core.api.Assertions.*;

/** Same executable harness for both CSVs; run in a temporary Maven project. */
class FineCalculatorCsvTest {
    @ParameterizedTest
    @CsvFileSource(resources = "/cases.csv", numLinesToSkip = 1, nullValues = "NULL")
    void cases(int days, MemberTier tier, BigDecimal expected, String expectedException) {
        var calculator = new FineCalculator();
        if (expectedException == null) {
            assertThat(expected).isNotNull();
            assertThat(calculator.calculate(days, tier)).isEqualByComparingTo(expected);
        } else {
            assertThat(expected).isNull();
            assertThat(expectedException).isEqualTo("IllegalArgumentException");
            assertThatIllegalArgumentException().isThrownBy(() -> calculator.calculate(days, tier));
        }
    }
}
