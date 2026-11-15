
from pathlib import Path
from collections import Counter
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

# 1. Dataset location
# 1. Correct Path Resolution
# __file__ is server/data_inspection/inspect_dataset.py
CURRENT_FILE = Path(__file__).resolve()
DATA_INSPECTION_DIR = CURRENT_FILE.parent       # points to server/data_inspection/
SERVER_DIR = DATA_INSPECTION_DIR.parent         # points to server/
BASE_DIR = SERVER_DIR.parent                    # points to minor_project/

# Point directly to plantvillage dataset inside the server folder
DATASET_DIR = SERVER_DIR / "plantvillage dataset" / "color"

# Report output folder inside server
REPORT_DIR = SERVER_DIR / "dataset_reports"
REPORT_DIR.mkdir(exist_ok=True)

# Supported image extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

if not DATASET_DIR.exists():
    raise FileNotFoundError(f"Dataset folder not found: {DATASET_DIR}")

# 3. Get class folders
class_folders = sorted(
    folder for folder in DATASET_DIR.iterdir()
    if folder.is_dir()
)

metadata = []
class_counts = {}
corrupted_images = []
all_formats = Counter()
all_dimensions = Counter()
all_modes = Counter()
total_size_bytes = 0

print("Starting dataset inspection...\n")

# 4. Inspect each class
for class_folder in class_folders:
    class_name = class_folder.name
    image_files = sorted(
        file for file in class_folder.rglob("*")
        if file.is_file()
        and file.suffix.lower() in IMAGE_EXTENSIONS
    )

    class_counts[class_name] = 0

    for image_path in image_files:
        try:
            # Verify that the image is readable
            with Image.open(image_path) as img:
                img.verify()

            # Reopen to collect image properties
            with Image.open(image_path) as img:
                width, height = img.size
                image_format = img.format
                image_mode = img.mode

            file_size = image_path.stat().st_size
            total_size_bytes += file_size

            class_counts[class_name] += 1
            all_formats[image_format] += 1
            all_dimensions[f"{width}x{height}"] += 1
            all_modes[image_mode] += 1

            metadata.append({
                "class": class_name,
                "filename": image_path.name,
                "width": width,
                "height": height,
                "format": image_format,
                "mode": image_mode,
                "file_size_kb": round(file_size / 1024, 2),
                "file_path": str(image_path)
            })

        except Exception as error:
            corrupted_images.append({
                "class": class_name,
                "filename": image_path.name,
                "error": str(error)
            })

# 5. Calculate dataset statistics
total_images = sum(class_counts.values())
total_classes = len(class_folders)
average_images = (
    total_images / total_classes if total_classes else 0
)

# 6. Save image-level metadata
metadata_df = pd.DataFrame(metadata)
metadata_df.to_csv(
    REPORT_DIR / "image_metadata.csv", index=False
)

# 7. Save class distribution
class_df = pd.DataFrame([
    {"class": name, "image_count": count}
    for name, count in class_counts.items()
]).sort_values("image_count", ascending=False)

class_df.to_csv(
    REPORT_DIR / "class_distribution.csv", index=False
)

# 8. Save corrupted image report
pd.DataFrame(corrupted_images).to_csv(
    REPORT_DIR / "corrupted_images.csv", index=False
)

# 9. Generate class distribution graph
if not class_df.empty:
    plt.figure(figsize=(14, max(8, total_classes * 0.3)))
    plt.barh(class_df["class"], class_df["image_count"])
    plt.xlabel("Number of Images")
    plt.ylabel("Disease Class")
    plt.title("PlantVillage Color Dataset - Class Distribution")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(
        REPORT_DIR / "class_distribution.png",
        dpi=200
    )
    plt.close()

# 10. Generate text report
report = f"""
PLANTVILLAGE DATASET INSPECTION REPORT

Dataset path: {DATASET_DIR}

TOTAL CLASSES: {total_classes}
TOTAL VALID IMAGES: {total_images}
CORRUPTED / UNREADABLE IMAGES: {len(corrupted_images)}
AVERAGE IMAGES PER CLASS: {average_images:.2f}
TOTAL IMAGE SIZE: {total_size_bytes / (1024**3):.3f} GB

IMAGE FORMATS:
{dict(all_formats)}

IMAGE COLOR MODES:
{dict(all_modes)}

IMAGE DIMENSIONS:
{dict(all_dimensions)}

CLASS COUNTS:
{class_counts}
"""

(REPORT_DIR / "inspection_report.txt").write_text(
    report, encoding="utf-8"
)

# 11. Print summary
print("=" * 55)
print("DATASET INSPECTION COMPLETED")
print("=" * 55)
print(f"Total classes: {total_classes}")
print(f"Total valid images: {total_images}")
print(f"Corrupted images: {len(corrupted_images)}")
print(f"Average images per class: {average_images:.2f}")
print(f"Total size: {total_size_bytes / (1024**3):.3f} GB")

print("\nImage formats:", dict(all_formats))
print("Image modes:", dict(all_modes))
print("Image dimensions:", dict(all_dimensions))

print("\nClass-wise image counts:")
print(class_df.to_string(index=False))

print(f"\nReports saved in: {REPORT_DIR}")
