package vn.edu.seminar.fine;

import java.math.BigDecimal;

/** Amounts are VND. Grace: NORMAL=0 days, VIP=2 days; cap=50,000 VND. */
public final class FineCalculator {
    public BigDecimal calculate(int daysLate, MemberTier tier) {
        if (tier == null) {
            throw new IllegalArgumentException("Hạng thành viên không được trống");
        }
        if (daysLate < 0) {
            throw new IllegalArgumentException("Số ngày trễ không được âm");
        }
        int graceDays = tier == MemberTier.VIP ? 2 : 0;
        if (daysLate <= graceDays) {
            return BigDecimal.ZERO;
        }
        long dailyRate = tier == MemberTier.VIP ? 1000L : 2000L;
        long amount = (daysLate - (long) graceDays) * dailyRate;
        return BigDecimal.valueOf(Math.min(amount, 50_000L));
    }
}
