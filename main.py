import streamlit as st
import requests

st.set_page_config(page_title="Fire Dataset Input", layout="centered")

st.title("🔥 Fire Dataset Input Form")

# Numeric inputs
temperature = st.number_input("Temperature (°C)", min_value=-50.0, max_value=60.0, step=0.1)
rh = st.number_input("Relative Humidity (%)", min_value=0, max_value=100, step=1)
ws = st.number_input("Wind Speed (km/h)", min_value=0.0, max_value=200.0, step=0.1)
rain = st.number_input("Rain (mm)", min_value=0.0, step=0.1)
ffmc = st.number_input("FFMC", min_value=0.0, step=0.1)
dmc = st.number_input("DMC", min_value=0.0, step=0.1)
isi = st.number_input("ISI", min_value=0.0, step=0.1)

# Category inputs
classes = st.selectbox("Classes", options=["fire", "not fire"])
region = st.selectbox("Region", options=["Bejaia", "Sidi-Bel Abbes"])

# Submit button
if st.button("Send to FastAPI"):
    # Prepare JSON
    st.success("🚀 Sending data to FastAPI...")

    payload = {
        "Temperature": temperature,
        "RH": rh,
        "Ws": ws,
        "Rain": rain,
        "FFMC": ffmc,
        "DMC": dmc,
        "ISI": isi,
        "Classes": 0 if classes == "not fire" else 1,
        "Region": 0 if region == "Bejaia" else 1,
    }


    # Send POST request to FastAPI
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)

        if response.status_code == 200:
            st.success("✅ Response from FastAPI:")
            result = response.json()
            fwi = result["FWI"]

            # --- Output Section ---
            st.header("📊 Prediction Result")

            # Show FWI as a metric card
            st.metric(label="🔥 Fire Weather Index", value=fwi)
        else:
            st.error(f"❌ Error: {response.status_code}")
    except Exception as e:
        st.error(f"⚠️ Could not connect to FastAPI: {e}")

