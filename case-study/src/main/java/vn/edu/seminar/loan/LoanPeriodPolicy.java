package vn.edu.seminar.loan;

import java.math.BigDecimal;
import vn.edu.seminar.fine.MemberTier;

/**
 * Số ngày được mượn: mặc định 14; VIP không nợ phí +7; sách mới −7.
 * Ví dụ dạy các loại coverage: có if không else, điều kiện ghép và 4 đường đi.
 */
public final class LoanPeriodPolicy {
    public int loanDays(MemberTier tier, boolean newRelease, BigDecimal unpaidFine) {
        int days = 14;
        if (tier == MemberTier.VIP && unpaidFine.signum() == 0) {
            days += 7;
        }
        if (newRelease) {
            days -= 7;
        }
        return days;
    }
}
