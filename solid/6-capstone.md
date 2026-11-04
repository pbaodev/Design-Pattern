# Bài tổng hợp: refactor một class vi phạm cả 5 nguyên lý

> **SOLID** · [← Tổng quan SOLID](README.md)

Bài này lấy một đoạn code checkout vi phạm cả 5 nguyên lý và refactor **từng bước**, mỗi bước áp dụng một nguyên lý.

---

## Code ban đầu

```python
class PaymentMethod(ABC):                            # ❌ I: fat interface
    @abstractmethod
    def pay(self, amount: float) -> None: ...

    @abstractmethod
    def save_card(self, token: str) -> None: ...


class CardPayment(PaymentMethod):
    def pay(self, amount):
        print(f"💳 Quẹt thẻ {amount:,.0f}đ")

    def save_card(self, token):
        print(f"💾 Lưu thẻ {token}")


class CashOnDelivery(PaymentMethod):
    def pay(self, amount):
        print(f"💵 Thu {amount:,.0f}đ khi giao")

    def save_card(self, token):                       # ❌ L + I: bị ép implement nên phải ném lỗi
        raise NotImplementedError("COD không có thẻ")


class InvoiceService:
    def __init__(self):
        self.db = SqliteDatabase("shop.db")           # ❌ D: tự tạo class cụ thể
        self.mailer = SmtpMailer("smtp.gmail.com")    # ❌ D

    def checkout(self, invoice: dict, customer_type: str,
                 payment: PaymentMethod, card_token: str | None = None):
        # ❌ S: một method làm 4 việc: tính tiền, thanh toán, lưu, gửi mail
        subtotal = sum(i["price"] * i["qty"] for i in invoice["items"])
        if customer_type == "vip":                    # ❌ O: thêm loại khách → sửa hàm này
            subtotal *= 0.9
        elif customer_type == "employee":
            subtotal *= 0.7
        total = subtotal * 1.1                        # VAT 10%

        payment.pay(total)
        if card_token and not isinstance(payment, CashOnDelivery):   # ❌ L: phải check kiểu
            payment.save_card(card_token)

        self.db.insert("invoices", {"id": invoice["id"], "total": total})
        self.mailer.send(invoice["email"], f"Hóa đơn #{invoice['id']}: {total:,.0f}đ")
```

| | Vi phạm | Hậu quả |
|---|---|---|
| **S** | `checkout()` đảm nhận cả tính tiền, thanh toán, lưu DB và gửi mail | Sửa nội dung email có thể làm hỏng phần tính tiền |
| **O** | Chuỗi `if/elif` theo `customer_type` | Thêm loại khách nào cũng phải sửa `checkout()` |
| **L** | `CashOnDelivery.save_card()` ném lỗi | Code gọi phải `isinstance()` để tránh crash |
| **I** | `PaymentMethod` bắt mọi phương thức thanh toán phải có `save_card()` | COD bị ép implement method vô nghĩa |
| **D** | Tự tạo `SqliteDatabase` và `SmtpMailer` | Không test được nếu thiếu DB và SMTP thật |

---

## Bước 1. S: tách trách nhiệm

Mỗi lý do thay đổi ứng với một class; `InvoiceService` chỉ còn điều phối.

```python
class PriceCalculator:       # đổi khi: chính sách giá thay đổi
    def total(self, invoice) -> float: ...

class InvoiceRepository:     # đổi khi: cách lưu trữ thay đổi
    def save(self, invoice_id, total): ...

class Notifier:              # đổi khi: nội dung hoặc kênh thông báo thay đổi
    def send(self, to, message): ...
```

## Bước 2. O: bỏ chuỗi if/elif theo loại khách

Mỗi chính sách giảm giá là một hàm ([Strategy](../03-behavioral/strategy.md) bản Pythonic), lưu trong một registry:

