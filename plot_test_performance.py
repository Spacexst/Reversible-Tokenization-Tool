import matplotlib.pyplot as plt
import numpy as np


# RAW EXECUTION TIMES (10 runs)

raw_times = [
    1.81, 1.71, 1.68, 1.66, 1.76,
    1.63, 1.71, 1.72, 1.73, 1.70
]

runs = [f"Run {i}" for i in range(1, 11)]


# SUMMARY METRICS

average = np.mean(raw_times)
minimum = np.min(raw_times)
maximum = np.max(raw_times)
std_dev = np.std(raw_times)
variance = np.var(raw_times)

metrics = ["Average", "Minimum", "Maximum", "Std Dev", "Variance"]
values = [average, minimum, maximum, std_dev, variance]


# PLOTTING

plt.figure(figsize=(12, 10))

# ---- 1. Line Chart (Raw Times) ----
plt.subplot(2, 1, 1)
plt.plot(runs, raw_times, marker='o', linewidth=2, color="royalblue")
plt.title("Raw Execution Times Across 10 Runs")
plt.xlabel("Execution Run")
plt.ylabel("Time (seconds)")
plt.grid(True)

# ---- 2. Bar Chart (Summary Metrics) ----
plt.subplot(2, 1, 2)
plt.bar(metrics, values, color="seagreen")
plt.title("Summary Performance Metrics")
plt.ylabel("Time (seconds)")
plt.grid(axis='y')

plt.tight_layout()
plt.show()
