import os
import random

PAGE_SIZE = 4096
OUTPUT_DIR = "pages"
RAW_TEXT_DIR = "raw_sources/text"
RAW_REPEAT_DIR = "raw_sources/repetitive"
PAGES_PER_CATEGORY = 125

os.makedirs(OUTPUT_DIR, exist_ok=True)

manifest = []  # (page_id, page_type, file_path)
page_counter = 0

def save_page(data, page_type):
    global page_counter
    if len(data) < PAGE_SIZE:
        data = data + b'\x00' * (PAGE_SIZE - len(data))
    else:
        data = data[:PAGE_SIZE]
    filename = f"{page_type}_{page_counter}.bin"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(data)
    manifest.append((page_counter, page_type, filepath))
    page_counter += 1

# 1. Zero pages (with a few stray bytes for realism)
for _ in range(PAGES_PER_CATEGORY):
    data = bytearray(PAGE_SIZE)
    if random.random() < 0.3:
        idx = random.randint(0, PAGE_SIZE - 1)
        data[idx] = random.randint(1, 255)
    save_page(bytes(data), "zero")

# 2. Random pages
for _ in range(PAGES_PER_CATEGORY):
    save_page(os.urandom(PAGE_SIZE), "random")

# 3. Text-like pages (chunked from real files)
text_files = []
for root, _, files in os.walk(RAW_TEXT_DIR):
    for f in files:
        text_files.append(os.path.join(root, f))

count = 0
for path in text_files:
    if count >= PAGES_PER_CATEGORY:
        break
    try:
        with open(path, "rb") as f:
            content = f.read()
    except Exception:
        continue
    for i in range(0, len(content), PAGE_SIZE):
        if count >= PAGES_PER_CATEGORY:
            break
        chunk = content[i:i + PAGE_SIZE]
        if len(chunk) < 200:  # skip tiny leftover fragments
            continue
        save_page(chunk, "text")
        count += 1

# 4. Repetitive pages (half from real images, half synthetic patterns)
repeat_files = []
for root, _, files in os.walk(RAW_REPEAT_DIR):
    for f in files:
        repeat_files.append(os.path.join(root, f))

count = 0
half = PAGES_PER_CATEGORY // 2

for path in repeat_files:
    if count >= half:
        break
    try:
        with open(path, "rb") as f:
            content = f.read()
    except Exception:
        continue
    for i in range(0, len(content), PAGE_SIZE):
        if count >= half:
            break
        chunk = content[i:i + PAGE_SIZE]
        if len(chunk) < 200:
            continue
        save_page(chunk, "repetitive")
        count += 1

# Fill remaining repetitive pages synthetically
while count < PAGES_PER_CATEGORY:
    pattern = bytes([random.randint(0, 255)] * random.choice([1, 2, 4, 8]))
    data = (pattern * (PAGE_SIZE // len(pattern) + 1))[:PAGE_SIZE]
    save_page(data, "repetitive")
    count += 1

# Save manifest
with open("manifest.csv", "w") as f:
    f.write("page_id,page_type,file_path\n")
    for pid, ptype, fpath in manifest:
        f.write(f"{pid},{ptype},{fpath}\n")

print(f"Generated {page_counter} pages. Manifest written to manifest.csv")