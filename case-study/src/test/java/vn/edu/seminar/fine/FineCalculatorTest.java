package vn.edu.seminar.fine;

import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;
import static org.assertj.core.api.Assertions.*;

class FineCalculatorTest {
    private final FineCalculator calculator = new FineCalculator();

    @ParameterizedTest(name = "{0} ngày trễ, {1} → {2} VND")
    @CsvFileSource(resources = "/fine-cases.csv", numLinesToSkip = 1)
    void tinhPhiTheoDuLieu(int days, MemberTier tier, BigDecimal expected) {
        // Arrange: dữ liệu từ CSV. Act: gọi logic thật. Assert: so giá trị tiền.
        assertThat(calculator.calculate(days, tier)).isEqualByComparingTo(expected);
    }

    @Test void tuChoiNgayAm() {
        assertThatIllegalArgumentException().isThrownBy(() -> calculator.calculate(-1, MemberTier.NORMAL));
    }

    @Test void tuChoiHangTrong() {
        assertThatIllegalArgumentException().isThrownBy(() -> calculator.calculate(1, null));
    }
}
