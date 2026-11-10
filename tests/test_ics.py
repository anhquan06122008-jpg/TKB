"""
Additional Engine Test: FAP HTML Table Extraction & ICS Generation
"""

import unittest
import re
from datetime import datetime

def generate_ics(events):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//EduMate//Universal Student Planner LMS 2.0//VI",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH"
    ]
    for ev in events:
        lines.append("BEGIN:VEVENT")
        lines.append(f"UID:{ev['uid']}@edumate.local")
        lines.append(f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}")
        lines.append(f"DTSTART:{ev['start']}")
        lines.append(f"DTEND:{ev['end']}")
        lines.append(f"SUMMARY:{ev['summary']}")
        if ev.get("location"):
            lines.append(f"LOCATION:{ev['location']}")
        if ev.get("description"):
            lines.append(f"DESCRIPTION:{ev['description']}")
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)

class TestIcsAndFap(unittest.TestCase):
    def test_ics_format(self):
        sample_events = [{
            "uid": "test1234",
            "start": "20261109T084500",
            "end": "20261109T101500",
            "summary": "AIF101 - AI Literacy",
            "location": "Phòng BE-302",
            "description": "Tiết 2"
        }]
        ics_text = generate_ics(sample_events)
        self.assertIn("BEGIN:VCALENDAR", ics_text)
        self.assertIn("SUMMARY:AIF101 - AI Literacy", ics_text)
        self.assertIn("LOCATION:Phòng BE-302", ics_text)
        self.assertIn("END:VCALENDAR", ics_text)

if __name__ == "__main__":
    unittest.main()
