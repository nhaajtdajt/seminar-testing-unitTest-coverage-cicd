package vn.edu.seminar.fine;

import java.math.BigDecimal;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;
import static org.assertj.core.api.Assertions.*;

/** Same executable harness for both CSVs; run in a temporary Maven project. */
class FineCalculatorCsvTest {
    @ParameterizedTest
    @CsvFileSource(resources = "/cases.csv", numLinesToSkip = 1, nullValues = "NULL")
    void cases(int days, MemberTier tier, String expected, String expectedException) {
        var calculator = new FineCalculator();
        // CSV can represent a blank field as either an unquoted null or quoted "".
        if (expectedException == null || expectedException.isEmpty()) {
            assertThat(expected).isNotEmpty();
            assertThat(calculator.calculate(days, tier)).isEqualByComparingTo(new BigDecimal(expected));
        } else {
            assertThat(expected).isNullOrEmpty();
            assertThat(expectedException).isEqualTo("IllegalArgumentException");
            assertThatIllegalArgumentException().isThrownBy(() -> calculator.calculate(days, tier));
        }
    }
}
