# SOLID: 5 nguyên lý thiết kế hướng đối tượng

> [← Trang chính](../README.md) · Code ví dụ: **Python 3.10+**

## SOLID là gì?

SOLID là 5 nguyên lý do Robert C. Martin (Uncle Bob) tổng hợp, giúp code **dễ hiểu, dễ sửa, dễ mở rộng và dễ test**. Mục tiêu chung: khi yêu cầu thay đổi, bạn **sửa ít chỗ nhất** và **không làm hỏng chỗ khác**.

- **SOLID** là *nguyên lý*: chỉ ra code nên hướng tới điều gì.
- **Design pattern** là *giải pháp cụ thể*: cách làm cho một tình huống. Phần lớn các pattern chính là cách hiện thực các nguyên lý SOLID.

## 5 nguyên lý

| | Nguyên lý | Một câu | Câu hỏi tự kiểm tra |
|---|---|---|---|
| **S** | [Single Responsibility](1-single-responsibility.md) | Mỗi class chỉ có **một lý do để thay đổi** | Class này đang phục vụ mấy nhóm yêu cầu khác nhau? |
| **O** | [Open/Closed](2-open-closed.md) | **Mở** để mở rộng, **đóng** để sửa đổi | Thêm tính năng mới có phải sửa code cũ không? |
| **L** | [Liskov Substitution](3-liskov-substitution.md) | Class con phải **thay được** class cha mà chương trình vẫn đúng | Thay class cha bằng class con, code gọi có bị "bất ngờ" không? |
| **I** | [Interface Segregation](4-interface-segregation.md) | Đừng ép class phụ thuộc vào **method nó không dùng** | Có class nào implement một method chỉ để `raise NotImplementedError` không? |
| **D** | [Dependency Inversion](5-dependency-inversion.md) | Phụ thuộc vào **abstraction**, không phụ thuộc vào class cụ thể | Class nghiệp vụ có tự tạo database hay API client cụ thể bên trong không? |

Học xong 5 bài thì làm [**Bài tổng hợp**](6-capstone.md): refactor từng bước một class vi phạm cả 5 nguyên lý.

## Cấu trúc mỗi bài

1. **Problem**: code vi phạm nguyên lý, kèm chỉ ra cụ thể chỗ đau.
2. **Solution**: cách sửa.
3. **Code**: bản đã refactor, chạy được.
4. **Trade-offs**: được gì, mất gì, và chuyện gì xảy ra khi áp dụng quá đà.
5. **Dấu hiệu vi phạm và liên hệ pattern**: cách nhận ra vi phạm, kèm link sang bài design pattern liên quan.
6. **Bài tập**: tự refactor trước, rồi mới mở đáp án.

## Dấu hiệu vi phạm (code smell)

| | Dấu hiệu |
|---|---|
| **S** | Class dài hàng nghìn dòng; tên chung chung kiểu `Manager`, `Utils`, `Helper`; một file import cả DB, email lẫn PDF |
| **O** | Chuỗi `if type == ...` hay `match` theo loại, cứ thêm loại mới là phải sửa |
| **L** | Subclass ném `NotImplementedError` hoặc để trống method của cha; code gọi phải dùng `isinstance()` để xử lý riêng |
| **I** | Interface có hơn 10 method; class implement "cho có" |
| **D** | `self.db = MySQLDatabase()` nằm trong `__init__`; không test được nếu thiếu DB thật |

## SOLID ↔ Design Pattern

| | Pattern hiện thực nguyên lý |
|---|---|
| **S** | [Facade](../02-structural/facade.md) (gom việc điều phối về một chỗ), [Command](../03-behavioral/command.md) (tách nơi ra lệnh khỏi nơi thực hiện) |
| **O** | [Strategy](../03-behavioral/strategy.md), [Decorator](../02-structural/decorator.md), [Factory Method](../01-creational/factory-method.md), [Observer](../03-behavioral/observer.md) |
| **L** | Mọi pattern dựa trên interface (Strategy, Proxy, Decorator...) chỉ chạy đúng khi các implementation tuân thủ LSP |
| **I** | [Adapter](../02-structural/adapter.md) và [Facade](../02-structural/facade.md) (chỉ đưa ra đúng interface client cần), `typing.Protocol` |
| **D** | [Adapter](../02-structural/adapter.md), [Proxy](../02-structural/proxy.md), Dependency Injection (cách thay thế [Singleton](../01-creational/singleton.md)) |

## ⚠️ Đừng áp dụng máy móc

SOLID là **kim chỉ nam**, không phải luật. Áp dụng quá đà sẽ sinh ra hàng chục class nhỏ và những interface chỉ có đúng một implementation, khiến code còn khó đọc hơn bản ban đầu.

- Hãy viết đơn giản trước, và **chỉ refactor theo SOLID khi thay đổi thật sự xuất hiện** (lần thứ 2–3 phải sửa cùng một chỗ).
- Nếu chỉ áp dụng được một phần, hãy ưu tiên **S** và **D**: hai nguyên lý này mang lại lợi ích rõ nhất là code dễ đọc và dễ test.

## Lộ trình

**S → O → L → I → D → [Bài tổng hợp](6-capstone.md)**. Bài nào cũng có bài tập: hãy tự làm trước khi mở đáp án.
