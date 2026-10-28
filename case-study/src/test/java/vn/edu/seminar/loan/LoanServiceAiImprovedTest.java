package vn.edu.seminar.loan;

import java.math.BigDecimal;
import java.util.Optional;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.ArgumentCaptor;
import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;
import static vn.edu.seminar.loan.LoanException.Code.*;

/** Adds boundary, oracle and side-effect checks to the two inherited draft tests. */
@Tag("ai-loan-improved")
class LoanServiceAiImprovedTest extends LoanServiceAiDraftTest {
    void rejects(LoanException.Code code) {
        assertThatThrownBy(() -> service.borrow(7, 9)).isInstanceOfSatisfying(LoanException.class,
                error -> assertThat(error.code()).isEqualTo(code));
        verify(books, never()).save(any());
        verify(loans, never()).save(any());
    }

    @Test void unavailableBookStopsBeforeMemberLookup() {
        when(books.findById(7)).thenReturn(Optional.of(new Book(7, false)));
        rejects(BOOK_UNAVAILABLE);
        verifyNoInteractions(members, loans);
    }

    @Test void missingMemberStopsBeforeLoanLookup() {
        when(books.findById(7)).thenReturn(Optional.of(new Book(7, true)));
        when(members.findById(9)).thenReturn(Optional.empty());
        rejects(MEMBER_NOT_FOUND);
        verifyNoInteractions(loans);
    }

    @ParameterizedTest @ValueSource(longs = {3, 4})
    void rejectsAtAndAboveLimit(long count) {
        availableMember(BigDecimal.ZERO);
        when(loans.countActiveByMemberId(9)).thenReturn(count);
        rejects(LIMIT_REACHED);
    }

    @ParameterizedTest @ValueSource(strings = {"0.01", "1000"})
    void rejectsAnyPositiveDebt(String debt) {
        availableMember(new BigDecimal(debt));
        rejects(UNPAID_FINE);
    }

    @ParameterizedTest @ValueSource(longs = {0, 2})
    void acceptsBelowLimitAndCapturesPersistedLoan(long count) {
        availableMember(new BigDecimal("0.00"));
        when(loans.countActiveByMemberId(9)).thenReturn(count);
        when(loans.save(any())).thenAnswer(call -> call.getArgument(0));
        Loan result = service.borrow(7, 9);
        var captured = ArgumentCaptor.forClass(Loan.class);
        verify(loans).save(captured.capture());
        assertThat(result).isEqualTo(captured.getValue());
        assertThat(result.id()).isNotBlank();
        assertThat(result.bookId()).isEqualTo(7);
        assertThat(result.memberId()).isEqualTo(9);
        assertThat(result.borrowedAt()).isEqualTo(now);
        verify(books).save(new Book(7, false));
    }
}
