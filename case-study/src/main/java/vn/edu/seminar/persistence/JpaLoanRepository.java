package vn.edu.seminar.persistence;

import org.springframework.stereotype.Repository;
import vn.edu.seminar.loan.Loan;
import vn.edu.seminar.loan.LoanRepository;

@Repository
class JpaLoanRepository implements LoanRepository {
    private final LoanJpaRepository jpa;

    JpaLoanRepository(LoanJpaRepository jpa) { this.jpa = jpa; }

    /** Seminar demo: loans are never returned, so every stored loan counts as active. */
    @Override public long countActiveByMemberId(long memberId) { return jpa.countByMemberId(memberId); }

    @Override public Loan save(Loan loan) {
        jpa.save(new LoanEntity(loan.id(), loan.bookId(), loan.memberId(), loan.borrowedAt()));
        return loan;
    }
}
