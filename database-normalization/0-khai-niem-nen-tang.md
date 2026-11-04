# 0. Khái niệm nền tảng

> **Normalization** · [← Tổng quan](README.md)

Mọi dạng chuẩn đều được định nghĩa dựa trên 2 khái niệm: **key** và **functional dependency**. Các bài sau đều dùng lại định nghĩa ở bài này.

---

## 1. Key (khóa)

Xét bảng `students`:

| student_id | email | citizen_id | name |
|---|---|---|---|
| 1 | an@uni.edu | 001099000001 | An |
| 2 | binh@uni.edu | 001099000002 | Bình |
| 3 | an2@uni.edu | 001099000003 | An |

| Loại key | Định nghĩa | Ví dụ |
|---|---|---|
| **Super key** | Tập cột xác định duy nhất một dòng, có thể chứa cột thừa | `(student_id)`, `(student_id, name)`, `(email, name)` |
| **Candidate key** | Super key **tối thiểu**: bỏ bất kỳ cột nào thì không còn duy nhất | `student_id`, `email`, `citizen_id` |
| **Primary key** | Candidate key được **chọn** làm định danh chính | `student_id` |
| **Alternate key** | Các candidate key còn lại, nên khai báo `UNIQUE` | `email`, `citizen_id` |
| **Composite key** | Key gồm nhiều cột | `(student_id, course_id)` trong bảng đăng ký môn |
| **Foreign key** | Cột tham chiếu tới key của bảng khác | `enrollments.student_id` → `students` |

`name` **không phải** key, vì có 2 sinh viên cùng tên An.

**Natural key và surrogate key:**
- **Natural key** có ý nghĩa nghiệp vụ, như email hay số CCCD, nhưng **có thể thay đổi** (người dùng đổi email).
- **Surrogate key** là id do hệ thống sinh ra (identity, UUID), không mang ý nghĩa gì nhưng **luôn ổn định**.
- Cách làm phổ biến: dùng surrogate key làm primary key, natural key khai báo `UNIQUE`.

```sql
CREATE TABLE students (
    student_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,  -- surrogate key
    email      VARCHAR(255) NOT NULL UNIQUE,                  -- candidate key → UNIQUE
    citizen_id CHAR(12)     NOT NULL UNIQUE,                  -- candidate key → UNIQUE
    name       VARCHAR(100) NOT NULL                          -- không phải key: được phép trùng
);
```

**Prime và non-prime attribute:**
- **Prime attribute** (thuộc tính khóa) là cột nằm trong **ít nhất một** candidate key: `student_id`, `email`, `citizen_id`.
- **Non-prime attribute** là các cột còn lại: `name`.

Định nghĩa 2NF và 3NF ở các bài sau dùng tới 2 khái niệm này.

## 2. Functional dependency (phụ thuộc hàm)

**A → B** (đọc là "A quyết định B") nghĩa là: hai dòng có cùng giá trị A thì **chắc chắn** có cùng giá trị B. A được gọi là *determinant*.

| Phụ thuộc | Đúng không? | Lý do |
|---|---|---|
| `student_id → name` | ✅ | Mỗi mã sinh viên ứng với đúng một tên |
| `email → name` | ✅ | Mỗi email thuộc về 1 sinh viên |
| `name → email` | ❌ | Có 2 bạn tên An với 2 email khác nhau |

> ⚠️ **Functional dependency đến từ quy tắc nghiệp vụ, không đến từ dữ liệu đang có.** Dữ liệu hiện tại có thể *tình cờ* thỏa một phụ thuộc. Ví dụ chưa có 2 sinh viên trùng tên, nhưng tên vẫn không quyết định được email. Để xác định FD, hỏi người nắm nghiệp vụ (*domain expert*): *"Có khi nào hai X giống nhau mà Y lại khác nhau không?"*

## 3. Hai loại dependency cần loại bỏ

| Kiểu | Định nghĩa | Ví dụ | Dạng chuẩn loại bỏ nó |
|---|---|---|---|
| **Partial dependency** | Cột chỉ phụ thuộc vào **một phần** của key ghép | Key `(student_id, course_id)`, nhưng `course_id → course_name` | [2NF](2-2nf.md) |
| **Transitive dependency** | Cột phụ thuộc vào key **gián tiếp**, thông qua một cột không phải key | `employee_id → department_id → department_name` | [3NF](3-3nf.md) |

## 4. Tách bảng không mất dữ liệu (lossless decomposition)

Chuẩn hóa nghĩa là **tách** một bảng thành nhiều bảng. Sau khi tách, phải `JOIN` lại được **chính xác** dữ liệu ban đầu: không thiếu dòng nào và không sinh dòng thừa (*spurious tuple*).

**Quy tắc:** cột chung giữa hai bảng phải là **key của ít nhất một bảng**.

Ví dụ tách **sai**: tách `enrollments(student_id, course_id, grade)` thành `(student_id, grade)` và `(course_id, grade)`. Cột chung `grade` không phải key của bảng nào, nên khi `JOIN` theo `grade`, mọi sinh viên có điểm 8.5 sẽ bị ghép với mọi môn có điểm 8.5, sinh ra dòng sai.

Ví dụ tách **đúng**: tách theo functional dependency như [công thức chung](README.md#công-thức-chung-để-tách-bảng). Cột chung luôn là primary key của bảng mới.

---

## Bài tập

Cho bảng đăng ký môn học (mỗi sinh viên học mỗi môn 1 lần):

| student_id | course_id | student_name | course_name | grade |
|---|---|---|---|---|
| SV01 | CS101 | An | Cấu trúc dữ liệu | 8.5 |
| SV01 | CS102 | An | Cơ sở dữ liệu | 7.0 |
| SV02 | CS101 | Bình | Cấu trúc dữ liệu | 9.0 |

1. Liệt kê các functional dependency.
2. Candidate key là gì? Đâu là prime attribute, đâu là non-prime attribute?
3. Có partial dependency nào không?

<details>
<summary><b>Xem đáp án</b></summary>

1. **Functional dependency:**
   - `student_id → student_name`
   - `course_id → course_name`
   - `(student_id, course_id) → grade`
2. **Candidate key:** `(student_id, course_id)`, và đây cũng là key duy nhất.
   - Prime attribute: `student_id`, `course_id`.
   - Non-prime attribute: `student_name`, `course_name`, `grade`.
3. **Có 2 partial dependency:**
   - `student_name` chỉ phụ thuộc vào `student_id`.
   - `course_name` chỉ phụ thuộc vào `course_id`.

   Chỉ có `grade` là phụ thuộc vào toàn bộ key. Bảng này **vi phạm 2NF**, và [bài 2NF](2-2nf.md) sẽ sửa nó.

</details>

---

[← Tổng quan](README.md) · [1NF →](1-1nf.md)
