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

---

## 10. PHIÊN BẢN TINH CHỈNH v3.2.0 (REFINEMENT & PEN301 RECURRING SCHEDULER FIX)

Theo yêu cầu từ **Master Prompt: TKB Website Refinement — 100 AI Battle System**, toàn bộ các tinh chỉnh sau đã được hoàn tất và kiểm thử nghiêm ngặt:

### 1. Sửa triệt để lỗi thuật toán tạo TKB lặp tuần (Lỗi môn PEN301)
- **Nguyên nhân cốt lõi (Root Cause):**
  - Trong hàm `occOn(r, k)` ban đầu: `if ((sub.from && k < sub.from) || (sub.to && k > sub.to)) return null;`
  - Quá trình import trước đây đã ghi cố định mốc `from: "2026-11-09"` và `to: "2026-11-14"` trực tiếp vào đối tượng môn học `PEN301` trong cơ sở dữ liệu.
  - Khi người dùng vào form thêm lịch xếp PEN301 từ `02/11/2026` đến `17/12/2026` (7 tuần), quy tắc (`rule`) được lưu đúng khoảng ngày nhưng hàm hiển thị `occOn` lại bị giới hạn bởi `sub.from` và `sub.to` (chỉ 1 tuần duy nhất).
- **Giải pháp tối ưu đã triển khai:**
  - Cập nhật hàm `occOn(r, k)` để khoảng ngày tại quy tắc (`r.from`, `r.to`) luôn được ưu tiên tuyệt đối:
    ```js
    const fromDate = r.from || sub.from;
    const toDate = r.to || sub.to;
    if (fromDate && k < fromDate) return null;
    if (toDate && k > toDate) return null;
    ```
  - Cập nhật logic lưu môn (`handleSaveAddClass`) để tự động mở rộng biên `sub.from` và `sub.to` tương ứng với khoảng ngày của quy tắc mới, đồng thời dọn dẹp các quy tắc cũ xung đột của môn.
  - Chạy script dọn dẹp database SQLite loại bỏ triệt để kẹp ngày cứng cũ trên môn PEN301.
  - **Kết quả nghiệm thu:** Toàn bộ 34 buổi học của PEN301 từ `02/11/2026` đến `17/12/2026` (Thứ 2 đến Thứ 6 hàng tuần, Tiết 3) hiển thị chính xác 100%. Các ngày `25/11/2026` và `26/11/2026` đều có lịch đầy đủ. Ngày `18/12/2026` (vượt quá ngày kết thúc) và các ngày Thứ 7, Chủ nhật không có lịch.

### 2. Thiết lập Màn hình Đăng nhập Chặn Trước (Auth Gate Screen)
- Bổ sung màn hình `#authGateScreen` chiếm toàn trang, ngăn người dùng chưa đăng nhập tiếp cận giao diện thời khóa biểu.
- Người dùng có thể đăng nhập hoặc đăng ký tài khoản EduMate Cloud ngay tại màn hình này.
- Khi người dùng đăng nhập thành công, token được lưu vào `authToken` và `edumate_current_user` trong `localStorage`, màn hình Auth Gate tự động ẩn đi và vào thẳng thời khóa biểu.
- Mỗi lần mở web, hệ thống kiểm tra token hợp lệ: nếu đã có phiên, bỏ qua ngay màn hình đăng nhập. Khi bấm Đăng xuất, phiên bị hủy và màn hình Auth Gate xuất hiện trở lại ngay lập tức.
- Bổ sung nút "Dùng tạm Offline / Chế độ Khách" dành cho người dùng muốn sử dụng nhanh mà không cần tạo tài khoản.

### 3. Loại bỏ hoàn toàn các tính năng thừa theo yêu cầu người dùng
- Đã gỡ bỏ toàn bộ modal `#fapModal`, nút đọc clipboard tự động, nút kéo Bookmarklet, nút copy console script, nút mở trang FAP, và nút chọn file HTML/HTM từ FAP.
- Đã gỡ bỏ toàn bộ modal `#oldImportModal`, khung kéo thả dropzone, parser HTML web cũ, bảng preview và cơ chế rollback web cũ.
- Đã xóa sạch các nút liên quan trên Sidebar và Topbar (`btnSideFap`, `btnSideOldImport`, `openOldImportTopBtn`).
- Đã xóa hơn 1,000 dòng code JavaScript và regex không còn sử dụng trong `index.html`.

### 4. Tinh gọn Modal Nhập Môn học (`#addClassModal`)
- Thiết kế cuộn dọc linh hoạt (`max-height: 88vh; overflow-y: auto`), không bị tràn màn hình trên mọi kích thước.
- Đưa trường **"Áp dụng từ ngày"** và **"Đến ngày"** lên ngay đầu sau Mã môn & Tên môn.
- Cho phép chọn nhiều thứ trong tuần linh hoạt qua các checkbox trực quan.
- Tùy chọn bật/tắt **"Áp dụng cùng tiết cho mọi thứ đã chọn"** giúp thao tác nhanh chỉ trong 1 cú click.

### 5. Kết quả Kiểm thử Tự động (Automated Test Suite)
- Đã chạy bộ 12 ca kiểm thử tự động toàn diện qua `unittest`:
  - `tests/test_pen301_scheduler.py`: Kiểm thử độc lập thuật toán lịch tuần PEN301 (34 buổi, kiểm tra ngày 25/11, 26/11, biên tháng 11-12, biên năm 2026-2027, một ngày duy nhất).
  - `tests/test_backend.py`: Kiểm thử API đăng ký, đăng nhập, phân quyền, cô lập dữ liệu người dùng.
  - `tests/test_engine.py`: Kiểm thử logic tuần, năm nhuận, chuyển đổi ngày.
  - `tests/test_html.py`: Kiểm thử cấu trúc HTML5 nghiêm ngặt, đảm bảo không có thẻ lỗi và xác nhận đã xóa modal FAP/Old Import.
  - `tests/test_ics.py`: Kiểm thử xuất lịch iCalendar chuẩn RFC 5545.
  - `tests/test_slots.py`: Kiểm thử nhận diện 8 tiết học.
