
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

# Project and dataset paths for scripts inside server/data_inspection/
CURRENT_FILE = Path(__file__).resolve()
SERVER_DIR = CURRENT_FILE.parent.parent         # points to server/
BASE_DIR = SERVER_DIR.parent                    # points to minor_project/

DATASET_DIR = SERVER_DIR / "plantvillage dataset" / "color"
OUTPUT_DIR = SERVER_DIR / "working_dataset"

extensions = {".jpg", ".jpeg", ".png"}

# Collect image paths and class labels
records = []

for class_folder in sorted(DATASET_DIR.iterdir()):
    if not class_folder.is_dir():
        continue

    for image_path in class_folder.rglob("*"):
        if image_path.suffix.lower() in extensions:
            records.append({
                "image_path": str(image_path.resolve()),
                "class_name": class_folder.name
            })

df = pd.DataFrame(records)

# First split: 70% training, 30% temporary
train_df, temp_df = train_test_split(
    df,
    test_size=0.30,
    stratify=df["class_name"],
    random_state=42
)

# Second split: 15% validation, 15% testing
val_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    stratify=temp_df["class_name"],
    random_state=42
)

train_df = train_df.copy()
val_df = val_df.copy()
test_df = test_df.copy()

train_df["split"] = "train"
val_df["split"] = "validation"
test_df["split"] = "test"

# Combine and save
final_df = pd.concat(
    [train_df, val_df, test_df],
    ignore_index=True
)

OUTPUT_DIR.mkdir(exist_ok=True)

final_df.to_csv(
    OUTPUT_DIR / "data_splits.csv",
    index=False
)

# Print summary
print("DATASET SPLIT COMPLETED")
print("-----------------------")
print("Total images:", len(final_df))
print("Training:", len(train_df))
print("Validation:", len(val_df))
print("Testing:", len(test_df))
print("Classes:", df["class_name"].nunique())

print("\nClass distribution by split:")
print(pd.crosstab(final_df["class_name"], final_df["split"]))

print("\nSaved: data_inspection/data_splits.csv")
