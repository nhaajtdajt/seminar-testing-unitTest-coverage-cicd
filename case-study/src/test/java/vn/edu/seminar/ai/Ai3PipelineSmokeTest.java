package vn.edu.seminar.ai;

import org.junit.jupiter.api.Test;
import vn.edu.seminar.fine.FineCalculator;
import vn.edu.seminar.fine.MemberTier;

class Ai3PipelineSmokeTest {
    @Test
    void calculatesNormalMemberFine() {
        new FineCalculator().calculate(1, MemberTier.NORMAL);
    }
}
