import lz4.frame
import zstandard as zstd
import time

zstd_compressor = zstd.ZstdCompressor()

def compress_page(data, method):
    start = time.perf_counter()

    if method == "lz4":
        compressed = lz4.frame.compress(data)
    elif method == "zstd":
        compressed = zstd_compressor.compress(data)
    elif method == "skip":
        compressed = data  # kept for completeness; not used by current decision logic
    else:
        raise ValueError(f"Unknown method: {method}")

    elapsed = time.perf_counter() - start
    ratio = len(data) / len(compressed) if len(compressed) > 0 else 1.0
    return compressed, ratio, elapsed