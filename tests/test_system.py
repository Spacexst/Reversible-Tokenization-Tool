import os
import tempfile
from pii_tokenizer import tokenize_file, detokenize_file


import db


def test_system_end_to_end():
    # Initialize DB fresh
    db.init_db()

    original_text = "John Doe has email john@example.com"

    # Create a temporary file with PII
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tmp:
        tmp.write(original_text)
        tmp_path = tmp.name

    # 1. Tokenize the file
    tokenized_path = tokenize_file(tmp_path)
    assert os.path.exists(tokenized_path)

    with open(tokenized_path, "r", encoding="utf-8") as f:
        tokenized_content = f.read()

    # Ensure original PII is not present
    assert "John Doe" not in tokenized_content
    assert "john@example.com" not in tokenized_content

    # Ensure tokens exist
    tokens = db.get_all_tokens()
    assert len(tokens) >= 2  # name + email

    # 2. Detokenize the file
    restored_path = detokenize_file(tokenized_path)
    assert os.path.exists(restored_path)

    with open(restored_path, "r", encoding="utf-8") as f:
        restored_content = f.read()

    # Ensure full round-trip restoration
    assert restored_content == original_text

    # Cleanup
    os.remove(tmp_path)
    os.remove(tokenized_path)
    os.remove(restored_path)
