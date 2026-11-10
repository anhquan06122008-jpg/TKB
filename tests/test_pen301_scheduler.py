"""
Comprehensive Test Suite for PEN301 & Universal Recurring Timetable Engine
Verifies:
1. Exact PEN301 scenario (02/11/2026 - 17/12/2026, Mon-Fri, Slot 3)
2. Occurrences present on ALL valid weekdays across all 7 weeks (specifically 25/11/2026 and 26/11/2026)
3. Zero occurrences on 18/12/2026 (beyond end date) and weekends (Saturday/Sunday)
4. Cross-month (Nov-Dec 2026) and Cross-year (Dec 2026 - Jan 2027) continuity
5. Single-day schedule rules
6. Rule-level date bounds taking precedence over stale subject bounds (the root cause of the PEN301 bug)
"""

import unittest
from datetime import date, timedelta

def to_key(d):
    return f"{d.year:04d}-{d.month:02d}-{d.day:02d}"

def from_key(s):
    y, m, d = map(int, s.split("-"))
    return date(y, m, d)

def add_days(s, n):
    return to_key(from_key(s) + timedelta(days=n))

def weekday_of(s):
    # Returns 1 for Monday ... 7 for Sunday (matching EduMate frontend)
    return from_key(s).weekday() + 1

def occ_on(rule, subject, k):
    """
    Python mirror of occOn(r, k) in index.html:
    Determines whether a rule produces an occurrence on date key k ('YYYY-MM-DD').
    """
    if not subject:
        return None
    
    # 1. Date bounding: Rule bounds take precedence; fallback to subject bounds
    from_date = rule.get("from") or subject.get("from")
    to_date = rule.get("to") or subject.get("to")
    
    if from_date and k < from_date:
        return None
    if to_date and k > to_date:
        return None
        
    # 2. Skip dates
    skip_list = rule.get("skip", [])
    if k in skip_list:
        return None
        
    # 3. Moved date exception
    moved_map = rule.get("moved", {})
    if k in moved_map:
        mv = moved_map[k]
        return {
            "sub": subject,
            "rule": rule,
            "slot": mv.get("slot", rule.get("slot")),
            "room": mv.get("room", rule.get("room", "")),
            "date": k,
            "isMoved": True,
            "note": mv.get("name") or mv.get("note") or ""
        }
        
    # 4. Weekday matching
    wd = weekday_of(k)
    if rule.get("wd") == wd:
        return {
            "sub": subject,
            "rule": rule,
            "slot": rule.get("slot"),
            "room": rule.get("room", ""),
            "date": k,
            "isMoved": False,
            "note": rule.get("note", "")
        }
        
    return None

def get_occurrences_for_range(rules, subjects_by_id, start_date, end_date):
    """Generates all timetable occurrences for each day in [start_date, end_date]."""
    cur = from_key(start_date)
    end = from_key(end_date)
    results = {}
    
    while cur <= end:
        k = to_key(cur)
        results[k] = []
        for r in rules:
            sub = subjects_by_id.get(r.get("sid"))
            occ = occ_on(r, sub, k)
            if occ:
                results[k].append(occ)
        cur += timedelta(days=1)
        
    return results

