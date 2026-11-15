from pathlib import Path
import json
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import our dedicated prediction logic from the service layer
from service.predict_service import preprocess_and_predict

# Initialize FastAPI app
app = FastAPI(title="Plant Disease Detection API", version="1.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define paths
SERVER_DIR = Path(__file__).resolve().parent  # points to server/
MODEL_PATH = SERVER_DIR / "model" / "best_model.keras"
CLASS_JSON_PATH = SERVER_DIR / "model" / "class_names.json"

# Global variables
model = None
class_names = []

@app.on_event("startup")
def load_model_and_classes():
    global model, class_names
    print("Loading model and class names into memory...")
    
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model file not found at {MODEL_PATH}. Complete training first!")
    
    if not CLASS_JSON_PATH.exists():
        raise RuntimeError(f"Class mapping json not found at {CLASS_JSON_PATH}.")

    # Load trained model once when server boots up
    model = tf.keras.models.load_model(MODEL_PATH)
    
    # Load class name mapping list/dictionary
    with open(CLASS_JSON_PATH, "r") as f:
        class_names = json.load(f)
    
    print("Model and classes loaded successfully!")

@app.get("/")
def home():
    return {"message": "Plant Disease Detection API is running!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 1. Validate file type at the route boundary
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File uploaded is not a valid image.")
    
    try:
        # 2. Read raw bytes from the uploaded file
        image_bytes = await file.read()
        
        # 3. Pass bytes to our service function to process and predict
        result = preprocess_and_predict(image_bytes, model, class_names)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)