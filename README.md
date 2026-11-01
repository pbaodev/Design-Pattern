# 10 Design Pattern phổ biến nhất

> Chọn lọc 10 trong 22 pattern của [catalog refactoring.guru](https://refactoring.guru/design-patterns/catalog), là những pattern gặp nhiều nhất trong thực tế.
> Code ví dụ viết bằng **Python 3.10+**. Bài nào cũng đi theo một khung: **Problem → Solution → Code → Trade-offs**.
>
> 📘 Học kèm: [**SOLID: 5 nguyên lý thiết kế**](solid/README.md), nền tảng giải thích *vì sao* các pattern tồn tại.

## Design pattern là gì?

Design pattern là **lời giải đã được kiểm chứng** cho những vấn đề thiết kế hay lặp lại. Nó không phải đoạn code để copy-paste mà là một **bản thiết kế**: bạn nắm ý tưởng rồi điều chỉnh theo bài toán của mình.

## 3 nhóm pattern

| Nhóm | Trả lời câu hỏi | Pattern trong bộ này |
|------|-----------------|---------------------|
| **Creational** (khởi tạo) | Tạo object thế nào cho linh hoạt? | Singleton, Factory Method, Builder |
| **Structural** (cấu trúc) | Ghép các object thành cấu trúc lớn hơn thế nào? | Adapter, Decorator, Facade, Proxy |
| **Behavioral** (hành vi) | Các object giao tiếp và chia trách nhiệm thế nào? | Strategy, Observer, Command |

## Danh sách bài học

| # | Pattern | Nhóm | Giải quyết vấn đề | Ví dụ trong bài |
|---|---------|------|-------------------|-----------------|
| 1 | [Singleton](01-creational/singleton.md) | Creational | Chỉ được có **đúng 1 instance** dùng chung | Kết nối database |
| 2 | [Factory Method](01-creational/factory-method.md) | Creational | Tạo object **mà không gắn chặt vào class cụ thể** | Gửi thông báo Email/SMS |
| 3 | [Builder](01-creational/builder.md) | Creational | Lắp ráp object **phức tạp, từng bước** | SQL query builder |
| 4 | [Adapter](02-structural/adapter.md) | Structural | Cho 2 interface **không tương thích** làm việc với nhau | Tích hợp cổng thanh toán bên thứ 3 |
| 5 | [Decorator](02-structural/decorator.md) | Structural | **Thêm hành vi** cho object mà không sửa class | Nén + mã hóa dữ liệu |
| 6 | [Facade](02-structural/facade.md) | Structural | **Đơn giản hóa** việc dùng một hệ thống phức tạp | Quy trình đặt hàng |
| 7 | [Proxy](02-structural/proxy.md) | Structural | **Kiểm soát truy cập** tới object (cache, lazy, phân quyền) | Cache cho API thời tiết |
| 8 | [Strategy](03-behavioral/strategy.md) | Behavioral | **Hoán đổi thuật toán** lúc runtime, bỏ chuỗi if/else | Tính phí vận chuyển |
| 9 | [Observer](03-behavioral/observer.md) | Behavioral | Một thay đổi cần **báo cho nhiều nơi** | Cảnh báo giá cổ phiếu |
| 10 | [Command](03-behavioral/command.md) | Behavioral | **Đóng gói hành động thành object** (undo, hàng đợi) | Undo/Redo trong editor |

## Cấu trúc mỗi bài

1. **Problem**: tình huống thực tế, kèm code "chưa dùng pattern" để thấy rõ vấn đề.
2. **Solution**: ý tưởng cốt lõi, kèm sơ đồ.
3. **Code**: ví dụ chạy được, có comment ở các dòng quan trọng, kèm mục *Pythonic hơn* là cách viết gọn hơn nhờ tính năng của Python.
4. **Trade-offs**: ưu và nhược điểm, khi nào nên và không nên dùng.
5. **Ngoài thực tế**: thư viện hoặc framework nào đang dùng pattern này, và nó dễ bị nhầm với pattern nào.

> Sơ đồ viết bằng Mermaid. GitHub hiển thị sẵn; trong VS Code cần cài extension *Markdown Preview Mermaid Support*.

## 3 nguyên lý nền tảng

Nắm được 3 nguyên lý này là hiểu được phần lớn lý do các pattern tồn tại:

1. **Program to an interface, not an implementation**: code phụ thuộc vào *interface* (`ABC`) chứ không vào class cụ thể, nhờ vậy dễ thay thế.
2. **Composition over inheritance**: quan hệ "có một" (chứa object khác) linh hoạt hơn "là một" (kế thừa), vì đổi được hành vi lúc runtime.
3. **Open/Closed Principle**: mở để mở rộng (thêm class mới), đóng để sửa đổi (không sửa code cũ).

Hầu hết các pattern dưới đây chỉ là cách áp dụng 3 nguyên lý này vào một tình huống cụ thể.

## Cheat sheet: gặp dấu hiệu X thì nghĩ tới pattern Y

| Dấu hiệu trong code | Pattern |
|---|---|
| Khối `if type == "a": A() elif type == "b": B()` lặp lại ở nhiều nơi | Factory Method |
| Constructor 7–8 tham số, hoặc phải ghép object từng bước có điều kiện | Builder |
| Khối `if method == "x": ... elif method == "y": ...` để chọn thuật toán | Strategy |
| Thư viện ngoài có interface khác với code của mình | Adapter |
| Muốn thêm logging/cache/nén... mà không sửa class gốc | Decorator / Proxy |
| Client phải gọi 5–6 subsystem theo đúng thứ tự | Facade |
| Một sự kiện xảy ra, nhiều module cần phản ứng | Observer |
| Cần undo/redo, đưa thao tác vào hàng đợi, hoặc ghi lại thao tác | Command |
| Cần đúng 1 object dùng chung toàn app | Singleton (cân nhắc Dependency Injection trước) |

## Các pattern dễ nhầm

**4 pattern "bọc" object.** Cả bốn đều đặt một object đứng trước object khác, chỉ khác nhau ở **mục đích**:

| Pattern | Interface so với object gốc | Mục đích |
|---|---|---|
| Adapter | **Khác** | Chuyển đổi interface cho tương thích |
| Decorator | **Giống** | Thêm hành vi, xếp chồng được nhiều lớp, do client tự lắp |
| Proxy | **Giống** | Kiểm soát truy cập (cache, lazy, quyền), thường tự quản lý object thật |
| Facade | **Mới, đơn giản hơn** | Gói *nhiều* subsystem sau một cửa duy nhất |

**Strategy vs Command.** Cả hai đều biến một thứ thành object. Strategy đóng gói *cách làm* một việc (thuật toán thay thế được). Command đóng gói *việc cần làm* (yêu cầu cụ thể, có thể lưu lại, hoãn hoặc hoàn tác).

**Factory Method vs Builder.** Factory Method quyết định *tạo class nào*, xong trong 1 bước. Builder quyết định *lắp ráp object ra sao*, qua nhiều bước.

## Lộ trình học gợi ý

1. **[Strategy](03-behavioral/strategy.md)** trước tiên: đơn giản nhất, thể hiện rõ nhất nguyên lý "program to an interface".
2. **Factory Method → Builder → Singleton**: nhóm khởi tạo.
3. **Adapter → Facade → Decorator → Proxy**: học liền 4 pattern "bọc" để thấy rõ khác biệt.
4. **Observer → Command**: giao tiếp giữa các object.

> 💡 Python có first-class function, module và cú pháp `@decorator`, nên nhiều pattern có cách viết gọn hơn bản OOP kinh điển. Hãy hiểu bản kinh điển trước, sau đó mới tới bản Pythonic.

## Học tiếp: SOLID

3 nguyên lý ở trên có họ hàng gần với **SOLID**, bộ 5 nguyên lý thiết kế mà phần lớn design pattern được xây dựng dựa trên. Open/Closed chính là chữ **O**, còn "program to an interface" là tinh thần của chữ **D** (Dependency Inversion). Xem [**solid/README.md**](solid/README.md): 5 bài, mỗi bài kèm bài tập, cùng một bài tổng hợp refactor từng bước.
