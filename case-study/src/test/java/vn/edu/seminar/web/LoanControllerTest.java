package vn.edu.seminar.web;

import java.time.Instant;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import vn.edu.seminar.loan.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(LoanController.class)
@Import(LoanExceptionHandler.class)
class LoanControllerTest {
    @Autowired MockMvc mvc;
    @MockitoBean LoanService service;

    @Test void taoPhieuMuonTraVe201() throws Exception {
        when(service.borrow(1, 1)).thenReturn(new Loan("L-1", 1, 1, Instant.parse("2026-10-16T00:00:00Z")));
        mvc.perform(post("/api/loans").contentType("application/json").content("{\"bookId\":1,\"memberId\":1}"))
                .andExpect(status().isCreated()).andExpect(jsonPath("$.id").value("L-1"));
        verify(service).borrow(1, 1);
    }

    @Test void dauVaoAmKhongGoiService() throws Exception {
        mvc.perform(post("/api/loans").contentType("application/json").content("{\"bookId\":-1,\"memberId\":1}"))
                .andExpect(status().isBadRequest());
        verifyNoInteractions(service);
    }

    @Test void thieuMemberIdKhongGoiService() throws Exception {
        mvc.perform(post("/api/loans").contentType("application/json").content("{\"bookId\":1}"))
                .andExpect(status().isBadRequest());
        verifyNoInteractions(service);
    }

    @Test void sachKhongTonTaiTraVe404() throws Exception {
        when(service.borrow(99, 1)).thenThrow(new LoanException(LoanException.Code.BOOK_NOT_FOUND));
        mvc.perform(post("/api/loans").contentType("application/json").content("{\"bookId\":99,\"memberId\":1}"))
                .andExpect(status().isNotFound()).andExpect(jsonPath("$.code").value("BOOK_NOT_FOUND"));
    }

    @Test void sachDaMuonTraVe409() throws Exception {
        when(service.borrow(2, 1)).thenThrow(new LoanException(LoanException.Code.BOOK_UNAVAILABLE));
        mvc.perform(post("/api/loans").contentType("application/json").content("{\"bookId\":2,\"memberId\":1}"))
                .andExpect(status().isConflict()).andExpect(jsonPath("$.code").value("BOOK_UNAVAILABLE"));
    }
}
