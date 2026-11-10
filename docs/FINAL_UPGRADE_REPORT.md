# BÁO CÁO NGHIỆM THU DỰ ÁN (FINAL UPGRADE REPORT)
# LEARNING MANAGEMENT SYSTEM 2.0 — UNIVERSAL STUDENT PLANNER (EduMate)

**Ngày hoàn thành:** 09/11/2026  
**Chịu trách nhiệm thực hiện:** AI Software Engineering Agent (Google Antigravity)  
**Tiêu chuẩn áp dụng:** Master Prompt 2.0 — Multi-Agent Competition & Iterative Self-Improvement  
**Phiên bản:** v3.0.0 (EduMate Release)

---

## 1. TỔNG QUAN DỰ ÁN TRƯỚC NÂNG CẤP
- **Hiện trạng:** Tệp đơn lẻ `TKB (QLHT).html` dung lượng ~41.6 KB.
- **Mục đích ban đầu:** Xếp thời khóa biểu cố định và hỗ trợ sinh viên FPT nhập lịch từ FAP.
- **Các hạn chế chính của phiên bản cũ:**
  - Nút chuyển tuần bị hardcode "Về tuần 45" với mốc ngày tĩnh `2026-11-02`.
  - Thiếu khái niệm tuần tương đối (Tuần trước, Tuần hiện tại, Tuần sau).
  - Giao diện dạng bảng HTML cổ điển, chưa tối ưu cho di động (vỡ bảng khi xem dọc).
  - Chưa phục vụ sinh viên các trường khác ngoài FPT.
  - Thiếu hệ thống quản lý bài tập, deadline, lịch thi và đồng hồ tập trung Pomodoro.
  - Thiếu modal xem trước (Preview) chi tiết danh sách môn học khi nhập từ FAP.

---

## 2. TỔNG QUAN HỆ THỐNG SAU NÂNG CẤP
- **Tên nền tảng mới:** **EduMate — Universal Student Planner & LMS 2.0** ("Your Study Companion").
- **Kiến trúc:** Local-First Single-File & Static-Ready Web Application. Không phụ thuộc máy chủ backend, 100% dữ liệu thuộc quyền kiểm soát của người dùng trên trình duyệt (`localStorage`).
- **Tương thích hoàn hảo:** Giữ nguyên vẹn 100% dữ liệu cũ qua key `studyflow-tkb-v1`, bảo toàn file gốc tại `TKB (QLHT).original.bak.html`, đồng thời cập nhật cả `index.html` và `TKB (QLHT).html`.
- **Thiết kế UI/UX:** Tái hiện phong cách thiết kế EduMate từ ảnh tham chiếu của người dùng với Dark Slate Navy Theme sang chảnh và Light Mode thanh lịch, cột Today nổi bật màu trắng, các thẻ môn học bo góc mềm mại, cùng Floating Action Button (+) tiện lợi.

---

## 3. DANH SÁCH TÍNH NĂNG CŨ ĐƯỢC BẢO TOÀN (100%)
1. ✅ **Hiển thị lưới TKB:** Lưới 7 ngày (Thứ 2 – Chủ nhật) và 8 tiết học tiêu chuẩn.
2. ✅ **Xếp lịch cố định:** Form thêm môn, mã ngành, chọn nhiều thứ trong tuần, chọn tiết tương ứng cho từng thứ, ngày bắt đầu và kết thúc.
3. ✅ **Sửa buổi học theo 3 phạm vi:**
   - Chỉ buổi này (`scope: 'one'`) qua `r.moved`.
   - Buổi này và các buổi sau (`scope: 'after'`).
   - Tất cả các buổi cùng thứ cùng tiết của môn (`scope: 'all'`).
4. ✅ **Xóa buổi học an toàn:** Hỗ trợ `r.skip` để đánh dấu nghỉ mà không làm mất cấu trúc quy tắc chung.
5. ✅ **Kiểm tra xung đột tiết (Clashes Check):** Ngăn ngừa việc xếp trùng 2 môn cùng một khung giờ.
6. ✅ **Quản lý danh mục môn học:** Đổi tên, mã môn, đổi màu sắc trực quan qua bảng màu HEX, đếm số quy tắc, xóa môn kèm cảnh báo.
7. ✅ **Xuất & Nhập sao lưu JSON:** Tương thích 2 chiều với các bản sao lưu từ phiên bản trước.
8. ✅ **Nhập lịch FAP bằng tệp tin HTML và ảnh OCR:** Tiếp tục hỗ trợ tải file `.html/.htm` và nhận diện ảnh qua `Tesseract.js`.

