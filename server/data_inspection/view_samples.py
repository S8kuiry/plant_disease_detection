
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import random
import math

# Project and dataset paths for scripts inside server/data_inspection/
CURRENT_FILE = Path(__file__).resolve()
SERVER_DIR = CURRENT_FILE.parent.parent         # points to server/
BASE_DIR = SERVER_DIR.parent                    # points to minor_project/

DATASET_DIR = SERVER_DIR / "plantvillage dataset" / "color"
OUTPUT_DIR = SERVER_DIR / "dataset_reports"
OUTPUT_DIR.mkdir(exist_ok=True)

random.seed(42)

extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

class_folders = sorted(
    folder for folder in DATASET_DIR.iterdir()
    if folder.is_dir()
)

columns = 5
rows = math.ceil(len(class_folders) / columns)

fig, axes = plt.subplots(
    rows, columns,
    figsize=(18, rows * 3.2)
)

axes = axes.flatten()

for index, folder in enumerate(class_folders):
    images = [
        path for path in folder.rglob("*")
        if path.is_file()
        and path.suffix.lower() in extensions
    ]

    ax = axes[index]

    if not images:
        ax.set_title(folder.name + "\n(NO IMAGES)")
        ax.axis("off")
        continue

    selected_image = random.choice(images)

    with Image.open(selected_image) as img:
        ax.imshow(img.convert("RGB"))

    ax.set_title(folder.name, fontsize=8)
    ax.axis("off")

for index in range(len(class_folders), len(axes)):
    axes[index].axis("off")

# plt.suptitle(
#     "PlantVillage Dataset - One Sample from Each Class",
#     fontsize=16
# )

plt.tight_layout()

OUTPUT_DIR.mkdir(exist_ok=True)

plt.savefig(
    OUTPUT_DIR / "sample_images.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()

print("Sample image sheet saved successfully.")
