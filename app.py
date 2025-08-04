import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from fpdf import FPDF
from io import BytesIO
from PIL import Image
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="Weathif", layout="wide")
st.title("🌦️ Weathif: Local Climate Storyteller")
st.markdown("Simulate temperature and rainfall changes in your city.")

# --- SESSION STATE ---
if "location" not in st.session_state:
    st.session_state["location"] = "Johannesburg"
    st.session_state["lat"] = -26.2041
    st.session_state["lon"] = 28.0473

# --- WEATHER MAP WITH OVERLAYS ---
st.subheader("🗺️ Weather Map (Click to change location)")
rain_layer = st.checkbox("🌧️ Rain", value=True)
clouds_layer = st.checkbox("☁️ Clouds")
temp_layer = st.checkbox("🌡️ Temperature")
satellite_layer = st.checkbox("🛰️ Satellite View")

m = folium.Map(location=[st.session_state["lat"], st.session_state["lon"]], zoom_start=6)
overlay_url = "https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid=0af289b66a2d00d87f756b520df639df"
layers = {
    "🌧️ Rain": "precipitation_new",
    "☁️ Clouds": "clouds_new",
    "🌡️ Temperature": "temp_new",
    "🛰️ Satellite View": "sat"
}

for name, key in layers.items():
    if ((name == "🌧️ Rain" and rain_layer) or
        (name == "☁️ Clouds" and clouds_layer) or
        (name == "🌡️ Temperature" and temp_layer) or
        (name == "🛰️ Satellite View" and satellite_layer)):
        folium.TileLayer(
            tiles=overlay_url.format(layer=key),
            attr="OpenWeatherMap",
            name=name,
            overlay=True,
            control=True,
        ).add_to(m)

# 📍 Marker for selected location
fg = folium.FeatureGroup(name="Selected Location")
folium.Marker(
    [st.session_state["lat"], st.session_state["lon"]],
    tooltip="📍 Selected Location",
).add_to(fg)
fg.add_to(m)

map_data = st_folium(m, width=700, height=450)

# Update location from map click
if map_data.get("last_clicked"):
    click_location = map_data["last_clicked"]
    lat, lon = click_location["lat"], click_location["lon"]
    st.session_state["lat"] = lat
    st.session_state["lon"] = lon
    geolocator = Nominatim(user_agent="weathif-app")
    try:
        location = geolocator.reverse((lat, lon), language="en", exactly_one=True)
        address = location.raw.get("address", {})
        city_name = (
            address.get("city") or address.get("town") or address.get("village")
            or address.get("state") or "Unknown"
        )
    except:
        city_name = "Unknown"
    st.session_state["location"] = city_name

st.info(f"📍 Selected Location: **{st.session_state['location']}** ({st.session_state['lat']:.2f}, {st.session_state['lon']:.2f})")

# --- CLIMATE SLIDERS ---
st.subheader("🔧 Adjust Climate Variables")

temp_change = st.slider("🌡️ Temperature Change (°C)", -5.0, 5.0, 0.0, step=0.1)
rain_change = st.slider("🌧️ Rainfall Change (%)", -50, 50, 0, step=1)

# --- DUMMY DATA (OR HOOK TO API LATER) ---
dates = pd.date_range(start="2023-01-01", end="2023-12-31")
temps = [25 + (i % 30) * 0.1 for i in range(len(dates))]
rain = [2 + (i % 7) * 0.5 for i in range(len(dates))]

df = pd.DataFrame({
    "Date": dates,
    "Temperature (°C)": [t + temp_change for t in temps],
    "Rainfall (mm)": [r * (1 + rain_change / 100) for r in rain]
})

# --- CHARTS ---
st.subheader("📊 Climate Forecast")
fig, ax = plt.subplots()
df.set_index("Date")[["Temperature (°C)", "Rainfall (mm)"]].plot(ax=ax)
st.pyplot(fig)

# --- AI-STYLE SUMMARY ---
st.subheader("🧠 AI-Generated Climate Impact Summary")

summary = f"""
In {st.session_state['location']}, a temperature change of **{temp_change:+.1f}°C** and a rainfall shift of **{rain_change:+}%**
could significantly alter seasonal weather patterns.

- 📈 Expect warmer days and higher evaporation rates.
- 🌾 Agriculture might need adaptation for resilient crops.
- 💧 Water demand could increase while rainfall becomes unpredictable.
- 🔥 Heatwaves and drought risk may rise during summer months.

These shifts can affect public health, ecosystems, and infrastructure — cities must prepare for more climate extremes.
"""

st.markdown(summary)

# --- EXPORT SECTION ---
st.subheader("📥 Export Your Scenario")

# Export to PDF
def export_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Weathif Climate Simulation", ln=True, align="C")
    pdf.ln()
    pdf.multi_cell(0, 10, summary)
    buf = BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf

# Export to PNG
def export_png():
    fig, ax = plt.subplots()
    df.set_index("Date")[["Temperature (°C)", "Rainfall (mm)"]].plot(ax=ax)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

col1, col2 = st.columns(2)
with col1:
    if st.download_button("📄 Download PDF", data=export_pdf(), file_name="weathif_summary.pdf"):
        st.success("PDF downloaded!")
with col2:
    if st.download_button("🖼️ Download Chart as PNG", data=export_png(), file_name="weathif_chart.png"):
        st.success("PNG downloaded!")
