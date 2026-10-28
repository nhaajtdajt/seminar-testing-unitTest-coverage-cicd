package vn.edu.seminar.antipattern;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.*;

/**
 * Minh họa 3 trường hợp Mockito bị lạm dụng hoặc chống chỉ định (Anti-patterns):
 * 1. Mock quá sâu (Train Wreck / vi phạm định luật Demeter).
 * 2. Test tự xác nhận (Self-fulfilling prophecy / Testing the mock).
 * 3. Mock logic thuần túy thay vì dùng đối tượng thật.
 *
 * Được đánh dấu tag "antipattern" để không chạy trong surefire pipeline chính.
 */
@Tag("antipattern")
@ExtendWith(MockitoExtension.class)
class MockitoAntiPatternTest {

    // Models giả lập cho trường hợp 1: Train Wreck
    interface Department { Manager getManager(); }
    interface Manager { Office getOffice(); }
    interface Office { String getAddress(); }

    @Mock Department department;
    @Mock Manager manager;
    @Mock Office office;

    @Test
    @DisplayName("Anti-pattern 1: Mock train-wreck (vi phạm Law of Demeter)")
    void antiPattern_trainWreckMocking() {
        // Mock sâu nhiều tầng: method chaining d->m->o->address
        // Vấn đề: Test bị gắn chặt (tightly-coupled) vào cấu trúc nội bộ của object graph.
        // Khi cấu trúc đổi (ví dụ: chuyển address lên Department), toàn bộ mock chain bị gãy dù hành vi không đổi.
        when(department.getManager()).thenReturn(manager);
        when(manager.getOffice()).thenReturn(office);
        when(office.getAddress()).thenReturn("227 Nguyen Van Cu, Q5");

        String actualAddress = department.getManager().getOffice().getAddress();

        assertThat(actualAddress).isEqualTo("227 Nguyen Van Cu, Q5");
        // Khắc phục: Áp dụng Law of Demeter / Tell Don't Ask: department.getOfficeAddress()
    }

    // Service giả lập cho trường hợp 2: Test tự xác nhận
    interface PricingService {
        long calculateDiscount(String memberTier, long amount);
    }

    @Mock PricingService pricingService;

    @Test
    @DisplayName("Anti-pattern 2: Self-fulfilling prophecy (Test chính mock thay vì test logic)")
    void antiPattern_selfFulfillingProphecy() {
        // Giả lập mock trả về 10_000
        when(pricingService.calculateDiscount("VIP", 100_000L)).thenReturn(10_000L);

        // Gọi mock và assert lại chính giá trị đã cấu hình
        long discount = pricingService.calculateDiscount("VIP", 100_000L);

        // Vấn đề: Test này 100% pass nhưng giá trị kiểm thử là 0.
        // Nó chỉ kiểm tra xem Mockito có nhớ giá trị vừa gán hay không,
        // hoàn toàn không kiểm thử bất kỳ thuật toán giảm giá nào của sản phẩm!
        assertThat(discount).isEqualTo(10_000L);
    }

    // Dịch vụ tính toán logic thuần cho trường hợp 3
    static class TaxCalculator {
        public double computeVat(double amount) {
            return amount * 0.10;
        }
    }

    @Mock TaxCalculator mockTaxCalculator;

    @Test
    @DisplayName("Anti-pattern 3: Mock đối tượng tính toán thuần túy (Pure Logic / Value Object)")
    void antiPattern_mockingPureLogic() {
        // Cố tình mock một class không hề có I/O hay side-effects
        when(mockTaxCalculator.computeVat(100.0)).thenReturn(10.0);

        double vat = mockTaxCalculator.computeVat(100.0);

        assertThat(vat).isEqualTo(10.0);
        // Vấn đề: Đối tượng pure logic không có dependency nên được khởi tạo trực tiếp (new TaxCalculator())
        // Việc mock vừa làm chậm tốc độ test (khởi tạo CGLIB/ByteBuddy proxy), vừa bỏ qua lỗi tính toán thật.
    }
}
