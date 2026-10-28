package vn.edu.seminar.loan;

import java.math.BigDecimal;
import java.time.*;
import java.util.Optional;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;
import static vn.edu.seminar.loan.LoanException.Code.*;

/** Codex draft, 28/10/2026. This is AI output, not an independent human baseline. */
@Tag("ai-loan-draft")
@ExtendWith(MockitoExtension.class)
class LoanServiceAiDraftTest {
    @Mock BookRepository books;
    @Mock MemberRepository members;
    @Mock LoanRepository loans;
    final Instant now = Instant.parse("2026-10-28T00:00:00Z");
    LoanService service;

    @BeforeEach void setUp() {
        service = new LoanService(books, members, loans, Clock.fixed(now, ZoneOffset.UTC));
    }

    void availableMember(BigDecimal debt) {
        when(books.findById(7)).thenReturn(Optional.of(new Book(7, true)));
        when(members.findById(9)).thenReturn(Optional.of(new Member(9, debt)));
    }

    @Test void borrowsAvailableBook() {
        availableMember(BigDecimal.ZERO);
        when(loans.save(any())).thenAnswer(call -> call.getArgument(0));
        Loan result = service.borrow(7, 9);
        assertThat(result.bookId()).isEqualTo(7);
        assertThat(result.memberId()).isEqualTo(9);
        verify(books).save(new Book(7, false));
    }

    @Test void rejectsMissingBook() {
        when(books.findById(7)).thenReturn(Optional.empty());
        assertThatThrownBy(() -> service.borrow(7, 9)).isInstanceOfSatisfying(LoanException.class,
                error -> assertThat(error.code()).isEqualTo(BOOK_NOT_FOUND));
        verifyNoInteractions(members, loans);
    }
}
