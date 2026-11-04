# SOLID: 5 nguyên lý thiết kế hướng đối tượng

> [← Trang chính](../README.md) · Code ví dụ: **Python 3.10+**

## SOLID là gì?

SOLID là 5 nguyên lý do Robert C. Martin (Uncle Bob) tổng hợp, giúp code **dễ hiểu, dễ sửa, dễ mở rộng và dễ test**. Mục tiêu chung: khi yêu cầu thay đổi, bạn **sửa ít chỗ nhất** và **không làm hỏng chỗ khác**.

- **SOLID** là *nguyên lý*: mô tả thiết kế cần đạt tới.
- **Design pattern** là *giải pháp cụ thể* cho một tình huống thiết kế. Phần lớn pattern là cách hiện thực các nguyên lý SOLID.

## 5 nguyên lý

| | Nguyên lý | Definition | Câu hỏi tự kiểm tra |
|---|---|---|---|
| **S** | [Single Responsibility](1-single-responsibility.md) | Mỗi class chỉ có một lý do để thay đổi, tức là chỉ phục vụ một nguồn yêu cầu. | Class này có đang làm cả tính tiền, lưu database và gửi email không? |
| **O** | [Open/Closed](2-open-closed.md) | Thêm hành vi mới bằng cách viết code mới, không sửa code đã chạy ổn. | Thêm một định dạng xuất báo cáo có phải sửa hàm đang xử lý các định dạng cũ không? |
| **L** | [Liskov Substitution](3-liskov-substitution.md) | Object của class con phải thay được object của class cha mà chương trình vẫn đúng, tức là class con tuân thủ mọi contract của class cha. | Thay bằng class con có khiến thao tác vốn hợp lệ bị lỗi hoặc cho kết quả sai không? |
| **I** | [Interface Segregation](4-interface-segregation.md) | Không ép class implement những method nó không dùng. | Class máy in có bị buộc implement `scan()` và `fax()` không? |
| **D** | [Dependency Inversion](5-dependency-inversion.md) | Nghiệp vụ phụ thuộc vào interface do chính nó định nghĩa; class database, email cụ thể implement interface đó. | Đổi MySQL sang PostgreSQL, quy tắc nghiệp vụ giữ nguyên, có phải sửa class nghiệp vụ không? |

Với các câu hỏi trên, **“Có” là dấu hiệu cần xem lại thiết kế**, chưa đủ để kết luận chắc chắn vi phạm.

Sau 5 bài là [**Bài tổng hợp**](6-capstone.md): refactor từng bước một class vi phạm cả 5 nguyên lý.

## Cấu trúc mỗi bài

Mở đầu mỗi bài là **Definition** và **Analogy**, sau đó:

1. **Problem**: code vi phạm nguyên lý và hậu quả cụ thể.
2. **Solution**: hướng refactor.
3. **Code**: bản đã refactor, chạy được.
4. **Trade-offs**: được gì, mất gì, rủi ro khi áp dụng quá mức; kèm mục *In practice*.
5. **Code smells & related patterns**: dấu hiệu nhận biết vi phạm và link sang các pattern liên quan.
6. **Bài tập**: tự refactor trước khi mở đáp án.

## Code smells

| | Dấu hiệu |
|---|---|
| **S** | Class dài hàng nghìn dòng; tên chung chung kiểu `Manager`, `Utils`, `Helper`; một file import cả DB, email lẫn PDF |
| **O** | Chuỗi `if type == ...` hay `match` theo loại, cứ thêm loại mới là phải sửa |
| **L** | Subclass ném `NotImplementedError` hoặc để trống method của cha; code gọi phải dùng `isinstance()` để xử lý riêng |
| **I** | Interface có hơn 10 method; class implement method rỗng chỉ để thỏa interface |
| **D** | `self.db = MySQLDatabase()` nằm trong `__init__`; không test được nếu thiếu DB thật |

## SOLID ↔ Design Pattern

| | Pattern hiện thực nguyên lý |
|---|---|
| **S** | [Facade](../02-structural/facade.md) (gom việc điều phối về một chỗ), [Command](../03-behavioral/command.md) (tách nơi ra lệnh khỏi nơi thực hiện) |
| **O** | [Strategy](../03-behavioral/strategy.md), [Template Method](../03-behavioral/template-method.md), [Decorator](../02-structural/decorator.md), [Factory Method](../01-creational/factory-method.md), [Observer](../03-behavioral/observer.md) |
| **L** | Mọi pattern dựa trên interface (Strategy, Decorator, Template Method...) chỉ chạy đúng khi các implementation tuân thủ LSP |
| **I** | [Adapter](../02-structural/adapter.md) và [Facade](../02-structural/facade.md) (chỉ đưa ra đúng interface client cần), `typing.Protocol` |
| **D** | [Adapter](../02-structural/adapter.md), [Decorator](../02-structural/decorator.md), Dependency Injection (cách thay thế [Singleton](../01-creational/singleton.md)) |

## ⚠️ Đừng áp dụng máy móc

SOLID là **kim chỉ nam**, không phải luật. Áp dụng quá mức sẽ sinh ra hàng chục class nhỏ và những interface chỉ có đúng một implementation, khiến code còn khó đọc hơn bản ban đầu.

- Viết đơn giản trước, **chỉ refactor theo SOLID khi thay đổi thực sự xuất hiện** (lần thứ 2–3 phải sửa cùng một chỗ).
- Nếu chỉ áp dụng được một phần, ưu tiên **S** và **D**: hai nguyên lý này cải thiện rõ nhất khả năng đọc và test.

## Lộ trình

**S → O → L → I → D → [Bài tổng hợp](6-capstone.md)**. Mỗi bài đều có bài tập; tự làm trước khi mở đáp án.
