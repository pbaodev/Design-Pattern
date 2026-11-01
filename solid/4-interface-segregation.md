# I: Interface Segregation Principle (ISP)

> **SOLID** · [← Tổng quan SOLID](README.md)

**Một câu:** Không nên ép một class phải phụ thuộc vào (hay phải implement) **những method mà nó không dùng**. Nhiều interface nhỏ, đúng nhu cầu, tốt hơn một interface to ôm đồm mọi thứ.

**Ví dụ đời thường:** Một bản mô tả công việc "Nhân viên" bắt người nhận việc làm cả lập trình, lái xe, nấu ăn lẫn kế toán, dù họ chỉ biết một việc. Tách ra thành từng vị trí riêng thì hợp lý hơn.

---

## 1. Problem

```python
from abc import ABC, abstractmethod


class Machine(ABC):                        # interface "béo"
    @abstractmethod
    def print_doc(self, doc): ...

    @abstractmethod
    def scan_doc(self, doc): ...

    @abstractmethod
    def fax_doc(self, doc, number): ...


class OldPrinter(Machine):                 # máy in đời cũ, chỉ biết in
    def print_doc(self, doc):
        print(f"In {doc}")

    def scan_doc(self, doc):               # bị ép implement
        raise NotImplementedError

    def fax_doc(self, doc, number):        # bị ép implement
        raise NotImplementedError
```

- `OldPrinter` phải viết những method **vô nghĩa**, và vì chúng ném lỗi nên nó **vi phạm luôn cả LSP**.
- Đổi chữ ký của `fax_doc()` thì **mọi class** đều phải sửa theo, kể cả những class không hề fax.
- Hàm chỉ cần in cũng phải nhận cả interface `Machine` to đùng, và khi test thì phải mock đủ 3 method.

## 2. Solution

1. Tách `Machine` thành các interface nhỏ theo **khả năng**: `Printer`, `Scanner`, `Fax`.
2. Mỗi class chỉ implement **đúng những gì nó làm được**.
3. Client chỉ phụ thuộc vào **đúng khả năng nó cần**.

Trong Python, nên dùng `typing.Protocol` (*structural typing*): class không cần kế thừa, chỉ cần có đúng method là được tính là implement.

## 3. Code

```python
from typing import Protocol


# ----- Interface nhỏ: mỗi cái là 1 khả năng -----
class Printer(Protocol):
    def print_doc(self, doc: str) -> None: ...


class Scanner(Protocol):
    def scan_doc(self, doc: str) -> str: ...


class Fax(Protocol):
    def fax_doc(self, doc: str, number: str) -> None: ...


# ----- Implementation: chỉ cài đúng thứ mình hỗ trợ -----
class OldPrinter:                          # không cần kế thừa: Protocol kiểm tra theo "hình dạng"
    def print_doc(self, doc):
        print(f"🖨️  In: {doc}")


class OfficeMachine:                       # máy đa năng: có đủ cả 3 khả năng
    def print_doc(self, doc):
        print(f"🖨️  In: {doc}")

    def scan_doc(self, doc):
        print(f"📠 Scan: {doc}")
        return f"scan_{doc}.pdf"

    def fax_doc(self, doc, number):
        print(f"📞 Fax {doc} tới {number}")


# ----- Client: chỉ phụ thuộc vào đúng khả năng nó cần -----
def print_invoice(printer: Printer, invoice_id: int):
    printer.print_doc(f"Hóa đơn #{invoice_id}")


def archive(scanner: Scanner, doc: str) -> str:
    return scanner.scan_doc(doc)


print_invoice(OldPrinter(), 1)             # 🖨️  In: Hóa đơn #1
print_invoice(OfficeMachine(), 2)          # 🖨️  In: Hóa đơn #2
print(archive(OfficeMachine(), "hop-dong"))
# 📠 Scan: hop-dong
# scan_hop-dong.pdf

# archive(OldPrinter(), "x")   ← type checker báo lỗi: OldPrinter không có scan_doc
```

> Muốn dùng `ABC` thay cho `Protocol` cũng được: `class OfficeMachine(Printer, Scanner, Fax)`, tức là kế thừa nhiều interface nhỏ cùng lúc.

## 4. Trade-offs

| ✅ Được | ❌ Mất |
|---|---|
| Không còn method thừa, không còn `NotImplementedError` | Quá nhiều interface nhỏ thì phân mảnh, khó tìm |
| Đổi một interface chỉ ảnh hưởng tới nơi dùng nó | Phải cân nhắc nên gom method nào vào chung |
| Dễ mock khi test: interface nhỏ thì fake chỉ cần 1–2 method | |
| Khả năng của từng class hiện rõ ngay trong type | |

**Thực dụng:** nhóm method theo **nhu cầu của client**, tức là những method thường được dùng cùng nhau. Đừng máy móc tách mỗi method thành một interface.

## 5. Dấu hiệu vi phạm và liên hệ pattern

**Dấu hiệu:**
- Implementation có method chỉ `raise NotImplementedError` hoặc `pass`.
- Interface có hơn 10 method, và hầu hết client chỉ dùng 2–3 cái.
- Fake/mock trong test phải giả lập nhiều method không liên quan.

**Liên hệ pattern:**
- [Adapter](../02-structural/adapter.md) và [Facade](../02-structural/facade.md) đều đưa ra **đúng interface client cần**, giấu phần còn lại.
- Ví dụ ISP mẫu mực ngay trong Python: `collections.abc` gồm `Iterable`, `Sized`, `Container`, `Hashable`... Mỗi cái chỉ có 1 method, và một class có thể kết hợp nhiều cái.

## 6. Bài tập

Trang báo cáo chỉ cần **đọc** user, nhưng muốn test thì phải mock đủ 5 method. Một bản *read replica* (chỉ đọc) cũng bị ép implement `save` và `delete`. Hãy tách interface.

```python
class UserRepository(ABC):
    @abstractmethod
    def get(self, user_id: int) -> dict: ...
    @abstractmethod
    def list_all(self) -> list[dict]: ...
    @abstractmethod
    def save(self, user: dict) -> None: ...
    @abstractmethod
    def delete(self, user_id: int) -> None: ...
    @abstractmethod
    def export_csv(self) -> str: ...
```

<details>
<summary><b>Xem đáp án</b></summary>

- Tách thành `UserReader` (đọc) và `UserWriter` (ghi).
- `export_csv` không thuộc trách nhiệm của repository (vi phạm SRP), nên chuyển sang một class exporter riêng, nhận vào một `UserReader`.

```python
from typing import Protocol


class UserReader(Protocol):
    def get(self, user_id: int) -> dict: ...
    def list_all(self) -> list[dict]: ...


class UserWriter(Protocol):
    def save(self, user: dict) -> None: ...
    def delete(self, user_id: int) -> None: ...


class ReadReplica:                         # chỉ đọc → chỉ implement UserReader
    def __init__(self, users: list[dict]):
        self._users = {u["id"]: u for u in users}

    def get(self, user_id):
        return self._users[user_id]

    def list_all(self):
        return list(self._users.values())


def user_report(reader: UserReader) -> str:   # chỉ phụ thuộc vào việc đọc
    return f"Tổng số user: {len(reader.list_all())}"


print(user_report(ReadReplica([{"id": 1}, {"id": 2}])))   # Tổng số user: 2
```

Repository chính (database thật) implement cả `UserReader` lẫn `UserWriter`.

</details>

---

[← L: Liskov Substitution](3-liskov-substitution.md) · [Tổng quan SOLID](README.md) · [D: Dependency Inversion →](5-dependency-inversion.md)
