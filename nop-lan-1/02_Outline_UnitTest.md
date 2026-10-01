# Outline chi tiết — Phần 1: UNIT TEST

**Phụ trách:** TV2 · **Thời lượng dự kiến khi seminar:** ~25 phút

> Đây là outline *dự kiến*, chưa phải nội dung slide hoàn chỉnh. Mỗi mục ghi rõ nhóm sẽ
> trình bày điều gì và **chứng minh bằng gì** — vì đề yêu cầu thể hiện các bước làm chứ
> không chỉ kết quả.

---

## 1. Lý thuyết & thuật ngữ

| Mục | Sẽ trình bày điều gì | Chứng minh bằng |
|---|---|---|
| 1.1 Unit test là gì, "unit" là gì | Phân biệt unit / integration / E2E qua kim tự tháp kiểm thử; vì sao unit test rẻ nhất nên chạy nhiều nhất | Bảng đo **thời gian chạy thật** của 3 loại test trên case study của nhóm |
| 1.2 Nguyên tắc FIRST | **F**ast · **I**ndependent · **R**epeatable · **S**elf-validating · **T**imely | Mỗi chữ ghép với một ví dụ **vi phạm** lấy từ code thật, không phải ví dụ sách vở |
| 1.3 Cấu trúc AAA | Arrange – Act – Assert; vì sao tách 3 khối giúp đọc test như đọc tài liệu đặc tả | Trích trực tiếp từ test của nhóm |
| 1.4 Test Double | Phân biệt 5 loại: Dummy · Stub · Spy · Mock · Fake | Bảng so sánh + ví dụ Mockito cho từng loại |
| 1.5 Nên test cái gì, không nên test cái gì | Logic nhiều nhánh thì test; getter/setter và code của framework thì không | Đối chiếu báo cáo coverage: chỉ rõ chỗ nào **cố ý** để trống và vì sao |
| 1.6 Quan hệ với TDD | Vòng đỏ – xanh – refactor; vì sao viết test trước lại dẫn tới thiết kế dễ test hơn | **Chính commit history của nhóm**: mỗi vòng TDD là một commit riêng |

**Thuật ngữ nhóm sẽ chốt cách dịch và giải thích trên slide:**
test fixture · test double · stub · mock · spy · assertion · parameterized test ·
flaky test (test chập chờn) · test smell · tautological test (test tự xác nhận chính nó).

## 2. Công cụ

**Công cụ demo sâu: JUnit Jupiter + Mockito + AssertJ.**

| Thành phần | Vai trò | Nguyên lý hoạt động (phải nói được trên slide) |
|---|---|---|
| JUnit Jupiter | Khung chạy test: annotation, vòng đời, phát hiện test | Engine quét class theo quy ước, dựng cây test, chạy từng node và thu kết quả; Maven Surefire là cầu nối giữa `mvn test` và engine |
| Mockito | Tạo test double cho dependency | Sinh lớp con giả lập lúc chạy (bytecode proxy), ghi lại lời gọi để `verify` và trả giá trị đã khai báo qua `when/thenReturn` |
| AssertJ | Assertion đọc được như một câu | API fluent, thông báo lỗi chi tiết hơn assertion mặc định |

**Các annotation sẽ dùng trong demo:** `@Test` · `@DisplayName` (đặt tên test bằng tiếng Việt) ·
`@BeforeEach` · `@Nested` · `@Tag` · `@ParameterizedTest` · `@CsvSource` · `@CsvFileSource` ·
`@MethodSource`; phía Mockito: `@Mock` · `@ExtendWith(MockitoExtension.class)` ·
`when/thenReturn` · `verify` · `verify(never())` · `ArgumentCaptor`.

**Các công cụ sẽ khảo sát và so sánh** (chi tiết ở `05_KhaoSat_SoSanh_CongCu.md`):
TestNG · Spock · JUnit 4 · EasyMock · JMockit · Hamcrest.

## 3. Demo dự kiến

