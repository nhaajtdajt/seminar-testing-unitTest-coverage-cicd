package vn.edu.seminar.loan;

import java.math.BigDecimal;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

/** Deliberately seeded wrong oracle for the video; not an observed API model error. */
@Tag("ai-loan-mistake")
class LoanServiceAiMistakeTest extends LoanServiceAiDraftTest {
    @Test void WRONG_allowsBorrowingWhenAlreadyHoldingThreeBooks() {
        availableMember(BigDecimal.ZERO);
        when(loans.countActiveByMemberId(9)).thenReturn(3L);
        // Wrong: the specification refuses at >=3, not >3. This must fail.
        assertThatCode(() -> service.borrow(7, 9)).doesNotThrowAnyException();
    }
}
