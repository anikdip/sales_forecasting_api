import pandas as pd
import streamlit as st
import joblib
from datetime import timedelta
from sklearn.preprocessing import LabelEncoder
import json
from fastapi import FastAPI
import uvicorn
import threading

# FastAPI app
app = FastAPI()

# Load the saved model
model_forecasting = joblib.load('models/linear_forecasting.pkl')
model_predictive = joblib.load('models/ramdom_predictive.pkl')
print("Model loaded successfully.")

@app.get("/")
def root():
    return {
        "message": "Welcome to the Sales Forecasting API!",
        "endpoints": {
            "/": "Project info and endpoints",
            "/health/": "API Health check",
            "/sales/national/": "7-day sales forecast (input: date)",
            "/sales/stores/items/": "Store & item sales prediction (input: date, store_id, item_id)"
        }
    }

# FastAPI endpoint: Health check
@app.get("/health/")
def health():
    return {"status": "Healthy", "message": "Welcome to the Sales Forecasting API!"}

# FastAPI endpoint: National sales forecast
@app.get("/sales/national/")
def sales_forecast(date: str):
    try:
        forecast = forecasting_predict(date)
        return json.dumps(forecast)
    except ValueError:
        return {"error": ValueError}

# FastAPI endpoint: Store and item sales prediction
@app.get("/sales/stores/items/")
def store_item_sales_forecast(date: str, store_id: int, item_id: int):
    try:
        prediction = sales_predictive(date, store_id, item_id)
        return json.dumps(prediction)
    except ValueError:
        return {"error": ValueError}


def forecasting_predict(date):
    predictions = {}
    for i in range(1, 8):
        date = pd.to_datetime(date)
        features = pd.DataFrame({
            'week_of_year': [date.isocalendar().week],
            'day_of_year': [date.dayofyear],
            'day_of_week': [date.dayofweek],
            'day': [date.day],
            'month': [date.month],
            'year': [date.year],
        })

        prediction = model_forecasting.predict(features)[0]
        predictions[date.strftime('%Y-%m-%d')] = round(prediction, 2)
        date = date + timedelta(days=i)

    return json.dumps(predictions)

def sales_predictive(date, store_id, item_id):
    date = pd.to_datetime(date)
    store_id_split = store_id.split("_")
    item_id_split = item_id.split("_")
    features = pd.DataFrame({
        'day_of_week': [date.dayofweek],
        'day': [date.day],
        'month': [date.month],
        'year': [date.year],
        'item_id': item_id,
        'dept_id': item_id_split[0]+"_"+item_id_split[1],
        'cat_id': item_id_split[0],
        'store_id': store_id,
        'state_id': store_id_split[0],
    })

    columns = ['item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
    for column in columns:
        features[column] = LabelEncoder().fit_transform(features[column])

    prediction = model_predictive.predict(features)
    return json.dumps({"prediction": prediction[0]})

# Streamlit app function
def run_streamlit_app():
    # API Endpoints
    st.title("Sales Forecasting API")

    # / endpoint
    if st.sidebar.button('API Description'):
        st.subheader("Project Objectives")
        st.write("This API provides sales forecasting for the next 7 days based on a provided date, as well as item-level sales forecasts.")

        st.subheader("Endpoints")
        st.write("""
        - **/ (GET)**: Displays project objectives and available API endpoints.
        - **/health/ (GET)**: Returns API status and a welcome message.
        - **/sales/national/ (GET)**: Returns a 7-day forecast of national sales starting from the given date.
        - **/sales/stores/items/ (GET)**: Returns predicted sales for a specific store and item on a specific date.
        """)

    # /health/ endpoint
    if st.sidebar.button('Health Check'):
        st.subheader("/health/")
        st.write("Status: 200 OK")
        st.write("Welcome to the Sales Forecasting API!")

    # /sales/national/ endpoint
    if st.sidebar.button('National Sales Forecast'):
        st.subheader("/sales/national/")
        input_date = st.date_input("Enter date (YYYY-MM-DD):")

        if input_date:
            try:
                forecast = forecasting_predict(input_date)
                st.json(forecast)
            except Exception as e:
                st.write("Error:", e)

    # /sales/stores/items/ endpoint
    if st.sidebar.button('Store-Item Sales Forecast'):
        st.subheader("/sales/stores/items/")
        input_date = st.text_input("Enter date (YYYY-MM-DD):")
        store_id = st.text_input("Enter Store ID:")
        item_id = st.text_input("Enter Item ID:")

        if input_date and store_id and item_id:
            try:
                # Dummy prediction, replace with actual model prediction
                prediction = sales_predictive(input_date, store_id, item_id)
                st.json(prediction)
            except Exception as e:
                st.write("Error:", e)

# Threading: Run both FastAPI and Streamlit at the same time
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Run FastAPI in a separate thread
    api_thread = threading.Thread(target=run_fastapi)
    api_thread.start()

    # Run the Streamlit app
    run_streamlit_app()
