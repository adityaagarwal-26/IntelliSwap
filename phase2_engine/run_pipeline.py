import csv
from pathlib import Path

from decision_logic import choose_compressor
from compress_engine import compress_page


# --------------------------------------------------
# Project paths
# --------------------------------------------------

# Project root = ~/os-project
PROJECT_ROOT = Path(__file__).resolve().parent.parent

FEATURES_FILE = PROJECT_ROOT / "phase1_data" / "features.csv"
PAGES_DIR = PROJECT_ROOT / "phase1_data" / "pages"
OUTPUT_FILE = Path(__file__).resolve().parent / "results.csv"


# --------------------------------------------------
# Validate input files
# --------------------------------------------------

if not FEATURES_FILE.exists():
    raise FileNotFoundError(
        f"Features file not found:\n{FEATURES_FILE}"
    )

if not PAGES_DIR.exists():
    raise FileNotFoundError(
        f"Pages directory not found:\n{PAGES_DIR}"
    )


# --------------------------------------------------
# Process pages
# --------------------------------------------------

rows_out = []

with open(FEATURES_FILE, "r", newline="") as f:

    reader = csv.DictReader(f)

    for row in reader:

        page_id = row["page_id"]
        page_type = row["page_type"]

        entropy = float(row["entropy"])
        zero_ratio = float(row["zero_ratio"])
        run_length_score = float(row["run_length_score"])

        # --------------------------------------------------
        # Resolve page path
        # --------------------------------------------------

        # Get only the filename from CSV.
        # Example:
        # "pages/zero_0.bin" -> "zero_0.bin"
        filename = Path(row["file_path"]).name

        file_path = PAGES_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Page file not found for {page_id}:\n{file_path}"
            )

        # --------------------------------------------------
        # Read page
        # --------------------------------------------------

        with open(file_path, "rb") as pf:
            data = pf.read()

        # Every memory page should be exactly 4096 bytes
        if len(data) != 4096:
            raise ValueError(
                f"{file_path} is {len(data)} bytes, "
                f"expected exactly 4096 bytes."
            )

        # --------------------------------------------------
        # Adaptive compression
        # --------------------------------------------------

        chosen_method = choose_compressor(
            entropy,
            zero_ratio,
            run_length_score
        )

        _, adaptive_ratio, adaptive_time = compress_page(
            data,
            chosen_method
        )

        # --------------------------------------------------
        # Baseline: Always LZ4
        # --------------------------------------------------

        _, lz4_ratio, lz4_time = compress_page(
            data,
            "lz4"
        )

        # --------------------------------------------------
        # Baseline: Always Zstd
        # --------------------------------------------------

        _, zstd_ratio, zstd_time = compress_page(
            data,
            "zstd"
        )

        # --------------------------------------------------
        # Store results
        # --------------------------------------------------

        rows_out.append({
            "page_id": page_id,
            "page_type": page_type,
            "chosen_method": chosen_method,

            "adaptive_ratio": round(adaptive_ratio, 4),
            "adaptive_time": round(adaptive_time, 6),

            "lz4_ratio": round(lz4_ratio, 4),
            "lz4_time": round(lz4_time, 6),

            "zstd_ratio": round(zstd_ratio, 4),
            "zstd_time": round(zstd_time, 6),
        })


# --------------------------------------------------
# Write results
# --------------------------------------------------

fieldnames = [
    "page_id",
    "page_type",
    "chosen_method",

    "adaptive_ratio",
    "adaptive_time",

    "lz4_ratio",
    "lz4_time",

    "zstd_ratio",
    "zstd_time",
]

with open(OUTPUT_FILE, "w", newline="") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(rows_out)


print(
    f"Done. Results for {len(rows_out)} pages "
    f"written to {OUTPUT_FILE}"
)