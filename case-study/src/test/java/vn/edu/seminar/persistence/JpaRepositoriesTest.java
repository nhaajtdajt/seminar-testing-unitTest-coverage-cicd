package vn.edu.seminar.persistence;

import java.math.BigDecimal;
import java.time.Instant;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.context.annotation.Import;
import vn.edu.seminar.loan.Book;
import vn.edu.seminar.loan.Loan;
import static org.assertj.core.api.Assertions.assertThat;

/** Integration test against H2: checks the mapping and the Spring Data query that unit tests with mocks cannot see. */
@DataJpaTest
@Import({JpaBookRepository.class, JpaMemberRepository.class, JpaLoanRepository.class})
class JpaRepositoriesTest {
    @Autowired JpaBookRepository books;
    @Autowired JpaMemberRepository members;
    @Autowired JpaLoanRepository loans;

    @Test void docDuLieuMauTuH2() {
        assertThat(books.findById(1)).contains(new Book(1, true));
        assertThat(books.findById(2)).contains(new Book(2, false));
        assertThat(members.findById(2).orElseThrow().unpaidFine()).isEqualByComparingTo(new BigDecimal("5000"));
        assertThat(books.findById(99)).isEmpty();
    }

    @Test void luuSachRoiDocLaiThayDoiTrangThai() {
        books.save(new Book(1, false));
        assertThat(books.findById(1)).contains(new Book(1, false));
    }

    @Test void demPhieuMuonTheoTungThanhVien() {
        Instant now = Instant.parse("2026-10-16T00:00:00Z");
        loans.save(new Loan("L-1", 1, 1, now));
        loans.save(new Loan("L-2", 3, 1, now));
        loans.save(new Loan("L-3", 3, 2, now));
        assertThat(loans.countActiveByMemberId(1)).isEqualTo(2);
        assertThat(loans.countActiveByMemberId(2)).isEqualTo(1);
        assertThat(loans.countActiveByMemberId(99)).isZero();
    }
}
