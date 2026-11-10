"""
Test parsing FAP ViewAttendstudent semester table
"""

import unittest
import re

def parse_fap_attend_row(row_text):
    # e.g. "1 | 09/11/2026 | Slot 2 (08:45-10:15) | Room BE-302 | PRN211 - Basic Cross-Platform Application Programming With .NET"
    date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})', row_text)
    slot_match = re.search(r'(?:slot|tiết)\s*(\d)', row_text, re.IGNORECASE)
    code_match = re.search(r'\b([A-Z]{2,5}\d{3}[A-Z]?)\b', row_text)
    room_match = re.search(r'(?:at|phòng|room)\s*[:\-]?\s*([A-Za-z0-9.\-]+)', row_text, re.IGNORECASE)
    
    return {
        "date": date_match.group(1) if date_match else None,
        "slot": int(slot_match.group(1)) if slot_match else None,
        "code": code_match.group(1) if code_match else None,
        "room": room_match.group(1) if room_match else None
    }

class TestAttendParse(unittest.TestCase):
    def test_semester_row(self):
        row = "1 15/09/2026 Slot 1 (07:30-09:00) Room BE-302 PRN211 Basic Cross-Platform"
        res = parse_fap_attend_row(row)
        self.assertEqual(res["date"], "15/09/2026")
        self.assertEqual(res["slot"], 1)
        self.assertEqual(res["code"], "PRN211")
        self.assertEqual(res["room"], "BE-302")

if __name__ == "__main__":
    unittest.main()