| Mã | Kịch bản | Nội dung | Số đo / minh chứng | Mức tự động |
|---|---|---|---|---|
| **UT-1** | **Cài đặt** | Thêm thư viện test vào `pom.xml`; chạy `mvn test` lần đầu; đọc output của Surefire; mở thư mục báo cáo | Số test chạy, thời gian | Fully automated |
| **UT-2** | **Chức năng cơ bản** | Viết lớp tính phí trả sách trễ theo TDD: đỏ → xanh → refactor, 4 vòng; cấu trúc AAA; tên test tiếng Việt; chuyển sang `@ParameterizedTest` đọc dữ liệu từ file CSV bên ngoài (**phần Data driven**) | Số ca kiểm thử, số vòng TDD; **commit history từng vòng** | Fully automated |
| **UT-3** | **Luồng xử lý phức tạp** | Test lớp nghiệp vụ cho mượn sách với 6 nhánh; mock 3 repository; `verify` đúng số lần gọi; `verify(never())` để chứng minh không ghi dữ liệu khi nghiệp vụ bị từ chối; `ArgumentCaptor` bắt đối tượng được lưu; dùng đồng hồ cố định để test không phụ thuộc thời gian thật (**phần Checkpoints**) | Số nhánh được phủ, số điểm kiểm chứng | Fully automated |

## 4. Điểm yếu của công cụ

Đề yêu cầu *"chỉ rõ những trường hợp công cụ có điểm yếu, không giải quyết tốt mục tiêu đặt
ra"*. Nhóm cam kết **mỗi điểm yếu dưới đây sẽ được chứng minh bằng code chạy thật**, không
chỉ nói lý thuyết.

| Điểm yếu | Cách nhóm sẽ chứng minh |
|---|---|
| **Mock quá sâu → test xanh nhưng hệ thống sai** | Viết hai bản test cho cùng một lớp: bản mock cả lớp tính phí, và bản dùng lớp tính phí thật. Sau đó **cố tình sửa sai công thức tính phí** → bản mock vẫn xanh, bản dùng thật đỏ ngay |
| **Test không có assertion vẫn được tính là "pass"** | Một test gọi method rồi không kiểm chứng gì; Surefire báo xanh. Đây cũng là đầu vào cho demo ở phần Code Coverage |
| **Test tự xác nhận chính nó (tautological)** | Mock trả về giá trị X rồi assert kết quả bằng X — test luôn xanh kể cả khi code bị xoá sạch |
| **Mockito không mock được `static` / `final` mặc định** | Thử mock hàm lấy ngày hiện tại → thất bại; từ đó giải thích vì sao nhóm chọn **inject đồng hồ** thay vì thêm thư viện `mockito-inline` |
| **`@InjectMocks` im lặng khi thiếu dependency** | Cố tình thiếu một mock → lỗi `NullPointerException` khó đọc, không chỉ ra nguyên nhân; từ đó giải thích vì sao nhóm khởi tạo bằng constructor tường minh |
| **Unit test không bắt được lỗi tích hợp** | Toàn bộ unit test xanh nhưng câu truy vấn Spring Data sai tên thuộc tính → chỉ test tích hợp với database mới lộ ra |

## 5. Bài tập áp dụng dự kiến cho lớp

| Bài | Yêu cầu | Gợi ý nhóm sẽ kèm theo |
|---|---|---|
| 1 | Cho sẵn một lớp tính giảm giá giỏ hàng chưa có test — viết test phủ hết các nhánh | Gợi ý liệt kê nhánh trước khi viết test; mẫu AAA |
| 2 | Chuyển 6 test lặp lại thành 1 `@ParameterizedTest` | Gợi ý chọn giữa `@CsvSource` và `@CsvFileSource` |
| 3 | Cho sẵn một lớp dịch vụ gọi 2 repository — viết test dùng Mockito | Gợi ý khi nào nên mock, khi nào dùng đối tượng thật |

*(Số lượng và mức độ bài tập nhóm xin ý kiến thầy/cô — xem `09_CauHoi_Cho_GV.md`.)*
