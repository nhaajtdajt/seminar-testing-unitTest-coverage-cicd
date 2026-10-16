package vn.edu.seminar.loan;

import java.util.Optional;

public interface MemberRepository {
    Optional<Member> findById(long id);
}
