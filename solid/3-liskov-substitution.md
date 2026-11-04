# L: Liskov Substitution Principle (LSP)

> **SOLID** · [← Tổng quan SOLID](README.md)

**Definition:** Mọi chỗ dùng **class cha** đều phải thay được bằng **class con** mà chương trình vẫn chạy **đúng**, nghĩa là class con tuân thủ toàn bộ *contract* của class cha.

**Analogy:** Thuê tài xế qua một công ty dịch vụ: bất kỳ ai được cử tới đều phải lái được xe. Cử người có chức danh tài xế nhưng không biết lái là vi phạm hợp đồng.

---

## 1. Problem

**Ví dụ kinh điển: hình vuông có phải là hình chữ nhật?**

```python
class Rectangle:
    def __init__(self, w, h):
        self.width, self.height = w, h

    def set_width(self, w):
        self.width = w

    def set_height(self, h):
        self.height = h

    def area(self):
        return self.width * self.height


class Square(Rectangle):              # "Hình vuông LÀ hình chữ nhật": đúng trong toán học
    def set_width(self, w):
        self.width = self.height = w  # buộc phải giữ 2 cạnh bằng nhau

    def set_height(self, h):
        self.width = self.height = h


def stretch(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(4)
    assert rect.area() == 20          # đúng với mọi Rectangle...

stretch(Rectangle(1, 1))   # OK
stretch(Square(1, 1))      # 💥 AssertionError: area = 16
```

**Ví dụ thực tế: tài khoản tiết kiệm có kỳ hạn.**

```python
class Account:
    def withdraw(self, amount):
        self.balance -= amount


class FixedDepositAccount(Account):           # có kỳ hạn: không được rút trước hạn
    def withdraw(self, amount):
        raise NotImplementedError("Không được rút trước hạn")


def pay_bills(accounts: list[Account]):
    for acc in accounts:
        acc.withdraw(100_000)                 # 💥 crash khi gặp FixedDepositAccount
```

Muốn tránh crash, code gọi phải thêm `if isinstance(acc, FixedDepositAccount): continue`, và như vậy lại vi phạm OCP.

> 💡 Quan hệ **is-a** trong thực tế chưa chắc là **is-a** trong code. Kế thừa phải dựa trên **hành vi**, không dựa trên cách phân loại khái niệm.

## 2. Solution

**Contract mà class con phải tuân thủ:**

| Quy tắc | Ví dụ |
|---|---|
| Precondition không được chặt hơn | Cha nhận mọi `amount > 0` thì con không được chỉ nhận `amount > 100` |
| Postcondition không được lỏng hơn | Cha luôn trả về `list` thì con không được trả `None` |
| Không ném exception mới | Con không được ném lỗi mà caller không lường trước (như `NotImplementedError`) |
| Giữ nguyên invariant | `width` và `height` của Rectangle độc lập với nhau |

**Cách sửa:** thiết kế lại cây kế thừa theo **khả năng**. Chỉ class nào thật sự rút được tiền mới có `withdraw()`.

## 3. Code

```python
class Account:
    def __init__(self, owner: str, balance: int = 0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: int) -> None:
        self.balance += amount


class WithdrawableAccount(Account):
    def withdraw(self, amount: int) -> None:
        if amount > self.balance:
            raise ValueError("Số dư không đủ")    # lỗi thuộc contract chung, caller đã biết trước
        self.balance -= amount


class CheckingAccount(WithdrawableAccount):      # tài khoản thanh toán
    pass


class SavingsAccount(WithdrawableAccount):       # tiết kiệm không kỳ hạn: rút được
    pass


class FixedDepositAccount(Account):              # có kỳ hạn: KHÔNG kế thừa khả năng rút tiền
    def __init__(self, owner: str, balance: int, term_months: int):
        super().__init__(owner, balance)
        self.term_months = term_months


def pay_bills(accounts: list[WithdrawableAccount], amount: int):
    for acc in accounts:
        acc.withdraw(amount)                     # phần tử nào cũng rút được, không cần isinstance
        print(f"✅ {acc.owner}: còn {acc.balance:,}đ")


pay_bills([CheckingAccount("An", 500_000), SavingsAccount("Bình", 300_000)], 100_000)
# ✅ An: còn 400,000đ
# ✅ Bình: còn 200,000đ

fixed = FixedDepositAccount("Chi", 10_000_000, term_months=12)
# pay_bills([fixed], 100_000)   ← mypy/pyright báo lỗi ngay lúc viết code, không phải đợi tới runtime
```

