import streamlit as st
import pandas as pd
import requests

# UI
st.set_page_config(layout="wide")
st.title("🌍 Weathif: Local Climate Storyteller")
st.markdown("Simulate real climate shifts based on live weather data.")

# Input: city (we’ll use lat/lon for now)
st.subheader("📍 Choose location and date")
city = st.selectbox("City", {
    "Johannesburg": (-26.2041, 28.0473),
    "Cape Town": (-33.9249, 18.4241),
    "Durban": (-29.8587, 31.0218)
})

start_date = st.date_input("Start date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End date", pd.to_datetime("2023-12-31"))

lat, lon = city

# Fetch real data from Open-Meteo
url = (
    f"https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}"
    f"&daily=temperature_2m_max,precipitation_sum&timezone=Africa%2FJohannesburg"
)

response = requests.get(url)
data = response.json()

# Data handling
if "daily" in data:
    df = pd.DataFrame(data["daily"])
    df["time"] = pd.to_datetime(df["time"])

    # Sliders
    temp_change = st.slider("🔺 Temperature change (%)", -50, 50, 0)
    rain_change = st.slider("💧 Rainfall change (%)", -50, 50, 0)

    df["Simulated Temp"] = df["temperature_2m_max"] * (1 + temp_change / 100)
    df["Simulated Rain"] = df["precipitation_sum"] * (1 + rain_change / 100)

    # Charts
    st.subheader("🌡️ Simulated Max Temperature")
    st.line_chart(df.set_index("time")[["Simulated Temp"]])

    st.subheader("🌧️ Simulated Rainfall")
    st.line_chart(df.set_index("time")[["Simulated Rain"]])
else:
    st.error("No data returned for selected range/location.")
