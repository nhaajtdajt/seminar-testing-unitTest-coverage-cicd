package vn.edu.seminar.persistence;

import org.springframework.data.jpa.repository.JpaRepository;

interface BookJpaRepository extends JpaRepository<BookEntity, Long> { }

interface MemberJpaRepository extends JpaRepository<MemberEntity, Long> { }

interface LoanJpaRepository extends JpaRepository<LoanEntity, String> {
    long countByMemberId(long memberId);
}
