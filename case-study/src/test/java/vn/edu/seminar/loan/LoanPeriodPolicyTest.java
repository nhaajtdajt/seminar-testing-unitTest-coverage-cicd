package vn.edu.seminar.loan;

import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import vn.edu.seminar.fine.MemberTier;
import static org.assertj.core.api.Assertions.assertThat;

/** Bộ test T1–T4: mỗi test thêm vào thì một loại coverage đạt 100% (xem BaoCao_ChiTiet mục 3.1). */
class LoanPeriodPolicyTest {
    private final LoanPeriodPolicy policy = new LoanPeriodPolicy();
    private static final BigDecimal NO_DEBT = BigDecimal.ZERO;
    private static final BigDecimal DEBT = new BigDecimal("2000");

    @Test void t1_vipKhongNoSachMoi() {
        assertThat(policy.loanDays(MemberTier.VIP, true, NO_DEBT)).isEqualTo(14);
    }

    @Test void t2_thuongKhongNoSachCu() {
        assertThat(policy.loanDays(MemberTier.NORMAL, false, NO_DEBT)).isEqualTo(14);
    }

    @Test void t3_vipNoPhiSachMoi() {
        assertThat(policy.loanDays(MemberTier.VIP, true, DEBT)).isEqualTo(7);
    }

    @Test void t4_vipKhongNoSachCu() {
        assertThat(policy.loanDays(MemberTier.VIP, false, NO_DEBT)).isEqualTo(21);
    }
}
