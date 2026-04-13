import os
import filecmp
import pytest
import db
from pii_tokenizer import tokenize_file, detokenize_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_FILE = os.path.normpath(os.path.join(
    BASE_DIR, "..", "sample_data", "test_file.txt"
))

# 🔥 This runs BEFORE every test automatically


@pytest.fixture(autouse=True)
def reset_db():
    db.init_db()


@pytest.fixture
def token_file():
    return tokenize_file(SAMPLE_FILE)


@pytest.fixture
def detoken_file(token_file):
    return detokenize_file(token_file)


def test_tokenization_creates_output(token_file):
    assert os.path.exists(token_file)


def test_tokenized_output_is_not_original(token_file):
    assert not filecmp.cmp(SAMPLE_FILE, token_file, shallow=False)


def test_detokenization_creates_output(detoken_file):
    assert os.path.exists(detoken_file)


def test_detokenized_output_matches_original(detoken_file):
    assert filecmp.cmp(SAMPLE_FILE, detoken_file, shallow=False)
