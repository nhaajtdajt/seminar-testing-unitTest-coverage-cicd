package vn.edu.seminar.fine;

import java.math.BigDecimal;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;
import static org.assertj.core.api.Assertions.assertThat;

@Tag("ai-data")
class FineCalculatorAiDataTest {
    @ParameterizedTest
    @CsvFileSource(resources = "/AI-4-boundaries.csv", numLinesToSkip = 1)
    void kiemDuLieuAiSinh(int days, MemberTier tier, BigDecimal expected) {
        assertThat(new FineCalculator().calculate(days, tier)).isEqualByComparingTo(expected);
    }
}
