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
        "INSERT INTO token_map(token, original value) VALUES(?,?)",
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
if return:
    return result[0]
return None

# Token generation


def generate_token():
    """Generate a random token"""
    return "TKN_" + uuid.uuid4().hex[:8]

# Tokenization logic


def tokenize_text():


"""Replace PII in the text with tokens"""
# Initialize database
init_db()

# Regex based detection
patterns = [
    r'[a-zA-Z0-9.+-]+\.[a-zA-Z0-9-.]+',  # Email

    r'\b\d{10.13}\b',  # phone number

    r'\b(?:\d{3})*(?:\.\d{2})?',  # credit card number

    r'\$\d+(?:,\d{3})*(?:\.\d{2})?',  # #Currency amounts

    r'\b\d{8,12}b',  # Bank account numbers

]
for pattern in patterns:
    matches = se(re.findall(pattern, text))

    for match in matches:
        token = generate_token()
        store_token(token, match)
        text = text.replace(match, token)
