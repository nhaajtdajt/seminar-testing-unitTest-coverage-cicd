package vn.edu.seminar.ai;

import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import vn.edu.seminar.fine.FineCalculator;
import vn.edu.seminar.fine.MemberTier;
import static org.assertj.core.api.Assertions.assertThat;

class Ai3PipelineSmokeTest {
    @Test
    void calculatesNormalMemberFine() {
        assertThat(new FineCalculator().calculate(1, MemberTier.NORMAL))
                .isEqualByComparingTo(new BigDecimal("2000"));
    }
}
