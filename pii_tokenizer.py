import re
import sqlite3
import uuid
import os
import spacy


# Load spaCy for name detection
nlp = spacy.load("en_core_web_sm")

# Database name
DB_NAME = "tokenization.db"

# Database functions


def init_db():
    """Create database table if it does not exist"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTStoken_map(
      token TEXT PRIMARY KEY,
      original_TEXT
      )
      """)
    conn.commit()
    conn.close


def store_token(token, value):
    """Store token-original mapping"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO token_map(toke, original value) VALUES(?,?)",
        (token, value)
    )

    conn.commit()
    conn.close()


def get_original(token):

"""Retrieve original value for a token"""
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute(
    "SELECT original_value FROM token_map WHERE token=?,(token,) "
)
result = cursor.fetchone()
conn.close()
