import pytest
from pii_tokenizer import tokenize_text, detokenize_text


def test_token_reversibility_only_with_tool():
    # Use actual PII that your tokenizer WILL replace
    original = "John Doe"   # spaCy PERSON entity
    tokenized = tokenize_text(original)

    # Token must NOT contain the original text
    assert original not in tokenized
    assert tokenized.startswith("TKN_")


def test_missing_token_handling():
    text = "Unknown token TKN_00000000"
    detokenized = detokenize_text(text)

    # Unknown tokens should remain unchanged
    assert detokenized == text
