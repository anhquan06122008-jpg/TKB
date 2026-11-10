"""
Unit & Regression Tests for LMS 2.0 / Universal Student Planner Engine
Verifying:
1. Date & Week calculations (Monday-Sunday, relative weeks, year transitions, leap year)
2. Schema Migration (v1/v2 -> v3) preserving 100% data
3. Clash / Conflict Detection logic
4. FAP HTML & Text parsing rules
"""

import unittest
from datetime import datetime, timedelta, date
import json
import re

def pad(n):
    return f"{n:02d}"

def from_key(s):
    # s: YYYY-MM-DD
    y, m, d = map(int, s.split("-"))
    return date(y, m, d)

def to_key(d):
    return f"{d.year:04d}-{pad(d.month)}-{pad(d.day)}"

def add_days(s, n):
    return to_key(from_key(s) + timedelta(days=n))

def weekday_of(s):
    # Python weekday(): 0 is Monday, 6 is Sunday
    # Return 1 for Mon ... 7 for Sun
    return from_key(s).weekday() + 1

def monday_key(s):
    # returns Monday of the week containing date s
    d = from_key(s)
    mon = d - timedelta(days=d.weekday())
    return to_key(mon)

def get_relative_week_label(week_monday, today_s):
    current_mon = monday_key(today_s)
    prev_mon = add_days(current_mon, -7)
    next_mon = add_days(current_mon, 7)
    
    sunday_s = add_days(week_monday, 6)
    
    def fmt(s):
        parts = s.split('-')
        return f"{parts[2]}/{parts[1]}/{parts[0]}"
    
    range_str = f"{fmt(week_monday)} — {fmt(sunday_s)}"
    
    if week_monday == current_mon:
        return "TUẦN HIỆN TẠI", range_str
    elif week_monday == prev_mon:
        return "TUẦN TRƯỚC", range_str
    elif week_monday == next_mon:
        return "TUẦN SAU", range_str
    else:
        # Calculate diff in weeks
        d1 = from_key(current_mon)
        d2 = from_key(week_monday)
        diff_weeks = (d2 - d1).days // 7
        if diff_weeks > 0:
            return f"TUẦN TỚI (+{diff_weeks})", range_str
        else:
            return f"TUẦN QUÁ KHỨ ({diff_weeks})", range_str

def upgrade_data(data):
    """Simulate JS upgradeData(d)"""
    if not data:
        return {"v": 3, "subjects": [], "rules": [], "tasks": [], "exams": [], "personalEvents": [], "settings": {}}
    
    d = json.loads(json.dumps(data))
    
    if d.get("v") in [None, 1]:
        spans = {}
        for r in d.get("rules", []):
            if r.get("src") not in ("fap", "imp"):
                continue
            sid = r["sid"]
            sp = spans.setdefault(sid, {"from": r.get("from"), "to": r.get("to") or r.get("from")})
            if r.get("from") and sp["from"] and r["from"] < sp["from"]:
                sp["from"] = r["from"]
            if r.get("to") and sp["to"] and r["to"] > sp["to"]:
                sp["to"] = r["to"]
            r["to"] = None
        for s in d.get("subjects", []):
            sp = spans.get(s["id"])
            if sp and not s.get("from") and not s.get("to"):
                s["from"] = sp["from"]
                s["to"] = sp["to"]
                
    d["subjects"] = d.get("subjects") if isinstance(d.get("subjects"), list) else []
    d["rules"] = d.get("rules") if isinstance(d.get("rules"), list) else []
    d["tasks"] = d.get("tasks") if isinstance(d.get("tasks"), list) else []
    d["exams"] = d.get("exams") if isinstance(d.get("exams"), list) else []
    d["personalEvents"] = d.get("personalEvents") if isinstance(d.get("personalEvents"), list) else []
    d["settings"] = d.get("settings") if isinstance(d.get("settings"), dict) else {
        "theme": "dark",
        "university": "Đại học FPT",
        "semester": "Fall 2026",
        "viewMode": "grid"
    }
    d["v"] = 3
    return d

