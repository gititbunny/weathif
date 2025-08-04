import streamlit as st
import pandas as pd
import requests

# --- Streamlit setup ---
st.set_page_config(page_title="Weathif", layout="wide")
st.title("🌍 Weathif: Local Climate Storyteller")
st.markdown("Simulate real climate shifts in any major South African city.")

# --- City coordinates ---
cities = {
    "Johannesburg": (-26.2041, 28.0473),
    "Cape Town": (-33.9249, 18.4241),
    "Durban": (-29.8587, 31.0218)
}

selected_city = st.selectbox("📍 Choose a city", list(cities.keys()))
lat, lon = cities[selected_city]

# --- Date range ---
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start date", pd.to_datetime("2023-01-01"))
with col2:
    end_date = st.date_input("End date", pd.to_datetime("2023-12-31"))

# --- Fetch real weather data ---
url = (
    f"https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={lat}&longitude={lon}"
    f"&start_date={start_date}&end_date={end_date}"
    f"&daily=temperature_2m_max,precipitation_sum"
    f"&timezone=Africa%2FJohannesburg"
)

response = requests.get(url)
data = response.json()

# --- Process data ---
if "daily" in data:
    df = pd.DataFrame(data["daily"])
    df["time"] = pd.to_datetime(df["time"])

    # --- Sliders for simulation ---
    st.subheader("🎛️ Simulate Climate Change")
    col3, col4 = st.columns(2)
    with col3:
        temp_change = st.slider("🔺 Temperature change (%)", -50, 50, 0)
    with col4:
        rain_change = st.slider("💧 Rainfall change (%)", -50, 50, 0)

    # --- Apply simulation ---
    df["Simulated Temp (°C)"] = df["temperature_2m_max"] * (1 + temp_change / 100)
    df["Simulated Rainfall (mm)"] = df["precipitation_sum"] * (1 + rain_change / 100)

    # --- Charts ---
    st.subheader("🌡️ Simulated Max Temperature")
    st.line_chart(df.set_index("time")[["Simulated Temp (°C)"]])

    st.subheader("🌧️ Simulated Rainfall")
    st.line_chart(df.set_index("time")[["Simulated Rainfall (mm)"]])
else:
    st.error("⚠️ No data found for the selected city and date range.")
