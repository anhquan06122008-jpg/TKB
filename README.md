# 📖 EduMate — Universal Student Planner & LMS 2.0
> **Your Study Companion** — Nền tảng quản lý thời khóa biểu và học tập thông minh, hiện đại, tối ưu cho sinh viên Đại học FPT và mọi trường đại học, cao đẳng, học sinh phổ thông.

![Version](https://img.shields.io/badge/version-3.5.0-blueviolet.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Web%20%7C%20Cloud%20Sync-orange.svg)
![Tests](https://img.shields.io/badge/tests-11%20passed-success.svg)

---

## 🌟 Giới thiệu tổng quan
**EduMate 2.0** là phiên bản nâng cấp toàn diện từ hệ thống Quản lý Thời khóa biểu ban đầu, mang phong cách giao diện hiện đại **Dark Slate Navy & Light Mode** tinh tế, tích hợp hệ thống **Tài khoản cá nhân & Đồng bộ đa thiết bị (Laptop ⟷ Điện thoại)** cùng công cụ **Nhập lịch từ website cũ (HTML/JSON)** an toàn và tiện lợi.

```
+-----------------------------------------------------------------------------------+
|  📖 EduMate                  [‹ Tuần trước] [Tuần hiện tại] [Tuần sau ›]          |
|  Your Study Companion        TUẦN HIỆN TẠI · 09/11/2026 — 15/11/2026              |
|                                                                                   |
|  [🏠] Dashboard               Mon 09   Tue 10   Wed 11   Thu 12 [Fri 13]  Sat 14  |
|  [📅] Thời khóa biểu (Active) +--------+--------+--------+--------+------+------+ |
|  [📝] Bài tập & Deadline      |Slot 1  |Calculus|        |        |      |      | |
|  [🎯] Lịch thi                |07-08:30|BE-302  |        |        |      |      | |
|  [⏱] Focus (Pomodoro)        +--------+--------+--------+--------+------+------+ |
|  [📥] Nhập FAP                |Slot 2  |        |Physics |        |      |      | |
|  [📂] Nhập web cũ (HTML)      |08:45-10|        |Lab 402 |        |      |      | |
|  [⚙] Cài đặt                  +--------+--------+--------+--------+------+------+ |
|                                                                                   |
|  [👤 Anh Quân · 🟢 Đồng bộ]                                              (+) FAB  |
+-----------------------------------------------------------------------------------+
```

---

## ✨ Các tính năng nâng cấp mới nhất (v3.5.0)

### 1. 👤 Hệ thống Tài khoản & Đồng bộ Đa thiết bị (Laptop ⟷ Điện thoại)
- **Đăng ký & Đăng nhập an toàn:** Hỗ trợ đăng ký tài khoản với tên đăng nhập hoặc email, bảo vệ bằng mã hóa chuẩn công nghiệp **PBKDF2-HMAC-SHA256 (100,000 vòng băm + 16-byte salt ngẫu nhiên)**.
- **Đồng bộ hóa 2 chiều tự động (Cloud Sync):**
  - Nhập/chỉnh sửa thời khóa biểu trên laptop $\rightarrow$ Mở điện thoại đăng nhập cùng tài khoản $\rightarrow$ Toàn bộ lịch học, phòng học, bài tập xuất hiện tức thì.
  - Chỉnh sửa trên điện thoại $\rightarrow$ Laptop tải lại hoặc bấm đồng bộ sẽ nhận được dữ liệu mới nhất.
- **Cô lập dữ liệu tuyệt đối (Data Isolation):** Mỗi tài khoản có cơ sở dữ liệu riêng biệt. Người dùng A tuyệt đối không xem hoặc can thiệp được lịch của Người dùng B.
- **Hoạt động Ngoại tuyến (Offline-First):** Khi mất mạng hoặc chưa đăng nhập, web tự động lưu trong `localStorage`. Khi đăng nhập lại, web tự động đồng bộ lên Cloud.

### 2. 📂 Nhập toàn bộ lịch từ Website QLHT cũ (HTML / JSON)
- **Nhập file HTML hoặc kéo thả:** Chuyển toàn bộ lịch học từ file HTML đã lưu của website QLHT cũ sang EduMate 2.0 mà không phải gõ lại từng môn học.
- **Nhận diện đầy đủ thông tin:** Tự động trích xuất Tên môn, Mã môn (`AIF101`, `PRN211`...), Phòng học (`BE-302`, `AL-102`...), Tiết học (Slot 1–8), Giờ học, và Màu sắc.
- **Bản xem trước & Chọn lọc (Preview):** Hiển thị danh sách kiểm tra trước khi lưu, gắn nhãn `[Mới]` hoặc `[Đã có]`.
- **2 Chế độ nhập an toàn:**
  - ➕ **Thêm vào lịch hiện tại (Gộp - Merge):** Giữ nguyên lịch đang có, chỉ thêm các môn mới.
  - ⚠️ **Thay thế toàn bộ (Replace):** Tự động tạo bản sao lưu dự phòng trước khi thay thế. Có nút **↩ Khôi phục bản sao lưu trước (Rollback)** nếu bạn muốn quay lại!

### 3. 📅 Quản lý Thời khóa biểu Thông minh
- **Hệ thống tuần tương đối:** `[‹ Tuần trước]`, `[Tuần hiện tại]`, `[Tuần sau ›]`, tự động xác định ngày thực tế theo múi giờ `Asia/Ho_Chi_Minh`.
- **3 Chế độ xem linh hoạt:**
  - **Lưới tuần (Weekly Grid View):** Bố cục trực quan, cột ngày hôm nay nổi bật dạng thẻ trắng chữ tím tương phản.
  - **Danh sách (Agenda View):** Hiển thị dạng danh sách theo từng ngày, cực kỳ mượt mà trên điện thoại di động.
  - **Hôm nay (Day View):** Tập trung xem lịch trình chi tiết trong ngày.

### 4. 📥 Nhập lịch từ FAP an toàn (FPT Academic Portal)
- Nút Bookmarklet thần kỳ **`⭐ [Lấy Lịch FAP]`** và nút **`📋 ĐỌC TỰ ĐỘNG TỪ CLIPBOARD`**.
- Nhận diện thông minh mọi cơ sở FPT (Hòa Lạc, TP.HCM, Đà Nẵng, Cần Thơ, Quy Nhơn) dù tiết 1 bắt đầu lúc `07:00` hay `07:30`.
- Hỗ trợ nhập cả lịch tuần (`WeeklyTimetable`) lẫn toàn bộ lịch cả kỳ (`ViewAttendstudent`).

### 5. 🚀 Bộ công cụ học tập toàn diện
- **Smart Dashboard:** Thống kê giờ học, đếm ngược đến tiết học tiếp theo, danh sách bài tập hôm nay.
- **Task Manager:** Quản lý bài tập theo môn, đặt deadline, mức độ ưu tiên, hiệu ứng âm thanh hoàn thành (Web Audio API).
- **Exam Tracker:** Quản lý ngày thi, giờ thi, phòng thi, số báo danh.
- **Focus Pomodoro:** Đếm ngược 25 phút / 5 phút nghỉ kèm chuông báo.
- **Xuất file iCalendar (.ics):** Đồng bộ trực tiếp vào Google Calendar, Apple Calendar trên điện thoại.

---

## 🚀 Hướng dẫn khởi chạy Máy chủ & Web

### Cách 1: Khởi chạy 1-Click trên Windows (Nhanh nhất & Khuyên dùng)
- Chỉ cần **nhấp đúp chuột vào file `Chay_Server.bat`** trong thư mục `TKB`.
- Tệp lệnh sẽ tự động nhận diện Python trên máy tính, khởi động máy chủ đồng bộ Cloud tại cổng `8080`, và **tự động mở trình duyệt web** tại `http://localhost:8080`.
- Đồng thời cửa sổ console sẽ in sẵn địa chỉ IP để mở trên điện thoại (ví dụ: `http://192.168.1.15:8080`).

### Cách 2: Khởi chạy thủ công qua Terminal
EduMate đi kèm máy chủ backend siêu tốc viết bằng Python chuẩn (không cần cài đặt thêm bất kỳ thư viện ngoài nào):

```bash
# Khởi chạy server
python server.py 8080
# Hoặc nếu dùng MSYS2:
C:\msys64\ucrt64\bin\python.exe server.py 8080
```
- Mở trên laptop: Truy cập `http://localhost:8080`.
- Mở trên điện thoại (cùng mạng Wi-Fi): Truy cập `http://<địa-chỉ-IP-máy-tính>:8080` (ví dụ `http://192.168.1.15:8080`).
- Đăng ký 1 tài khoản $\rightarrow$ Lịch học tự động đồng bộ giữa cả 2 thiết bị!

### Cách 3: Chạy trực tiếp tệp tin (Local-First Offline)
Chỉ cần nhấp đúp chuột vào file `index.html` hoặc `TKB (QLHT).html` để mở ngay trên trình duyệt bất kỳ. Web vẫn hoạt động 100% bằng bộ nhớ cục bộ, hoặc bấm **[Dùng Hồ sơ Cục bộ (Offline)]** trong hộp thoại tài khoản mà không cần bật server.

---

## 🧪 Kiểm thử tự động (Automated Testing)
Dự án có bộ kiểm thử tự động 12 bài test nghiêm ngặt bao phủ backend, auth, bảo mật, import HTML, ping/health check và logic lịch:

```bash
python -m unittest discover tests
```

- `tests/test_backend.py`: Kiểm thử Đăng ký, Đăng nhập, Băm mật khẩu, Cô lập dữ liệu giữa nhiều người dùng, Push và Pull đồng bộ.
- `tests/test_html_import.py`: Kiểm thử trích xuất thời khóa biểu từ file HTML website QLHT cũ, chế độ gộp và thay thế.
- `tests/test_slots.py`: Kiểm thử nhận diện khung giờ học các cơ sở FPT.
- `tests/test_attend.py` & `tests/test_fap_full.py`: Kiểm thử bộ phân tích lịch tuần và lịch cả kỳ FAP.
- `tests/test_engine.py`: Kiểm thử logic tính tuần, xử lý năm nhuận, múi giờ và migration schema.
- `tests/test_html.py`: Kiểm thử tính hợp lệ cú pháp HTML5.

---

## 🔒 Bảo mật & An toàn dữ liệu
- **Không bao giờ lưu mật khẩu dạng thô:** Băm mật khẩu bằng PBKDF2-HMAC-SHA256 với 100,000 vòng lặp và salt ngẫu nhiên 16 bytes.
- **Token phiên an toàn:** Sử dụng token ngẫu nhiên 32 bytes của hệ thống bảo mật (`secrets.token_hex(32)`).
- **Không chứa Secrets trong Git:** File cơ sở dữ liệu `database.db` và các tệp môi trường được bảo vệ trong `.gitignore`.
- **Tự động sao lưu trước khi ghi đè:** Hỗ trợ rollback 1-click khi nhập file thay thế.

---

## 📄 Bản quyền
Được phát triển và hoàn thiện bởi AI Software Engineering Team (Google Antigravity).
