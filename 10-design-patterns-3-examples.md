# 10 Design Patterns — 3 ví dụ ứng dụng cho mỗi pattern

> **Mục đích:** Bảng ôn tập 10 Design Patterns theo ba loại ví dụ: **đời thực**, **Python/framework**, và **HR Manager**. Các ví dụ framework có thể chỉ **tương đồng về ý tưởng thiết kế**, không nhất thiết là triển khai đầy đủ của pattern theo GoF.

| # | Design Pattern | Nhóm | Ví dụ đời thực | Ví dụ Python / Framework | Ví dụ HR Manager |
|---|---|---|---|---|---|
| 1 | **Singleton** | Creational | Một đầu mối quản lý cấu hình dùng chung cho các bộ phận. | `logging.getLogger("app")` trả về cùng một logger khi dùng cùng tên; đây là **registry theo tên**, tương tự Singleton nhưng không phải chỉ có một logger cho toàn hệ thống. | Một đối tượng `AppConfig` dùng chung để truy cập cấu hình ứng dụng; chỉ cần Singleton nếu thực sự yêu cầu một instance trong phạm vi process. |
| 2 | **Factory Method** | Creational | Nhà máy logistics: `RoadLogistics` tạo `Truck`, `SeaLogistics` tạo `Ship`. | Django class-based views: `get_form()` sử dụng `get_form_class()` để xác định class form cần khởi tạo; minh họa cơ chế tùy biến việc tạo đối tượng. | `EmailNotifier.create_sender()` tạo `EmailSender`, còn `SlackNotifier.create_sender()` tạo `SlackSender`. |
| 3 | **Builder** | Creational | Tùy biến cấu hình ô tô qua từng bước: động cơ → màu sắc → nội thất. | SQLAlchemy tạo truy vấn qua các bước `select(...).where(...).order_by(...)`; đây là **fluent/generative API tương tự Builder**, không phải GoF Builder đầy đủ. | `EmployeeBuilder().name("An").department("IT").salary(2000).build()` tạo dữ liệu nhân viên theo từng bước. |
| 4 | **Adapter** | Structural | Bộ chuyển USB-C sang HDMI giúp hai giao diện kết nối không tương thích làm việc với nhau. | SQLAlchemy `TypeDecorator` có thể chuyển đổi dữ liệu giữa Python và DB (`process_bind_param`, `process_result_value`); **tương tự ý tưởng thích nghi**, dù tên và thiết kế của API là Type Decorator. | `SMSAdapter.send()` chuyển lời gọi từ hệ thống mới thành `OldSMS.send_sms()` của API cũ. |
| 5 | **Decorator** | Structural | Gói quà: bổ sung giấy gói, nơ, thiệp mà không thay đổi món quà gốc. | Python function decorators như `@functools.lru_cache` thêm caching quanh lời gọi hàm; cùng ý tưởng bọc hành vi, khác cách triển khai class-based GoF. | `LoggingDecorator(EmailService())` ghi log trước/sau khi gọi `send()`, không sửa class EmailService. |
| 6 | **Facade** | Structural | Nút “Đặt hàng” điều phối kiểm tra hàng, thanh toán và xác nhận sau một thao tác. | Django `django.contrib.auth.authenticate()` cung cấp API đơn giản để thử các authentication backends; **mang đặc điểm của Facade**. | `LeaveFacade.request_leave()` phối hợp kiểm tra số ngày phép, lưu yêu cầu và gửi thông báo. |
| 7 | **Strategy** | Behavioral | Ứng dụng bản đồ chọn thuật toán tìm đường theo đi bộ, ô tô hoặc xe đạp. | Django password hashers cho phép sử dụng các thuật toán băm mật khẩu khác nhau qua giao diện chung; tương tự Strategy. | `OvertimeCalculator(WeekendStrategy())` áp dụng công thức OT ngày cuối tuần, có thể thay bằng `HolidayStrategy`. |
| 8 | **Observer** | Behavioral | Người đăng ký kênh nhận thông báo khi kênh có nội dung mới. | Django Signals: receiver đăng ký nhận sự kiện như `post_save`; minh họa cơ chế subscribe/notify. | Khi duyệt nghỉ phép, `LeaveSubject` thông báo cho `EmailObserver`, `AuditObserver` và các observer khác. |
| 9 | **Command** | Behavioral | Nút điều khiển TV đóng gói lệnh bật/tắt âm lượng để thiết bị thực hiện. | Django management commands đóng gói tác vụ như `migrate` thành lệnh có thể gọi qua CLI; **tương đồng với Command**, không nhất thiết đủ các vai trò GoF. | `ApproveLeaveCommand` chứa `leave_id` và receiver `LeaveService`; `CommandBus` gọi `execute()` để thực hiện. |
| 10 | **Template Method** | Behavioral | Quy trình pha đồ uống giữ các bước chung, tùy chỉnh cách pha cho từng loại. | `unittest.TestCase` điều phối quy trình chạy test và cho phép tùy chỉnh `setUp()`, test method, `tearDown()`; tương đồng Template Method. | `Report.generate()` quy định `load() → format() → export()`; `PDFReport` và `ExcelReport` override bước `export()`. |

## Ghi nhớ nhanh

| Pattern | Ý chính |
|---|---|
| Singleton | Dùng chung một instance trong phạm vi thiết kế |
| Factory Method | Class con quyết định đối tượng nào được tạo |
| Builder | Xây dựng đối tượng qua nhiều bước |
| Adapter | Chuyển đổi interface cho tương thích |
| Decorator | Bọc đối tượng để bổ sung hành vi |
| Facade | Đơn giản hóa cách gọi nhiều subsystem |
| Strategy | Hoán đổi thuật toán / chính sách xử lý |
| Observer | Đăng ký và nhận thông báo theo sự kiện |
| Command | Đóng gói một yêu cầu thành đối tượng |
| Template Method | Cố định bộ khung thuật toán, tùy chỉnh từng bước |

**Lưu ý:** Ví dụ thực tiễn chỉ minh họa cách áp dụng. Không nhất thiết phải dùng pattern nếu giải pháp đơn giản hơn đã đáp ứng yêu cầu. Với ví dụ Python/framework, nên phân biệt rõ **cơ chế tương tự** và **việc triển khai chính xác pattern GoF** khi giải thích với mentor.
