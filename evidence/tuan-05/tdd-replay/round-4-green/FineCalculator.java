package vn.edu.seminar.fine;
import java.math.BigDecimal;
public final class FineCalculator { public BigDecimal calculate(int daysLate, MemberTier tier) { return BigDecimal.valueOf(Math.min(50000L, tier == MemberTier.VIP ? Math.max(0, daysLate - 2L) * 1000 : daysLate * 2000L)); } }
