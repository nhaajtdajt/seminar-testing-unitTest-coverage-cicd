package vn.edu.seminar.persistence;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;

@Entity
@Table(name = "loans")
class LoanEntity {
    @Id private String id;
    private long bookId;
    private long memberId;
    private Instant borrowedAt;

    protected LoanEntity() { }
    LoanEntity(String id, long bookId, long memberId, Instant borrowedAt) {
        this.id = id; this.bookId = bookId; this.memberId = memberId; this.borrowedAt = borrowedAt;
    }

    String id() { return id; }
    long bookId() { return bookId; }
    long memberId() { return memberId; }
    Instant borrowedAt() { return borrowedAt; }
}
