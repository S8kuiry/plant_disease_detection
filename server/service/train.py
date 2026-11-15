
from pathlib import Path
import sys
import tensorflow as tf

# Project paths
# Get the exact directories sorted out
SERVICE_DIR = Path(__file__).resolve().parent          # points to server/service/
SERVER_DIR = SERVICE_DIR.parent                        # points to server/
BASE_DIR = SERVER_DIR.parent                           # points to minor_project/

# Since all service files are in the same folder, import them directly using relative imports!
from preprocessing import train_dataset, val_dataset
from model_builder import model

# Where your saved model weights and JSON files will go:
MODEL_DIR = SERVER_DIR / "model"                       # points to server/model/
MODEL_DIR.mkdir(exist_ok=True)

# Callbacks
callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        MODEL_DIR / "best_model.keras",
        monitor="val_accuracy",
        save_best_only=True,
        mode="max",
        verbose=1
    ),

    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True,
        verbose=1
    ),

    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=2,
        min_lr=1e-6,
        verbose=1
    )
]

# Train
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=10,
    callbacks=callbacks
)

# Save final model
model.save(MODEL_DIR / "final_model.keras")

print("\nTraining completed.")
