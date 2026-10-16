package vn.edu.seminar.persistence;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "books")
class BookEntity {
    @Id private Long id;
    private boolean available;

    protected BookEntity() { }
    BookEntity(Long id, boolean available) { this.id = id; this.available = available; }

    Long id() { return id; }
    boolean available() { return available; }
}
