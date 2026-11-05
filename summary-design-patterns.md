# Tổng quan 10 Design Patterns

Design Pattern (mẫu thiết kế) là một giải pháp thiết kế có thể tái sử dụng cho một loại vấn đề thường gặp trong phát triển phần mềm hướng đối tượng.

10 patterns trong ảnh A4 tôi đã tạo được chia thành 3 nhóm:

| Nhóm       | Mục đích                                     | Design Patterns                              |
| ---------- | -------------------------------------------- | -------------------------------------------- |
| Creational | Cách tạo đối tượng                           | Singleton, Factory Method, Builder           |
| Structural | Cách tổ chức và kết hợp các đối tượng        | Adapter, Decorator, Facade                   |
| Behavioral | Cách các đối tượng phối hợp và xử lý hành vi | Strategy, Observer, Command, Template Method |

Dưới đây là nội dung của từng pattern theo ảnh mặt trước, gồm Purpose, Python Code và giải thích. Code được đánh máy lại theo bản dùng để tạo ảnh, chuẩn hóa một số dòng cho dễ đọc.

## I. Creational Patterns — Nhóm khởi tạo

### 1. Singleton

Purpose: Ensure only one instance of a class exists.

Đảm bảo một class chỉ có một instance (đối tượng) trong phạm vi áp dụng.

```python

```

Giải thích: Khi gọi `Singleton()` lần đầu, chương trình tạo một object. Các lần sau sẽ trả về chính object đã tạo, thay vì tạo object mới.

Ứng dụng: Một số loại đối tượng cấu hình hoặc registry dùng chung. Cần thận trọng với global state và concurrency.

### 2. Factory Method

Purpose: Let subclasses decide which object to create.

Cho phép class con quyết định loại object cụ thể cần tạo.

```
class Button: passclass HTML(Button): passclass Dialog:    def create(self):        raise NotImplementedErrorclass Web(Dialog):    def create(self):        return HTML()b = Web().create()
```

Giải thích: `Dialog` định nghĩa phương thức tạo object, còn `Web` quyết định tạo `HTML`.

Ứng dụng: Tạo các thành phần giao diện hoặc đối tượng xử lý tương ứng với từng môi trường.

### 3. Builder

Purpose: Construct complex objects step by step.

Xây dựng một object qua nhiều bước thay vì truyền quá nhiều tham số vào constructor.

```
class UserBuilder:    def __init__(self):        self.d = {}    def name(self, v):        self.d["name"] = v        return self    def age(self, v):        self.d["age"] = v        return self    def build(self):        return self.d.copy()u = UserBuilder().name("An").age(20).build()
```

Giải thích: Gọi lần lượt `name()`, `age()`, sau đó `build()` để tạo dữ liệu hoàn chỉnh. Mỗi method trả về `self` để có thể gọi liên tiếp.

Ứng dụng: Xây dựng đối tượng cấu hình, truy vấn phức tạp hoặc đối tượng có nhiều thuộc tính tùy chọn.

## II. Structural Patterns — Nhóm cấu trúc

### 4. Adapter

Purpose: Make incompatible interfaces work together.

Giúp hai thành phần có interface không tương thích làm việc được với nhau.

```
class OldAPI:    def sms(self, x):        print(x)class Adapter:    def __init__(self, api):        self.api = api    def send(self, x):        self.api.sms(x)Adapter(OldAPI()).send("Hi")
```

Giải thích: Code mới muốn gọi `send()`, nhưng hệ thống cũ chỉ có `sms()`. Adapter chuyển lời gọi `send()` thành `sms()` mà không phải sửa OldAPI.

Ứng dụng: Tích hợp API cũ hoặc dịch vụ bên thứ ba vào hệ thống mới.

### 5. Decorator

Purpose: Add behavior without modifying the original class.

Bổ sung hành vi cho object mà không sửa code gốc.

```
class Email:    def send(self, x):        print(x)class Log:    def __init__(self, obj):        self.obj = obj    def send(self, x):        print("log")        self.obj.send(x)Log(Email()).send("Hi")
```

Giải thích: `Log` bọc `Email`. Khi gọi `send()`, chương trình ghi log trước rồi gọi phương thức gửi email gốc.

Ứng dụng: Logging, caching, đo thời gian xử lý hoặc bổ sung hành vi quanh một chức năng.

Lưu ý: Decorator Pattern này không hoàn toàn đồng nghĩa với cú pháp `@decorator` của Python, dù cả hai có cùng ý tưởng bổ sung hành vi.

### 6. Facade

Purpose: Provide a simple interface to complex subsystems.

Cung cấp một interface đơn giản để sử dụng nhiều hệ thống con phức tạp.

