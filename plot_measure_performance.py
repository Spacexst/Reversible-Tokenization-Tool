import matplotlib.pyplot as plt
import numpy as np


# RAW EXECUTION TIMES (10 runs)

tokenization_times = [
    1.1604017, 1.2090162, 1.1768601, 1.1758056, 1.1058101,
    1.0940170, 1.1324196, 1.1787680, 1.1551117, 1.1312100
]

detokenization_times = [
    0.0001814, 0.000022999, 0.00002050, 0.00002030, 0.00002110,
    0.00002080, 0.00002110, 0.00002030, 0.00002080, 0.00002050
]

runs = [f"Run {i}" for i in range(1, 11)]


# SUMMARY METRICS

metrics = ["Average", "Minimum", "Maximum", "Std Dev", "Variance"]

token_summary = [
    np.mean(tokenization_times),
    np.min(tokenization_times),
    np.max(tokenization_times),
    np.std(tokenization_times),
    np.var(tokenization_times)
]

detoken_summary = [
    np.mean(detokenization_times),
    np.min(detokenization_times),
    np.max(detokenization_times),
    np.std(detokenization_times),
    np.var(detokenization_times)
]

x = np.arange(len(metrics))
width = 0.35

# -----------------------------
# PLOTTING
# -----------------------------
plt.figure(figsize=(12, 10))

# ---- 1. Line Chart (Raw Times) ----
plt.subplot(2, 1, 1)
plt.yscale("log")  # required because detokenization is tiny
plt.plot(runs, tokenization_times, marker='o', label="Tokenization")
plt.plot(runs, detokenization_times, marker='o', label="Detokenization")
plt.title("Raw Execution Times Across 10 Runs (Log Scale)")
plt.xlabel("Execution Run")
plt.ylabel("Time (seconds, log scale)")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()

# ---- 2. Bar Chart (Summary Metrics) ----
plt.subplot(2, 1, 2)
plt.yscale("log")
plt.bar(x - width/2, token_summary, width, label="Tokenization")
plt.bar(x + width/2, detoken_summary, width, label="Detokenization")
plt.title("Summary Performance Metrics")
plt.xlabel("Metrics")
plt.ylabel("Time (seconds, log scale)")
plt.xticks(x, metrics)
plt.grid(axis='y', which="both", linestyle="--", linewidth=0.5)
plt.legend()

plt.tight_layout()
plt.show()
