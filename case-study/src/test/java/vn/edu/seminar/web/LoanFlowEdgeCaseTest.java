package vn.edu.seminar.web;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;
import vn.edu.seminar.loan.Book;
import vn.edu.seminar.loan.BookRepository;
import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/** Integration test: HTTP → real LoanService → H2, for cases LoanFlowTest does not cover. */
@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class LoanFlowEdgeCaseTest {
    @Autowired MockMvc mvc;
    @Autowired BookRepository books;

    private ResultActions borrow(long bookId, long memberId) throws Exception {
        return mvc.perform(post("/api/loans").contentType("application/json")
                .content("{\"bookId\":" + bookId + ",\"memberId\":" + memberId + "}"));
    }

    @Test void thanhVienKhongTonTaiTraVe404() throws Exception {
        borrow(1, 99).andExpect(status().isNotFound()).andExpect(jsonPath("$.code").value("MEMBER_NOT_FOUND"));
        assertThat(books.findById(1)).contains(new Book(1, true));
    }

    @Test void muonBiTuChoiKhongKhoaSach() throws Exception {
        borrow(3, 2).andExpect(status().isConflict()).andExpect(jsonPath("$.code").value("UNPAID_FINE"));
        assertThat(books.findById(3)).contains(new Book(3, true));
        borrow(3, 1).andExpect(status().isCreated()).andExpect(jsonPath("$.memberId").value(1));
    }

    @Test void cuonThuTuBiChanVaSachVanConTrenKe() throws Exception {
        books.save(new Book(4, true));
        books.save(new Book(5, true));
        borrow(1, 1).andExpect(status().isCreated());
        borrow(3, 1).andExpect(status().isCreated());
        borrow(4, 1).andExpect(status().isCreated());
        borrow(5, 1).andExpect(status().isConflict()).andExpect(jsonPath("$.code").value("LIMIT_REACHED"));
        assertThat(books.findById(5)).contains(new Book(5, true));
    }
}