class TestPen301Scheduler(unittest.TestCase):
    def setUp(self):
        # Setup PEN301 Subject and Rules matching the user's input:
        # Subject: PEN301 - Tiếng Anh
        # Range: 2026-11-02 to 2026-12-17
        # Weekdays: Mon(1), Tue(2), Wed(3), Thu(4), Fri(5)
        # Slot: 3 (10:30-12:00)
        # Room: 327
        self.subject_pen301 = {
            "id": "sub_pen301",
            "name": "Tiếng Anh",
            "code": "PEN301",
            "color": "#3b82f6",
            "from": "2026-11-02",
            "to": "2026-12-17"
        }
        
        self.rules_pen301 = [
            {"id": "r_mon", "sid": "sub_pen301", "wd": 1, "slot": 3, "room": "327", "from": "2026-11-02", "to": "2026-12-17"},
            {"id": "r_tue", "sid": "sub_pen301", "wd": 2, "slot": 3, "room": "327", "from": "2026-11-02", "to": "2026-12-17"},
            {"id": "r_wed", "sid": "sub_pen301", "wd": 3, "slot": 3, "room": "327", "from": "2026-11-02", "to": "2026-12-17"},
            {"id": "r_thu", "sid": "sub_pen301", "wd": 4, "slot": 3, "room": "327", "from": "2026-11-02", "to": "2026-12-17"},
            {"id": "r_fri", "sid": "sub_pen301", "wd": 5, "slot": 3, "room": "327", "from": "2026-11-02", "to": "2026-12-17"},
        ]
        
        self.subjects = {"sub_pen301": self.subject_pen301}

    def test_full_range_pen301_coverage(self):
        """Verify PEN301 classes appear on ALL weekdays from 02/11/2026 to 17/12/2026."""
        occs = get_occurrences_for_range(self.rules_pen301, self.subjects, "2026-11-01", "2026-12-20")
        
        # 1. Check start boundary: 2026-11-01 (Sunday before range) -> 0
        self.assertEqual(len(occs["2026-11-01"]), 0, "Sunday 2026-11-01 must have 0 classes")
        
        # 2. Check first day: 2026-11-02 (Monday) -> 1 class
        self.assertEqual(len(occs["2026-11-02"]), 1)
        self.assertEqual(occs["2026-11-02"][0]["slot"], 3)
        self.assertEqual(occs["2026-11-02"][0]["room"], "327")
        self.assertEqual(occs["2026-11-02"][0]["sub"]["code"], "PEN301")
        
        # 3. Check specific dates requested by user: 25/11/2026 (Wed) & 26/11/2026 (Thu)
        self.assertEqual(len(occs["2026-11-25"]), 1, "2026-11-25 (Wed) MUST have class")
        self.assertEqual(occs["2026-11-25"][0]["slot"], 3)
        self.assertEqual(len(occs["2026-11-26"]), 1, "2026-11-26 (Thu) MUST have class")
        self.assertEqual(occs["2026-11-26"][0]["slot"], 3)
        
        # 4. Check month boundary: 2026-11-30 (Mon) and 2026-12-01 (Tue)
        self.assertEqual(len(occs["2026-11-30"]), 1)
        self.assertEqual(len(occs["2026-12-01"]), 1)
        
        # 5. Check last day: 2026-12-17 (Thursday) -> 1 class
        self.assertEqual(len(occs["2026-12-17"]), 1, "2026-12-17 (Thu) is the last day and MUST have class")
        
        # 6. Check end boundary: 2026-12-18 (Friday, out of range) -> 0 classes
        self.assertEqual(len(occs["2026-12-18"]), 0, "2026-12-18 is beyond end date and MUST have 0 classes")
        self.assertEqual(len(occs["2026-12-19"]), 0)
        self.assertEqual(len(occs["2026-12-20"]), 0)

    def test_total_count_of_pen301_sessions(self):
        """Count total sessions: 7 weeks minus Friday in week 7 = 5 + 5 + 5 + 5 + 5 + 5 + 4 = 34 sessions."""
        occs = get_occurrences_for_range(self.rules_pen301, self.subjects, "2026-11-02", "2026-12-17")
        total_sessions = sum(len(session_list) for session_list in occs.values())
        self.assertEqual(total_sessions, 34, "Expected exactly 34 sessions of PEN301")

    def test_stale_subject_bounds_regression(self):
        """
        Verify the root cause fix:
        If subject has stale narrow bounds (e.g. from='2026-11-09', to='2026-11-14') from previous imports,
        rule.from and rule.to must take precedence, ensuring classes still render on 25/11 and 02/11!
        """
        stale_subject = {
            "id": "sub_stale",
            "name": "Tiếng Anh",
            "code": "PEN301",
            "color": "#3b82f6",
            "from": "2026-11-09", # Stale 1-week clamp
            "to": "2026-11-14"
        }
        
        rule_wed = {
            "id": "r_stale_wed",
            "sid": "sub_stale",
            "wd": 3, # Wednesday
            "slot": 3,
            "room": "327",
            "from": "2026-11-02", # Expanded rule date range
            "to": "2026-12-17"
        }
        
        # 2026-11-04 is Wednesday in week 1 (< stale_subject.from)
        occ_week1 = occ_on(rule_wed, stale_subject, "2026-11-04")
        self.assertIsNotNone(occ_week1, "Week 1 (2026-11-04) must render despite stale subject bounds")
        
        # 2026-11-25 is Wednesday in week 4 (> stale_subject.to)
        occ_week4 = occ_on(rule_wed, stale_subject, "2026-11-25")
        self.assertIsNotNone(occ_week4, "Week 4 (2026-11-25) must render despite stale subject bounds")

    def test_cross_year_scheduling(self):
        """Verify scheduler works across Year Boundaries (e.g., Dec 2026 to Jan 2027)."""
        cross_sub = {"id": "sub_cross", "name": "Linear Algebra", "code": "MAS291"}
        cross_rule = {
            "id": "r_cross",
            "sid": "sub_cross",
            "wd": 5, # Friday
            "slot": 2,
            "from": "2026-12-18",
            "to": "2027-01-15"
        }
        subs = {"sub_cross": cross_sub}
        
        occs = get_occurrences_for_range([cross_rule], subs, "2026-12-15", "2027-01-25")
        # 2026-12-18 (Fri) -> Class
        self.assertEqual(len(occs["2026-12-18"]), 1)
        # 2026-12-25 (Fri) -> Class
        self.assertEqual(len(occs["2026-12-25"]), 1)
        # 2027-01-01 (Fri) -> Class (New Year's Day)
        self.assertEqual(len(occs["2027-01-01"]), 1)
        # 2027-01-08 (Fri) -> Class
        self.assertEqual(len(occs["2027-01-08"]), 1)
        # 2027-01-15 (Fri) -> Class (Last)
        self.assertEqual(len(occs["2027-01-15"]), 1)
        # 2027-01-22 (Fri) -> 0 (Past end date)
        self.assertEqual(len(occs["2027-01-22"]), 0)

    def test_single_day_schedule(self):
        """Verify single-day workshop or one-off exam schedule."""
        single_sub = {"id": "sub_single", "name": "Workshop", "code": "WKS101"}
        single_rule = {
            "id": "r_single",
            "sid": "sub_single",
            "wd": 2, # Tuesday
            "slot": 4,
            "from": "2026-11-10",
            "to": "2026-11-10"
        }
        subs = {"sub_single": single_sub}
        
        self.assertIsNotNone(occ_on(single_rule, single_sub, "2026-11-10"))
        self.assertIsNone(occ_on(single_rule, single_sub, "2026-11-17"))
        self.assertIsNone(occ_on(single_rule, single_sub, "2026-11-03"))

if __name__ == "__main__":
    unittest.main()
