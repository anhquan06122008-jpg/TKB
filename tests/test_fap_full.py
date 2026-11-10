"""
Comprehensive test for FAP grid and attendance parser
"""

import unittest
import re

def pad(n):
    return f"{n:02d}"

def detect_slot(text):
    if not text:
        return 0
    m = re.search(r'(?:slot|tiết)\s*(\d)', text, re.IGNORECASE) or re.match(r'^\s*(\d)\s*$', text)
    if m:
        return min(8, max(1, int(m.group(1))))
    h = re.search(r'(\d{1,2}):(\d{2})', text)
    if h:
        mins = int(h.group(1)) * 60 + int(h.group(2))
        if 420 <= mins <= 505: return 1
        if 506 <= mins <= 590: return 2
        if 591 <= mins <= 685: return 3
        if 710 <= mins <= 805: return 4
        if 806 <= mins <= 925: return 5
        if 926 <= mins <= 1035: return 6
        if 1036 <= mins <= 1135: return 7
        if 1136 <= mins <= 1260: return 8
    return 0

def parse_fap_html_simulation(html_content, current_monday="2026-11-09"):
    out = []
    seen = set()
    
    # 1. Row attendance format test
    row_pattern = re.compile(r'<tr>(.*?)</tr>', re.DOTALL | re.IGNORECASE)
    cell_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL | re.IGNORECASE)
    
    rows = row_pattern.findall(html_content)
    for r in rows:
        cells = [re.sub(r'<[^>]+>', ' ', c).strip() for c in cell_pattern.findall(r)]
        row_text = " ".join(cells)
        dm = re.search(r'(\d{1,2})/(\d{1,2})(?:/(\d{4}))?', row_text) or re.search(r'(\d{4})-(\d{2})-(\d{2})', row_text)
        cm = re.search(r'\b([A-Z]{2,5}\d{3}[A-Z]?)\b', row_text)
        slot = detect_slot(row_text)
        if dm and cm and slot:
            if dm.group(0).count('-') == 2:
                date = dm.group(0)
            else:
                yr = dm.group(3) if dm.group(3) else current_monday[:4]
                date = f"{yr}-{pad(int(dm.group(2)))}-{pad(int(dm.group(1)))}"
            code = cm.group(1)
            room_m = re.search(r'(?:at|phòng|room)\s*[:\-]?\s*([A-Za-z0-9.\-]+)', row_text, re.IGNORECASE)
            room = room_m.group(1) if room_m else ''
            key = f"{date}|{slot}|{code}"
            if key not in seen:
                seen.add(key)
                out.append({"date": date, "slot": slot, "code": code, "room": room})
    return out

class TestFapFull(unittest.TestCase):
    def test_fap_full_semester_import(self):
        sample_html = """
        <table>
            <tr>
                <td>1</td>
                <td>09/11/2026</td>
                <td>Slot 1 (07:30 - 09:00)</td>
                <td>at BE-302</td>
                <td>PRN211 - Cross Platform</td>
            </tr>
            <tr>
                <td>2</td>
                <td>10/11/2026</td>
                <td>Slot 2 (09:10 - 10:40)</td>
                <td>at AL-L401</td>
                <td>SWP391 - Software Project</td>
            </tr>
        </table>
        """
        res = parse_fap_html_simulation(sample_html)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]["code"], "PRN211")
        self.assertEqual(res[0]["slot"], 1)
        self.assertEqual(res[0]["room"], "BE-302")
        self.assertEqual(res[1]["code"], "SWP391")
        self.assertEqual(res[1]["slot"], 2)
        self.assertEqual(res[1]["room"], "AL-L401")

if __name__ == "__main__":
    unittest.main()