- **Trạng thái:** `12 passed in 0.626s — OK`.

---

## 11. PHIÊN BẢN HỢP NHẤT BỐ CỤC v3.7.0 (UNIFIED SAAS LAYOUT & PRECISION SCOPE ENGINE)

Theo yêu cầu từ **Master Prompt: Unified TKB Website Layout — 100 AI Battle**:

### 1. Hợp nhất Bố cục Toàn trang (Unified App Shell)
- **Nguyên nhân layout cũ bị rời rạc:**
  - Header trên cùng (`topbar`) tách biệt với phần dưới bởi khoảng đệm đen 24px của `.view-container`.
  - Khung thời khóa biểu bị bọc trong một "hòn đảo card" (`.schedule-card`) có viền, bóng và khoảng cách độc lập, tạo cảm giác hai trang web bị ghép thô thiển.
  - Tồn tại hai thanh cuộn dọc (scrollbar trên `body` và scrollbar trên `.main-wrapper`).
- **Kiến trúc bố cục mới:**
  ```text
  APP SHELL (#app, 100vw x 100vh)
  ├── SIDEBAR (.sidebar, 250px cố định bên trái, điều hướng đầy đủ, cuộn độc lập)
  └── MAIN CONTENT (.main-wrapper, chiếm trọn diện tích còn lại)
      ├── 1. PAGE HEADER (.app-header: Tiêu đề trang, Học kỳ, Tìm kiếm nhanh, User Pill, + Thêm lịch)
      ├── 2. TIMETABLE TOOLBAR (.timetable-toolbar: Tuần trước/hiện tại/sau, Chọn ngày, Lưới/DS/Hôm nay)
      └── 3. TIMETABLE GRID (#scheduleView: Gắn liền mạch trực tiếp ngay dưới toolbar, 0px padding)
          ├── Sticky Day Header (.schedule-header: Cột 🕒 + Thứ 2 -> CN, highlight Ngày hôm nay)
          └── Scrollable Grid Body (.schedule-body-scroll: 8 Tiết học cuộn mượt mà)
  ```
- **Trải nghiệm nhất quán:**
  - Không còn bất kỳ khoảng trống đen bất thường nào.
  - Thanh cuộn được quản lý gọn gàng bên trong vùng lưới thời khóa biểu, triệt tiêu hoàn toàn lỗi cuộn kép.
  - Trên màn hình nhỏ ($\le 768\text{px}$), sidebar tự chuyển thành menu trượt mượt mà (Off-canvas Drawer).

### 2. Sửa lỗi Nhập Môn học & Điều hướng Trực quan
- Tự động nhận diện linh hoạt: Cho phép người dùng nhập Mã ngành hoặc Tên môn học (tự động điền chéo nếu để trống một trong hai).
- Ngay sau khi bấm "Lưu", hệ thống tự động chuyển ngay góc nhìn thời khóa biểu đến tuần bắt đầu của môn học đó (`currentMonday = mondayKey(from)`), giải quyết dứt điểm thắc mắc "tôi nhập lịch lên không được" do giao diện đứng ở tuần khác.
- Hiển thị Toast thông báo trạng thái tức thì (`showToast`).

### 3. Bộ 3 Phạm vi Chỉnh sửa & Xóa Nhanh (Precision Scope Engine)
Modal sửa môn học (`#editClassModal`) nay áp dụng chuẩn xác cho cả **Lưu thay đổi** và **Xóa nhanh** theo 3 phạm vi:
1. **Chỉ ngày này (`one`)**:
   - *Sửa:* Di dời chỉ buổi học này sang tiết khác / phòng khác qua `r.moved[date]`.
   - *Xóa:* Thêm ngày này vào `r.skip`, các tuần trước và sau vẫn học bình thường. Nút bấm: `🗑️ Xóa chỉ ngày này`.
2. **Áp dụng cho ngày này và những ngày sau (`after`)**:
   - *Sửa:* Giữ nguyên lịch cũ trước ngày này, tự động chia tách rule và tạo rule mới từ ngày này trở về sau với tiết/phòng học mới.
   - *Xóa:* Giới hạn ngày kết thúc của rule đến trước ngày này (`r.to = addDays(date, -1)`). Nút bấm: `🗑️ Xóa từ ngày này về sau`.
3. **Áp dụng với thứ ... này vào những tuần sau / tất cả các tuần (`all`)**:
   - *Sửa:* Cập nhật toàn bộ các buổi học cùng thứ của môn sang tiết/phòng mới.
   - *Xóa:* Xóa toàn bộ các rule cùng thứ của môn học. Nút bấm: `🗑️ Xóa toàn bộ thứ này`.

### 4. Kết quả Kiểm thử Tự động Bộ Mới
- 16 bài kiểm thử tự động toàn diện đạt 100%:
  - `tests/test_edit_scope.py`: Kiểm thử chuyên sâu 3 phạm vi sửa và 3 phạm vi xóa (PASS).
  - `tests/test_pen301_scheduler.py`: Kiểm thử thuật toán PEN301 toàn diện (PASS).
  - `tests/test_html.py`: Kiểm thử tính hợp lệ HTML5 và kiến trúc header/toolbar mới (PASS).
  - `tests/test_backend.py`, `tests/test_engine.py`, `tests/test_ics.py`, `tests/test_slots.py`: Tất cả PASS.
- **Trạng thái:** `16 passed in 0.613s — OK`.





