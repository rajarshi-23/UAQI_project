import streamlit as st
import pickle
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd

# Load the trained model
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

# Function to classify AQI
def classify_aqi(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    else:
        return "Severe"

st.title("AQI Prediction App")

# Add a session state to freeze inputs after prediction
if 'predicted' not in st.session_state:
    st.session_state['predicted'] = False

# Disable input if prediction already done
disabled = st.session_state['predicted']

# User Inputs
with st.form("input_form"):
    st.subheader("Enter Pollution Levels:")
    PM25 = st.number_input("PM2.5 (µg/m³)", value=0.0, disabled=disabled)
    PM10 = st.number_input("PM10 (µg/m³)", value=0.0, disabled=disabled)
    NO = st.number_input("NO (µg/m³)", value=0.0, disabled=disabled)
    NO2 = st.number_input("NO2 (µg/m³)", value=0.0, disabled=disabled)
    NOx = st.number_input("NOx (µg/m³)", value=0.0, disabled=disabled)
    NH3 = st.number_input("NH3 (µg/m³)", value=0.0, disabled=disabled)
    CO = st.number_input("CO (mg/m³)", value=0.0, disabled=disabled)
    SO2 = st.number_input("SO2 (µg/m³)", value=0.0, disabled=disabled)
    O3 = st.number_input("O3 (µg/m³)", value=0.0, disabled=disabled)
    Benzene = st.number_input("Benzene (µg/m³)", value=0.0, disabled=disabled)
    Toluene = st.number_input("Toluene (µg/m³)", value=0.0, disabled=disabled)
    Xylene = st.number_input("Xylene (µg/m³)", value=0.0, disabled=disabled)

    submitted = st.form_submit_button("Predict AQI")

if submitted and not st.session_state['predicted']:
    input_data = pd.DataFrame([{
        'PM2.5': PM25,
        'PM10': PM10,
        'NO': NO,
        'NO2': NO2,
        'NOx': NOx,
        'NH3': NH3,
        'CO': CO,
        'SO2': SO2,
        'O3': O3,
        'Benzene': Benzene,
        'Toluene': Toluene,
        'Xylene': Xylene
    }])

    prediction = model.predict(input_data)[0]
    aqi_class = classify_aqi(prediction)

    st.success(f"Predicted AQI: {prediction:.2f}")
    st.info(f"AQI Category: {aqi_class}")

    # Freeze input after prediction
    st.session_state['predicted'] = True

# Add refresh button
if st.session_state['predicted']:
    if st.button("Predict Again (Refresh)"):
        st.session_state['predicted'] = False
        st.rerun()
