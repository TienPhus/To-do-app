# ✅ Do-It — To-do App

Ứng dụng quản lý công việc cá nhân với tính năng phân danh mục, theo dõi tiến độ và đăng nhập bằng tài khoản Google qua Firebase Authentication.

---

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Kiến trúc](#kiến-trúc)
- [Cài đặt môi trường](#cài-đặt-môi-trường)
- [Cấu hình Firebase](#cấu-hình-firebase)
- [Chạy Backend](#chạy-backend)
- [Chạy Frontend](#chạy-frontend)
- [Video Demo](#video-demo)

---

## Giới thiệu

**Do-It** là ứng dụng to-do app được xây dựng theo mô hình frontend–backend tách biệt. Backend xử lý logic và xác thực, frontend hiển thị giao diện và giao tiếp với backend qua REST API. Dữ liệu được lưu trên Firebase Firestore, người dùng đăng nhập bằng tài khoản Google.

---

## Tính năng

- Đăng nhập / Đăng xuất bằng Google (Firebase Authentication)
- Tạo, xem, xóa danh mục (category)
- Thêm, cập nhật trạng thái (Todo / Ongoing / Done), xóa task
- Mỗi task thuộc về một danh mục cụ thể
- Thanh tiến độ hiển thị % hoàn thành theo từng danh mục
- Dữ liệu lưu và đọc từ Firestore theo từng người dùng

---

## Kiến trúc

```
Do-It/
├── backend/
│   ├── main.py                  # FastAPI entry point
│   ├── routers/
│   │   ├── auth.py              # Xác thực Firebase token
│   │   ├── tasks.py             # CRUD tasks
│   │   └── categories.py        # CRUD categories
│   ├── schemas/
│   │   └── task.py              # Pydantic schemas
│   ├── services/
│   │   ├── firebase.py          # Khởi tạo Firebase Admin SDK
│   │   └── firestore.py         # Thao tác Firestore
│   └── .env.example
├── frontend/
│   └── index.html               # Giao diện HTML + Firebase JS SDK
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Cài đặt môi trường

**Yêu cầu:** Python 3.11+ (64-bit)

```bash
# Tạo virtual environment
python -m venv .venv

# Kích hoạt (Windows)
.venv\Scripts\activate

# Kích hoạt (Linux/Mac)
source .venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

---

## Cấu hình Firebase

### Lấy Service Account Key (cho Backend)

- Vào [Firebase Console](https://console.firebase.google.com) → Project Settings → Service Accounts
- Click **Generate new private key** → tải file JSON
- Đổi tên thành `serviceAccountKey.json` và đặt vào thư mục `backend/`

> ⚠️ File `serviceAccountKey.json` không commit lên GitHub (đã có trong `.gitignore`)

### Tạo Composite Index cho Firestore

Lần đầu chạy query sẽ xuất hiện lỗi kèm link tạo index trong terminal — click vào link đó và chọn **Save**.

---

## Chạy Backend

```bash
cd backend
uvicorn main:app --reload
```

Server chạy tại: `http://127.0.0.1:8000`

Swagger UI: `http://127.0.0.1:8000/docs`

### Các endpoint chính

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Kiểm tra server |
| GET | `/health` | Health check |
| POST | `/auth/verify` | Xác thực Firebase token |
| GET | `/auth/me` | Thông tin user hiện tại |
| GET | `/tasks/` | Lấy danh sách tasks |
| POST | `/tasks/` | Thêm task mới |
| PATCH | `/tasks/{id}` | Cập nhật trạng thái task |
| DELETE | `/tasks/{id}` | Xóa task |
| GET | `/categories/` | Lấy danh sách danh mục |
| POST | `/categories/` | Tạo danh mục mới |
| DELETE | `/categories/{id}` | Xóa danh mục và toàn bộ tasks |

---

## Chạy Frontend

```bash
cd frontend
python -m http.server 5500
```

Mở trình duyệt tại: `http://localhost:5500/index.html`

> **Lưu ý:** Cần chạy qua HTTP server (không mở file trực tiếp) để Firebase Google Login hoạt động đúng.

---

## Video Demo

> 🎬 [Link video demo](https://...)

Nội dung video:
- Giới thiệu ứng dụng
- Chạy backend và frontend
- Đăng nhập bằng Google (Firebase Authentication)
- Tạo danh mục và thêm tasks
- Cập nhật trạng thái task (Todo / Ongoing / Done)
- Xem tiến độ hoàn thành theo danh mục
- Minh họa dữ liệu lưu trên Firestore
