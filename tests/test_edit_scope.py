"""
Unit tests for Edit Scope and Delete Scope logic:
1. Scope 'one': Only this single occurrence on 'date' is moved / skipped.
2. Scope 'after': Occurrence on 'date' and all subsequent dates are moved / deleted.
3. Scope 'all': All occurrences on this weekday across all weeks are updated / deleted.
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
    return from_key(s).weekday() + 1

def occ_on(rule, subject, k):
    if not subject:
        return None
    from_date = rule.get("from") or subject.get("from")
    to_date = rule.get("to") or subject.get("to")
    if from_date and k < from_date:
        return None
    if to_date and k > to_date:
        return None
    if weekday_of(k) != rule.get("wd"):
        return None
    if k in rule.get("skip", []):
        return None
    if k in rule.get("moved", {}):
        mv = rule["moved"][k]
        return {
            "sub": subject,
            "rule": rule,
            "slot": mv.get("slot", rule.get("slot")),
            "room": mv.get("room", rule.get("room", "")),
            "date": k,
            "isMoved": True
        }
    return {
        "sub": subject,
        "rule": rule,
        "slot": rule.get("slot"),
        "room": rule.get("room", ""),
        "date": k,
        "isMoved": False
    }

class TestEditScopeLogic(unittest.TestCase):
    def setUp(self):
        self.subject = {
            "id": "sub_math",
            "name": "Toán Cao Cấp",
            "code": "MAE101",
            "from": "2026-11-02",
            "to": "2026-11-30"
        }
        # Every Wednesday (wd = 3) Slot 2 Room 101
        self.rule = {
            "id": "r_wed",
            "sid": "sub_math",
            "wd": 3,
            "slot": 2,
            "room": "101",
            "from": "2026-11-02",
            "to": "2026-11-30",
            "skip": [],
            "moved": {}
        }

    def test_scope_one_edit(self):
        """Moving only 2026-11-18 from slot 2 to slot 4, room 202"""
        d = "2026-11-18"
        self.rule["moved"][d] = {"slot": 4, "room": "202"}

        # 2026-11-11 (prior week) is still Slot 2 Room 101
        occ_prior = occ_on(self.rule, self.subject, "2026-11-11")
        self.assertEqual(occ_prior["slot"], 2)
        self.assertEqual(occ_prior["room"], "101")

        # 2026-11-18 is changed to Slot 4 Room 202
        occ_moved = occ_on(self.rule, self.subject, d)
        self.assertEqual(occ_moved["slot"], 4)
        self.assertEqual(occ_moved["room"], "202")

        # 2026-11-25 (subsequent week) is still original Slot 2 Room 101
        occ_next = occ_on(self.rule, self.subject, "2026-11-25")
        self.assertEqual(occ_next["slot"], 2)
        self.assertEqual(occ_next["room"], "101")

    def test_scope_after_edit(self):
        """
        Moving from 2026-11-18 onwards to slot 5 room 303:
        Original rule ends at 2026-11-17.
        New rule starts from 2026-11-18 with slot 5 room 303.
        """
        d = "2026-11-18"
        self.rule["to"] = add_days(d, -1) # 2026-11-17
        new_rule = {
            "id": "r_wed_split",
            "sid": "sub_math",
            "wd": 3,
            "slot": 5,
            "room": "303",
            "from": d,
            "to": "2026-11-30",
            "skip": [],
            "moved": {}
        }
        rules = [self.rule, new_rule]

        # 2026-11-11: Rule 1 matches Slot 2
        o11 = [occ_on(r, self.subject, "2026-11-11") for r in rules if occ_on(r, self.subject, "2026-11-11")][0]
        self.assertEqual(o11["slot"], 2)

        # 2026-11-18: Rule 2 matches Slot 5 Room 303
        o18 = [occ_on(r, self.subject, "2026-11-18") for r in rules if occ_on(r, self.subject, "2026-11-18")][0]
        self.assertEqual(o18["slot"], 5)
        self.assertEqual(o18["room"], "303")

        # 2026-11-25: Rule 2 matches Slot 5 Room 303
        o25 = [occ_on(r, self.subject, "2026-11-25") for r in rules if occ_on(r, self.subject, "2026-11-25")][0]
        self.assertEqual(o25["slot"], 5)
        self.assertEqual(o25["room"], "303")

    def test_scope_one_delete(self):
        """Deleting only 2026-11-18: Adds 2026-11-18 to skip"""
        d = "2026-11-18"
        self.rule["skip"].append(d)

        self.assertIsNotNone(occ_on(self.rule, self.subject, "2026-11-11"))
        self.assertIsNone(occ_on(self.rule, self.subject, d))
        self.assertIsNotNone(occ_on(self.rule, self.subject, "2026-11-25"))

    def test_scope_after_delete(self):
        """Deleting from 2026-11-18 onwards: sets rule.to = 2026-11-17"""
        d = "2026-11-18"
        self.rule["to"] = add_days(d, -1)

        self.assertIsNotNone(occ_on(self.rule, self.subject, "2026-11-11"))
        self.assertIsNone(occ_on(self.rule, self.subject, "2026-11-18"))
        self.assertIsNone(occ_on(self.rule, self.subject, "2026-11-25"))

if __name__ == "__main__":
    unittest.main()
