import io
import numpy as np
from PIL import Image
import tensorflow as tf

def preprocess_and_predict(image_bytes: bytes, model: tf.keras.Model, class_names) -> dict:
    """
    Takes raw image bytes, preprocesses them to match MobileNetV2 training specifications,
    runs model inference, and returns the predicted class name and confidence score.
    """
    # 1. Open image from bytes and ensure it's in RGB format
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # 2. Resize to 224x224 (matching MobileNetV2 training input size)
    image = image.resize((224, 224))
    
    # 3. Convert image to numpy array and scale pixels (-1 to 1)
    # Note: This matches the exact preprocessing scaling used during your training pipeline
    img_array = np.array(image, dtype=np.float32)
    img_array = (img_array / 127.5) - 1.0  
    
    # 4. Expand dimensions to create a batch of 1: shape becomes (1, 224, 224, 3)
    # Why? Models are built to accept batches of images, even if we are only sending 1.
    img_array = np.expand_dims(img_array, axis=0) 
    
    # 5. Run inference (Model prediction)
    predictions = model.predict(img_array)
    
    # 6. Extract the winning class index and confidence score
    predicted_index = int(np.argmax(predictions[0]))
    confidence = float(np.max(predictions[0]))
    
    # 7. Map index to the human-readable plant disease name
    if isinstance(class_names, dict):
        predicted_class = class_names.get(str(predicted_index), "Unknown")
    else:
        predicted_class = class_names[predicted_index]
        
    return {
        "class": predicted_class,
        "confidence": round(confidence * 100, 2)
    }