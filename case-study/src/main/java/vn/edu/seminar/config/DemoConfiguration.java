package vn.edu.seminar.config;

import java.time.Clock;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import vn.edu.seminar.loan.*;

@Configuration
public class DemoConfiguration {
    @Bean Clock clock() { return Clock.systemUTC(); }

    @Bean LoanService loanService(BookRepository books, MemberRepository members, LoanRepository loans, Clock clock) {
        return new LoanService(books, members, loans, clock);
    }
}
