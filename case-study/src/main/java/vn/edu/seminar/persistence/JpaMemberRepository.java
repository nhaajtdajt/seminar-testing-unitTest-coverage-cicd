package vn.edu.seminar.persistence;

import java.util.Optional;
import org.springframework.stereotype.Repository;
import vn.edu.seminar.loan.Member;
import vn.edu.seminar.loan.MemberRepository;

@Repository
class JpaMemberRepository implements MemberRepository {
    private final MemberJpaRepository jpa;

    JpaMemberRepository(MemberJpaRepository jpa) { this.jpa = jpa; }

    @Override public Optional<Member> findById(long id) {
        return jpa.findById(id).map(entity -> new Member(entity.id(), entity.unpaidFine()));
    }
}