```
class Stock:    def ok(self):        return Trueclass Pay:    def charge(self):        print("Paid")class Checkout:    def order(self):        if Stock().ok():            Pay().charge()Checkout().order()
```

Giải thích: Client chỉ cần gọi `Checkout.order()`. Bên trong, Checkout tự phối hợp kiểm tra tồn kho và thanh toán.

Ứng dụng: Một service điều phối nhiều thành phần như kiểm tra tồn kho, thanh toán và tạo đơn hàng.

## III. Behavioral Patterns — Nhóm hành vi

### 7. Strategy

Purpose: Switch algorithms without changing the client.

Cho phép thay đổi thuật toán hoặc cách xử lý mà không phải sửa client.

```python
class Normal:
    def calc(self, x):
        return x

class VIP:
    def calc(self, x):
        return x * 0.8

class Cart:
    def __init__(self, s):
        self.s = s

    def total(self, x):
        return self.s.calc(x)

print(Cart(VIP()).total(100))
```

Giải thích: `Cart` không cần biết chi tiết cách giảm giá. Nó chỉ gọi `calc()` của strategy được truyền vào.

Ứng dụng: Các chính sách giảm giá, tính lương, tính OT hoặc lựa chọn thuật toán.

Đây cũng là cấu trúc tương tự ví dụ OCP chúng ta đã học.

### 8. Observer

Purpose: Notify subscribers when an event occurs.

Thông báo cho các đối tượng đăng ký khi một sự kiện xảy ra.

```python
class Subject:
    def __init__(self):
        self.fns = []

    def add(self, f):
        self.fns += [f]

    def emit(self, x):
        for f in self.fns:
            f(x)

s = Subject()
s.add(print)
s.emit("Updated")
```

Giải thích: `Subject` lưu danh sách các hàm theo dõi. Khi gọi `emit()`, tất cả hàm đã đăng ký sẽ được thông báo.

Ứng dụng: Hệ thống sự kiện, thông báo khi yêu cầu nghỉ phép được duyệt, cập nhật giao diện theo trạng thái.

### 9. Command

Purpose: Encapsulate a request as an object.

Đóng gói một yêu cầu hoặc hành động thành một object riêng.

```
class Lamp:    def on(self):        print("On")class OnCmd:    def __init__(self, obj):        self.obj = obj    def execute(self):        self.obj.on()class Remote:    def press(self, c):        c.execute()Remote().press(OnCmd(Lamp()))
```

Giải thích: `Remote` không trực tiếp điều khiển Lamp. Nó nhận một Command và gọi `execute()`. Command chịu trách nhiệm thực hiện hành động tương ứng.

Ứng dụng: Undo/Redo, job queue, task scheduling hoặc lưu lịch sử thao tác.

### 10. Template Method

Purpose: Define an algorithm skeleton, allowing subclasses to customize steps.

Định nghĩa bộ khung cố định của thuật toán, cho phép class con tùy chỉnh từng bước.

```
class Report:    def run(self):        self.load()        self.render()    def load(self):        print("Load")    def render(self):        raise NotImplementedErrorclass PDF(Report):    def render(self):        print("PDF")PDF().run()
```

Giải thích: `Report.run()` quy định thứ tự `load()` rồi `render()`. Class PDF chỉ cần định nghĩa cách render, không thay đổi quy trình chung.

Ứng dụng: Quy trình xuất báo cáo PDF, Excel hoặc các pipeline xử lý có nhiều bước cố định.

## Tổng kết: Phân biệt nhanh 10 Patterns

| Pattern         | Từ khóa cần nhớ                      |
| --------------- | ------------------------------------ |
| Singleton       | Một instance                         |
| Factory Method  | Class con quyết định object được tạo |
| Builder         | Tạo object từng bước                 |
| Adapter         | Chuyển đổi interface                 |
| Decorator       | Bọc object để thêm hành vi           |
| Facade          | Đơn giản hóa hệ thống phức tạp       |
| Strategy        | Hoán đổi thuật toán                  |
| Observer        | Theo dõi và nhận thông báo           |
| Command         | Đóng gói hành động                   |
| Template Method | Bộ khung quy trình cố định           |

Lưu ý về bản A4: Các đoạn code trong ảnh là minh họa tối giản để ghi nhớ pattern, chưa phải implementation production-ready và chưa có unit test. Khi học sâu từng pattern, chúng ta sẽ phân tích ví dụ vi phạm hoặc chưa dùng pattern, refactor, viết pytest và giải thích best practices.

Thứ tự học tiếp: Bắt đầu với Singleton, theo đúng cách chúng ta đã học SOLID: hiểu vấn đề trước, sau đó xem code, giải thích từng phần và kiểm tra khả năng hiểu.