package vn.edu.seminar.web;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/** Integration test: real service and in-memory repositories, no Mockito. */
@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class LoanFlowTest {
    @Autowired MockMvc mvc;

    @Test void muonSachRoiMuonLaiBiChan() throws Exception {
        mvc.perform(post("/api/loans").contentType("application/json").content("{\"bookId\":1,\"memberId\":1}"))
                .andExpect(status().isCreated()).andExpect(jsonPath("$.bookId").value(1));
        mvc.perform(post("/api/loans").contentType("application/json").content("{\"bookId\":1,\"memberId\":1}"))
                .andExpect(status().isConflict()).andExpect(jsonPath("$.code").value("BOOK_UNAVAILABLE"));
    }

    @Test void thanhVienConNoKhongMuonDuoc() throws Exception {
        mvc.perform(post("/api/loans").contentType("application/json").content("{\"bookId\":3,\"memberId\":2}"))
                .andExpect(status().isConflict()).andExpect(jsonPath("$.code").value("UNPAID_FINE"));
    }
}
