import csv
from collections import defaultdict

with open("../phase2_engine/results.csv") as f:
    rows = list(csv.DictReader(f))

# ---- Overall averages ----
def avg(key):
    return sum(float(r[key]) for r in rows) / len(rows)

overall_stats = {
    "adaptive_ratio": avg("adaptive_ratio"),
    "lz4_ratio": avg("lz4_ratio"),
    "zstd_ratio": avg("zstd_ratio"),
    "adaptive_time": avg("adaptive_time"),
    "lz4_time": avg("lz4_time"),
    "zstd_time": avg("zstd_time"),
}

# ---- Per-page-type averages (adaptive only) ----
type_groups = defaultdict(list)
for r in rows:
    type_groups[r["page_type"]].append(r)

per_type_stats = {}
for ptype, group in type_groups.items():
    per_type_stats[ptype] = {
        "count": len(group),
        "avg_adaptive_ratio": sum(float(r["adaptive_ratio"]) for r in group) / len(group),
        "avg_lz4_ratio": sum(float(r["lz4_ratio"]) for r in group) / len(group),
        "avg_zstd_ratio": sum(float(r["zstd_ratio"]) for r in group) / len(group),
    }

# ---- Method distribution ----
method_counts = defaultdict(int)
for r in rows:
    method_counts[r["chosen_method"]] += 1

# ---- Write summary to CSV (for easy pasting into paper tables) ----
with open("summary_stats.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Metric", "Value"])
    for k, v in overall_stats.items():
        writer.writerow([k, round(v, 4)])
    writer.writerow([])
    writer.writerow(["page_type", "count", "avg_adaptive_ratio", "avg_lz4_ratio", "avg_zstd_ratio"])
    for ptype, stats in per_type_stats.items():
        writer.writerow([ptype, stats["count"], round(stats["avg_adaptive_ratio"], 4),
                          round(stats["avg_lz4_ratio"], 4), round(stats["avg_zstd_ratio"], 4)])
    writer.writerow([])
    writer.writerow(["chosen_method", "count"])
    for method, count in method_counts.items():
        writer.writerow([method, count])

# ---- Also print to console ----
print("=== Overall Averages ===")
for k, v in overall_stats.items():
    print(f"{k}: {v:.4f}")

print("\n=== Per-Page-Type Averages ===")
for ptype, stats in per_type_stats.items():
    print(f"{ptype}: {stats}")

print("\n=== Method Distribution ===")
for method, count in method_counts.items():
    print(f"{method}: {count}")

print("\nSummary written to summary_stats.csv")