You need two terminal windows to run this (one for the engine, one for the dashboard).

Terminal 1 (The API):

cd airbnb_milan
source .venv/bin/activate
uvicorn app.api:app --reload

Wait until you see "Application startup complete".

cd airbnb_milan
source .venv/bin/activate
streamlit run app/frontend.py

Your browser will open, and you will see your fully functioning prototype running on your local machine, powered by the model you just trained and saved!