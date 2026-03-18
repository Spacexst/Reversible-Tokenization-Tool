import re
import sqlite3
import uuid
import os
import spacy


# Load spaCy model for name detection
nlp = spacy.load("en_core_web_sm")

# Database name
DB_NAME = "tokenization.db"


# ---------------------------
# Database functions
# ---------------------------

def init_db():
    """Create database table if it does not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS token_map(
        token TEXT PRIMARY KEY,
        original_value TEXT
    )
    """)

    conn.commit()
    conn.close()


def store_token(token, value):
    """Store token-original mapping."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO token_map(token, original_value) VALUES (?, ?)",
        (token, value)
    )

    conn.commit()
    conn.close()


def get_original(token):
    """Retrieve original value for a token."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT original_value FROM token_map WHERE token=?",
        (token,)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    return None


# ---------------------------
# Token generation
# ---------------------------

def generate_token():
    """Generate a random token."""
    return "TKN_" + uuid.uuid4().hex[:8]


# ---------------------------
# Tokenization logic
# ---------------------------

def tokenize_text(text):
    """Replace PII in text with tokens."""

    # Initialize database
    init_db()

    # -----------------------
    # Regex-based detection
    # -----------------------
    patterns = [
        r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',  # Email
        r'\b\d{10,13}\b',                                  # Phone numbers
        # Credit card numbers
        r'\b(?:\d[ -]*?){13,16}\b',
        r'\$\d+(?:,\d{3})*(?:\.\d{2})?',                    # Currency amounts
        # Bank account numbers
        r'\b\d{8,12}\b'
    ]

    for pattern in patterns:
        matches = set(re.findall(pattern, text))

        for match in matches:
            token = generate_token()
            store_token(token, match)
            text = text.replace(match, token)

    # -----------------------
    # spaCy Name Detection
    # -----------------------
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text

            token = generate_token()
            store_token(token, name)

            text = text.replace(name, token)

    return text


# ---------------------------
# File tokenization
# ---------------------------

def tokenize_file(file_path):
    """Tokenize a file and create a tokenized version."""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            content = f.read()

    tokenized_text = tokenize_text(content)

    base, ext = os.path.splitext(file_path)
    output_file = f"{base}_tokenized{ext}"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(tokenized_text)

    return output_file


# ---------------------------
# Detokenization
# ---------------------------


def detokenize_text(text):
    """Replace tokens with original values."""

    tokens = re.findall(r'TKN_[a-f0-9]{8}', text)

    for token in tokens:
        original = get_original(token)

        if original:
            text = text.replace(token, original)

    return text


def detokenize_file(file_path):
    """Restore original data from tokenized file."""

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    restored_text = detokenize_text(content)

    base, ext = os.path.splitext(file_path)
    output_file = f"{base}_restored{ext}"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(restored_text)

    return output_file


nlp = spacy.load("en_core_web_sm")


def tokenize_text(text):
    init_db()

    # Collect all matches first
    all_matches = []

    # Regex matches
    patterns = [
        r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',  # Emails
        r'\b\d{10,13}\b',                                   # Phone numbers
        r'\b(?:\d[ -]*?){13,16}\b',                         # Credit cards
        r'\$\d+(?:,\d{3})*(?:\.\d{2})?',                    # Currency
        r'\b\d{8,12}\b'                                     # Bank accounts
    ]
    for pattern in patterns:
        all_matches.extend(re.findall(pattern, text))

    # spaCy names
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            all_matches.append(ent.text)

    # Replace **unique matches only**, longest first
    for match in sorted(set(all_matches), key=len, reverse=True):
        token = generate_token()
        store_token(token, match)
        text = text.replace(match, token)

    return text
