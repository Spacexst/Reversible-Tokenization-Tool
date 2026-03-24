# db.py
import sqlite3
from encryption_utils import encrypt_data, decrypt_data
from audit_logger import log_action

DB_FILE = "token_map.db"


# Get DB Connection (with FK enabled)

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Database Initialization
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Token storage table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            token TEXT PRIMARY KEY,
            value BLOB NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Audit log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (token) REFERENCES tokens(token)
        )
    """)

    # Index for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_token ON tokens(token)")

    conn.commit()
    conn.close()


# Store token + encrypted value

def store_token(token, original_value):
    conn = get_connection()
    cursor = conn.cursor()

    encrypted_value = encrypt_data(original_value)

    cursor.execute(
        "INSERT OR REPLACE INTO tokens (token, value) VALUES (?, ?)",
        (token, encrypted_value)
    )

    # Audit log in DB
    cursor.execute(
        "INSERT INTO audit_log (token, action) VALUES (?, ?)",
        (token, "TOKENIZE")
    )

    conn.commit()
    conn.close()

    # Also log to file/console
    log_action(token, "TOKENIZE")


# Retrieve original value

def get_original(token):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM tokens WHERE token=?", (token,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return None

    encrypted_value = result[0]
    original_value = decrypt_data(encrypted_value)

    # Audit log in DB
    cursor.execute(
        "INSERT INTO audit_log (token, action) VALUES (?, ?)",
        (token, "DETOKENIZE")
    )
    conn.commit()
    conn.close()

    # Also log to file/console
    log_action(token, "DETOKENIZE")

    return original_value


# Mask data (for safe display)


def mask_data(data):
    data = str(data)
    if len(data) <= 4:
        return "****"
    return data[:2] + "****" + data[-2:]


# Get all tokens (with optional masking)

def get_all_tokens(mask=True):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT token, value FROM tokens")
    rows = cursor.fetchall()

    conn.close()

    results = []
    for token, value in rows:
        original = decrypt_data(value)
        if mask:
            original = mask_data(original)
        results.append((token, original))

    return results


# Get audit logs

def get_audit_logs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, token, action, timestamp
        FROM audit_log
        ORDER BY timestamp DESC
    """)

    logs = cursor.fetchall()
    conn.close()

    return logs
