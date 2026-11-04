# 10 Design Pattern phổ biến nhất

> 10 pattern được dùng nhiều nhất trong 22 pattern của [catalog refactoring.guru](https://refactoring.guru/design-patterns/catalog).
> Code ví dụ viết bằng **Python 3.10+**. Bài nào cũng đi theo một khung: **Problem → Solution → Code → Trade-offs**.
>
> 📘 Học kèm: [**SOLID: 5 nguyên lý thiết kế**](solid/README.md), nền tảng giải thích _vì sao_ các pattern tồn tại.
> 🗄️ Chủ đề khác: [**Database Normalization**](database-normalization/README.md), chuẩn hóa cơ sở dữ liệu từ 1NF tới BCNF.

## Design pattern là gì?

Design pattern (mẫu thiết kế) là một **giải pháp có thể tái sử dụng** cho một loại vấn đề thường gặp khi thiết kế phần mềm hướng đối tượng. Pattern không phải đoạn code để copy-paste mà là một **bản thiết kế**: bạn nắm ý tưởng rồi điều chỉnh theo bài toán cụ thể.

## 3 nhóm pattern

| Nhóm                      | Trả lời câu hỏi                                   | Pattern trong bộ này                         |
| ------------------------- | ------------------------------------------------- | -------------------------------------------- |
| **Creational** (khởi tạo) | Tạo object thế nào cho linh hoạt?                 | Singleton, Factory Method, Builder           |
| **Structural** (cấu trúc) | Ghép các object thành cấu trúc lớn hơn thế nào?   | Adapter, Decorator, Facade                   |
| **Behavioral** (hành vi)  | Các object giao tiếp và chia trách nhiệm thế nào? | Strategy, Template Method, Observer, Command |

## Danh sách bài học

| #   | Pattern                                             | Nhóm       | Giải quyết vấn đề                                           | Ví dụ trong bài                    |
| --- | --------------------------------------------------- | ---------- | ----------------------------------------------------------- | ---------------------------------- |
| 1   | [Singleton](01-creational/singleton.md)             | Creational | Chỉ được có **đúng 1 instance** dùng chung                  | Kết nối database                   |
| 2   | [Factory Method](01-creational/factory-method.md)   | Creational | Tạo object **mà không gắn chặt vào class cụ thể**           | Gửi thông báo Email/SMS            |
| 3   | [Builder](01-creational/builder.md)                 | Creational | Lắp ráp object **phức tạp, từng bước**                      | SQL query builder                  |
| 4   | [Adapter](02-structural/adapter.md)                 | Structural | Cho 2 interface **không tương thích** làm việc với nhau     | Tích hợp cổng thanh toán bên thứ 3 |
| 5   | [Decorator](02-structural/decorator.md)             | Structural | **Thêm hành vi** cho object mà không sửa class              | Nén + mã hóa dữ liệu               |
| 6   | [Facade](02-structural/facade.md)                   | Structural | **Đơn giản hóa** việc dùng một hệ thống phức tạp            | Quy trình đặt hàng                 |
| 7   | [Strategy](03-behavioral/strategy.md)               | Behavioral | **Hoán đổi thuật toán** lúc runtime, bỏ chuỗi if/else       | Tính phí vận chuyển                |
| 8   | [Template Method](03-behavioral/template-method.md) | Behavioral | **Cố định khung các bước**, class con chỉ viết lại vài bước | Import dữ liệu CSV/JSON            |
| 9   | [Observer](03-behavioral/observer.md)               | Behavioral | Một thay đổi cần **báo cho nhiều nơi**                      | Cảnh báo giá cổ phiếu              |
| 10  | [Command](03-behavioral/command.md)                 | Behavioral | **Đóng gói hành động thành object** (undo, hàng đợi)        | Undo/Redo trong editor             |

## Cấu trúc mỗi bài

Mở đầu mỗi bài là **Purpose** (pattern giải quyết việc gì) và **Analogy** (ví dụ ngoài phần mềm), sau đó:

1. **Problem**: tình huống thực tế và đoạn code chưa dùng pattern.
2. **Solution**: ý tưởng cốt lõi, kèm sơ đồ class.
3. **Code**: ví dụ chạy được, comment ở các dòng quan trọng. Mục _Pythonic approach_ trình bày cách viết gọn hơn bằng tính năng riêng của Python.
4. **Trade-offs**: ưu, nhược điểm; _Use when_ và _Avoid when(không nên dùng khi)_.
5. **Real-world usage**: thư viện, framework đang dùng pattern, và pattern hay bị nhầm với nó.

> Sơ đồ viết bằng Mermaid. GitHub hiển thị sẵn; trong VS Code cần cài extension _Markdown Preview Mermaid Support_.

## 3 nguyên lý nền tảng

Nắm được 3 nguyên lý này là hiểu được phần lớn lý do các pattern tồn tại:

1. **Program to an interface, not an implementation**: code phụ thuộc vào _interface_ (`ABC`) chứ không vào class cụ thể, nhờ vậy dễ thay thế.
2. **Composition over inheritance**: quan hệ "có một" (chứa object khác) linh hoạt hơn "là một" (kế thừa), vì đổi được hành vi lúc runtime.
3. **Open/Closed Principle**: mở để mở rộng (thêm class mới), đóng để sửa đổi (không sửa code cũ).

Hầu hết các pattern dưới đây chỉ là cách áp dụng 3 nguyên lý này vào một tình huống cụ thể.

## Cheat sheet: code smell → pattern

| Code smell                                                              | Pattern                                         |
| ----------------------------------------------------------------------- | ----------------------------------------------- |
| Khối `if type == "a": A() elif type == "b": B()` lặp lại ở nhiều nơi    | Factory Method                                  |
| Constructor 7–8 tham số, hoặc phải ghép object từng bước có điều kiện   | Builder                                         |
| Khối `if method == "x": ... elif method == "y": ...` để chọn thuật toán | Strategy                                        |
| Thư viện ngoài có interface khác với code của mình                      | Adapter                                         |
| Muốn thêm logging/cache/nén... mà không sửa class gốc                   | Decorator                                       |
| Nhiều class copy-paste cùng các bước xử lý, chỉ khác 1–2 bước           | Template Method                                 |
| Client phải gọi 5–6 subsystem theo đúng thứ tự                          | Facade                                          |
| Một sự kiện xảy ra, nhiều module cần phản ứng                           | Observer                                        |
| Cần undo/redo, đưa thao tác vào hàng đợi, hoặc ghi lại thao tác         | Command                                         |
| Cần đúng 1 object dùng chung toàn app                                   | Singleton (cân nhắc Dependency Injection trước) |

## Các pattern dễ nhầm

**3 pattern "bọc" object.** Cả ba đều đặt một object đứng trước object khác, chỉ khác nhau ở **mục đích**:

| Pattern   | Interface so với object gốc | Mục đích                                                 |
| --------- | --------------------------- | -------------------------------------------------------- |
| Adapter   | **Khác**                    | Chuyển đổi interface cho tương thích                     |
| Decorator | **Giống**                   | Thêm hành vi, xếp chồng được nhiều lớp, do client tự lắp |
| Facade    | **Mới, đơn giản hơn**       | Gói _nhiều_ subsystem sau một cửa duy nhất               |

**Strategy vs Template Method.** Cả hai đều cho phép thay đổi thuật toán. Template Method dùng **kế thừa**: class cha giữ khung, class con thay _vài bước_, cố định từ lúc định nghĩa class. Strategy dùng **composition**: context giữ một strategy object, thay được _toàn bộ thuật toán_ và đổi được lúc runtime.

**Strategy vs Command.** Cả hai đều biến một thứ thành object. Strategy đóng gói _cách làm_ một việc (thuật toán thay thế được). Command đóng gói _việc cần làm_ (yêu cầu cụ thể, có thể lưu lại, hoãn hoặc hoàn tác).

**Factory Method vs Builder.** Factory Method quyết định _tạo class nào_, xong trong 1 bước. Builder quyết định _lắp ráp object ra sao_, qua nhiều bước.

## Lộ trình học gợi ý

1. **[Strategy](03-behavioral/strategy.md)** trước tiên: đơn giản nhất, thể hiện rõ nhất nguyên lý "program to an interface".
2. **[Template Method](03-behavioral/template-method.md)** ngay sau đó: cùng bài toán thay đổi thuật toán nhưng dùng kế thừa, để thấy rõ "composition over inheritance".
3. **Factory Method → Builder → Singleton**: nhóm khởi tạo.
4. **Adapter → Facade → Decorator**: học liền 3 pattern "bọc" để thấy rõ khác biệt.
5. **Observer → Command**: giao tiếp giữa các object.

> 💡 Python có first-class function, module và cú pháp `@decorator`, nên nhiều pattern có cách viết gọn hơn bản OOP kinh điển. Hãy hiểu bản kinh điển trước, sau đó mới tới bản Pythonic.

## Học tiếp: SOLID

3 nguyên lý ở trên gắn trực tiếp với **SOLID**, bộ 5 nguyên lý thiết kế làm nền cho phần lớn design pattern. Open/Closed chính là chữ **O**, còn "program to an interface" là tinh thần của chữ **D** (Dependency Inversion). Xem [**solid/README.md**](solid/README.md): 5 bài, mỗi bài kèm bài tập, cùng một bài tổng hợp refactor từng bước.