```python
DiscountPolicy = Callable[[float], float]      # nhận subtotal, trả về số tiền giảm

discounts = {
    "vip": lambda s: s * 0.1,
    "employee": lambda s: s * 0.3,
}
# Thêm "student" = thêm 1 dòng, PriceCalculator không phải sửa
```

## Bước 3 + 4. L và I: hai vi phạm cùng nguyên nhân

Vi phạm L (COD ném lỗi) **bắt nguồn từ** vi phạm I (fat interface). Đây là trường hợp rất phổ biến: interface quá lớn buộc class con implement method không phù hợp, dẫn tới vi phạm LSP.

- **I:** `PaymentMethod` chỉ còn `pay()`, thao tác mọi phương thức thanh toán đều hỗ trợ.
- Lưu thẻ là **logic riêng của thanh toán thẻ**, nên chuyển vào `CardPayment`.
- **L:** từ giờ mọi `PaymentMethod` đều thay thế được cho nhau, `checkout()` không cần `isinstance()` nữa.

```python
class PaymentMethod(Protocol):
    def pay(self, amount: float) -> None: ...

class CardPayment:
    def __init__(self, token: str, remember: bool = False): ...
    def pay(self, amount): ...       # tự lưu thẻ nếu remember=True

class CashOnDelivery:
    def pay(self, amount): ...       # không còn method nào bị ép
```

## Bước 5. D: nhận dependency từ ngoài vào

`InvoiceService` chỉ biết các abstraction (`InvoiceRepository`, `Notifier`). Class cụ thể nào được dùng thì do **composition root** quyết định.

---

## Kết quả cuối cùng

```python
from dataclasses import dataclass
from typing import Callable, Protocol


@dataclass
class Item:
    name: str
    price: int
    qty: int


@dataclass
class Invoice:
    id: int
    email: str
    customer_type: str
    items: list[Item]


# ===== Abstractions (D + I): interface nhỏ, do tầng nghiệp vụ định nghĩa =====
class PaymentMethod(Protocol):
    def pay(self, amount: float) -> None: ...


class InvoiceRepository(Protocol):
    def save(self, invoice_id: int, total: float) -> None: ...


class Notifier(Protocol):
    def send(self, to: str, message: str) -> None: ...


DiscountPolicy = Callable[[float], float]       # nhận subtotal, trả về số tiền giảm


# ===== Nghiệp vụ =====
class PriceCalculator:                          # S: chỉ lo tính tiền
    VAT = 0.1

    def __init__(self, discounts: dict[str, DiscountPolicy]):
        self._discounts = discounts             # O: thêm loại khách = thêm 1 entry

    def total(self, invoice: Invoice) -> float:
        subtotal = sum(i.price * i.qty for i in invoice.items)
        discount = self._discounts.get(invoice.customer_type, lambda s: 0)(subtotal)
        return (subtotal - discount) * (1 + self.VAT)


class InvoiceService:                           # S: chỉ điều phối; D: nhận dependency từ ngoài
    def __init__(self, calculator: PriceCalculator, repo: InvoiceRepository, notifier: Notifier):
        self._calculator = calculator
        self._repo = repo
        self._notifier = notifier

    def checkout(self, invoice: Invoice, payment: PaymentMethod) -> float:
        total = self._calculator.total(invoice)
        payment.pay(total)                      # L: PaymentMethod nào cũng dùng được, không isinstance
        self._repo.save(invoice.id, total)
        self._notifier.send(invoice.email, f"Hóa đơn #{invoice.id}: {total:,.0f}đ")
        return total


# ===== Chi tiết hạ tầng: implement các abstraction =====
class CardPayment:
    def __init__(self, token: str, remember: bool = False):
        self._token = token
        self._remember = remember

    def pay(self, amount):
        print(f"💳 Quẹt thẻ {amount:,.0f}đ")
        if self._remember:                      # I: lưu thẻ là logic riêng của CardPayment
            print(f"💾 Lưu thẻ {self._token}")


class CashOnDelivery:
    def pay(self, amount):
        print(f"💵 Thu {amount:,.0f}đ khi giao")


class SqliteInvoiceRepository:
    def save(self, invoice_id, total):
        print(f"🗄️  Lưu hóa đơn #{invoice_id}")


class EmailNotifier:
    def send(self, to, message):
        print(f"📧 {to}: {message}")


# ===== Composition root: nơi duy nhất lắp ráp các class cụ thể =====
discounts: dict[str, DiscountPolicy] = {
    "vip": lambda s: s * 0.1,
    "employee": lambda s: s * 0.3,
}
service = InvoiceService(PriceCalculator(discounts), SqliteInvoiceRepository(), EmailNotifier())

service.checkout(
    Invoice(1, "an@example.com", "vip", [Item("Tai nghe", 1_000_000, 2)]),
    CardPayment("tok_123", remember=True),
)
# 💳 Quẹt thẻ 1,980,000đ
# 💾 Lưu thẻ tok_123
# 🗄️  Lưu hóa đơn #1
# 📧 an@example.com: Hóa đơn #1: 1,980,000đ

service.checkout(
    Invoice(2, "binh@example.com", "regular", [Item("Sạc", 200_000, 1)]),
    CashOnDelivery(),
)
# 💵 Thu 220,000đ khi giao
# 🗄️  Lưu hóa đơn #2
# 📧 binh@example.com: Hóa đơn #2: 220,000đ
```

