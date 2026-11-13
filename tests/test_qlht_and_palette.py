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
        """Grid and Agenda/Day views must have overflow-y:auto to enable scrolling"""
        self.assertIn("$('gridDisplayWrap').style.display = 'flex';", self.index_content)
        self.assertIn(".schedule-body-scroll", self.index_content)
        self.assertIn("overflow-y: auto;", self.index_content)
        self.assertIn(".schedule-body-scroll::-webkit-scrollbar", self.index_content)
        self.assertIn("#agendaDisplayWrap, #dayDisplayWrap", self.index_content)
        self.assertIn("-webkit-overflow-scrolling: touch;", self.index_content)

    def test_requirement_3_10_color_palette(self):
        """Extended Color Palette (>=30 colors) & sync helpers must be integrated into Add & Edit modals"""
        palette_match = re.search(r'const PALETTE = \[([\s\S]*?)\];', self.index_content)
        self.assertIsNotNone(palette_match, "PALETTE definition must exist")
        hex_colors = re.findall(r"'#[0-9a-fA-F]{6}'", palette_match.group(1))
        self.assertGreaterEqual(len(hex_colors), 30, f"PALETTE must contain at least 30 colors, found {len(hex_colors)}")

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

    def test_requirement_course_integration_and_advanced_color_system(self):
        """Master Prompt: Existing course selector, courseId binding, duplicate-code safety, >=30 colors, HEX picker, auto-assign, contrast, safe delete"""
        # 1. Existing Course Selector + New Course toggle & 10-field Add Form
        self.assertIn('id="modeExistingCourseBtn"', self.index_content)
        self.assertIn('id="modeNewCourseBtn"', self.index_content)
        self.assertIn('id="existingCourseSelect"', self.index_content)
        self.assertIn('id="selectedCourseId"', self.index_content)
        self.assertIn('id="newCourseLecturer"', self.index_content)
        self.assertIn('id="newCourseNotes"', self.index_content)
        self.assertIn('function applySelectedCourseToAddForm', self.index_content)
        self.assertIn('function setAddCourseMode', self.index_content)

        # 2. courseId linkage, migration & duplicate course code protection
        self.assertIn('s.courseId', self.index_content)
        self.assertIn('r.courseId', self.index_content)
        self.assertIn('backup-pre-courseid', self.index_content)
        self.assertIn('function findSubjectByIdentity', self.index_content)

        # 3. Advanced Color Picker (>=30 colors, native color picker, HEX input, auto/random/reset, contrast)
        self.assertIn('const COLOR_GROUPS = [', self.index_content)
        self.assertIn('id="colorPickerModal"', self.index_content)
        self.assertIn('id="cpkNativeInput"', self.index_content)
        self.assertIn('id="cpkHexInput"', self.index_content)
        self.assertIn('id="cpkAutoBtn"', self.index_content)
        self.assertIn('id="cpkRandomBtn"', self.index_content)
        self.assertIn('id="cpkResetBtn"', self.index_content)
        self.assertIn('id="cpkLiveCardPreview"', self.index_content)
        self.assertIn('function autoAssignCourseColor', self.index_content)
        self.assertIn('function getContrastPaletteForBg', self.index_content)
        self.assertIn('function normalizeHexColor', self.index_content)

        # 4. Safe Subject Deletion Modal
        self.assertIn('id="deleteCourseModal"', self.index_content)
        self.assertIn('name="delCourseAction"', self.index_content)
        self.assertIn('function handleConfirmDeleteCourse', self.index_content)

    def test_requirement_3_multi_slot_retention(self):
        """Adding a second slot for the same course on the same day must not delete the first slot"""
        self.assertIn("p.wd === r.wd && p.slot === r.slot", self.index_content)
        # Old destructive filter must not be present
        self.assertNotIn("pickedWds.includes(r.wd)", self.index_content)

    def test_zero_server_offline_and_phone_sync(self):
        """Zero-server usage: offline sync guards, URL #sync= transfer modal, PWA assets, and cloud config"""
        import os
        import json

        # 1. Offline session guards & instant standalone entry
        self.assertIn("function isOfflineSession()", self.index_content)
        self.assertIn("💾 Lưu tại máy (Offline)", self.index_content)
        self.assertIn('id="gateStandaloneBtn"', self.index_content)
        self.assertIn("function activateOfflineSession(", self.index_content)

        # 2. Zero-server URL hash (#sync=...) transfer engine & modal
        self.assertIn('id="phoneSyncModal"', self.index_content)
        self.assertIn('id="openPhoneSyncSidebarBtn"', self.index_content)
        self.assertIn('id="openPhoneSyncSettingsBtn"', self.index_content)
        self.assertIn("async function encodeSyncPayload(", self.index_content)
        self.assertIn("async function decodeSyncPayload(", self.index_content)
        self.assertIn("async function handleUrlSyncImport()", self.index_content)

        # 3. PWA meta tags & supporting files
        self.assertIn('<link rel="manifest" href="manifest.json">', self.index_content)
        self.assertIn('apple-mobile-web-app-capable', self.index_content)
        self.assertTrue(os.path.exists("manifest.json"))
        self.assertTrue(os.path.exists("sw.js"))
        self.assertTrue(os.path.exists("icon.svg"))
        with open("manifest.json", "r", encoding="utf-8") as mf:
            manifest = json.load(mf)
        self.assertEqual(manifest.get("display"), "standalone")
        self.assertEqual(manifest.get("short_name"), "QLHT")

        # 4. Cloud deployment support (optional 24/7 server hosting)
        self.assertTrue(os.path.exists("render.yaml"))
        with open("server.py", "r", encoding="utf-8") as sf:
            srv = sf.read()
        self.assertIn('os.environ.get("PORT"', srv)
        self.assertIn('os.environ.get("QLHT_DB_PATH")', srv)

if __name__ == "__main__":
    unittest.main()
