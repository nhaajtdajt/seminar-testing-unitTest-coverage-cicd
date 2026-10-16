package vn.edu.seminar.persistence;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;

@Entity
@Table(name = "members")
class MemberEntity {
    @Id private Long id;
    private BigDecimal unpaidFine;

    protected MemberEntity() { }
    MemberEntity(Long id, BigDecimal unpaidFine) { this.id = id; this.unpaidFine = unpaidFine; }

    Long id() { return id; }
    BigDecimal unpaidFine() { return unpaidFine; }
}
