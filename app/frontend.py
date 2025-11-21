import streamlit as st
import requests

st.set_page_config(page_title="Airbnb ROI Calculator", page_icon="🏠")

st.title("🏡 Airbnb Value Estimator")
st.markdown("### Is your property a hidden gem?")

# --- 1. INPUTS ---
col1, col2 = st.columns(2)

with col1:
    accommodates = st.slider("Accommodates", 1, 16, 4)
    bedrooms = st.number_input("Bedrooms", 1, 10, 1)
    bathrooms = st.number_input("Bathrooms", 1.0, 5.0, 1.0)

with col2:
    room_type = st.selectbox("Room Type", ["Entire home/apt", "Private room", "Shared room"])
    neighbourhood = st.selectbox("Neighbourhood", ["Duomo", "Navigli", "Brera", "Isola"]) # Add your real ones

# --- 2. ACTION ---
if st.button("💰 Calculate Price & ROI", type="primary"):
    # Prepare data for API
    payload = {
        "accommodates": accommodates,
        "bathrooms": bathrooms,
        "bedrooms": bedrooms,
        "room_type": room_type,
        "neighbourhood_cleansed": neighbourhood
    }
    
    try:
        # Call the local API
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if "predicted_price" in result:
                price = result['predicted_price']
                
                # --- 3. DISPLAY RESULT & ROI LOGIC ---
                st.success(f"### Predicted Nightly Rate: €{price}")
                
                # Simple ROI Logic (The logic you wanted to build!)
                occupancy_rate = 0.70 # Assume 70% occupancy
                monthly_revenue = price * 30 * occupancy_rate
                
                st.metric(label="Est. Monthly Revenue (70% Occ.)", value=f"€{monthly_revenue:,.2f}")
                
                st.info("📉 Next Step: Compare this with the selling price to see if you should SELL or RENT.")
            else:
                st.error(f"Error: {result}")
        else:
            st.error("Failed to connect to the prediction engine.")
            
    except Exception as e:
        st.error(f"Connection Error: Is the API running? \n{e}")