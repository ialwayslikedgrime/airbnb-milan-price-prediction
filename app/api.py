from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import os

app = FastAPI(title="Airbnb Price Predictor")

# --- 1. DYNAMIC MODEL LOADING ---
# This block automatically finds the newest model in your 'models' folder
def load_latest_model():
    # Go up one level from 'app/' to root, then into 'models/'
    model_dir = Path(__file__).parent.parent / "models"
    
    # Get all .pkl files
    files = list(model_dir.glob("*.pkl"))
    if not files:
        raise FileNotFoundError("No model files found in 'models/' folder!")
    
    # Sort by modification time (newest first)
    latest_model_path = max(files, key=os.path.getctime)
    print(f"Loading model: {latest_model_path.name}")
    return joblib.load(latest_model_path)

model_pipeline = load_latest_model()

# --- 2. DEFINE INPUT (The "Top Features" only) ---
class HouseInput(BaseModel):
    accommodates: int
    bathrooms: float
    bedrooms: int
    room_type: str
    neighbourhood_cleansed: str
    # You can add more here if you want the user to control them

@app.post("/predict")
def predict_price(features: HouseInput):
    # A. Create a DataFrame with the User's Input
    input_data = {
        "accommodates": features.accommodates,
        "bathrooms": features.bathrooms,
        "bedrooms": features.bedrooms,
        "room_type": features.room_type,
        "neighbourhood_cleansed": features.neighbourhood_cleansed,
    }
    
    # B. FILL MISSING FEATURES (Crucial!)
    # Your model expects ~50 columns. We must provide them all.
    # We create a DataFrame with the same columns as the training data
    # (The pipeline knows the columns, but for safety we usually hardcode defaults)
    
    # Hack: Get feature names from the preprocessor step in the pipeline
    # Note: This varies slightly based on scikit-learn version/pipeline structure
    # For now, we will trust the pipeline to handle 'ignore' on unknown cols if robust,
    # BUT ideally, you should load a 'defaults.json' here.
    # Let's assume we fill defaults for the demo:
    
    df = pd.DataFrame([input_data])
    
    # Add missing columns with "neutral" values (e.g., 0 or mean)
    # This is a PROTOTYPE shortcut. In production, you'd calculate real defaults.
    required_cols = [
        'host_listings_count', 'beds', 'minimum_nights_avg_ntm', 'number_of_reviews', 
        'property_type', 'host_location' # ... add all 50 columns here if strictly needed
    ]
    
    for col in required_cols:
        if col not in df.columns:
            if "count" in col or "reviews" in col:
                df[col] = 1  # Default count
            elif "type" in col or "location" in col:
                df[col] = "Apartment" # Default category
            else:
                df[col] = 0

    try:
        # C. PREDICT
        log_prediction = model_pipeline.predict(df)[0]
        price = np.expm1(log_prediction) # Inverse Log
        
        return {"predicted_price": round(float(price), 2)}
    except Exception as e:
        return {"error": str(e), "message": "Model expected specific columns. Check inputs."}