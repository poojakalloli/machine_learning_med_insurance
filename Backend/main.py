from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

app = FastAPI(title="Insurance ML Backend")

# Build path relative to the project directory
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "insurance_model.pkl"

pipeline = joblib.load(MODEL_PATH)

# Define request body validation
class PatientSchema(BaseModel):
    age: int
    sex: str
    bmi: float
    children: int
    smoker: str
    region: str

@app.get("/")
def health_check():
    return {"status": "Backend running successfully!"}

@app.post("/predict")
def predict_charges(patient: PatientSchema):
    # Convert incoming API payload to DataFrame using modern Pydantic v2 syntax
    input_df = pd.DataFrame([patient.model_dump()])
    
    # Predict log values and transform back to original scale
    log_pred = pipeline.predict(input_df)[0]
    usd_pred = np.expm1(log_pred)
    inr_pred = usd_pred * 83.0  # Conversion rate: 1 USD ≈ 83.0 INR
    
    return {
        "status": "success",
        "predicted_inr": round(float(inr_pred), 2),
        "predicted_usd": round(float(usd_pred), 2)
    }