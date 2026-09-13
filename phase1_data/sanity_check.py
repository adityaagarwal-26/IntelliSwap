import csv
from collections import defaultdict

FEATURES_FILE = "features.csv"

stats = defaultdict(lambda: {"entropy": [], "zero_ratio": [], "run_length_score": []})

with open(FEATURES_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ptype = row["page_type"]
        stats[ptype]["entropy"].append(float(row["entropy"]))
        stats[ptype]["zero_ratio"].append(float(row["zero_ratio"]))
        stats[ptype]["run_length_score"].append(float(row["run_length_score"]))

print(f"{'Type':<12} {'Avg Entropy':<12} {'Avg ZeroRatio':<14} {'Avg RunLen':<10} {'Count'}")
for ptype, vals in stats.items():
    n = len(vals["entropy"])
    avg_e = sum(vals["entropy"]) / n
    avg_z = sum(vals["zero_ratio"]) / n
    avg_r = sum(vals["run_length_score"]) / n
    print(f"{ptype:<12} {avg_e:<12.3f} {avg_z:<14.3f} {avg_r:<10.3f} {n}")