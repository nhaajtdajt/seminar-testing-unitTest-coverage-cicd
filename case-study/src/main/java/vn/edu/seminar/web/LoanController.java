package vn.edu.seminar.web;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Positive;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import vn.edu.seminar.loan.Loan;
import vn.edu.seminar.loan.LoanService;

@RestController
@RequestMapping("/api/loans")
public class LoanController {
    private final LoanService service;

    public LoanController(LoanService service) { this.service = service; }

    public record BorrowRequest(@Positive long bookId, @Positive long memberId) { }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Loan borrow(@Valid @RequestBody BorrowRequest request) {
        return service.borrow(request.bookId(), request.memberId());
    }
}