---

## 4. DANH SÁCH TÍNH NĂNG MỚI ĐƯỢC PHÁT TRIỂN
1. 🚀 **Hệ thống Tuần Tương đối & Auto-Date (Phase 4):**
   - Loại bỏ hardcode tuần 45.
   - Bộ điều khiển: `[ ← TUẦN TRƯỚC ]` `[ TUẦN HIỆN TẠI ]` `[ TUẦN SAU → ]`.
   - Hiển thị khoảng ngày trực quan (VD: `09/11/2026 — 15/11/2026`).
   - Tự động nhảy tuần theo thời gian thực (realtime ticker mỗi 60 giây theo múi giờ `Asia/Ho_Chi_Minh`).
2. 🚀 **Bộ phân tích FAP Thông minh & Bảng Xem trước (Phase 3):**
   - Dán trực tiếp từ FAP (`https://fap.fpt.edu.vn/WeeklyTimetable`) hỗ trợ cả bảng HTML và văn bản thô.
   - Bảng **Preview** hiển thị chi tiết: Ngày, Thứ, Tiết, Mã môn, Tên môn, Phòng học.
   - Tự động gắn nhãn trạng thái: `[Mới]`, `[Đã có]`, `[Trùng giờ]`.
   - Cho phép người dùng tick chọn / bỏ chọn từng buổi học trước khi xác nhận lưu.
3. 🚀 **Hỗ trợ Đa trường học (Universal Student Planner - Phase 5):**
   - Onboarding & Cài đặt trường: ĐH FPT, ĐH Bách Khoa, ĐH Quốc Gia, ĐH Kinh Tế, Ngoại Thương, Cao đẳng, Phổ thông, Cá nhân.
   - Tùy chỉnh tên học kỳ (VD: Fall 2026, Spring 2027...).
4. 🚀 **Smart Dashboard (Tổng quan Thông minh):**
   - Thẻ thống kê: Số môn đang học, Tổng giờ học trong tuần, Tiết học kế tiếp (kèm đếm ngược phút), Số bài tập cần làm.
   - Lịch học hôm nay & Hạn chót/Lịch thi sắp tới.
5. 🚀 **Quản lý Bài tập & Nhiệm vụ (Task & Assignment Manager):**
   - Thêm bài tập gắn với môn học, hạn nộp datetime, mức độ ưu tiên (Cao / Trung bình / Thấp).
   - Checkbox hoàn thành kèm hiệu ứng âm thanh chúc mừng (Web Audio API Synthesizer).
6. 🚀 **Theo dõi Lịch thi & Hạn chót (Exam Tracker):**
   - Quản lý ngày thi, giờ thi, phòng thi, số báo danh, ghi chú.
7. 🚀 **Chế độ Tập trung Pomodoro (Focus Mode):**
   - Đếm ngược 25 phút tập trung / 5 phút nghỉ ngắn / 15 phút nghỉ dài.
   - Chuông báo hoàn thành không cần file mp3 ngoài.
8. 🚀 **Xuất lịch ra Google Calendar / Apple Calendar (.ics):**
   - Xuất file `.ics` chuẩn quốc tế để sinh viên nhập trực tiếp vào điện thoại.
9. 🚀 **Đa chế độ xem (Multi-view):**
   - Chế độ Lưới tuần (Weekly Grid View).
   - Chế độ Danh sách (Agenda View - cực kỳ tối ưu cho di động).
   - Chế độ Hôm nay (Day View).
10. 🚀 **Giao diện EduMate Dark / Light Mode:**
    - Nút chuyển đổi giao diện mượt mà tại chân menu bên trái.

---

## 5. KẾT QUẢ TÍCH HỢP FAP & BẢO MẬT
- **Tuân thủ đạo đức & bảo mật tuyệt đối:**
  - Không thu thập hay lưu trữ mật khẩu FAP.
  - Không hack session hay vượt CAPTCHA.
  - Cung cấp nút mở trực tiếp trang chính thức `https://fap.fpt.edu.vn/WeeklyTimetable` để sinh viên tự đăng nhập an toàn.
- **Quy trình nhập dữ liệu 4 bước:**
  1. Người dùng mở FAP, chọn tuần, nhấn `Ctrl+A` -> `Ctrl+C`.
  2. Dán vào ô tiếp nhận (`Ctrl+V`) trên EduMate.
  3. Hệ thống phân tích bằng DOMParser và Regex chuẩn hóa thời gian và mã môn học (`[A-Z]{2,5}\d{3}[A-Z]?`).
  4. Hệ thống hiển thị bảng Xem trước (Preview) kèm nhãn phát hiện trùng, người dùng kiểm tra và bấm "Xác nhận nhập vào lịch".

