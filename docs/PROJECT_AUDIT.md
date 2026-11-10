# PROJECT AUDIT REPORT — LEARNING MANAGEMENT SYSTEM 2.0
**Dự án:** Quản lý Thời khóa biểu & Học tập (Learning Management System / Universal Student Planner)  
**Ngày thực hiện kiểm tra:** 09/11/2026  
**Thực hiện bởi:** AI Software Engineering Agent (Google Antigravity)  
**Mục tiêu:** Đánh giá toàn diện mã nguồn hiện tại, cấu trúc dữ liệu, các tính năng gốc, điểm mạnh, điểm yếu và rủi ro trước khi tiến hành nâng cấp.

---

## 1. Cấu trúc thư mục & Tổng quan tệp nguồn
- Thư mục làm việc: `C:\Users\anhqu\Downloads\TKB`
- Tệp nguồn ban đầu: `TKB (QLHT).html` (kích thước ~41.6 KB, 773 dòng code)
- Tệp sao lưu an toàn: `TKB (QLHT).original.bak.html` (được tạo trước khi chỉnh sửa)
- Định dạng kiến trúc: **Single-File Web Application (SPA / Local-first)** thuần Vanilla HTML5, CSS3 và Modern JavaScript (ES6+), lưu trữ dữ liệu hoàn toàn trên trình duyệt (`localStorage`).
- Phụ thuộc ngoài (External Dependencies):
  - `Tesseract.js` (v5.1.1 CDN jsDelivr) phục vụ tính năng nhận diện chữ qua ảnh (OCR). Chạy client-side hoàn toàn.

---

## 2. Công nghệ & Stack kỹ thuật
- **Frontend Core:** Pure HTML5 semantics (`<header>`, `<main>`, `<dialog>`, `<form>`, `<fieldset>`, `<table>`).
- **Styling:** CSS variables (`--bg`, `--fg`, `--mut`, `--line`, `--card`, `--acc`, `--bad`), hỗ trợ light/dark mode cơ bản qua `@media (prefers-color-scheme: dark)`.
- **State Management & Database:** Client-side `localStorage` với key chính `studyflow-tkb-v1`.
- **Date/Time Engine:** Chuỗi ISO (`YYYY-MM-DD`), UTC milliseconds, tự chuẩn hóa sang định dạng Việt Nam `DD/MM/YYYY`.
- **Khả năng chạy độc lập:** 100% offline-ready, không phụ thuộc backend server, có thể mở trực tiếp bằng trình duyệt (`file:///`) hoặc host tĩnh trên GitHub Pages/Vercel/Netlify.

---

## 3. Kiến trúc dữ liệu hiện tại (Schema v2)
Khóa lưu trữ `localStorage`: `studyflow-tkb-v1`
Cấu trúc JSON:
```json
{
  "v": 2,
  "subjects": [
    {
      "id": "string (uid)",
      "name": "string (Tên môn học)",
      "code": "string (Mã môn học, ví dụ AIF101)",
      "color": "string (Mã màu HEX)",
      "from": "string | null (YYYY-MM-DD)",
      "to": "string | null (YYYY-MM-DD)"
    }
  ],
  "rules": [
    {
      "id": "string (uid)",
      "sid": "string (Subject ID)",
      "wd": "number (1=Thứ 2 ... 7=Chủ nhật)",
      "slot": "number (1 đến 8)",
      "room": "string (Phòng học / Zoom)",
      "from": "string | null (YYYY-MM-DD)",
      "to": "string | null (YYYY-MM-DD)",
      "skip": ["YYYY-MM-DD"],
      "moved": {
        "YYYY-MM-DD": {
          "slot": "number",
          "room": "string",
          "name": "string",
          "code": "string"
        }
      },
      "src": "string (tùy chọn: 'fap' | 'imp')"
    }
  ]
}
```

### Các khung giờ học mặc định (Slots):
1. Tiết 1: 07:00 – 08:00 (hoặc 08:30)
2. Tiết 2: 08:45 – 10:15
3. Tiết 3: 10:30 – 12:00
4. Tiết 4: 12:30 – 14:00
5. Tiết 5: 14:15 – 15:45
6. Tiết 6: 16:00 – 17:30
7. Tiết 7: 17:45 – 19:15
8. Tiết 8: 19:30 – 21:00

---

