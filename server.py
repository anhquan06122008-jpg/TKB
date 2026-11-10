"""
EduMate LMS 2.0 — Backend Server & REST API
Features:
1. User Authentication (Register, Login, Logout, Change Password) using PBKDF2-HMAC-SHA256
2. Multi-device Timetable Synchronization (Push & Pull) with SQLite3
3. Static Web Server serving EduMate frontend
4. 100% Zero external pip dependencies (Pure Python Standard Library)
"""

import http.server
import socketserver
import urllib.parse
import sqlite3
import hashlib
import secrets
import json
import os
import sys
from datetime import datetime, timedelta, timezone

DB_FILE = os.path.join(os.path.dirname(__file__), "database.db")
DEFAULT_PORT = int(os.environ.get("PORT", 8080))

# ==============================================================================
# DATABASE MANAGEMENT
# ==============================================================================
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        display_name TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    # Sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        token TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    # Schedules table (stores user timetable data JSON)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedules (
        user_id TEXT PRIMARY KEY,
        data_json TEXT NOT NULL,
        version INTEGER NOT NULL DEFAULT 1,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    conn.commit()
    conn.close()

# ==============================================================================
# SECURITY & AUTH HELPERS
# ==============================================================================
def hash_password(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    # NIST recommended PBKDF2-HMAC-SHA256 with 100,000 iterations
    pwd_bytes = password.encode('utf-8')
    salt_bytes = bytes.fromhex(salt)
    key = hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt_bytes, 100000)
    return key.hex(), salt

def verify_password(password, stored_hash, salt):
    key, _ = hash_password(password, salt)
    return hmac_compare(key, stored_hash)

def hmac_compare(val1, val2):
    return secrets.compare_digest(val1, val2)

def generate_token():
    return secrets.token_hex(32)