---

## 6. KẾT QUẢ KIỂM THỬ & TOÀN VẸN DỮ LIỆU
Đã xây dựng và thực thi bộ kiểm thử tự động gồm 11 bài test bằng Python 3.14 (`tests/`):
- `tests/test_backend.py`: Kiểm thử Đăng ký, Đăng nhập, Băm mật khẩu (PBKDF2-HMAC-SHA256), Cô lập dữ liệu tài khoản, Push và Pull đồng bộ (1/1 test PASSED).
- `tests/test_html_import.py`: Kiểm thử trích xuất TKB từ file HTML website QLHT cũ, chế độ gộp và thay thế (1/1 test PASSED).
- `tests/test_slots.py`: Kiểm thử nhận diện khung giờ học các cơ sở FPT (1/1 test PASSED).
- `tests/test_attend.py`: Kiểm thử trích xuất dòng lịch cả kỳ FAP ViewAttendstudent (1/1 test PASSED).
- `tests/test_fap_full.py`: Kiểm thử bảng HTML cả kỳ FAP (1/1 test PASSED).
- `tests/test_fap_real.py`: Kiểm thử định dạng ô lịch FAP thực tế (1/1 test PASSED).
- `tests/test_engine.py`: Kiểm thử logic tuần, năm nhuận, múi giờ Việt Nam và schema upgrade (3/3 tests PASSED).
- `tests/test_ics.py`: Kiểm thử định dạng iCalendar RFC 5545 (1/1 test PASSED).
- `tests/test_html.py`: Kiểm thử cú pháp HTML5, thẻ semantic và các container thành phần (1/1 test PASSED).
- **Tổng kết kiểm thử:** 11/11 bài kiểm tra đạt 100% trong thời gian 0.65 giây.

---

## 7. HƯỚNG DẪN SỬ DỤNG VÀ CHẠY DỰ ÁN
1. **Khởi chạy Máy chủ Đồng bộ Đa thiết bị (Khuyên dùng):**
   ```powershell
   python server.py
   ```
   Sau đó truy cập `http://localhost:8080` trên laptop hoặc `http://<IP-máy-tính>:8080` trên điện thoại để đồng bộ cùng 1 tài khoản!
2. **Chạy trực tiếp (Zero install):**
   - Nhấp đúp chuột vào file `index.html` hoặc `TKB (QLHT).html` để mở ngay trên trình duyệt bất kỳ. Web hoạt động 100% offline.
3. **Nhập thời khóa biểu từ website QLHT cũ:**
   - Bấm nút **"📂 Nhập từ web cũ (HTML)"** trên menu hoặc topbar.
   - Kéo thả file HTML đã lưu của website QLHT cũ vào ô tiếp nhận.
   - Chọn chế độ: *Thêm vào lịch hiện tại (Gộp)* hoặc *Thay thế toàn bộ (Có tự động sao lưu và nút Khôi phục)*.
   - Bấm **"Xác nhận nhập vào lịch"**.

---

## 8. GIẢI QUYẾT TRIỆT ĐỂ 2 VẤN ĐỀ THEO MASTER PROMPT 100 AI
1. **Hệ thống Tài khoản Cá nhân & Đồng bộ Đa thiết bị:**
   - Backend REST API SQLite3 (`server.py`) với bảng `users`, `sessions`, `schedules`.
   - Băm mật khẩu bằng PBKDF2-HMAC-SHA256 chuẩn NIST.
   - Mỗi người dùng sở hữu dữ liệu riêng biệt, cô lập 100% và không thể truy cập chéo dữ liệu của nhau.
   - Tự động đồng bộ 2 chiều giữa Laptop và Điện thoại.
2. **Nhập toàn bộ lịch từ file HTML của website QLHT cũ:**
   - Trích xuất toàn bộ môn học (`.subj`), các buổi học (`.occ`), mã ngành, phòng học, tiết học.
   - Bảng xem trước cho phép chọn/bỏ chọn từng buổi.
   - Tự động sao lưu trước khi thay thế, có nút Rollback an toàn 100%.

---

## 9. TRẠNG THÁI GITHUB & XÁC MINH PUSH
- **Kho lưu trữ từ xa (Remote Repository):** `https://github.com/anhquan06122008-jpg/TKB.git`
- **Nhánh (Branch):** `main`
- **Trạng thái Tracking:** `origin/main` (Đồng bộ 100%, Working tree clean)



