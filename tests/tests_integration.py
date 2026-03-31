import os
import filecmp
from pii_tokenizer import tokenize_file, detokenize_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_FILE = os.path.normpath(os.path.join(
    BASE_DIR, "..", "sample_data", "test_file.txt"))


def test_file_tokenization_and_detokenization():
    token_file = tokenize_file(SAMPLE_FILE)
    assert os.path.exists(token_file)

    assert not filecmp.cmp(SAMPLE_FILE, token_file, shallow=False)

    detoken_file = detokenize_file(token_file)
    assert os.path.exists(detoken_file)

    assert filecmp.cmp(SAMPLE_FILE, detoken_file, shallow=False)
