package vn.edu.seminar.loan;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneId;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class LoanServiceGeminiDraftTest {

    private BookRepository books;
    private MemberRepository members;
    private LoanRepository loans;
    private Clock clock;
    private LoanService loanService;

    private static final Instant FIXED_INSTANT = Instant.parse("2026-03-30T10:00:00Z");

    @BeforeEach
    void setUp() {
        books = mock(BookRepository.class);
        members = mock(MemberRepository.class);
        loans = mock(LoanRepository.class);
        clock = Clock.fixed(FIXED_INSTANT, ZoneId.of("UTC"));
        loanService = new LoanService(books, members, loans, clock);
    }

    @Test
    void borrow_whenBookNotFound_throwsBookNotFoundException() {
        long bookId = 1L;
        long memberId = 100L;

        when(books.findById(bookId)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> loanService.borrow(bookId, memberId))
                .isInstanceOf(LoanException.class)
                .hasMessage(LoanException.Code.BOOK_NOT_FOUND.name())
                .extracting(e -> ((LoanException) e).code())
                .isEqualTo(LoanException.Code.BOOK_NOT_FOUND);

        verifyNoInteractions(members, loans);
    }

    @Test
    void borrow_whenBookUnavailable_throwsBookUnavailableException() {
        long bookId = 1L;
        long memberId = 100L;

        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, false)));

        assertThatThrownBy(() -> loanService.borrow(bookId, memberId))
                .isInstanceOf(LoanException.class)
                .hasMessage(LoanException.Code.BOOK_UNAVAILABLE.name())
                .extracting(e -> ((LoanException) e).code())
                .isEqualTo(LoanException.Code.BOOK_UNAVAILABLE);

        verifyNoInteractions(members, loans);
    }

    @Test
    void borrow_whenMemberNotFound_throwsMemberNotFoundException() {
        long bookId = 1L;
        long memberId = 100L;

        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, true)));
        when(members.findById(memberId)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> loanService.borrow(bookId, memberId))
                .isInstanceOf(LoanException.class)
                .hasMessage(LoanException.Code.MEMBER_NOT_FOUND.name())
                .extracting(e -> ((LoanException) e).code())
                .isEqualTo(LoanException.Code.MEMBER_NOT_FOUND);

        verifyNoInteractions(loans);
    }

    @Test
    void borrow_whenActiveLoansCountIsThree_throwsLimitReachedException() {
        long bookId = 1L;
        long memberId = 100L;

        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, true)));
        when(members.findById(memberId)).thenReturn(Optional.of(new Member(memberId, BigDecimal.ZERO)));
        when(loans.countActiveByMemberId(memberId)).thenReturn(3L);

        assertThatThrownBy(() -> loanService.borrow(bookId, memberId))
                .isInstanceOf(LoanException.class)
                .hasMessage(LoanException.Code.LIMIT_REACHED.name())
                .extracting(e -> ((LoanException) e).code())
                .isEqualTo(LoanException.Code.LIMIT_REACHED);
    }

    @Test
    void borrow_whenActiveLoansCountIsMoreThanThree_throwsLimitReachedException() {
        long bookId = 1L;
        long memberId = 100L;

        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, true)));
        when(members.findById(memberId)).thenReturn(Optional.of(new Member(memberId, BigDecimal.ZERO)));
        when(loans.countActiveByMemberId(memberId)).thenReturn(4L);

        assertThatThrownBy(() -> loanService.borrow(bookId, memberId))
                .isInstanceOf(LoanException.class)
                .hasMessage(LoanException.Code.LIMIT_REACHED.name())
                .extracting(e -> ((LoanException) e).code())
                .isEqualTo(LoanException.Code.LIMIT_REACHED);
    }

    @Test
    void borrow_whenMemberHasUnpaidFine_throwsUnpaidFineException() {
        long bookId = 1L;
        long memberId = 100L;

        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, true)));
        when(members.findById(memberId)).thenReturn(Optional.of(new Member(memberId, new BigDecimal("0.01"))));
        when(loans.countActiveByMemberId(memberId)).thenReturn(2L);

        assertThatThrownBy(() -> loanService.borrow(bookId, memberId))
                .isInstanceOf(LoanException.class)
                .hasMessage(LoanException.Code.UNPAID_FINE.name())
                .extracting(e -> ((LoanException) e).code())
                .isEqualTo(LoanException.Code.UNPAID_FINE);

        verify(loans, never()).save(any());
    }

    @Test
    void borrow_whenMemberHasZeroUnpaidFineAndUnderLimit_createsLoanAndUpdatesBook() {
        long bookId = 1L;
        long memberId = 100L;

        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, true)));
        when(members.findById(memberId)).thenReturn(Optional.of(new Member(memberId, new BigDecimal("0.00"))));
        when(loans.countActiveByMemberId(memberId)).thenReturn(2L);

        Loan expectedLoan = new Loan("loan-uuid-123", bookId, memberId, FIXED_INSTANT);
        when(loans.save(any(Loan.class))).thenReturn(expectedLoan);

        Loan result = loanService.borrow(bookId, memberId);

        assertThat(result).isEqualTo(expectedLoan);

        ArgumentCaptor<Loan> loanCaptor = ArgumentCaptor.forClass(Loan.class);
        verify(loans).save(loanCaptor.capture());
        Loan capturedLoan = loanCaptor.getValue();

        assertThat(capturedLoan.bookId()).isEqualTo(bookId);
        assertThat(capturedLoan.memberId()).isEqualTo(memberId);
        assertThat(capturedLoan.borrowedAt()).isEqualTo(FIXED_INSTANT);
        assertThat(capturedLoan.id()).isNotNull().isNotBlank();

        verify(books).save(new Book(bookId, false));
    }
}
