package vn.edu.seminar.fine;
import java.math.BigDecimal;
public final class FineCalculator { public BigDecimal calculate(int daysLate, MemberTier tier) { return BigDecimal.valueOf(daysLate * 2000L); } }
