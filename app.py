import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Weathif", layout="wide")
st.title("🌍 Weathif: Local Climate Storyteller")
st.markdown("Simulate temperature and rainfall changes in your city.")

# Dummy data for now
dates = pd.date_range(start="2023-01-01", end="2023-12-31")
temps = [25 + (i % 30) * 0.1 for i in range(len(dates))]
rain = [2 + (i % 7) * 0.5 for i in range(len(dates))]

df = pd.DataFrame({
    "Date": dates,
    "Temperature (°C)": temps,
    "Rainfall (mm)": rain
})

# Sliders for simulation
temp_change = st.slider("🔺 Temperature change (%)", -50, 50, 0)
rain_change = st.slider("💧 Rainfall change (%)", -50, 50, 0)

# Apply changes
df["Temperature (°C)"] *= (1 + temp_change / 100)
df["Rainfall (mm)"] *= (1 + rain_change / 100)

# Charts
st.subheader("📈 Simulated Temperature Over Time")
st.line_chart(df[["Date", "Temperature (°C)"]].set_index("Date"))

st.subheader("🌧️ Simulated Rainfall Over Time")
st.line_chart(df[["Date", "Rainfall (mm)"]].set_index("Date"))