def get_authenticated_user(headers):
    auth_header = headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header[7:].strip()
    if not token:
        return None
    
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
        SELECT u.id, u.username, u.email, u.display_name, u.created_at
        FROM sessions s
        JOIN users u ON s.user_id = u.id
        WHERE s.token = ? AND s.expires_at > ?
    """, (token, now_str))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row["id"],
            "username": row["username"],
            "email": row["email"],
            "displayName": row["display_name"],
            "createdAt": row["created_at"]
        }
    return None

# ==============================================================================
# HTTP REQUEST HANDLER
# ==============================================================================
class EduMateHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve static files from workspace directory
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

    def send_json(self, status_code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        # Handle CORS Preflight
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/auth/me":
            user = get_authenticated_user(self.headers)
            if not user:
                return self.send_json(401, {"success": False, "error": "Chưa đăng nhập hoặc phiên hết hạn."})
            return self.send_json(200, {"success": True, "user": user})

        elif path == "/api/sync/pull":
            user = get_authenticated_user(self.headers)
            if not user:
                return self.send_json(401, {"success": False, "error": "Chưa đăng nhập."})
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT data_json, version, updated_at FROM schedules WHERE user_id = ?", (user["id"],))
            row = cursor.fetchone()
            conn.close()
            if row:
                try:
                    data = json.loads(row["data_json"])
                except Exception:
                    data = None
                return self.send_json(200, {
                    "success": True,
                    "data": data,
                    "version": row["version"],
                    "updatedAt": row["updated_at"]
                })
            else:
                return self.send_json(200, {
                    "success": True,
                    "data": None,
                    "version": 0,
                    "updatedAt": None
                })

        # Default static file handler
        if path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        # Parse JSON body
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            body = json.loads(post_data.decode('utf-8')) if post_data else {}
        except Exception:
            return self.send_json(400, {"success": False, "error": "Dữ liệu JSON không hợp lệ."})

        # --- 1. REGISTER ---
        if path == "/api/auth/register":
            username = body.get("username", "").strip().lower()
            email = body.get("email", "").strip().lower()
            password = body.get("password", "").strip()
            display_name = body.get("displayName", "").strip() or username

            if not username or len(username) < 3:
                return self.send_json(400, {"success": False, "error": "Tên đăng nhập tối thiểu 3 ký tự."})
            if not email or "@" not in email:
                return self.send_json(400, {"success": False, "error": "Email không hợp lệ."})
            if not password or len(password) < 6:
                return self.send_json(400, {"success": False, "error": "Mật khẩu tối thiểu 6 ký tự."})

            conn = get_db()
            cursor = conn.cursor()
            # Check unique
            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                conn.close()
                return self.send_json(409, {"success": False, "error": "Tên đăng nhập hoặc email đã tồn tại."})

            user_id = secrets.token_hex(8)
            pwd_hash, salt = hash_password(password)
            now_str = datetime.now(timezone.utc).isoformat()

            cursor.execute("""
                INSERT INTO users (id, username, email, password_hash, salt, display_name, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, username, email, pwd_hash, salt, display_name, now_str))

            # Auto create session
            token = generate_token()
            expires_at = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
            cursor.execute("""
                INSERT INTO sessions (token, user_id, created_at, expires_at)
                VALUES (?, ?, ?, ?)
            """, (token, user_id, now_str, expires_at))

            conn.commit()
            conn.close()

            user_obj = {
                "id": user_id,
                "username": username,
                "email": email,
                "displayName": display_name,
                "createdAt": now_str
            }
            return self.send_json(201, {"success": True, "token": token, "user": user_obj})

        # --- 2. LOGIN ---
        elif path == "/api/auth/login":
            login_id = body.get("login", "").strip().lower()
            password = body.get("password", "").strip()

            if not login_id or not password:
                return self.send_json(400, {"success": False, "error": "Vui lòng nhập tên đăng nhập/email và mật khẩu."})

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email, password_hash, salt, display_name, created_at
                FROM users
                WHERE username = ? OR email = ?
            """, (login_id, login_id))
            row = cursor.fetchone()

            if not row or not verify_password(password, row["password_hash"], row["salt"]):
                conn.close()
                return self.send_json(401, {"success": False, "error": "Tài khoản hoặc mật khẩu không chính xác."})

            # Create session
            token = generate_token()
            now_str = datetime.now(timezone.utc).isoformat()
            expires_at = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()

            cursor.execute("""
                INSERT INTO sessions (token, user_id, created_at, expires_at)
                VALUES (?, ?, ?, ?)
            """, (token, row["id"], now_str, expires_at))
            conn.commit()
            conn.close()

            user_obj = {
                "id": row["id"],
                "username": row["username"],
                "email": row["email"],
                "displayName": row["display_name"],
                "createdAt": row["created_at"]
            }
            return self.send_json(200, {"success": True, "token": token, "user": user_obj})

        # --- 3. LOGOUT ---
        elif path == "/api/auth/logout":
            auth_header = self.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header[7:].strip()
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
                conn.commit()
                conn.close()
            return self.send_json(200, {"success": True, "message": "Đã đăng xuất thành công."})

        # --- 4. CHANGE PASSWORD ---
        elif path == "/api/auth/change-password":
            user = get_authenticated_user(self.headers)
            if not user:
                return self.send_json(401, {"success": False, "error": "Chưa đăng nhập."})

            old_password = body.get("oldPassword", "").strip()
            new_password = body.get("newPassword", "").strip()

            if not old_password or not new_password or len(new_password) < 6:
                return self.send_json(400, {"success": False, "error": "Mật khẩu mới phải có tối thiểu 6 ký tự."})

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash, salt FROM users WHERE id = ?", (user["id"],))
            row = cursor.fetchone()
            if not row or not verify_password(old_password, row["password_hash"], row["salt"]):
                conn.close()
                return self.send_json(400, {"success": False, "error": "Mật khẩu hiện tại không đúng."})

            new_hash, new_salt = hash_password(new_password)
            cursor.execute("UPDATE users SET password_hash = ?, salt = ? WHERE id = ?", (new_hash, new_salt, user["id"]))
            conn.commit()
            conn.close()
            return self.send_json(200, {"success": True, "message": "Đổi mật khẩu thành công!"})

        # --- 5. SYNC PUSH ---
        elif path == "/api/sync/push":
            user = get_authenticated_user(self.headers)
            if not user:
                return self.send_json(401, {"success": False, "error": "Chưa đăng nhập."})

            data_obj = body.get("data")
            if not data_obj or not isinstance(data_obj, dict):
                return self.send_json(400, {"success": False, "error": "Dữ liệu thời khóa biểu không hợp lệ."})

            data_str = json.dumps(data_obj, ensure_ascii=False)
            now_str = datetime.now(timezone.utc).isoformat()

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO schedules (user_id, data_json, version, updated_at)
                VALUES (?, ?, 1, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    data_json = excluded.data_json,
                    version = schedules.version + 1,
                    updated_at = excluded.updated_at
            """, (user["id"], data_str, now_str))

            cursor.execute("SELECT version FROM schedules WHERE user_id = ?", (user["id"],))
            ver = cursor.fetchone()["version"]
            conn.commit()
            conn.close()

            return self.send_json(200, {
                "success": True,
                "version": ver,
                "updatedAt": now_str
            })

        return self.send_json(404, {"success": False, "error": "API route không tồn tại."})

def run_server(port=DEFAULT_PORT):
    init_db()
    with socketserver.TCPServer(("", port), EduMateHandler) as httpd:
        print(f"🚀 EduMate LMS 2.0 Server đang chạy tại http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã tắt server.")
            httpd.server_close()

if __name__ == "__main__":
    init_db()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    run_server(port)
