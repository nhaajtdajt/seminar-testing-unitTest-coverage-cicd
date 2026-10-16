package vn.edu.seminar.loan;

import java.time.Instant;

public record Loan(String id, long bookId, long memberId, Instant borrowedAt) { }
