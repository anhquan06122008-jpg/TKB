# DATA INTEGRITY SPECIFICATION & MIGRATION PROTOCOL
**Dự án:** LMS 2.0 — Universal Student Planner (EduMate)  
**Ngày lập:** 09/11/2026

---

## 1. Nguyên tắc tối cao về bảo tồn dữ liệu
1. **Không làm mất lịch cũ:** Bất kỳ người dùng nào đang có dữ liệu trong `localStorage['studyflow-tkb-v1']` khi mở website phiên bản 2.0 phải nhìn thấy toàn bộ thời khóa biểu của mình hiển thị trọn vẹn, chính xác từng ngày, từng tiết và từng phòng học.
2. **Không ghi đè tự ý:** Việc nhập dữ liệu mới (thêm thủ công hoặc từ FAP) luôn được kiểm tra xung đột trước khi ghi vào lưu trữ.
3. **Tương thích 2 chiều:** File sao lưu JSON tạo từ phiên bản cũ (v1, v2) có thể nhập mượt mà vào phiên bản mới (v3). Đồng thời tính năng xuất file vẫn đảm bảo cấu trúc JSON mà phiên bản cũ có thể đọc được.
4. **Cơ chế sao lưu an toàn khi có lỗi:** Nếu phát hiện dữ liệu bị lỗi cú pháp JSON do bên ngoài, tự động sao lưu dữ liệu thô sang khóa `studyflow-tkb-v1-loi` và thông báo cho người dùng, không bao giờ xóa dữ liệu.

---

## 2. Đặc tả Schema Migration (v2 -> v3)

### Schema v2 (Hiện tại):
```typescript
interface ScheduleDataV2 {
  v: 2;
  subjects: Array<{
    id: string;
    name: string;
    code: string;
    color: string;
    from?: string | null;
    to?: string | null;
  }>;
  rules: Array<{
    id: string;
    sid: string;
    wd: number; // 1 (Mon) -> 7 (Sun)
    slot: number; // 1 -> 8
    room: string;
    from: string | null;
    to: string | null;
    skip: string[]; // YYYY-MM-DD
    moved: Record<string, {
      slot?: number;
      room?: string;
      name?: string;
      code?: string;
    }>;
    src?: 'fap' | 'imp' | string;
  }>;
}
```

### Schema v3 (Nâng cấp mở rộng):
```typescript
interface ScheduleDataV3 extends ScheduleDataV2 {
  v: 3;
  // Giữ nguyên 100% subjects và rules của v2!
  
  // Bổ sung các mảng quản lý thông minh (tùy chọn, mặc định rỗng []):
  tasks?: Array<{
    id: string;
    title: string;
    sid?: string; // liên kết với môn học
    deadline?: string; // YYYY-MM-DDTHH:mm
    priority: 'high' | 'medium' | 'low';
    completed: boolean;
    createdAt: string;
  }>;
  
  exams?: Array<{
    id: string;
    sid: string;
    subjectName?: string;
    date: string; // YYYY-MM-DD
    time: string; // HH:mm
    room: string;
    seat?: string;
    notes?: string;
  }>;
  
  personalEvents?: Array<{
    id: string;
    title: string;
    date: string; // YYYY-MM-DD
    timeStart: string; // HH:mm
    timeEnd: string; // HH:mm
    color?: string;
    notes?: string;
  }>;
  
  settings?: {
    theme?: 'dark' | 'light' | 'system';
    university?: string;
    semester?: string;
    viewMode?: 'grid' | 'agenda' | 'day';
    notificationsEnabled?: boolean;
    slotCustomTimes?: Array<[string, string]>;
  };
}
```

---

## 3. Hàm Upgrade an toàn
```javascript
function upgradeData(d) {
  if (!d) return { v: 3, subjects: [], rules: [], tasks: [], exams: [], personalEvents: [], settings: {} };
  
  // Nếu là v1: xử lý quy tắc khoảng ngày môn học
  if (d.v === undefined || d.v === 1) {
    const spans = {};
    (d.rules || []).forEach(r => {
      if (r.src !== 'fap' && r.src !== 'imp') return;
      const sp = spans[r.sid] || (spans[r.sid] = { from: r.from, to: r.to || r.from });
      if (r.from < sp.from) sp.from = r.from;
      if (r.to && r.to > sp.to) sp.to = r.to;
      r.to = null;
    });
    (d.subjects || []).forEach(s => {
      const sp = spans[s.id];
      if (sp && !s.from && !s.to) { s.from = sp.from; s.to = sp.to; }
    });
  }
  
  // Nâng cấp lên v3: giữ nguyên toàn bộ subjects và rules
  d.subjects = Array.isArray(d.subjects) ? d.subjects : [];
  d.rules = Array.isArray(d.rules) ? d.rules : [];
  d.tasks = Array.isArray(d.tasks) ? d.tasks : [];
  d.exams = Array.isArray(d.exams) ? d.exams : [];
  d.personalEvents = Array.isArray(d.personalEvents) ? d.personalEvents : [];
  d.settings = typeof d.settings === 'object' && d.settings !== null ? d.settings : {
    theme: 'dark',
    university: 'Đại học FPT',
    semester: 'Fall 2026',
    viewMode: 'grid'
  };
  d.v = 3;
  return d;
}
```

---

## 4. Kế hoạch kiểm thử tính toàn vẹn (Data Integrity Verification)
1. Tạo bộ dữ liệu mẫu v2 chuẩn gồm 5 môn học, 12 quy tắc, 3 buổi bị hoán đổi (`moved`), 2 buổi bị hủy (`skip`).
2. Chạy hàm `upgradeData` và kiểm tra 100% các môn học, quy tắc, buổi học giữ nguyên giá trị.
3. Xuất file và nhập lại file sao lưu để chứng minh tính đối xứng (Idempotence: `import(export(data)) === data`).
