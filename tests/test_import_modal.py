"""
Test timetable import functionality: modal presence, clipboard parsing, table parser logic
"""

import unittest
import re

class TestTimetableImport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("index.html", "r", encoding="utf-8") as f:
            cls.html = f.read()

    def test_import_modal_elements(self):
        # 1. Dialog presence and accessibility
        self.assertIn('id="importModal"', self.html)
        self.assertIn('id="importModalTitle"', self.html)
        self.assertIn('Nhập lịch', self.html)

        # 2. Navigation buttons
        self.assertIn('id="btnSideImport"', self.html)
        self.assertIn('id="openImportModalBtn"', self.html)

        # 3. Import interactive controls
        self.assertIn('id="importReadClipboardBtn"', self.html)
        self.assertIn('id="importPasteArea"', self.html)
        self.assertIn('id="importFileInput"', self.html)
        self.assertIn('id="importPreviewContainer"', self.html)
        self.assertIn('id="importPreviewTableBody"', self.html)
        self.assertIn('id="importSelectAllCheck"', self.html)
        self.assertIn('id="importExecuteBtn"', self.html)
        self.assertIn('id="copyConsoleScriptBtn"', self.html)

    def test_import_js_functions(self):
        # Verify required JS functions exist
        self.assertIn('function parseImportHtmlOrText', self.html)
        self.assertIn('function processPastedImportContent', self.html)
        self.assertIn('function readFromClipboard', self.html)
        self.assertIn('function renderImportPreview', self.html)
        self.assertIn('function executeImport', self.html)
        self.assertIn('function openImportModal', self.html)
        self.assertIn('function detectSlot', self.html)

    def test_regex_course_code_detection(self):
        sample_text = "Thứ 2 ngày 09/11/2026 Tiết 3: PEN301 tại phòng 327 (Attend)"
        code_match = re.search(r'\b([A-Z]{2,5}\d{3}[A-Z]?)\b', sample_text)
        self.assertIsNotNone(code_match)
        self.assertEqual(code_match.group(1), "PEN301")

        sample_text_2 = "PRN211 - Advanced Cross-Platform C# Programming at Hall A-101"
        code_match_2 = re.search(r'\b([A-Z]{2,5}\d{3}[A-Z]?)\b', sample_text_2)
        self.assertIsNotNone(code_match_2)
        self.assertEqual(code_match_2.group(1), "PRN211")

if __name__ == "__main__":
    unittest.main()