### Nhờ D, test không cần DB, SMTP hay cổng thanh toán

```python
class FakeRepo:
    def __init__(self):
        self.saved: dict[int, float] = {}

    def save(self, invoice_id, total):
        self.saved[invoice_id] = total


class FakeNotifier:
    def __init__(self):
        self.sent_to: list[str] = []

    def send(self, to, message):
        self.sent_to.append(to)


class FakePayment:
    def __init__(self):
        self.charged = 0.0

    def pay(self, amount):
        self.charged = amount


repo, notifier, payment = FakeRepo(), FakeNotifier(), FakePayment()
InvoiceService(PriceCalculator({}), repo, notifier).checkout(
    Invoice(9, "test@example.com", "regular", [Item("A", 100, 1)]), payment
)
assert round(payment.charged) == 110
assert 9 in repo.saved
assert notifier.sent_to == ["test@example.com"]
print("✅ Test pass")
```

---

## Khi có yêu cầu mới, phải sửa gì?

| Yêu cầu mới | Việc phải làm | Có sửa `InvoiceService` không? |
|---|---|---|
| Thêm loại khách "student" giảm 5% | Thêm 1 dòng vào `discounts` | ❌ Không |
| Thêm thanh toán qua ví MoMo | Viết class `MomoPayment` có `pay()` | ❌ Không |
| Chuyển từ SQLite sang PostgreSQL | Viết `PostgresInvoiceRepository`, đổi 1 dòng ở composition root | ❌ Không |
| Gửi thông báo qua Zalo thay vì email | Viết `ZaloNotifier`, đổi 1 dòng ở composition root | ❌ Không |
| Đổi mức VAT | Sửa `PriceCalculator.VAT` | ❌ Không |

Đây chính là mục tiêu của SOLID: **thay đổi chỉ chạm vào đúng một chỗ, và chỗ đó dễ tìm.**

## Trade-offs

Từ 4 class ban đầu, code tăng lên khoảng 12 class, protocol và type alias, tức là **nhiều code hơn**. Refactor này đáng làm khi:
- Yêu cầu **thay đổi thường xuyên** (giá, phương thức thanh toán, kênh thông báo).
- Code cần **unit test** và được **nhiều người** cùng bảo trì.

Với prototype hoặc script dùng một lần, bản ban đầu thường là lựa chọn đúng. Chỉ refactor **khi chi phí thay đổi thực sự xuất hiện**.

---

[← D: Dependency Inversion](5-dependency-inversion.md) · [Tổng quan SOLID](README.md)
