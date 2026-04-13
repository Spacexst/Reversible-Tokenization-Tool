import time
from pii_tokenizer import tokenize_text, detokenize_text

TEXT = "John Doe lives in London and works at Microsoft." * 1000


def measure(fn, label):
    times = []
    for _ in range(10):
        start = time.perf_counter()
        fn(TEXT)
        end = time.perf_counter()
        times.append(end - start)
    print(f"{label} times:", times)
    return times


if __name__ == "__main__":
    token_times = measure(tokenize_text, "Tokenization")
    detoken_times = measure(detokenize_text, "Detokenization")

    print("\nTokenization avg:", sum(token_times)/len(token_times))
    print("Detokenization avg:", sum(detoken_times)/len(detoken_times))
