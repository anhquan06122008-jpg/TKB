"""
Tests for EduMate -> QLHT Rebranding, 8 Slots Scrollable Grid, 
and 10 Standard Colors Palette & Multi-Slot Retention
"""

import unittest
import hashlib
import re

class TestQlhtAndPalette(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("index.html", "r", encoding="utf-8") as f:
            cls.index_content = f.read()
        with open("TKB (QLHT).html", "r", encoding="utf-8") as f:
            cls.tkb_content = f.read()

    def test_file_synchronization(self):
        """index.html and TKB (QLHT).html must be 100% byte-for-byte identical"""
        h1 = hashlib.sha256(self.index_content.encode('utf-8')).hexdigest()
        h2 = hashlib.sha256(self.tkb_content.encode('utf-8')).hexdigest()
        self.assertEqual(h1, h2, "index.html and TKB (QLHT).html must be identical")

    def test_requirement_4_qlht_branding(self):
        """Web name must be QLHT in title, sidebar, and modals"""
        self.assertIn("<title>QLHT — Hệ Thống Quản Lý Thời Khóa Biểu & Học Tập</title>", self.index_content)
        self.assertIn("<h1>QLHT</h1>", self.index_content)
        self.assertIn("<span>Quản Lý Học Tập</span>", self.index_content)
        self.assertIn("QLHT LMS</h1>", self.index_content)
        self.assertIn("Tài khoản QLHT Cloud</h2>", self.index_content)
        self.assertIn("Tối (Dark Mode - QLHT Slate)</option>", self.index_content)

    def test_requirement_2_scroll_8_slots(self):
        """Grid must be flexbox with flex:1, height:0, overflow-y:auto to enable scrolling 8 slots"""
        self.assertIn("$('gridDisplayWrap').style.display = 'flex';", self.index_content)
        self.assertIn(".schedule-body-scroll", self.index_content)
        self.assertIn("overflow-y: auto;", self.index_content)
        self.assertIn(".schedule-body-scroll::-webkit-scrollbar", self.index_content)

    def test_requirement_3_10_color_palette(self):
        """10 Standard Colors Palette must be defined and integrated into Add & Edit modals"""
        # Palette must contain 10 colors
        palette_match = re.search(r'const PALETTE = \[([\s\S]*?)\];', self.index_content)
        self.assertIsNotNone(palette_match, "PALETTE definition must exist")
        hex_colors = re.findall(r"'#[0-9a-fA-F]{6}'", palette_match.group(1))
        self.assertEqual(len(hex_colors), 10, f"PALETTE must contain exactly 10 colors, found {len(hex_colors)}")

        # Add modal swatch container & sync notice
        self.assertIn('id="courseColorPalette"', self.index_content)
        self.assertIn('id="colorSyncNotice"', self.index_content)
        self.assertIn('id="newCourseColor"', self.index_content)

        # Edit modal swatch container
        self.assertIn('id="editColorPalette"', self.index_content)
        self.assertIn('id="editCourseColor"', self.index_content)

        # JavaScript helper functions
        self.assertIn('function renderColorPalette', self.index_content)
        self.assertIn('function syncAddModalColorFromExisting', self.index_content)

    def test_requirement_3_multi_slot_retention(self):
        """Adding a second slot for the same course on the same day must not delete the first slot"""
        self.assertIn("p.wd === r.wd && p.slot === r.slot", self.index_content)
        # Old destructive filter must not be present
        self.assertNotIn("pickedWds.includes(r.wd)", self.index_content)

if __name__ == "__main__":
    unittest.main()
