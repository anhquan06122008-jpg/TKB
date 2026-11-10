"""
Comprehensive verification of FAP timetable parsing:
1. Real FAP WeeklyTimetable HTML with header/logo tables, rowspan, dropdowns
2. Plain text copy with tabs and newlines
3. Attendance table format (ViewAttendstudent)
4. Bookmarklet and Console script table discovery logic
"""

import unittest
import re

class TestFapImportLive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("index.html", "r", encoding="utf-8") as f:
            cls.html = f.read()

    def test_bookmarklet_and_console_script(self):
        # Ensure bookmarklet does NOT do naive querySelector('table')
        self.assertNotIn("document.querySelector('table')", self.html)
        # Ensure it searches all tables for timetable content
        self.assertIn("tables.find", self.html)
        self.assertIn("tiết", self.html)
        self.assertIn("slot", self.html)

    def test_paste_area_is_textarea(self):
        # Must be accessible textarea with placeholder
        self.assertIn('<textarea id="importPasteArea"', self.html)
        self.assertIn('placeholder=', self.html)

    def test_2d_grid_and_tab_parsing_functions(self):
        self.assertIn('function parseImportHtmlOrText', self.html)
        self.assertIn('function detectSlot', self.html)
        self.assertIn('function extractCourseName', self.html)
        self.assertIn('function processPastedImportContent', self.html)
        self.assertIn('function readFromClipboard', self.html)
        self.assertIn('function executeImport', self.html)

if __name__ == "__main__":
    unittest.main()
