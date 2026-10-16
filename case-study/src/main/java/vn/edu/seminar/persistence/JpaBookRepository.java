package vn.edu.seminar.persistence;

import java.util.Optional;
import org.springframework.stereotype.Repository;
import vn.edu.seminar.loan.Book;
import vn.edu.seminar.loan.BookRepository;

@Repository
class JpaBookRepository implements BookRepository {
    private final BookJpaRepository jpa;

    JpaBookRepository(BookJpaRepository jpa) { this.jpa = jpa; }

    @Override public Optional<Book> findById(long id) {
        return jpa.findById(id).map(entity -> new Book(entity.id(), entity.available()));
    }

    @Override public void save(Book book) { jpa.save(new BookEntity(book.id(), book.available())); }
}
