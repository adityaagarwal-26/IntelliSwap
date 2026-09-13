# Phase 1 - Dataset & Feature Extraction

## Page format
- Page size: 4096 bytes (matches standard OS page size)
- Total pages: 500 (125 per category)
- Categories: zero, random, text, repetitive

## Files
- `pages/` — raw 4KB page files, named `{type}_{id}.bin`
- `manifest.csv` — page_id, page_type, file_path (intermediate)
- `features.csv` — final output: page_id, page_type, entropy, zero_ratio, run_length_score, file_path
- `generate_pages.py` — generates pages/manifest from raw_sources/
- `features.py` — computes features from manifest, writes features.csv
- `sanity_check.py` — verifies feature averages per category

## Feature definitions
- **entropy**: Shannon entropy over byte distribution (0–8)
- **zero_ratio**: fraction of bytes equal to 0 (0–1)
- **run_length_score**: average length of consecutive identical bytes

## Sanity check results
Type         Avg Entropy  Avg ZeroRatio  Avg RunLen Count
zero         0.001        1.000          3331.413   125
random       7.955        0.004          1.004      125
text         5.119        0.037          1.300      125
repetitive   3.563        0.001          2064.927   125

## Sources
- Text pages: chunked from torvalds/linux and psf/requests repos
- Random pages: os.urandom()
- Zero pages: generated, 30% chance of 1 stray non-zero byte
- Repetitive pages: half from uncompressed BMP/PPM images, half synthetic repeating patterns