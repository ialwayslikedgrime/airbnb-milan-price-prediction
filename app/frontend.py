import streamlit as st
import requests

st.title("🏡 Airbnb Milan Price Estimator")

# --- INPUTS (Must match the 10 features in api.py) ---
col1, col2 = st.columns(2)

with col1:
    neighbourhood = st.selectbox("Neighbourhood", ["Duomo", "Navigli", "Brera", "Isola", "Buenos Aires", "Porta Romana"]) 
    room_type = st.selectbox("Room Type", ["Entire home/apt", "Private room", "Shared room"])
    property_type = st.selectbox("Property Type", ["Entire rental unit", "Entire condo", "Private room in rental unit", "Entire loft"])
    bathrooms = st.number_input("Bathrooms", 1.0, 5.0, 1.0)
    accommodates = st.slider("Accommodates (Guests)", 1, 16, 2)

with col2:
    bedrooms = st.number_input("Bedrooms", 1, 10, 1)
    
    # Categorical Reviews 
    review_options = ["top_reviews", "high_reviews", "medium_reviews", "low_reviews", "no_reviews"]
    days_first_options = ["no_review_yet", "new (<= 6 months)", "established (<= 1 year)", "mature (<= 3 years)", "veteran (<= 5 years)", "legacy (over 5 years)"]
    days_last_options = ["no_review", "very_recent (<= 1 week)", "recent (<= 1 month)", "old (<= 6 months)", "very_old (<= 1 year)"]

    score_loc = st.selectbox("Location Review Score", review_options)
    score_acc = st.selectbox("Accuracy Review Score", review_options)
    days_last = st.selectbox("Last Review Recency", days_last_options)
    days_first = st.selectbox("Host Since / First Review", days_first_options)

if st.button("Calculate Price"):
    # This payload MUST have 10 items
    payload = {
        "neighbourhood_cleansed": neighbourhood,
        "room_type": room_type,
        "property_type": property_type,
        "bathrooms": bathrooms,
        "accommodates": accommodates,
        "bedrooms": bedrooms,
        "review_scores_location": score_loc,
        "days_since_last_review": days_last,
        "days_since_first_review": days_first,
        "review_scores_accuracy": score_acc
    }
    
    try:
        # Ensure port matches your running uvicorn (usually 8000)
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if response.status_code == 200:
            st.success(f"Prediction: €{response.json().get('predicted_price', 'Error')}")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Connection Error: {e}")