# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

# 1. Load the trained Pipeline
# This contains the ColumnTransformer, SelectKBest, and XGBoost
model_pipeline = joblib.load('airbnb_xgboost_pipeline.pkl')

app = FastAPI(title="Airbnb Price Predictor")

# 2. Define Input Schema 
# MUST match the columns in your X_train exactly (order doesn't matter, names do)
class HouseFeatures(BaseModel):
    # Numeric Features
    accommodates: int
    bathrooms: float
    bedrooms: int
    beds: int
    minimum_nights_avg_ntm: float
    maximum_nights_avg_ntm: float
    number_of_reviews: int
    
    # Categorical Features (strings)
    neighbourhood_cleansed: str
    property_type: str
    room_type: str
    
    # Add all other inputs your model needs here...
    # For the prototype, ensure you cover the required fields used by the model

@app.post("/predict")
def predict_price(features: HouseFeatures):
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([features.model_dump()])
        
        # 3. Predict (Result is in Log Scale)
        log_prediction = model_pipeline.predict(input_df)[0]
        
        # 4. Inverse Log Transform to get Real Price
        real_price = np.expm1(log_prediction)
        
        return {
            "predicted_log_price": float(log_prediction),
            "predicted_price_usd": float(real_price)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))