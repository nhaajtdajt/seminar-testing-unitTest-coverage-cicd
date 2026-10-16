package vn.edu.seminar.loan;

import java.math.BigDecimal;
import java.time.Clock;
import java.util.UUID;
import static vn.edu.seminar.loan.LoanException.Code.*;

/** In-memory seminar demo; synchronization is limited to this single application instance. */
public class LoanService {
    private final BookRepository books;
    private final MemberRepository members;
    private final LoanRepository loans;
    private final Clock clock;

    public LoanService(BookRepository books, MemberRepository members, LoanRepository loans, Clock clock) {
        this.books = books;
        this.members = members;
        this.loans = loans;
        this.clock = clock;
    }

    public synchronized Loan borrow(long bookId, long memberId) {
        Book book = books.findById(bookId).orElseThrow(() -> new LoanException(BOOK_NOT_FOUND));
        if (!book.available()) {
            throw new LoanException(BOOK_UNAVAILABLE);
        }
        Member member = members.findById(memberId).orElseThrow(() -> new LoanException(MEMBER_NOT_FOUND));
        if (loans.countActiveByMemberId(memberId) >= 3) {
            throw new LoanException(LIMIT_REACHED);
        }
        if (member.unpaidFine().compareTo(BigDecimal.ZERO) > 0) {
            throw new LoanException(UNPAID_FINE);
        }
        Loan loan = loans.save(new Loan(UUID.randomUUID().toString(), bookId, memberId, clock.instant()));
        books.save(new Book(bookId, false));
        return loan;
    }
}