## 4. Đánh giá tính năng hiện tại (Gốc)
1. **Lưới thời khóa biểu tuần:** Bảng hiển thị 7 cột thứ (Thứ 2 -> Chủ nhật) và 8 hàng tiết.
2. **Điều hướng tuần:**
   - Nút `Tuần trước`, `Tuần sau`, input `Đi tới ngày`.
   - **Hạn chế:** Nút "Về tuần 45" bị hardcode với `START = '2026-11-02'`, hiển thị tiêu đề `Tuần ${isoWeek}` chưa linh hoạt theo tuần thực tế hiện tại.
3. **Thêm lịch cố định:** Form thêm môn học, mã ngành, chọn nhiều thứ trong tuần, chọn tiết tương ứng cho từng thứ, ngày bắt đầu và kết thúc.
4. **Sửa & Xóa lịch theo phạm vi:**
   - Sửa/Xóa chỉ buổi này (`scope: 'one'`).
   - Sửa/Xóa buổi này và các buổi sau (`scope: 'after'`).
   - Sửa/Xóa tất cả các buổi cùng thứ cùng tiết của môn (`scope: 'all'`).
   - Kiểm tra xung đột tiết (Clashes check) trước khi lưu.
5. **Quản lý danh mục môn học:** Đổi tên, đổi mã, đổi mã màu trực tiếp, đếm số quy tắc, xóa môn học kèm xác nhận.
6. **Sao lưu & Phục hồi:** Xuất file JSON `studyflow-sao-luu-YYYY-MM-DD.json` và nhập file JSON kiểm tra hợp lệ.
7. **Nhập thời khóa biểu từ FAP (FPT Academic Portal):**
   - Hỗ trợ dán HTML (`Ctrl + V`) hoặc tải file `.html/.htm` lưu từ FAP `https://fap.fpt.edu.vn/WeeklyTimetable`.
   - Hỗ trợ nhận diện lịch qua ảnh chụp OCR (Tesseract.js).
   - Kiểm tra xung đột với lịch tự thêm trước khi áp dụng.

---

## 5. Những điểm hạn chế & Tồn đọng cần nâng cấp
1. **Giao diện & Trải nghiệm người dùng:**
   - Giao diện dạng bảng cơ bản, thiếu tính thẩm mỹ hiện đại, chưa có sidebar điều hướng trực quan.
   - Chưa phản ánh được thiết kế "EduMate" cao cấp như trong ảnh người dùng tham chiếu (theme dark navy hiện đại, card sự kiện bo tròn với icon sinh động, highlight ngày hiện tại rõ ràng).
   - Chưa tối ưu cho thiết bị di động (table tràn màn hình ngang).
2. **Cơ chế tuần & ngày:**
   - Nút "Về tuần 45" cố định, gây khó hiểu cho sinh viên các học kỳ khác hoặc trường khác.
   - Cần cơ chế tương đối: **[ ← TUẦN TRƯỚC ] [ TUẦN HIỆN TẠI ] [ TUẦN SAU → ]** kèm khoảng ngày cụ thể.
3. **Khả năng dùng chung cho mọi trường (Universal Student Planner):**
   - Tiêu đề và thuật ngữ ban đầu mang tính chất FPT (tiết slot FPT, FAP). Cần có quy trình Onboarding linh hoạt, hỗ trợ cả sinh viên FPT lẫn sinh viên các trường khác (Bách Khoa, Quốc Gia, Kinh Tế, Ngoại Thương, v.v.) và học sinh phổ thông.
4. **Nhập FAP thông minh:**
   - Thiếu modal Xem trước (Preview) chi tiết từng buổi học với checkbox chọn/bỏ chọn trước khi nhập.
   - Thiếu thông báo rõ ràng về các buổi bị trùng (Duplicate / Clash detection).
5. **Thiếu các công cụ quản lý học tập thông minh:**
   - Chưa có Dashboard tổng quan (hôm nay học gì, tiết tiếp theo khi nào).
   - Chưa có Quản lý bài tập & Nhiệm vụ (Task & Assignment Manager).
   - Chưa có Theo dõi lịch thi & Hạn chót (Exam & Deadline Tracker).
   - Chưa có Đồng hồ Pomodoro / Focus Mode.
   - Chưa có Thống kê số giờ học trong tuần.
   - Chưa có Xuất lịch ra Google Calendar / Apple Calendar (`.ics`).

---

## 6. Kết luận & Cam kết
- Toàn bộ dữ liệu trong `studyflow-tkb-v1` và các file sao lưu JSON cũ sẽ được **bảo toàn 100%**.
- Nâng cấp phiên bản 2.0 theo hướng Module hóa rõ ràng, hiệu năng cao, giao diện đẳng cấp, không phát sinh lỗi phá vỡ hệ thống cũ.
