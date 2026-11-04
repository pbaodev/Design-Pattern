# O: Open/Closed Principle (OCP)

> **SOLID** · [← Tổng quan SOLID](README.md)

**Definition:** Code nên **mở để mở rộng** (thêm hành vi mới) nhưng **đóng để sửa đổi** (không phải sửa code cũ đã chạy ổn).

**Analogy:** Máy khoan thay được mũi: khoan gỗ hay bê tông chỉ cần lắp mũi khác, không phải tháo máy ra sửa.

---

## 1. Problem

```python
class ReportExporter:
    def export(self, rows: list[dict], fmt: str) -> str:
        if fmt == "csv":
            ...
        elif fmt == "json":
            ...
        elif fmt == "html":
            ...
        # Thêm "xlsx" → lại sửa hàm này
```

- Mỗi lần thêm định dạng là phải **sửa hàm đã chạy ổn**, và phải **test lại tất cả** định dạng cũ.
- Hàm ngày càng phình to, và hai người cùng thêm định dạng sẽ conflict ở cùng một chỗ.

## 2. Solution

1. Tạo **abstraction** `Exporter` với method `export(rows)`.
2. Mỗi định dạng là **một class riêng**.
3. Code dùng (`ReportService`) chỉ biết `Exporter`, nên thêm định dạng mới **chỉ cần thêm class mới** và đăng ký nó.

- **Đóng:** `ReportService` và các exporter cũ không bao giờ phải sửa.
- **Mở:** hành vi mở rộng được bằng cách thêm class mới.

## 3. Code

```python
import csv
import io
import json
from abc import ABC, abstractmethod


class Exporter(ABC):
    @abstractmethod
    def export(self, rows: list[dict]) -> str: ...


class CsvExporter(Exporter):
    def export(self, rows):
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        return buf.getvalue()


class JsonExporter(Exporter):
    def export(self, rows):
        return json.dumps(rows, ensure_ascii=False)


# ----- ĐÓNG: không bao giờ phải sửa khi thêm định dạng -----
class ReportService:
    def __init__(self, exporters: dict[str, Exporter]):
        self._exporters = exporters

    def export(self, rows: list[dict], fmt: str) -> str:
        return self._exporters[fmt].export(rows)


# ----- MỞ: thêm định dạng mới = thêm class mới -----
class MarkdownExporter(Exporter):
    def export(self, rows):
        header = "| " + " | ".join(rows[0]) + " |"
        divider = "|" + "---|" * len(rows[0])
        lines = ["| " + " | ".join(str(v) for v in r.values()) + " |" for r in rows]
        return "\n".join([header, divider, *lines])


rows = [{"sp": "Bàn phím", "sl": 2}, {"sp": "Chuột", "sl": 5}]
service = ReportService({
    "csv": CsvExporter(),
    "json": JsonExporter(),
    "md": MarkdownExporter(),          # chỉ thêm 1 dòng đăng ký
})
print(service.export(rows, "json"))    # [{"sp": "Bàn phím", "sl": 2}, {"sp": "Chuột", "sl": 5}]
print(service.export(rows, "md"))
# | sp | sl |
# |---|---|
# | Bàn phím | 2 |
# | Chuột | 5 |
```

## 4. Trade-offs

| ✅ Được | ❌ Mất |
|---|---|
| Thêm tính năng không phải sửa code đã test, giảm regression | Phải **đoán trước điểm mở rộng**: đoán sai thì có abstraction thừa |
| Mỗi biến thể nằm riêng, dễ test | Nhiều class hơn |
| Nhiều người làm song song mà không conflict | Không thể "đóng" với **mọi** kiểu thay đổi |

**In practice: Rule of Three.** Lần đầu viết trực tiếp, lần thứ hai ghi nhận, đến lần thứ ba phải thêm biến thể ở cùng một chỗ thì mới refactor theo OCP.

## 5. Code smells & related patterns

**Code smells:**
- Chuỗi `if/elif` hoặc `match` theo loại (`type`, `kind`, `fmt`), cứ thêm loại mới là phải sửa.
- Thêm một loại mới phải sửa nhiều file cùng lúc (*shotgun surgery*).

**Related patterns:** OCP là nguyên lý được nhiều pattern hiện thực nhất:
- [Strategy](../03-behavioral/strategy.md): ví dụ ở trên chính là Strategy kết hợp một registry.
- [Decorator](../02-structural/decorator.md): thêm hành vi mà không sửa class.
- [Factory Method](../01-creational/factory-method.md): thêm loại sản phẩm mà không sửa creator.
- [Observer](../03-behavioral/observer.md): thêm subscriber mà không sửa publisher.

## 6. Bài tập

Hãy thêm loại khách `"student"` được giảm 5% **mà không sửa hàm tính giảm giá**. Gợi ý: cần refactor hàm này một lần trước.

```python
def calculate_discount(customer_type: str, amount: int) -> int:
    if customer_type == "regular":
        return 0
    elif customer_type == "vip":
        return amount * 10 // 100
    elif customer_type == "employee":
        return amount * 30 // 100
```

<details>
<summary><b>Xem đáp án</b></summary>

Mỗi chính sách giảm giá là một **hàm** (bản Pythonic của Strategy), lưu trong một registry:

```python
from typing import Callable

DiscountPolicy = Callable[[int], int]

DISCOUNTS: dict[str, DiscountPolicy] = {
    "regular": lambda amount: 0,
    "vip": lambda amount: amount * 10 // 100,
    "employee": lambda amount: amount * 30 // 100,
}


def calculate_discount(customer_type: str, amount: int) -> int:
    return DISCOUNTS[customer_type](amount)       # hàm này không bao giờ phải sửa nữa


# Mở rộng: chỉ thêm 1 dòng
DISCOUNTS["student"] = lambda amount: amount * 5 // 100
print(calculate_discount("student", 200_000))    # 10000
```

Nếu chính sách cần state hoặc config, ví dụ "giảm 10% nhưng tối đa 50k", hãy dùng class `DiscountPolicy(ABC)` thay cho lambda.

</details>

---

[← S: Single Responsibility](1-single-responsibility.md) · [Tổng quan SOLID](README.md) · [L: Liskov Substitution →](3-liskov-substitution.md)
