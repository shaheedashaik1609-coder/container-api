import joblib
import pandas as pd
from fastapi import APIRouter, Depends

from app.schemas import DwellRequest
from app.security import verify_key

from pathlib import Path

router = APIRouter(prefix="/predict", tags=["prediction"], dependencies=[Depends(verify_key)])
#Load once at startup, not on every request
MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "dwell_model.pkl"
model = joblib.load(MODEL_PATH)


FEATURES = ["weight_kg", "is_40ft", "arrival_hour", "day_of_week"]

@router.post("/dwell_time")
def predict_dwell(request: DwellRequest):
    input_data = pd.DataFrame([request.model_dump()])[FEATURES]
    prediction = float(model.predict(input_data)[0])
    return {"predicted_dwell_days" : round(prediction,1), "model_version": "rf-v1"}


