package vn.edu.seminar.loan;

import java.util.Optional;

public interface BookRepository {
    Optional<Book> findById(long id);
    void save(Book book);
}
