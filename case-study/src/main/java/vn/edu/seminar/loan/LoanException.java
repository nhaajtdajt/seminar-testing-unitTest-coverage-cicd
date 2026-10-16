package vn.edu.seminar.loan;

public class LoanException extends RuntimeException {
    public enum Code { BOOK_NOT_FOUND, BOOK_UNAVAILABLE, MEMBER_NOT_FOUND, LIMIT_REACHED, UNPAID_FINE }
    private final Code code;

    public LoanException(Code code) {
        super(code.name());
        this.code = code;
    }

    public Code code() { return code; }
}
