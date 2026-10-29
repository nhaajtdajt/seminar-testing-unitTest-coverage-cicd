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
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class LoanServiceGeminiAdditionalTest {

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
    @DisplayName("Ném lỗi LIMIT_REACHED khi số sách đang mượn lớn hơn 3 (ví dụ 4)")
    void borrow_ActiveLoansGreaterThanThree_ThrowsLoanExceptionLimitReached() {
        long bookId = 101L;
        long memberId = 1L;
        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, true)));
        when(members.findById(memberId)).thenReturn(Optional.of(new Member(memberId, BigDecimal.ZERO)));
        when(loans.countActiveByMemberId(memberId)).thenReturn(4L);

        assertThatThrownBy(() -> loanService.borrow(bookId, memberId))
                .isInstanceOf(LoanException.class)
                .extracting(e -> ((LoanException) e).code())
                .isEqualTo(LoanException.Code.LIMIT_REACHED);
    }

    @Test
    @DisplayName("Mượn sách thành công khi tiền phạt dạng BigDecimal có scale khác 0 (ví dụ 0.00)")
    void borrow_Success_WhenFineIsZeroWithScale() {
        long bookId = 102L;
        long memberId = 2L;
        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, true)));
        when(members.findById(memberId)).thenReturn(Optional.of(new Member(memberId, new BigDecimal("0.00"))));
        when(loans.countActiveByMemberId(memberId)).thenReturn(1L);
        when(loans.save(any(Loan.class))).thenAnswer(i -> i.getArgument(0));

        Loan result = loanService.borrow(bookId, memberId);

        assertThat(result).isNotNull();
        assertThat(result.memberId()).isEqualTo(memberId);
    }

    @Test
    @DisplayName("Xác nhận thông tin đối tượng Loan được lưu vào LoanRepository có UUID hợp lệ và Instant đúng từ Clock")
    void borrow_Success_VerifiesLoanSavedToRepository() {
        long bookId = 103L;
        long memberId = 3L;
        when(books.findById(bookId)).thenReturn(Optional.of(new Book(bookId, true)));
        when(members.findById(memberId)).thenReturn(Optional.of(new Member(memberId, BigDecimal.ZERO)));
        when(loans.countActiveByMemberId(memberId)).thenReturn(0L);
        when(loans.save(any(Loan.class))).thenAnswer(i -> i.getArgument(0));

        loanService.borrow(bookId, memberId);

        ArgumentCaptor<Loan> loanCaptor = ArgumentCaptor.forClass(Loan.class);
        verify(loans).save(loanCaptor.capture());
        Loan capturedLoan = loanCaptor.getValue();

        assertThat(capturedLoan.bookId()).isEqualTo(bookId);
        assertThat(capturedLoan.memberId()).isEqualTo(memberId);
        assertThat(capturedLoan.borrowedAt()).isEqualTo(fixedNow);
        assertThat(capturedLoan.id()).satisfies(id -> assertThat(UUID.fromString(id)).isNotNull());
    }
}
