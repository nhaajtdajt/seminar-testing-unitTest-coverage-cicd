package vn.edu.seminar.loan;

public interface LoanRepository {
    long countActiveByMemberId(long memberId);
    Loan save(Loan loan);
}
