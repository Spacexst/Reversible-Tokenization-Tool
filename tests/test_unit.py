import pytest
import re
from pii_tokenizer import generate_token, detokenize_text, tokenize_text
from encryption_utils import encrypt_data, decrypt_data

# Token generation


# def test_generate_token_format():
#     token = generate_token()

#     assert token.startswith("TKN_")
#     assert len(token) == 12  # e.g., TKN_ + 8 hex chars


def test_generate_token_format():
    token = generate_token()

    # Basic checks
    assert token.startswith("TKN_")
    assert len(token) == 12  # TKN_ + 8 hex chars

    # Stronger format validation
    import re
    assert re.fullmatch(r"TKN_[0-9A-Fa-f]{8}", token)


def test_generate_token_uniqueness():
    token1 = generate_token()
    token2 = generate_token()

    assert token1 != token2


def test_generate_token_empty_input():
    token = generate_token()

    assert token.startswith("TKN_")

# Encryption/Decryption


def test_encrypt_decrypt():
    original = "Sensitive Data 123"
    encrypted = encrypt_data(original)
    decrypted = decrypt_data(encrypted)

    assert decrypted == original


def test_encrypt_non_ascii():
    original = "こんにちは世界"
    encrypted = encrypt_data(original)
    decrypted = decrypt_data(encrypted)

    assert decrypted == original


def test_detokenize_text():
    text = "Name: John Doe"
    tokenized = tokenize_text(text)
    detokenized = detokenize_text(tokenized)

    assert detokenized == text
