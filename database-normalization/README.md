# Database Normalization (chuẩn hóa cơ sở dữ liệu)

> [← Trang chính](../README.md) · SQL ví dụ: **PostgreSQL 16**

## Normalization là gì?

Normalization là quá trình tổ chức lại các bảng sao cho **mỗi sự thật (fact) chỉ được lưu ở đúng một nơi**. Mục tiêu là loại bỏ dữ liệu dư thừa, từ đó tránh được các lỗi khi thêm, sửa, xóa dữ liệu (*anomaly*).

## Vì sao cần chuẩn hóa: 3 loại anomaly

Xét bảng đơn hàng chưa được chuẩn hóa sau:

| order_id | customer_email | customer_name | product | price |
|---|---|---|---|---|
| 1 | an@example.com | An | Bàn phím | 800,000 |
| 2 | an@example.com | An | Chuột | 300,000 |
| 3 | binh@example.com | Bình | Màn hình | 3,000,000 |

| Anomaly | Hậu quả |
|---|---|
| **Update** (sửa) | An đổi tên phải sửa **2 dòng**; sót một dòng là dữ liệu mâu thuẫn (một email, hai tên) |
| **Insert** (thêm) | Không lưu được khách **chưa có đơn nào**, vì thiếu `order_id` |
| **Delete** (xóa) | Xóa đơn số 3 thì **mất luôn** thông tin khách Bình |

Cả 3 anomaly có chung nguyên nhân: **thông tin của khách hàng bị lưu lặp lại trong bảng đơn hàng**.

## Các dạng chuẩn

| Dạng | Definition | Câu hỏi tự kiểm tra | Loại bỏ |
|---|---|---|---|
| [**1NF**](1-1nf.md) | Mỗi ô chỉ chứa 1 giá trị, không có nhóm cột lặp lại | Có ô nào chứa danh sách, hoặc có các cột `phone1`, `phone2` không? | Giá trị đa trị |
| [**2NF**](2-2nf.md) | 1NF, và cột không phải key phải phụ thuộc vào **toàn bộ** key | Với key ghép: có cột nào chỉ phụ thuộc vào một phần của key không? | Partial dependency |
| [**3NF**](3-3nf.md) | 2NF, và cột không phải key **không phụ thuộc vào cột không phải key khác** | Có cột nào suy ra được từ một cột không phải key không? | Transitive dependency |
| [**BCNF**](4-bcnf.md) | Mọi determinant đều phải là super key | Có FD A → B nào mà A không phải super key không? | FD có determinant không phải key, còn sót sau 3NF |

Mỗi dạng chuẩn bao gồm luôn dạng chuẩn trước nó: đạt BCNF thì chắc chắn đã đạt 3NF, 2NF và 1NF.

> 💡 **Mnemonic** cho 1NF đến 3NF: mọi cột phải phụ thuộc vào *"the key (1NF), the whole key (2NF), and nothing but the key (3NF)"*.

## Bài học

| # | Bài | Nội dung |
|---|---|---|
| 0 | [Khái niệm nền tảng](0-khai-niem-nen-tang.md) | Key, functional dependency, cách tách bảng không mất dữ liệu. **Đọc bài này trước** |
| 1 | [1NF](1-1nf.md) | Số điện thoại nằm chung một ô |
| 2 | [2NF](2-2nf.md) | Bảng đăng ký môn học |
| 3 | [3NF](3-3nf.md) | Nhân viên và phòng ban |
| 4 | [BCNF](4-bcnf.md) | Sinh viên, môn học và giảng viên |
| 5 | [Bài tổng hợp](5-capstone.md) | Chuẩn hóa từng bước một bảng đơn hàng xuất từ Excel |

Bài 1 đến 4 theo cùng một khung: **Definition → Problem → Solution → SQL → Trade-offs**, sau đó là dấu hiệu vi phạm và bài tập (đáp án ẩn).

## Công thức chung để tách bảng

Mọi bài đều dùng chung một thao tác:

> Thấy một phụ thuộc **A → B vi phạm dạng chuẩn** thì tách (A, B) ra **bảng mới với A là primary key**. Bảng cũ bỏ B đi và giữ A làm **foreign key**.

## Checklist khi thiết kế một bảng

- [ ] Mỗi ô chỉ chứa 1 giá trị, không có cột đánh số kiểu `xxx1`, `xxx2` (1NF)
- [ ] Bảng có primary key, và các candidate key khác đã được khai báo `UNIQUE`
- [ ] Với composite key: mọi non-prime attribute phụ thuộc vào **toàn bộ** key (2NF)
- [ ] Không có cột mô tả một thực thể khác, ví dụ tên phòng ban trong bảng nhân viên (3NF)
- [ ] Mọi quy tắc nghiệp vụ dạng "mỗi X chỉ có 1 Y" đều có X là key của một bảng nào đó (BCNF)
- [ ] Mọi quan hệ giữa các bảng đều có `FOREIGN KEY`

## Chuẩn hóa tới đâu là đủ?

- Với hệ thống nghiệp vụ (OLTP: đặt hàng, ngân hàng, quản lý), **3NF là mục tiêu chuẩn**. Phần lớn bảng đạt 3NF cũng đã đạt BCNF.
- Hệ thống báo cáo và data warehouse thường **cố ý denormalize** để tăng tốc độ đọc. Đây là quyết định có chủ đích, không phải thiếu sót thiết kế.
