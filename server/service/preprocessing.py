
from pathlib import Path
import pandas as pd
import tensorflow as tf

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "working_dataset" / "data_splits.csv"

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
AUTOTUNE = tf.data.AUTOTUNE

# Load split information
df = pd.read_csv(CSV_PATH)

# Create consistent class-to-label mapping
class_names = sorted(df["class_name"].unique())
class_to_index = {
    name: index for index, name in enumerate(class_names)
}

print("Number of classes:", len(class_names))

# Data augmentation (training only)
augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.02),
    tf.keras.layers.RandomZoom(0.1)
])

# Load and preprocess one image
def load_image(image_path, label):
    image = tf.io.read_file(image_path)

    image = tf.io.decode_image(
        image,
        channels=3,
        expand_animations=False
    )

    image.set_shape([None, None, 3])

    image = tf.image.resize(image, IMG_SIZE)

    image = preprocess_input(image)

    return image, label


def create_dataset(split, training=False):

    split_df = df[df["split"] == split].copy()

    labels = [
        class_to_index[name]
        for name in split_df["class_name"]
    ]

    dataset = tf.data.Dataset.from_tensor_slices(
        (
            split_df["image_path"].values,
            labels
        )
    )

    if training:
        dataset = dataset.shuffle(
            buffer_size=5000,
            seed=42
        )

    dataset = dataset.map(
        load_image,
        num_parallel_calls=AUTOTUNE
    )

    if training:
        dataset = dataset.map(
            lambda x, y: (augmentation(x, training=True), y),
            num_parallel_calls=AUTOTUNE
        )

    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(AUTOTUNE)

    return dataset


# Create all three datasets
train_dataset = create_dataset("train", training=True)
val_dataset = create_dataset("validation")
test_dataset = create_dataset("test")

# Verify one batch
images, labels = next(iter(train_dataset))

print("\nPREPROCESSING CHECK")
print("Image batch shape:", images.shape)
print("Label batch shape:", labels.shape)
print("Pixel minimum:", tf.reduce_min(images).numpy())
print("Pixel maximum:", tf.reduce_max(images).numpy())
print("Training batches:", tf.data.experimental.cardinality(train_dataset).numpy())
print("Validation batches:", tf.data.experimental.cardinality(val_dataset).numpy())
print("Testing batches:", tf.data.experimental.cardinality(test_dataset).numpy())

print("\nPreprocessing pipeline created successfully.")
