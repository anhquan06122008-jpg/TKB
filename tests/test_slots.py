"""
Test slot detection with various FPT campus slot times
"""

import unittest

def detect_slot_improved(text):
    import re
    # Check for slot number directly
    m = re.search(r'(?:slot|tiết)\s*(\d)', text, re.IGNORECASE) or re.match(r'^\s*(\d)\s*$', text)
    if m:
        return min(8, max(1, int(m.group(1))))
    
    # Check for time range (e.g. 07:30, 09:10, 08:45)
    h = re.search(r'(\d{1,2}):(\d{2})', text)
    if h:
        hour = int(h.group(1))
        minute = int(h.group(2))
        total_mins = hour * 60 + minute
        
        # Ranges:
        # Slot 1: 07:00 - 08:30 (420 to 500 mins) -> 07:00 to 08:20
        if 420 <= total_mins <= 500:
            return 1
        # Slot 2: 08:45 or 09:10 (510 to 590 mins)
        elif 501 <= total_mins <= 590:
            return 2
        # Slot 3: 10:30 or 10:50 (600 to 680 mins)
        elif 591 <= total_mins <= 680:
            return 3
        # Slot 4: 12:30 or 12:50 (730 to 800 mins)
        elif 720 <= total_mins <= 800:
            return 4
        # Slot 5: 14:15 or 14:30 (840 to 920 mins)
        elif 830 <= total_mins <= 920:
            return 5
        # Slot 6: 16:00 or 16:10 (950 to 1030 mins)
        elif 940 <= total_mins <= 1030:
            return 6
        # Slot 7: 17:45 or 18:00 (1050 to 1130 mins)
        elif 1040 <= total_mins <= 1130:
            return 7
        # Slot 8: 19:30 or 19:40 (1150 to 1230 mins)
        elif 1140 <= total_mins <= 1260:
            return 8
            
    return 0

class TestSlotDetection(unittest.TestCase):
    def test_slots(self):
        self.assertEqual(detect_slot_improved("07:30 - 09:00"), 1)
        self.assertEqual(detect_slot_improved("07:00 - 08:30"), 1)
        self.assertEqual(detect_slot_improved("09:10 - 10:40"), 2)
        self.assertEqual(detect_slot_improved("08:45 - 10:15"), 2)
        self.assertEqual(detect_slot_improved("10:50 - 12:20"), 3)
        self.assertEqual(detect_slot_improved("10:30 - 12:00"), 3)
        self.assertEqual(detect_slot_improved("12:50 - 14:20"), 4)
        self.assertEqual(detect_slot_improved("14:30 - 16:00"), 5)
        self.assertEqual(detect_slot_improved("16:10 - 17:40"), 6)

if __name__ == "__main__":
    unittest.main()
