package vn.edu.seminar.loan;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneId;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class LoanServiceGeminiDraftTest {

    @Mock
    private BookRepository books;

    @Mock
    private MemberRepository members;

    @Mock
    private LoanRepository loans;

    private Clock clock;
    private LoanService loanService;
    private final Instant fixedNow = Instant.parse("2026-03-30T10:00:00Z");

    @BeforeEach
    void setUp() {
        clock = Clock.fixed(fixedNow, ZoneId.of("UTC"));
        loanService = new LoanService(books, members, loans, clock);
    }

    @Test
    @DisplayName("Ném lỗi BOOK_NOT_FOUND khi không tìm thấy sách")
    void borrow_BookNotFound_ThrowsLoanExceptionBookNotFound() {
        long bookId = 100L;
        long memberId = 1L;
        when(books.findById(bookId)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> loanService.borrow(bookId, memberId))
                .isInstanceOf(LoanException.class)
                .extracting(e -> ((LoanException) e).code())
                .isEqualTo(LoanException.Code.BOOK_NOT_FOUND);

        verifyNoInteractions(members);
        verifyNoInteractions(loans);
    }

    @Test
    @DisplayName("Ném lỗi BOOK_UNAVAILABLE khi sách không còn khả dụng")
    void borrow_BookUnavailable_ThrowsLoanExceptionBookUnavailable() {
        long bookId = 100L;
        long memberId = 1L;
        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, false)));

        assertThatThrownBy(() -> loanService.borrow(bookId, memberId))
                .isInstanceOf(LoanException.class)
                .extracting(e -> ((LoanException) e).code())
                .isEqualTo(LoanException.Code.BOOK_UNAVAILABLE);

        verifyNoInteractions(members);
        verifyNoInteractions(loans);
    }

    @Test
    @DisplayName("Ném lỗi MEMBER_NOT_FOUND khi không tìm thấy thành viên")
    void borrow_MemberNotFound_ThrowsLoanExceptionMemberNotFound() {
        long bookId = 100L;
        long memberId = 1L;
        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, true)));
        when(members.findById(memberId)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> loanService.borrow(bookId, memberId))
                .isInstanceOf(LoanException.class)
                .extracting(e -> ((LoanException) e).code())
                .isEqualTo(LoanException.Code.MEMBER_NOT_FOUND);

        verifyNoInteractions(loans);
    }

    @Test
    @DisplayName("Ném lỗi LIMIT_REACHED khi thành viên đang vay 3 hoặc nhiều hơn 3 thư mục")
    void borrow_ActiveLoansLimitReached_ThrowsLoanExceptionLimitReached() {
        long bookId = 100L;
        long memberId = 1L;
        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, true)));
        when(members.findById(memberId)).thenReturn(Optional.of(new Member(memberId, BigDecimal.ZERO)));
        when(loans.countActiveByMemberId(memberId)).thenReturn(3L);

        assertThatThrownBy(() -> loanService.borrow(bookId, memberId))
                .isInstanceOf(LoanException.class)
                .extracting(e -> ((LoanException) e).code())
                .isEqualTo(LoanException.Code.LIMIT_REACHED);
    }

    @Test
    @DisplayName("Ném lỗi UNPAID_FINE khi thành viên có tiền phạt chưa thanh toán lớn hơn 0")
    void borrow_MemberHasUnpaidFine_ThrowsLoanExceptionUnpaidFine() {
        long bookId = 100L;
        long memberId = 1L;
        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, true)));
        when(members.findById(memberId)).thenReturn(Optional.of(new Member(memberId, new BigDecimal("0.01"))));
        when(loans.countActiveByMemberId(memberId)).thenReturn(2L);

        assertThatThrownBy(() -> loanService.borrow(bookId, memberId))
                .isInstanceOf(LoanException.class)
                .extracting(e -> ((LoanException) e).code())
                .isEqualTo(LoanException.Code.UNPAID_FINE);
    }

    @Test
    @DisplayName("Mượn sách thành công khi số sách đang mượn = 2 và tiền phạt = 0")
    void borrow_Success_WhenActiveLoansUnderLimitAndZeroFine() {
        long bookId = 100L;
        long memberId = 1L;
        Book availableBook = new Book(bookId, true);
        Member member = new Member(memberId, BigDecimal.ZERO);

        when(books.findById(bookId)).thenReturn(Optional.of(availableBook));
        when(members.findById(memberId)).thenReturn(Optional.of(member));
        when(loans.countActiveByMemberId(memberId)).thenReturn(2L);
        when(loans.save(any(Loan.class))).thenAnswer(invocation -> invocation.getArgument(0));

        Loan result = loanService.borrow(bookId, memberId);

        assertThat(result).isNotNull();
        assertThat(result.bookId()).isEqualTo(bookId);
        assertThat(result.memberId()).isEqualTo(memberId);
        assertThat(result.borrowedAt()).isEqualTo(fixedNow);
        assertThat(result.id()).isNotBlank();

        ArgumentCaptor<Book> bookCaptor = ArgumentCaptor.forClass(Book.class);
        verify(books).save(bookCaptor.capture());
        assertThat(bookCaptor.getValue().id()).isEqualTo(bookId);
        assertThat(bookCaptor.getValue().available()).isFalse();
    }

    @Test
    @DisplayName("Mượn sách thành công khi tiền phạt có giá trị âm")
    void borrow_Success_WhenMemberHasNegativeFine() {
        long bookId = 200L;
        long memberId = 2L;
        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, true)));
        when(members.findById(memberId)).thenReturn(Optional.of(new Member(memberId, new BigDecimal("-5.00"))));
        when(loans.countActiveByMemberId(memberId)).thenReturn(0L);
        when(loans.save(any(Loan.class))).thenAnswer(i -> i.getArgument(0));

        Loan result = loanService.borrow(bookId, memberId);

        assertThat(result).isNotNull();
        assertThat(result.bookId()).isEqualTo(bookId);
        assertThat(result.memberId()).isEqualTo(memberId);
        verify(books).save(new Book(bookId, false));
    }
}
