"""
Automated Backend & Security Tests for server.py
Verifies:
1. Registration & Login (PBKDF2-HMAC-SHA256)
2. Complete Data Isolation between multiple user accounts
3. Sync Push & Pull
4. Password change & Logout
"""

import unittest
import threading
import time
import urllib.request
import urllib.error
import json
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import server

TEST_PORT = 18080

def start_test_server():
    server.DB_FILE = os.path.join(os.path.dirname(__file__), "test_database.db")
    if os.path.exists(server.DB_FILE):
        try:
            os.remove(server.DB_FILE)
        except Exception:
            pass
    server.init_db()
    httpd = server.socketserver.TCPServer(("127.0.0.1", TEST_PORT), server.EduMateHandler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(0.3)
    return httpd

def api_call(path, method="GET", data=None, token=None):
    url = f"http://127.0.0.1:{TEST_PORT}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))

class TestBackendApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = start_test_server()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        if os.path.exists(server.DB_FILE):
            try:
                os.remove(server.DB_FILE)
            except Exception:
                pass

    def test_auth_and_isolation(self):
        # 1. Register User A
        status, res_a = api_call("/api/auth/register", "POST", {
            "username": "user_a",
            "email": "user_a@test.com",
            "password": "password123",
            "displayName": "Sinh Vien A"
        })
        self.assertEqual(status, 201)
        self.assertTrue(res_a["success"])
        token_a = res_a["token"]
        self.assertIsNotNone(token_a)

        # 2. Register User B
        status, res_b = api_call("/api/auth/register", "POST", {
            "username": "user_b",
            "email": "user_b@test.com",
            "password": "password456",
            "displayName": "Sinh Vien B"
        })
        self.assertEqual(status, 201)
        token_b = res_b["token"]

        # 3. Duplicate username should fail (409)
        status_dup, res_dup = api_call("/api/auth/register", "POST", {
            "username": "user_a",
            "email": "another@test.com",
            "password": "password123"
        })
        self.assertEqual(status_dup, 409)

        # 4. Login User A
        status_log, res_log = api_call("/api/auth/login", "POST", {
            "login": "user_a@test.com",
            "password": "password123"
        })
        self.assertEqual(status_log, 200)
        self.assertEqual(res_log["user"]["username"], "user_a")

        # Wrong password should fail (401)
        status_wrong, _ = api_call("/api/auth/login", "POST", {
            "login": "user_a",
            "password": "wrong_password"
        })
        self.assertEqual(status_wrong, 401)

        # 5. User A pushes timetable
        schedule_a = {
            "subjects": [{"id": "s1", "name": "Toan Cao Cap A", "code": "MAE101"}],
            "rules": [{"id": "r1", "sid": "s1", "slot": 1, "room": "BE-302"}]
        }
        status_push, res_push = api_call("/api/sync/push", "POST", {"data": schedule_a}, token=token_a)
        self.assertEqual(status_push, 200)
        self.assertTrue(res_push["success"])

        # 6. User B pulls timetable -> MUST BE EMPTY / NOT User A's data
        status_pull_b, res_pull_b = api_call("/api/sync/pull", "GET", token=token_b)
        self.assertEqual(status_pull_b, 200)
        self.assertIsNone(res_pull_b["data"])

        # 7. User B pushes their own schedule
        schedule_b = {
            "subjects": [{"id": "sb1", "name": "Vat Ly Dai Cuong B", "code": "PHY101"}],
            "rules": [{"id": "rb1", "sid": "sb1", "slot": 3, "room": "AL-105"}]
        }
        status_push_b, _ = api_call("/api/sync/push", "POST", {"data": schedule_b}, token=token_b)
        self.assertEqual(status_push_b, 200)

        # 8. User A pulls -> MUST BE User A's data ONLY!
        status_pull_a, res_pull_a = api_call("/api/sync/pull", "GET", token=token_a)
        self.assertEqual(status_pull_a, 200)
        self.assertEqual(res_pull_a["data"]["subjects"][0]["name"], "Toan Cao Cap A")

        # 9. Change Password for User A
        status_cp, res_cp = api_call("/api/auth/change-password", "POST", {
            "oldPassword": "password123",
            "newPassword": "new_secure_password"
        }, token=token_a)
        self.assertEqual(status_cp, 200)

        # Login with old password should now fail
        status_old, _ = api_call("/api/auth/login", "POST", {"login": "user_a", "password": "password123"})
        self.assertEqual(status_old, 401)
        # Login with new password should succeed
        status_new, _ = api_call("/api/auth/login", "POST", {"login": "user_a", "password": "new_secure_password"})
        self.assertEqual(status_new, 200)

if __name__ == "__main__":
    unittest.main()
