from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import os

app = FastAPI(title="Airbnb Price Predictor (Lite)")

# --- 1. DYNAMIC MODEL LOADING ---
def load_latest_model():
    """
    Finds the most recently created .pkl file in the models directory.
    This ensures we always use the latest training run without changing code.
    """
    # Go up from 'app/' to project root, then into 'models/'
    model_dir = Path(__file__).resolve().parent.parent / "models"
    
    # Find all .pkl files
    files = list(model_dir.glob("*.pkl"))
    if not files:
        raise FileNotFoundError(f"No model files found in {model_dir}!")
    
    # Sort by creation time (newest first) and pick the top one
    latest_model_path = max(files, key=os.path.getctime)
    print(f"🚀 Loading model: {latest_model_path.name}")
    
    return joblib.load(latest_model_path)

# Load the model once when the app starts
model = load_latest_model()

# --- 2. DEFINE INPUT SCHEMA ---
# These must match the "Top 10" features selected by your simplified_model.py
class HouseInput(BaseModel):
    neighbourhood_cleansed: str
    room_type: str
    property_type: str
    bathrooms: float
    accommodates: int
    bedrooms: int
    
    # These are categorical (strings) because your data was binned 
    # (e.g., "top_reviews", "recent", etc.)
    review_scores_location: str     
    days_since_last_review: str     
    days_since_first_review: str    
    review_scores_accuracy: str     

@app.post("/predict")
def predict_price(features: HouseInput):
    # 1. Convert the user input (Pydantic object) to a Python Dictionary
    input_data = features.model_dump()
    
    # 2. Convert to DataFrame (The model expects a DataFrame)
    df = pd.DataFrame([input_data])
    
    try:
        # 3. Predict
        # The model pipeline handles scaling and one-hot encoding automatically.
        # Result is in Log Scale.
        log_prediction = model.predict(df)[0]
        
        # 4. Convert Log Scale back to Euros
        price = np.expm1(log_prediction)
        
        return {
            "predicted_price": round(float(price), 2),
            "model_used": str(model.steps[-1][1]) # Optional: verifies which model ran
        }
        
    except Exception as e:
        # Print error to terminal for debugging
        import traceback
        traceback.print_exc()
        return {"error": str(e), "message": "Prediction failed. Check terminal for details."}