import csv
import matplotlib.pyplot as plt
from collections import defaultdict

with open("../phase2_engine/results.csv") as f:
    rows = list(csv.DictReader(f))

# Plot 1: overall avg ratio comparison
adaptive = sum(float(r["adaptive_ratio"]) for r in rows) / len(rows)
lz4 = sum(float(r["lz4_ratio"]) for r in rows) / len(rows)
zstd = sum(float(r["zstd_ratio"]) for r in rows) / len(rows)

plt.figure()
plt.bar(["Adaptive", "LZ4-only", "Zstd-only"], [adaptive, lz4, zstd])
plt.ylabel("Avg Compression Ratio")
plt.title("Compression Ratio: Adaptive vs Static Baselines")
plt.savefig("plots/ratio_comparison.png")
plt.close()

# Plot 2: routing breakdown by page type
type_method = defaultdict(lambda: {"lz4": 0, "zstd": 0})
for r in rows:
    type_method[r["page_type"]][r["chosen_method"]] += 1

types = list(type_method.keys())
lz4_counts = [type_method[t]["lz4"] for t in types]
zstd_counts = [type_method[t]["zstd"] for t in types]

x = range(len(types))
plt.figure()
plt.bar(x, lz4_counts, width=0.4, label="LZ4", align="center")
plt.bar([i + 0.4 for i in x], zstd_counts, width=0.4, label="Zstd", align="center")
plt.xticks([i + 0.2 for i in x], types)
plt.ylabel("Page Count")
plt.title("Routing Decision by Page Type")
plt.legend()
plt.savefig("plots/routing_by_type.png")
plt.close()

print("Plots saved to plots/")