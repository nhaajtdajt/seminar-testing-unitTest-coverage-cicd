package vn.edu.seminar.fine;

import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.stream.Stream;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.TestFactory;
import static org.assertj.core.api.Assertions.*;

/** Executed only after a real person supplies and freezes the independent oracle. */
@Tag("ai-human")
class FineCalculatorHumanDataTest {
    @TestFactory Stream<DynamicTest> humanOracle() throws Exception {
        Path path = Path.of(System.getProperty("ai4.cases", "../ai/human/frozen/cases.csv"));
        var rows = Files.readAllLines(path);
        assertThat(rows.getFirst()).isEqualTo("daysLate,tier,expected,expectedException");
        assertThat(rows.size()).isGreaterThan(1);
        return rows.stream().skip(1).map(row -> DynamicTest.dynamicTest(row, () -> {
            String[] fields = row.split(",", -1);
            assertThat(fields).hasSize(4);
            int days = Integer.parseInt(fields[0]);
            MemberTier tier = fields[1].equals("NULL") ? null : MemberTier.valueOf(fields[1]);
            var calculator = new FineCalculator();
            if (fields[3].isEmpty()) {
                assertThat(calculator.calculate(days, tier)).isEqualByComparingTo(new BigDecimal(fields[2]));
            } else {
                assertThat(fields[3]).isEqualTo("IllegalArgumentException");
                assertThatIllegalArgumentException().isThrownBy(() -> calculator.calculate(days, tier));
            }
        }));
    }
}
