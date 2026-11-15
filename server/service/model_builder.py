
from pathlib import Path
import pandas as pd
import json
import tensorflow as tf

# Project paths
SERVICE_DIR = Path(__file__).resolve().parent          # points to server/service/
SERVER_DIR = SERVICE_DIR.parent                        # points to server/
BASE_DIR = SERVER_DIR.parent                           # points to minor_project/
CSV_PATH = BASE_DIR / 'server' / "working_dataset" / "data_splits.csv"
MODEL_DIR = BASE_DIR / "model" 
MODEL_DIR.mkdir(exist_ok=True)

# Read class names from dataset manifest
df = pd.read_csv(CSV_PATH)
class_names = sorted(df["class_name"].unique())
NUM_CLASSES = len(class_names)

# Save class mapping for future predictions
with open(MODEL_DIR / "class_names.json", "w") as f:
    json.dump(class_names, f, indent=4)

print("Number of classes:", NUM_CLASSES)

# Load pretrained MobileNetV2
base_model = tf.keras.applications.MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze pretrained backbone
base_model.trainable = False

# Build classification head
inputs = tf.keras.Input(shape=(224, 224, 3))

features = base_model(inputs, training=False)

x = tf.keras.layers.GlobalAveragePooling2D()(features)

x = tf.keras.layers.Dropout(0.2)(x)

outputs = tf.keras.layers.Dense(
    NUM_CLASSES,
    activation="softmax"
)(x)

model = tf.keras.Model(inputs, outputs)

# Compile model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Display architecture
model.summary()

print("\nMobileNetV2 model created successfully.")
print("Class mapping saved:", MODEL_DIR / "class_names.json")
