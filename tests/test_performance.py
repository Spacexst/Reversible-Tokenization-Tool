import pytest
import time
from pii_tokenizer import tokenize_text, detokenize_text


def test_large_text_performance():
    large_text = "SensitiveData " * 10000

    start = time.time()
    tokenized = tokenize_text(large_text)
    token_time = time.time() - start

    start = time.time()
    detokenized = detokenize_text(tokenized)
    detoken_time = time.time() - start

    # Verify correctness
    assert detokenized == large_text
    # Optional: print performance metrics
    print(f"Tokenization time: {token_time:.2f}s")
    print(f"Detokenization time: {detoken_time:.2f}s")
