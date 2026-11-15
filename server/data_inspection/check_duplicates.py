
from pathlib import Path
from collections import defaultdict
from PIL import Image
import hashlib

DATASET = Path(__file__).resolve().parent / "plantvillage dataset" / "color"

hashes = defaultdict(list)

for path in DATASET.rglob("*"):
    if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        continue

    try:
        with Image.open(path) as img:
            digest = hashlib.sha256(img.convert("RGB").tobytes()).hexdigest()
        hashes[digest].append(str(path))
    except Exception:
        continue

duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}

print("Unique image groups:", len(hashes))
print("Duplicate groups:", len(duplicates))
print("Total images involved in duplicates:",
      sum(len(paths) for paths in duplicates.values()))

with open("duplicate_report.txt", "w") as f:
    for paths in duplicates.values():
        f.write("\n".join(paths) + "\n\n")

print("Report saved: duplicate_report.txt")
