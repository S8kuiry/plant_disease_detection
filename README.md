# Plant Disease Detection

A React + FastAPI app that diagnoses plant leaf diseases using a MobileNetV2 deep‑learning model (38 classes). The pre‑trained model is bundled, so you can run it **without any dataset**.

---

## 1. Folder Structure

```text
minor_project/
├── client/                       # React + Vite frontend (UI + upload + result)
│   ├── src/
│   │   ├── components/           # ImageUpload, ResultCard, Navbar
│   │   ├── services/api.js       # Axios call to /predict
│   │   ├── pages/Home.jsx        # Main page
│   │   └── ...
│   ├── index.html
│   ├── package.json
│   └── .env                      # VITE_API_BASE_URL=http://localhost:8000
│
├── server/                       # FastAPI backend
│   ├── main.py                   # FastAPI app; /predict endpoint; loads model at startup
│   ├── requirements.txt          # Python deps: fastapi, uvicorn, tensorflow, etc.
│   ├── service/
│   │   ├── train.py              # Retrains the model on your dataset
│   │   ├── model_builder.py      # MobileNetV2 model definition
│   │   ├── preprocessing.py      # Dataset loading + augmentation
│   │   └── predict_service.py    # Inference on a single image
│   ├── model/                    # BUNDLED — pre-trained model (no training needed)
│   │   ├── best_model.keras
│   │   ├── final_model.keras
│   │   └── class_names.json      # 38 class → index mapping
│   └── venv/                     # Python virtual environment (git-ignored)
│
└── README.md
```

---

## 2. Quick Start — Run the App (No Dataset Required)

### Step 1 — Clone and enter
```bash
git clone <your-repo-url>
cd minor_project
```

### Step 2 — Start the Backend (FastAPI)
```bash
cd server
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Check: open `http://localhost:8000/` → you should see `Plant Disease Detection API is running!`

### Step 3 — Start the Frontend (React)
```bash
cd ../client
npm install
npm run dev
```
Open `http://localhost:5173`.

### Step 4 — Use it
Upload a leaf image → click **Detect Disease** → the app returns the predicted disease + confidence.

> Frontend assumes backend is at `http://localhost:8000`. If you change the port, update
> `client/.env` (`VITE_API_BASE_URL`).

---

## 3. Training with Your Own Dataset/Model

> Run these in order from the `server/` directory. The bundled model in `model/`
> already predicts out-of-the-box, so this section is only needed if you want to
> retrain or fine-tune.

### Step 1 — Place your dataset
Put your PlantVillage-style dataset (each class in its own subfolder) at:
`server/plantvillage dataset/color/`

### Step 2 — (Optional) Inspect & clean
```bash
# Inspect dataset stats (classes, image sizes, corrupted files)
python data_inspection/inspect_dataset.py

# Check for duplicate images
python data_inspection/check_duplicates.py
```

### Step 3 — Split into train / val / test
```bash
python data_inspection/split_dataset.py
```
This reads all class folders, then writes `working_dataset/data_splits.csv`
(creating `working_dataset/` if needed) with columns: `image_path`, `class_name`, `split`.

### Step 4 — Train the model
```bash
python service/train.py
```
This internally:
- Runs `preprocessing.py` to load + augment the split datasets
- Runs `model_builder.py` to build the MobileNetV2 model + write `class_names.json`
- Trains and saves `model/best_model.keras` and `model/final_model.keras`

### Step 5 — Restart the backend
Stop and restart the backend (`uvicorn main:app`). It auto-loads the new
`best_model.keras` and `class_names.json`.

> **Files in order of execution:** `data_inspection/split_dataset.py` → `service/train.py`
> (which calls `preprocessing.py` and `model_builder.py`).

---

## 4. API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/predict` | Upload an image (`file` field, `image/png` or `image/jpeg`) → returns `{"class": "...", "confidence": XX.XX}`. |

Example:
```bash
curl -X POST http://localhost:8000/predict -F "file=@leaf.jpg"
```

---

## 5. Quick Troubleshooting

| Problem | Fix |
|---------|-----|
| Frontend: "Failed to connect to prediction server" | Backend must be running on `http://localhost:8000`. |
| `ModuleNotFoundError` on fastapi/tensorflow | Run `pip install -r server/requirements.txt` in the active venv. |
| "Model file not found" on startup | Run training (`service/train.py`) first. |
| Port in use (8000/5173) | Stop the other process, or use another port. |
