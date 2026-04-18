def byte_level_match_rate(original_file_path, detokenized_file_path):
    with open(original_file_path, "rb") as f1:
        original_bytes = f1.read()
    with open(detokenized_file_path, "rb") as f2:
        detok_bytes = f2.read()

    total_bytes = max(len(original_bytes), len(detok_bytes))
    if total_bytes == 0:
        return 100.0

    matching = sum(b1 == b2 for b1, b2 in zip(original_bytes, detok_bytes))
    matching -= abs(len(original_bytes) - len(detok_bytes))

    return (matching / total_bytes) * 100


original_path = "data/original.txt"
detokenized_path = "data/detokenized.txt"

match_rate = byte_level_match_rate(original_path, detokenized_path)

print(f"Byte-level match rate: {match_rate:.2f}%")

if match_rate == 100.0:
    print("H2 supported: Detokenization is perfectly reversible.")
else:
    print("H2 NOT supported: Differences found between original and detokenized text.")
