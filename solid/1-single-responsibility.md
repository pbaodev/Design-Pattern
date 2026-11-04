# S: Single Responsibility Principle (SRP)

> **SOLID** · [← Tổng quan SOLID](README.md)

**Definition:** Mỗi class chỉ nên có **một lý do để thay đổi**.

"Trách nhiệm" ở đây **không** phải "chỉ làm một việc nhỏ", mà là class chỉ phục vụ **một nguồn yêu cầu thay đổi** (*actor*), ví dụ phòng kinh doanh, đội DBA hoặc bộ phận marketing.

**Analogy:** Ở nhà hàng, đầu bếp nấu ăn, thu ngân tính tiền, phục vụ bưng bê. Nếu một người kiêm cả ba, chỉ riêng việc đổi thực đơn cũng làm xáo trộn khâu thu tiền.

---

## 1. Problem

```python
class OrderService:
    def place_order(self, order: dict):
        # (1) Nghiệp vụ: tính tiền
        total = sum(i["price"] * i["qty"] for i in order["items"])
        if total > 1_000_000:
            total *= 0.95

        # (2) Lưu trữ
        with sqlite3.connect("shop.db") as conn:
            conn.execute("INSERT INTO orders VALUES (?, ?)", (order["id"], total))

        # (3) Thông báo
        smtp = smtplib.SMTP("smtp.gmail.com")
        smtp.sendmail("shop@x.com", order["email"], f"Tổng tiền: {total}")
```

Class này có **3 lý do để thay đổi**, đến từ 3 nhóm người khác nhau:

| Ai yêu cầu | Thay đổi gì |
|---|---|
| Phòng kinh doanh | Chính sách giảm giá |
| Đội backend / DBA | Đổi SQLite sang PostgreSQL |
| Marketing | Nội dung email, hoặc chuyển sang gửi SMS |

- Sửa phần email có thể **vô tình làm hỏng** phần tính tiền, vì cả hai nằm chung một hàm.
- Muốn **test logic tính tiền** thì phải có cả database lẫn SMTP server.

## 2. Solution

1. Tách mỗi trách nhiệm thành **một class riêng**: `PriceCalculator`, `OrderRepository`, `OrderNotifier`.
2. `OrderService` chỉ còn **điều phối** các bước, không tự làm chi tiết.

## 3. Code

```python
from dataclasses import dataclass


@dataclass
class Item:
    name: str
    price: int
    qty: int


@dataclass
class Order:
    id: int
    email: str
    items: list[Item]


# ----- Mỗi class có đúng 1 lý do để thay đổi -----
class PriceCalculator:                 # đổi khi: chính sách giá thay đổi
    def total(self, order: Order) -> int:
        total = sum(i.price * i.qty for i in order.items)
        return int(total * 0.95) if total > 1_000_000 else total


class OrderRepository:                 # đổi khi: cách lưu trữ thay đổi
    def __init__(self):
        self._rows: dict[int, int] = {}            # giả lập database

    def save(self, order: Order, total: int) -> None:
        self._rows[order.id] = total
        print(f"💾 Lưu đơn #{order.id}")


class OrderNotifier:                   # đổi khi: nội dung hoặc kênh thông báo thay đổi
    def send_confirmation(self, order: Order, total: int) -> None:
        print(f"📧 Gửi {order.email}: Đơn #{order.id}, tổng {total:,}đ")


# ----- Class điều phối: chỉ nối các bước lại với nhau -----
class OrderService:
    def __init__(self, calculator: PriceCalculator, repo: OrderRepository, notifier: OrderNotifier):
        self.calculator = calculator
        self.repo = repo
        self.notifier = notifier

    def place_order(self, order: Order) -> int:
        total = self.calculator.total(order)
        self.repo.save(order, total)
        self.notifier.send_confirmation(order, total)
        return total


service = OrderService(PriceCalculator(), OrderRepository(), OrderNotifier())
order = Order(1, "an@example.com", [Item("Bàn phím", 800_000, 1), Item("Chuột", 300_000, 1)])
service.place_order(order)
# 💾 Lưu đơn #1
# 📧 Gửi an@example.com: Đơn #1, tổng 1,045,000đ

# Test logic giá: không cần database, không cần email
assert PriceCalculator().total(order) == 1_045_000
```

## 4. Trade-offs

| ✅ Được | ❌ Mất |
|---|---|
| Class nhỏ, dễ đọc, dễ đặt tên | Nhiều class và file hơn, phải nhảy qua lại khi đọc |
| Sửa một phần không ảnh hưởng phần khác | Tách quá nhỏ (mỗi class 1 method) làm mất cái nhìn tổng thể |
| Test riêng từng phần | |
| Dùng lại được: `PriceCalculator` dùng luôn cho trang giỏ hàng | |

**In practice:** tách theo **lý do thay đổi**, không theo số dòng code. Một class 300 dòng phục vụ đúng một nghiệp vụ vẫn có thể hợp lý.

## 5. Code smells & related patterns

**Code smells:**
- Tên class có chữ `And`, `Manager`, `Utils`, `Helper`.
- Mô tả class cần dùng chữ "và": "class này tính tiền **và** lưu DB **và** gửi mail".
- Một file import từ nhiều tầng khác nhau: DB driver, HTTP client, template email.
- Xem `git log`: class bị sửa vì nhiều lý do không liên quan tới nhau.

**Related patterns:**
- `OrderService` ở trên chính là một [Facade](../02-structural/facade.md) nhỏ, chỉ điều phối các bước.
- [Command](../03-behavioral/command.md) tách nơi *ra lệnh* khỏi nơi *thực hiện*.

## 6. Bài tập

Class dưới đây có mấy lý do để thay đổi? Hãy tách nó ra.

```python
class Report:
    def __init__(self, title, rows):
        self.title = title
        self.rows = rows

    def total(self):
        return sum(r["amount"] for r in self.rows)

    def to_html(self):
        return f"<h1>{self.title}</h1><p>Tổng: {self.total()}</p>"

    def save_to_file(self, path):
        with open(path, "w") as f:
            f.write(self.to_html())
```

<details>
<summary><b>Xem đáp án</b></summary>

Class này có **3 lý do để thay đổi**:
1. Dữ liệu và cách tính: thêm cột, đổi công thức tổng.
2. Định dạng hiển thị: HTML → PDF, Excel.
3. Nơi lưu: file local → S3, gửi email.

```python
class Report:                              # dữ liệu + tính toán
    def __init__(self, title: str, rows: list[dict]):
        self.title = title
        self.rows = rows

    def total(self) -> int:
        return sum(r["amount"] for r in self.rows)


class HtmlReportFormatter:                 # định dạng
    def format(self, report: Report) -> str:
        return f"<h1>{report.title}</h1><p>Tổng: {report.total()}</p>"


class FileStorage:                         # lưu trữ
    def save(self, content: str, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


report = Report("Doanh thu", [{"amount": 100}, {"amount": 250}])
FileStorage().save(HtmlReportFormatter().format(report), "report.html")
```

Cần thêm bản PDF? Viết thêm `PdfReportFormatter`, không phải sửa `Report` hay `FileStorage`.

</details>

---

[← Tổng quan SOLID](README.md) · [O: Open/Closed →](2-open-closed.md)
