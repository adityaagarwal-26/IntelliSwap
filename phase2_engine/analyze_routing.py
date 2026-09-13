import csv
from collections import Counter

with open("results.csv") as f:
    rows = list(csv.DictReader(f))

# Time comparison
avg_adaptive_time = sum(float(r["adaptive_time"]) for r in rows) / len(rows)
avg_lz4_time = sum(float(r["lz4_time"]) for r in rows) / len(rows)
avg_zstd_time = sum(float(r["zstd_time"]) for r in rows) / len(rows)

print(f"Adaptive avg time: {avg_adaptive_time:.6f}s")
print(f"LZ4-only avg time: {avg_lz4_time:.6f}s")
print(f"Zstd-only avg time: {avg_zstd_time:.6f}s")
print()

# Routing distribution
method_counts = Counter(r["chosen_method"] for r in rows)
print("Method distribution:", dict(method_counts))
print()

# Routing distribution broken down by actual page_type (ground truth)
type_method = Counter((r["page_type"], r["chosen_method"]) for r in rows)
print("page_type -> chosen_method breakdown:")
for (ptype, method), count in sorted(type_method.items()):
    print(f"  {ptype:<12} -> {method:<6} : {count}")