**Sửa ví dụ Rectangle/Square:** không cho `Square` kế thừa `Rectangle`. Cả hai implement `Shape` và là immutable object, nên không còn setter nào phá vỡ contract:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...


@dataclass(frozen=True)
class Rect(Shape):
    width: float
    height: float

    def area(self):
        return self.width * self.height


@dataclass(frozen=True)
class Square(Shape):
    side: float

    def area(self):
        return self.side ** 2


print([s.area() for s in (Rect(5, 4), Square(4))])   # [20, 16]
```

## 4. Trade-offs

| ✅ Được | ❌ Mất |
|---|---|
| Đa hình an toàn: code gọi tin tưởng được mọi subclass | Phải suy nghĩ kỹ hơn khi thiết kế cây kế thừa |
| Không cần rải `isinstance()` khắp nơi | Đôi khi phải tách thêm class hoặc interface |
| Cây class phản ánh đúng hành vi thật | Python không kiểm tra LSP lúc runtime, phải dựa vào test và type checker |

**Tip:** subclass phải override một method chỉ để **vô hiệu hóa** nó là dấu hiệu thiết kế sai; cân nhắc dùng composition thay cho kế thừa.

## 5. Code smells & related patterns

**Code smells:**
- Subclass override bằng `raise NotImplementedError`, hoặc để trống (`pass`) một method có ý nghĩa ở class cha.
- Code gọi phải `isinstance()` để xử lý riêng từng subclass.
- Subclass trả về kiểu khác, hoặc `None`, trong khi class cha luôn trả giá trị.
- Tài liệu nội bộ có ghi chú kiểu "không gọi method X trên class Y".

**Related patterns:** [Strategy](../03-behavioral/strategy.md), [Decorator](../02-structural/decorator.md), [Template Method](../03-behavioral/template-method.md) đều dựa trên việc **thay object này bằng object khác cùng interface**. Nếu một strategy hoặc class con hành xử khác contract, ví dụ ném exception mới, client sẽ lỗi. LSP chính là điều kiện để các pattern đó chạy đúng.

## 6. Bài tập

Code dưới đây vi phạm LSP ở đâu? Hãy sửa lại.

```python
class Bird:
    def fly(self) -> str:
        return "Đang bay"


class Penguin(Bird):
    def fly(self):
        raise NotImplementedError("Chim cánh cụt không bay được")


def migrate(birds: list[Bird]):
    for b in birds:
        print(b.fly())
```

<details>
<summary><b>Xem đáp án</b></summary>

`Penguin` phá contract "mọi `Bird` đều `fly()` được", nên `migrate()` sẽ crash. Cách sửa: chỉ đặt `fly()` vào những class thật sự bay được.

```python
class Bird:
    def eat(self) -> str:
        return "Đang ăn"


class FlyingBird(Bird):
    def fly(self) -> str:
        return "Đang bay"


class Sparrow(FlyingBird):
    pass


class Penguin(Bird):                    # không kế thừa FlyingBird
    def swim(self) -> str:
        return "Đang bơi"


def migrate(birds: list[FlyingBird]):   # chỉ nhận chim biết bay
    for b in birds:
        print(b.fly())


migrate([Sparrow()])                    # Đang bay
# migrate([Penguin()])  ← type checker báo lỗi ngay
```

</details>

---

[← O: Open/Closed](2-open-closed.md) · [Tổng quan SOLID](README.md) · [I: Interface Segregation →](4-interface-segregation.md)
