import re
import spacy
import db

nlp = spacy.load("en_core_web_sm")

# Regex patterns matching your tokenizer
PII_PATTERNS = [
    r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',  # email
    r'\b\d{10}\b',                                     # phone number
    r'\b\d{4}-\d{4}-\d{4}-\d{4}\b',                    # credit card
    r'\$\d+(?:\.\d{2})?'                               # money (no commas)
]


def extract_regex_values(text):
    values = []
    for pattern in PII_PATTERNS:
        for m in re.finditer(pattern, text):
            values.append(m.group())
    return values


def extract_person_values(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ == "PERSON"]


def extract_tokens(text):
    return re.findall(r"TKN_[0-9a-fA-F]+", text)


def compute_precision_recall_f1(original_text, tokenized_text):
    # Load all tokens from DB
    token_map = {token: db.get_original(token)
                 for token in extract_tokens(tokenized_text)}

    # Ground truth PII values
    true_values = set(extract_regex_values(original_text) +
                      extract_person_values(original_text))

    # Predicted values (detokenized)
    predicted_values = set(token_map.values())

    TP = len(true_values & predicted_values)
    FP = len(predicted_values - true_values)
    FN = len(true_values - predicted_values)

    precision = TP / (TP + FP) if TP + FP > 0 else 0
    recall = TP / (TP + FN) if TP + FN > 0 else 0
    f1 = 2 * precision * recall / \
        (precision + recall) if precision + recall > 0 else 0

    return precision, recall, f1


# Load files
with open("data/original.txt", "r") as f:
    original_text = f.read()

with open("data/tokenized.txt", "r") as f:
    tokenized_text = f.read()

precision, recall, f1 = compute_precision_recall_f1(
    original_text, tokenized_text)

print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
