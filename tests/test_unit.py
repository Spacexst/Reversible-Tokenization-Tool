import pytest
import re
from pii_tokenizer import generate_token, detokenize_text, tokenize_text
from encryption_utils import encrypt_data, decrypt_data
from db import get_all_tokens, get_original, get_audit_logs


def test_audit_access_auditor():
    assert has_audit_access("auditor") is True


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

# Detokenization tests


def test_detokenize_text():
    text = "Name: John Doe"
    tokenized = tokenize_text(text)
    detokenized = detokenize_text(tokenized)

    assert detokenized == text

# Admin Logic (Role based access control)


def has_admin_access(role):
    return role == "admin"


def has_audit_access(role):
    return role in ("admin", "auditor")


def test_admin_access_allowed():
    assert has_admin_access("admin") is True


def test_admin_access_denies():
    assert has_admin_access("operator") is False


def test_audit_admin_access():
    assert has_audit_access("admin") is True


def test_audit_access_denied():
    assert has_audit_access("operator") is False

# Database/Admin Tools tests


def test_get_all_tokens_returns_list():
    tokens = get_all_tokens()
    assert isinstance(tokens, list)


def test_get_audit_logs_returns_list():
    logs = get_audit_logs()
    assert isinstance(logs, list)


def test_get_original_valid_token():
    tokens = get_all_tokens(mask=False)
    if not tokens:
        pytest.skip("No tokens in database")

    token, original = tokens[0]
    result = get_original(token)

    assert result == original


def test_get_original_invalid_token():
    result = get_original("INVALID_TOKEN_123")
    assert result is None


def test_audit_log_structure():
    logs = get_audit_logs()

    if not logs:
        pytest.skip("No audit logs in database")

    log = logs[0]

    # expected structure: (id, token, action, timestamp)
    assert len(log) == 4
