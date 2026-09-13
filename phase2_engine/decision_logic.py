def choose_compressor(entropy, zero_ratio, run_length_score):
    """
    Returns one of: 'skip', 'lz4', 'zstd'
    Rules based on Phase 1 sanity-check ranges:
      - zero pages: entropy ~0, zero_ratio ~1
      - random pages: entropy ~8, zero_ratio ~0
      - text/repetitive: mid entropy, higher run_length_score
    """
    if zero_ratio > 0.9:
        return "lz4"          # near-empty page, not worth compressing
    if entropy > 7.0:
        return "lz4"           # high entropy = compression won't help much, use cheap/fast         # highly repetitive, LZ4 handles this well and fast
    return "zstd"              # moderate entropy, worth spending time for better ratio