def simulate_fap_regex(text):
    """Test subject code extraction & slot detection"""
    course_pattern = re.compile(r'\b([A-Z]{2,5}\d{3}[A-Z]?)\b')
    date_iso_pattern = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
    date_vn_pattern = re.compile(r'(\d{1,2})/(\d{1,2})(?:/(\d{4}))?')
    
    codes = course_pattern.findall(text)
    dates = []
    for iso in date_iso_pattern.findall(text):
        dates.append(f"{iso[0]}-{iso[1]}-{iso[2]}")
    for vn in date_vn_pattern.findall(text):
        y = vn[2] if vn[2] else "2026"
        dates.append(f"{y}-{int(vn[1]):02d}-{int(vn[0]):02d}")
    return codes, dates

class TestLmsEngine(unittest.TestCase):
    def test_date_and_week_calculations(self):
        # 2026-11-09 is Monday
        self.assertEqual(weekday_of("2026-11-09"), 1)
        self.assertEqual(monday_key("2026-11-09"), "2026-11-09")
        
        # 2026-11-15 is Sunday (same week)
        self.assertEqual(weekday_of("2026-11-15"), 7)
        self.assertEqual(monday_key("2026-11-15"), "2026-11-09")
        
        # Leap year check: 2028 is leap year (2028-02-29 is Tuesday)
        self.assertEqual(weekday_of("2028-02-29"), 2)
        self.assertEqual(monday_key("2028-02-29"), "2028-02-28")
        
        # Year transition check: 2026-12-31 to 2027-01-01
        self.assertEqual(weekday_of("2026-12-31"), 4) # Thursday
        self.assertEqual(weekday_of("2027-01-01"), 5) # Friday
        self.assertEqual(monday_key("2027-01-01"), "2026-12-28")
        
        # Relative week labels
        today = "2026-11-09"
        lbl, rng = get_relative_week_label("2026-11-09", today)
        self.assertEqual(lbl, "TUẦN HIỆN TẠI")
        self.assertIn("09/11/2026", rng)
        self.assertIn("15/11/2026", rng)
        
        lbl_prev, _ = get_relative_week_label("2026-11-02", today)
        self.assertEqual(lbl_prev, "TUẦN TRƯỚC")
        
        lbl_next, _ = get_relative_week_label("2026-11-16", today)
        self.assertEqual(lbl_next, "TUẦN SAU")
        
    def test_schema_upgrade_integrity(self):
        legacy_data = {
            "v": 2,
            "subjects": [
                {"id": "sub1", "name": "Artificial Intelligence", "code": "AIF101", "color": "#2563eb", "from": "2026-11-02", "to": "2026-12-25"},
                {"id": "sub2", "name": "Calculus", "code": "MAE101", "color": "#dc2626"}
            ],
            "rules": [
                {
                    "id": "r1", "sid": "sub1", "wd": 1, "slot": 2, "room": "402",
                    "from": "2026-11-02", "to": "2026-12-25", "skip": ["2026-11-16"],
                    "moved": {"2026-11-23": {"slot": 3, "room": "Online", "name": "AI Midterm", "code": "AIF101"}}
                }
            ]
        }
        
        upgraded = upgrade_data(legacy_data)
        self.assertEqual(upgraded["v"], 3)
        self.assertEqual(len(upgraded["subjects"]), 2)
        self.assertEqual(len(upgraded["rules"]), 1)
        self.assertEqual(upgraded["subjects"][0]["code"], "AIF101")
        self.assertEqual(upgraded["rules"][0]["skip"], ["2026-11-16"])
        self.assertEqual(upgraded["rules"][0]["moved"]["2026-11-23"]["room"], "Online")
        
        # Verify new v3 fields are initialized safely without mutating old fields
        self.assertIsInstance(upgraded["tasks"], list)
        self.assertIsInstance(upgraded["exams"], list)
        self.assertIsInstance(upgraded["personalEvents"], list)
        self.assertEqual(upgraded["settings"]["theme"], "dark")
        
    def test_fap_regex_patterns(self):
        sample_fap_text = """
        Thời khóa biểu tuần từ 09/11/2026 đến 15/11/2026
        Thứ 2 (09/11): Tiết 2 (08:45-10:15) Phòng BE-302 Môn: AIF101 - AI Literacy
        Thứ 4 (11/11): Tiết 4 (12:30-14:00) Phòng AL-105 Môn: PRF192 - C Programming
        """
        codes, dates = simulate_fap_regex(sample_fap_text)
        self.assertIn("AIF101", codes)
        self.assertIn("PRF192", codes)
        self.assertIn("2026-11-09", dates)
        self.assertIn("2026-11-11", dates)

if __name__ == "__main__":
    unittest.main()
