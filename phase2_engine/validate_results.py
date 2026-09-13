import csv

with open("results.csv") as f:
    rows = list(csv.DictReader(f))

avg_adaptive = sum(float(r["adaptive_ratio"]) for r in rows) / len(rows)
avg_lz4 = sum(float(r["lz4_ratio"]) for r in rows) / len(rows)
avg_zstd = sum(float(r["zstd_ratio"]) for r in rows) / len(rows)

print(f"Adaptive avg ratio: {avg_adaptive:.3f}")
print(f"LZ4-only avg ratio: {avg_lz4:.3f}")
print(f"Zstd-only avg ratio: {avg_zstd:.3f}")

avg_adaptive_time = sum(float(r["adaptive_time"]) for r in rows) / len(rows)
avg_lz4_time = sum(float(r["lz4_time"]) for r in rows) / len(rows)
avg_zstd_time = sum(float(r["zstd_time"]) for r in rows) / len(rows)

print(f"Adaptive avg time: {avg_adaptive_time:.6f}s")
print(f"LZ4-only avg time: {avg_lz4_time:.6f}s")
print(f"Zstd-only avg time: {avg_zstd_time:.6f}s")