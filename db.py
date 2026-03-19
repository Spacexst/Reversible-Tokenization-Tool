# db.py
import sqlite3
from encryption_utils import encrypt_data, decrypt_data

DB_FILE = "token_map.db"


# -----------------------------
# Database Initialization
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            token TEXT PRIMARY KEY,
            value BLOB
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Store token + encrypted value
# -----------------------------
def store_token(token, original_value):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    encrypted_value = encrypt_data(original_value)

    cursor.execute(
        "INSERT OR REPLACE INTO tokens (token, value) VALUES (?, ?)",
        (token, encrypted_value)
    )

    conn.commit()
    conn.close()


# -----------------------------
# Retrieve original value
# -----------------------------
def get_original(token):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM tokens WHERE token=?", (token,))
    result = cursor.fetchone()

    conn.close()

    if result:
        encrypted_value = result[0]
        return decrypt_data(encrypted_value)

    return None


# -----------------------------
# (Optional) Get all tokens (for GUI)
# -----------------------------
def get_all_tokens():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT token, value FROM tokens")
    rows = cursor.fetchall()

    conn.close()

    # decrypt values before returning
    return [(t, decrypt_data(v)) for t, v in rows]
