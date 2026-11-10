"""
Verify HTML, tags, and script integrity for index.html
"""

import unittest
from html.parser import HTMLParser

class StrictHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.errors = []
        self.self_closing = {
            'meta', 'link', 'img', 'br', 'hr', 'input', 'col', 'base', 'area', 'param'
        }

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in self.self_closing:
            self.tags.append(tag.lower())

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.self_closing:
            return
        if not self.tags:
            self.errors.append(f"Unexpected closing tag </{tag}> with empty stack")
            return
        last = self.tags.pop()
        if last != tag:
            # allow some laxness for p / li but report
            self.errors.append(f"Mismatched tag: expected </{last}>, found </{tag}>")

class TestHtmlIntegrity(unittest.TestCase):
    def test_html_parsing(self):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        parser = StrictHTMLParser()
        parser.feed(content)
        # Check required semantic elements
        self.assertIn("<!DOCTYPE html>", content)
        self.assertIn("<title>EduMate — Universal Student Planner & LMS 2.0</title>", content)
        self.assertIn("id=\"appHeader\"", content)
        self.assertIn("id=\"timetableToolbar\"", content)
        self.assertIn("id=\"pageTitleText\"", content)
        self.assertIn("id=\"scheduleHeader\"", content)
        self.assertIn("id=\"scheduleBodyScroll\"", content)
        self.assertIn("id=\"authGateScreen\"", content)
        self.assertIn("id=\"addClassModal\"", content)
        self.assertIn("id=\"newCourseFrom\"", content)
        self.assertIn("id=\"newCourseTo\"", content)
        self.assertIn("id=\"syncSlotsCheckbox\"", content)
        self.assertIn("name=\"editScope\"", content)
        self.assertNotIn("id=\"fapModal\"", content)
        self.assertNotIn("id=\"oldImportModal\"", content)
        self.assertIn("id=\"importModal\"", content)
        self.assertIn("id=\"btnSideImport\"", content)
        self.assertIn("id=\"openImportModalBtn\"", content)
        self.assertIn("id=\"relativeWeekLabel\"", content)
        self.assertIn("studyflow-tkb-v1", content)
        self.assertEqual(len(parser.errors), 0, f"HTML parser errors found: {parser.errors}")

if __name__ == "__main__":
    unittest.main()
