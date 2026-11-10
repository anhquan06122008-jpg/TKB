# FEATURE INVENTORY & COMPATIBILITY MATRIX
**Dự án:** LMS 2.0 — Universal Student Planner (EduMate)  
**Ngày lập:** 09/11/2026

Bảng danh mục tính năng gốc, trạng thái bảo toàn và các tính năng mới được nâng cấp trong LMS 2.0:

---

## 1. Danh mục tính năng gốc (100% Giữ nguyên & Tương thích)

| STT | Mã tính năng | Tên tính năng gốc | Mô tả chi tiết | Tình trạng kế thừa trong LMS 2.0 |
|---|---|---|---|---|
| 1 | `LEG-01` | Lưới TKB tuần | Lưới hiển thị các ngày Thứ 2 đến Chủ nhật, 8 tiết | **Giữ nguyên 100%**, nâng cấp UI sang chảnh, hỗ trợ cả Grid View & Agenda View |
| 2 | `LEG-02` | Điều hướng tuần | Chuyển tuần qua nút bấm, chọn ngày nhảy | **Giữ nguyên**, thay "Về tuần 45" bằng "Tuần hiện tại / Hôm nay", thêm khoảng ngày cụ thể |
| 3 | `LEG-03` | Thêm lịch cố định | Thêm môn, mã ngành, chọn nhiều thứ, chọn tiết, phòng, khoảng ngày | **Giữ nguyên 100%**, thiết kế modal mới đẹp hơn, dễ thao tác hơn |
| 4 | `LEG-04` | Sửa buổi học | Sửa thông tin 1 buổi (`one`), buổi này và sau (`after`), tất cả buổi (`all`) | **Giữ nguyên 100%**, giữ trọn vẹn logic `r.moved` và `r.skip` |
| 5 | `LEG-05` | Xóa buổi học | Xóa 1 buổi (`skip.push`), xóa các buổi sau, hoặc xóa toàn bộ môn | **Giữ nguyên 100%**, có hộp thoại xác nhận an toàn |
| 6 | `LEG-06` | Kiểm tra xung đột (Clashes) | Ngăn ngừa trùng tiết cùng khung giờ | **Giữ nguyên 100%**, cảnh báo trực quan với danh sách buổi trùng |
| 7 | `LEG-07` | Quản lý môn học | Đổi tên môn, đổi mã môn, đổi màu sắc môn, xóa môn | **Giữ nguyên 100%**, bổ sung color palette phong phú và bộ icon |
| 8 | `LEG-08` | Xuất sao lưu JSON | Xuất toàn bộ dữ liệu ra file `.json` | **Giữ nguyên 100%**, định dạng tương thích hoàn toàn |
| 9 | `LEG-09` | Nhập sao lưu JSON | Nhập file `.json`, tự nâng cấp schema, phục hồi dữ liệu | **Giữ nguyên 100%**, hỗ trợ cả schema v1, v2 và v3 |
| 10 | `LEG-10` | Nhập FAP (Paste / File) | Đọc bảng HTML từ clipboard hoặc file `.html/.htm` FAP | **Giữ nguyên & nâng cấp vượt bậc**: thêm xem trước, checkbox, phát hiện trùng |
| 11 | `LEG-11` | Nhập từ ảnh OCR | Nhận diện lịch qua Tesseract.js trong trình duyệt | **Giữ nguyên 100%**, cải thiện khả năng lọc từ |
| 12 | `LEG-12` | LocalStorage Persistence | Lưu trữ trực tiếp trên trình duyệt máy khách | **Giữ nguyên 100%**, key `studyflow-tkb-v1` |

---

## 2. Danh mục tính năng nâng cấp mới (LMS 2.0 / Universal Student Planner)

| STT | Mã tính năng | Tên tính năng mới | Mô tả chi tiết & Lợi ích |
|---|---|---|---|
| 13 | `NEW-01` | **Hệ thống tuần tương đối** | `[ ← TUẦN TRƯỚC ] [ TUẦN HIỆN TẠI ] [ TUẦN SAU → ]`, kèm khoảng ngày tự động cập nhật theo múi giờ `Asia/Ho_Chi_Minh` |
| 14 | `NEW-02` | **FAP Import Wizard & Preview** | Bảng xem trước danh sách môn trích xuất từ FAP, phát hiện trùng, cho phép chọn/bỏ chọn từng buổi trước khi nhập |
| 15 | `NEW-03` | **Universal Onboarding** | Tùy chọn sinh viên FPT (tích hợp FAP) hoặc sinh viên Đại học / Cao đẳng / Phổ thông khác (nhập thủ công, mẫu lịch tiêu chuẩn) |
| 16 | `NEW-04` | **Smart Dashboard Overview** | Thống kê số môn đang học, tổng số giờ học tuần này, buổi học tiếp theo với đồng hồ đếm ngược, việc cần làm hôm nay |
| 17 | `NEW-05` | **Task & Assignment Manager** | Quản lý bài tập/deadline theo môn học, mức độ ưu tiên (High/Med/Low), trạng thái (Chưa làm, Đang làm, Hoàn thành) |
| 18 | `NEW-06` | **Exam & Deadline Tracker** | Quản lý lịch thi (môn thi, phòng thi, số báo danh, ngày giờ thi) kèm đếm ngược ngày thi |
| 19 | `NEW-07` | **Focus / Pomodoro Timer** | Bộ đếm giờ tập trung học tập 25 phút / 5 phút nghỉ, giúp sinh viên tập trung tối đa |
| 20 | `NEW-08` | **Smart Search & Filter** | Thanh tìm kiếm tức thời theo tên môn, mã ngành, phòng học, bài tập |
| 21 | `NEW-09` | **Personal Events Calendar** | Thêm lịch cá nhân, hoạt động ngoại khóa, lịch làm thêm không trùng với lịch học |
| 22 | `NEW-10` | **Export to iCalendar (.ics)** | Cho phép đồng bộ lịch học với Google Calendar, Apple Calendar, Outlook trên điện thoại |
| 23 | `NEW-11` | **Sleek EduMate UI (Dark/Light)** | Thiết kế Dark Navy đẳng cấp theo phong cách tham chiếu của người dùng, chuyển đổi Dark/Light mode mượt mà |
| 24 | `NEW-12` | **Mobile Responsive & Agenda View** | Giao diện tự co giãn trên điện thoại, hỗ trợ chế độ xem lịch dạng danh sách (Agenda) cực kỳ tiện dụng trên màn hình nhỏ |
| 25 | `NEW-13` | **In-app Smart Notifications** | Thông báo nhắc nhở trước giờ học 15 phút ngay trên trình duyệt |
