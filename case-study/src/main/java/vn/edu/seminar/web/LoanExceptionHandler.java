package vn.edu.seminar.web;

import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import vn.edu.seminar.loan.LoanException;

@RestControllerAdvice
public class LoanExceptionHandler {
    @ExceptionHandler(LoanException.class)
    public ResponseEntity<Map<String, String>> handle(LoanException exception) {
        int status = switch (exception.code()) {
            case BOOK_NOT_FOUND, MEMBER_NOT_FOUND -> 404;
            default -> 409;
        };
        return ResponseEntity.status(status).body(Map.of("code", exception.code().name()));
    }
}
