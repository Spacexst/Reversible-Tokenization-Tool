# tokenizer.py
import re
import os
import uuid
import spacy

import db


# Load spaCy model (once)
nlp = spacy.load("en_core_web_sm")


# Generate token

def generate_token():
    return "TKN_" + uuid.uuid4().hex[:8]


# Tokenization Logic

def tokenize_text(text):

    db.init_db()

    # Regex patterns (non-name PII)
    patterns = [
        r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',  # email
        r'\b\d{10}\b',                                     # phone
        r'\b\d{4}-\d{4}-\d{4}-\d{4}\b',                     # credit card
        r'\$\d+(?:\.\d{2})?'                               # money
    ]

    processed = {}

    # Step 1: Regex tokenization

    for pattern in patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            if match in processed:
                token = processed[match]
            else:
                token = generate_token()
                processed[match] = token
                db.store_token(token, match)

            text = re.sub(re.escape(match), token, text)

    # Step 2: spaCy NER (Names)

    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":

            name = ent.text

            if name in processed:
                token = processed[name]
            else:
                token = generate_token()
                processed[name] = token
                db.store_token(token, name)

            # Replace full name safely
            text = text.replace(name, token)

    return text


# Tokenize file

def tokenize_file(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    tokenized_text = tokenize_text(content)

    base, ext = os.path.splitext(file_path)
    output_file = f"{base}_tokenized{ext}"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(tokenized_text)

    return output_file


# Detokenization Logic

def detokenize_text(text):

    tokens = re.findall(r'TKN_[a-f0-9]{8}', text)

    for token in tokens:
        original = db.get_original(token)

        if original:

            text = text.replace(token, original)

    return text


# Detokenize file

def detokenize_file(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    restored_text = detokenize_text(content)

    base, ext = os.path.splitext(file_path)
    output_file = f"{base}_restored{ext}"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(restored_text)

    return output_file
