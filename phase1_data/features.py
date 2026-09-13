import csv
import math
from collections import Counter

MANIFEST_FILE = "manifest.csv"
OUTPUT_FILE = "features.csv"

def shannon_entropy(data):
    if not data:
        return 0.0
    counts = Counter(data)
    length = len(data)
    entropy = 0.0
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy

def zero_ratio(data):
    return data.count(0) / len(data)

def run_length_score(data):
    # average length of consecutive identical bytes
    runs = []
    current_byte = data[0]
    current_len = 1
    for b in data[1:]:
        if b == current_byte:
            current_len += 1
        else:
            runs.append(current_len)
            current_byte = b
            current_len = 1
    runs.append(current_len)
    return sum(runs) / len(runs)

rows = []
with open(MANIFEST_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        page_id = row["page_id"]
        page_type = row["page_type"]
        file_path = row["file_path"]

        with open(file_path, "rb") as pf:
            data = pf.read()

        entropy = shannon_entropy(data)
        zratio = zero_ratio(data)
        rlscore = run_length_score(data)

        rows.append({
            "page_id": page_id,
            "page_type": page_type,
            "entropy": round(entropy, 4),
            "zero_ratio": round(zratio, 4),
            "run_length_score": round(rlscore, 4),
            "file_path": file_path
        })

with open(OUTPUT_FILE, "w", newline="") as f:
    fieldnames = ["page_id", "page_type", "entropy", "zero_ratio", "run_length_score", "file_path"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Features written to {OUTPUT_FILE} for {len(rows)} pages")