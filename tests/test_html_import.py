"""
Test extracting timetable data from saved old QLHT HTML files
"""

import unittest
import re
import json

def parse_old_qlht_html(html_text):
    """Simulate JS parseOldWebsiteHtmlOrJson using DOM-like regex"""
    subjects_map = {}
    extracted_rules = []
    
    # 1. Check if raw JSON backup was pasted/embedded
    try:
        data = json.loads(html_text)
        if isinstance(data, dict) and "subjects" in data and "rules" in data:
            return {
                "source": "json",
                "subjects": data["subjects"],
                "rules": data["rules"]
            }
    except Exception:
        pass
        
    # Check if script contains JSON
    m_script = re.search(r'data\s*=\s*(\{.*?subjects.*?rules.*?\});', html_text, re.DOTALL)
    if m_script:
        try:
            data = json.loads(m_script.group(1))
            return {
                "source": "embedded_json",
                "subjects": data.get("subjects", []),
                "rules": data.get("rules", [])
            }
        except Exception:
            pass

    # 2. Extract subjects from <div class="subj" data-id="...">
    subj_pattern = re.compile(
        r'<div[^>]*class=["\'][^"\']*subj[^"\']*["\'][^>]*data-id=["\']([^"\']+)["\'][^>]*>(.*?)</div>',
        re.DOTALL | re.IGNORECASE
    )
    for sid, body in subj_pattern.findall(html_text):
        # Find input tags inside body
        inputs = re.findall(r'<input[^>]+>', body, re.IGNORECASE)
        name, code, color = "Môn học", "", "#7c3aed"
        for inp in inputs:
            act_m = re.search(r'data-act=["\']([^"\']+)["\']', inp)
            val_m = re.search(r'value=["\']([^"\']*)["\']', inp)
            if act_m and val_m:
                act = act_m.group(1)
                val = val_m.group(1)
                if act == 'name': name = val
                elif act == 'code': code = val
                elif act == 'color': color = val
        subjects_map[sid] = {"id": sid, "name": name, "code": code, "color": color}

    # 3. Extract occurrences from <button class="occ" ...>
    occ_pattern = re.compile(
        r'<button[^>]*class=["\'][^"\']*occ[^"\']*["\'][^>]*data-rule=["\']([^"\']+)["\'][^>]*data-date=["\']([^"\']+)["\'][^>]*>(.*?)</button>',
        re.DOTALL | re.IGNORECASE
    )
    
    for rid, date_str, body in occ_pattern.findall(html_text):
        name_m = re.search(r'<strong>(.*?)</strong>', body)
        sub_info_m = re.search(r'<span>(.*?)</span>', body)
        
        name = name_m.group(1).strip() if name_m else "Môn học"
        info = sub_info_m.group(1).strip() if sub_info_m else ""
        
        # info has "CODE · ROOM · START-END"
        parts = [p.strip() for p in info.split('·')]
        code = parts[0] if len(parts) > 0 and not ':' in parts[0] else ""
        room = parts[1] if len(parts) > 2 else (parts[0] if len(parts) == 2 and not ':' in parts[0] else "")
        time_part = parts[-1] if ':' in parts[-1] else ""
        
        slot = 1
        if "08:45" in time_part or "09:10" in time_part: slot = 2
        elif "10:30" in time_part or "10:50" in time_part: slot = 3
        elif "12:30" in time_part or "12:50" in time_part: slot = 4
        elif "14:15" in time_part or "14:30" in time_part: slot = 5
        elif "16:00" in time_part or "16:10" in time_part: slot = 6
        elif "17:45" in time_part or "18:00" in time_part: slot = 7
        elif "19:30" in time_part: slot = 8
        
        extracted_rules.append({
            "ruleId": rid,
            "date": date_str,
            "name": name,
            "code": code,
            "room": room,
            "slot": slot
        })

    return {
        "source": "html_table",
        "subjects": list(subjects_map.values()),
        "occurrences": extracted_rules
    }

class TestOldHtmlImport(unittest.TestCase):
    def test_parse_old_html_sample(self):
        sample_saved_html = """
        <!DOCTYPE html>
        <html>
        <body>
        <div id="sList">
            <div class="subj" data-id="s_ai">
                <input type="color" value="#2563eb" data-act="color">
                <input type="text" value="Tri Tue Nhan Tao" data-act="name">
                <input type="text" value="AIF101" data-act="code">
            </div>
            <div class="subj" data-id="s_calc">
                <input type="color" value="#dc2626" data-act="color">
                <input type="text" value="Giai Tich 1" data-act="name">
                <input type="text" value="MAE101" data-act="code">
            </div>
        </div>
        <table id="grid">
            <tr>
                <td>
                    <button type="button" class="occ" style="--c:#2563eb" data-rule="r_ai_1" data-date="2026-11-09">
                        <strong>Tri Tue Nhan Tao</strong>
                        <span>AIF101 · BE-302 · 07:00–08:30</span>
                    </button>
                </td>
                <td>
                    <button type="button" class="occ" style="--c:#dc2626" data-rule="r_calc_1" data-date="2026-11-10">
                        <strong>Giai Tich 1</strong>
                        <span>MAE101 · AL-102 · 08:45–10:15</span>
                    </button>
                </td>
            </tr>
        </table>
        </body>
        </html>
        """
        res = parse_old_qlht_html(sample_saved_html)
        self.assertEqual(res["source"], "html_table")
        self.assertEqual(len(res["subjects"]), 2)
        self.assertEqual(res["subjects"][0]["code"], "AIF101")
        self.assertEqual(len(res["occurrences"]), 2)
        self.assertEqual(res["occurrences"][0]["code"], "AIF101")
        self.assertEqual(res["occurrences"][0]["room"], "BE-302")
        self.assertEqual(res["occurrences"][0]["slot"], 1)
        self.assertEqual(res["occurrences"][1]["code"], "MAE101")
        self.assertEqual(res["occurrences"][1]["slot"], 2)

if __name__ == "__main__":
    unittest.main()
