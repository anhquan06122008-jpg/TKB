"""
Test real-world FAP HTML table structures
"""

import unittest
import re

def parse_fap_sample(html_snippet):
    courses = re.findall(r'\b([A-Z]{2,5}\d{3}[A-Z]?)\b', html_snippet)
    rooms = re.findall(r'(?:at|phòng|room)\s*[:\-]?\s*<b>?\s*([A-Za-z0-9\-]+)', html_snippet, re.IGNORECASE)
    times = re.findall(r'(\d{1,2}:\d{2})\s*[-–]\s*(\d{1,2}:\d{2})', html_snippet)
    dates = re.findall(r'(\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})', html_snippet)
    return courses, rooms, times, dates

class TestRealFap(unittest.TestCase):
    def test_fap_structure(self):
        fap_td = """
        <td align="center">
            <a href="ActivityDetail.aspx?id=12345"><b>PRN211</b></a>
            <br>at <b>BE-302</b>
            <br>(07:30-09:00)
            <br><span style="color:green;">(attended)</span>
            <br><span>(SonNT)</span>
        </td>
        """
        courses, rooms, times, _ = parse_fap_sample(fap_td)
        self.assertIn("PRN211", courses)
        self.assertIn("BE-302", rooms)
        self.assertEqual(times[0], ("07:30", "09:00"))

if __name__ == "__main__":
    unittest.main()
