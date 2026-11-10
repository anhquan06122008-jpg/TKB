# 📖 EduMate — Universal Student Planner & LMS 2.0
> **Your Study Companion** — Nền tảng quản lý thời khóa biểu và học tập thông minh, hiện đại, tối ưu cho sinh viên Đại học FPT và mọi trường đại học, cao đẳng, học sinh phổ thông.

![Version](https://img.shields.io/badge/version-3.0.0-blueviolet.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Web%20(Local--First)-orange.svg)
![Tests](https://img.shields.io/badge/tests-5%20passed-success.svg)

---

## 🌟 Giới thiệu tổng quan
**EduMate 2.0** là phiên bản nâng cấp toàn diện từ hệ thống Quản lý Thời khóa biểu ban đầu, mang phong cách giao diện hiện đại **Dark Slate Navy & Light Mode** tinh tế, tích hợp các công cụ học tập tiên tiến giúp sinh viên tối ưu hóa kế hoạch học tập cá nhân.

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
|  [⚙] Cài đặt                  |08:45-10|        |Lab 402 |        |      |      | |
|                               +--------+--------+--------+--------+------+------+ |
|  [🌙 Dark / Light Mode]                                                  (+) FAB  |
+-----------------------------------------------------------------------------------+
```

---

## ✨ Các tính năng nổi bật

### 1. 📅 Quản lý Thời khóa biểu Thông minh
- **Hệ thống tuần tương đối:** Chuyển đổi linh hoạt giữa `Tuần trước`, `Tuần hiện tại`, `Tuần sau`, tự động cập nhật mốc ngày theo thời gian thực (múi giờ Việt Nam `Asia/Ho_Chi_Minh`), không còn bị gò bó bởi số tuần cố định.
- **Đa chế độ xem:**
  - **Lưới tuần (Weekly Grid View):** Bố cục cột thứ và hàng tiết chuẩn mực. Cột ngày hôm nay được làm nổi bật với thẻ màu trắng chữ tím tương phản như phong cách thiết kế EduMate.
  - **Danh sách (Agenda View):** Hiển thị lịch trình dạng thẻ theo từng ngày, cực kỳ mượt mà và trực quan trên điện thoại di động.
  - **Hôm nay (Day View):** Tập trung vào lịch trình chi tiết của ngày hiện tại.

### 2. 📥 Nhập lịch từ FAP an toàn & Bộ phân tích thông minh
- Hỗ trợ sinh viên FPT lấy lịch học từ `https://fap.fpt.edu.vn/WeeklyTimetable` qua phương thức copy/paste trực tiếp hoặc tải file HTML.
- **Interactive Preview Table:** Bảng xem trước toàn bộ các buổi học kèm checkbox chọn lọc từng buổi và nhãn phát hiện trạng thái:
  - 🟢 `[Mới]`: Buổi học mới phát hiện.
  - 🟡 `[Đã có]`: Buổi học đã có trong lịch.
  - 🔴 `[Trùng giờ]`: Buổi học bị xung đột tiết với môn khác.
- **An toàn 100%:** Tuyệt đối không yêu cầu mật khẩu FAP, không can thiệp trái phép tài khoản người dùng.

### 3. 🌐 Universal Student Planner (Dành cho mọi sinh viên)
- Tùy chỉnh trường học: Đại học FPT, Bách Khoa, Quốc Gia, Kinh Tế, Ngoại Thương, Cao đẳng, Học sinh phổ thông, hoặc người học tự do.
- Tùy chỉnh tên học kỳ và khung giờ tiết học linh hoạt.

### 4. 🚀 Bộ công cụ hỗ trợ học tập thông minh
- **Smart Dashboard:** Thống kê tổng số môn học, số giờ học trong tuần, đếm ngược đến buổi học kế tiếp, danh sách bài tập cần nộp hôm nay.
- **Task & Assignment Manager:** Quản lý bài tập theo môn, đặt deadline, mức độ ưu tiên, đánh dấu hoàn thành kèm chuông báo âm thanh chúc mừng.
- **Exam Tracker:** Quản lý ngày thi, giờ thi, phòng thi, số báo danh và ghi chú mang máy tính/thẻ sinh viên.
- **Focus / Pomodoro Mode:** Đồng hồ đếm ngược 25 phút tập trung / 5 phút nghỉ ngắn, tích hợp chuông báo Web Audio API.
- **Đồng bộ Google Calendar & Apple Calendar (.ics):** Xuất toàn bộ lịch học ra tệp tin `.ics` để đồng bộ trực tiếp vào điện thoại.
- **Sao lưu & Phục hồi JSON:** Đảm bảo dữ liệu luôn an toàn, chuyển đổi dễ dàng giữa các thiết bị.

---

## 🚀 Hướng dẫn khởi chạy & Cài đặt

### Cách 1: Chạy trực tiếp (Không cần cài đặt)
Chỉ cần nhấp đúp chuột vào file `index.html` (hoặc `TKB (QLHT).html`) để mở ngay trên trình duyệt bất kỳ (Edge, Chrome, Brave, Firefox, Safari).

### Cách 2: Khởi chạy qua Local Web Server
```bash
# Sử dụng Python
python -m http.server 8000

# Hoặc dùng bất kỳ static server nào bạn thích
```
Sau đó truy cập: `http://localhost:8000`

---

## 🧪 Kiểm thử tự động (Automated Testing)
Dự án được xây dựng với các bộ kiểm thử tự động nghiêm ngặt bằng Python nằm trong thư mục `tests/`:

```bash
python -m unittest discover tests
```

- `test_engine.py`: Kiểm thử logic tính tuần tương đối, xử lý ranh giới năm, năm nhuận, và kiểm tra tính toàn vẹn khi nâng cấp schema v2 -> v3.
- `test_ics.py`: Kiểm thử cấu trúc tệp xuất lịch iCalendar RFC 5545.
- `test_html.py`: Kiểm thử cấu trúc HTML5, thẻ semantic và các container thành phần.

---

## 🔒 Bảo mật & Quyền riêng tư (Privacy-First)
- **Local-First:** Toàn bộ dữ liệu được lưu cục bộ trong `localStorage` của trình duyệt người dùng.
- **Zero Tracker / Zero Ad:** Không có script theo dõi người dùng, không gửi dữ liệu học tập cá nhân lên bất kỳ máy chủ bên thứ ba nào.
- **Không bao giờ yêu cầu hay lưu mật khẩu FAP.**

---

## 📄 Bản quyền & Tác giả
Phát triển và nâng cấp bởi AI Software Engineering Agent (Google Antigravity)  
Giữ trọn bản quyền cho người dùng.
