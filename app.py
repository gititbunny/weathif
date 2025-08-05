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

st.set_page_config(layout="wide", page_title="Weathif", page_icon="🌦️")
st.title("Weathif: Local Climate Storyteller")

# Geolocation input
location = st.text_input("Enter a location", "Tzaneen, South Africa")
geolocator = Nominatim(user_agent="weathif")
geo = geolocator.geocode(location)

if geo is None:
    st.error("Location not found. Please enter a valid location.")
    st.stop()

lat, lon = geo.latitude, geo.longitude

# Sidebar sliders
st.sidebar.header("🌧️ Climate Scenario Adjustments")
temp_change = st.sidebar.slider("Change in Temperature (°C)", -5.0, 5.0, 0.0)
rain_change = st.sidebar.slider("Change in Rainfall (%)", -100, 100, 0)

# Simulated current weather data
current_temp = 28.0  # example temp
current_rain = 70.0  # mm/month

# Scenario calculations
future_temp = current_temp + temp_change
future_rain = current_rain * (1 + rain_change / 100)

# Summary for export and display
summary = (
    f"Location: {location}\n"
    f"Current Avg Temp: {current_temp}°C\n"
    f"Future Avg Temp: {future_temp}°C\n"
    f"Current Avg Rainfall: {current_rain} mm/month\n"
    f"Future Avg Rainfall: {future_rain:.1f} mm/month\n"
)

# Scenario visualization
st.subheader("🌡️ Climate Scenario Impact")
df = pd.DataFrame({
    "Metric": ["Avg Temperature (°C)", "Avg Rainfall (mm/month)"],
    "Current": [current_temp, current_rain],
    "Future": [future_temp, future_rain]
})

fig, ax = plt.subplots()
bar_width = 0.35
index = range(len(df))

bar1 = ax.bar(index, df["Current"], bar_width, label="Current")
bar2 = ax.bar([i + bar_width for i in index], df["Future"], bar_width, label="Future")

ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(df["Metric"], rotation=0)
ax.legend()
ax.set_ylabel("Value")
ax.set_title("Climate Scenario Comparison")

st.pyplot(fig)

# Weather overlay map
st.subheader("🗺️ Weather Map Overlay")

overlay_url = "https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid=0af289b66a2d00d87f756b520df639df"
overlay_layers = {
    "🌧️ Rain": "precipitation_new",
    "☁️ Clouds": "clouds_new",
    "🌡️ Temperature": "temp_new",
    "🛰️ Satellite View": "satellite"
}

rain_layer = st.checkbox("Show Rain Overlay")
clouds_layer = st.checkbox("Show Cloud Overlay")
temp_layer = st.checkbox("Show Temperature Overlay")
satellite_layer = st.checkbox("Show Satellite View")

m = folium.Map(location=[lat, lon], zoom_start=7)

for name, key in overlay_layers.items():
    if (
        (name == "🌧️ Rain" and rain_layer)
        or (name == "☁️ Clouds" and clouds_layer)
        or (name == "🌡️ Temperature" and temp_layer)
        or (name == "🛰️ Satellite View" and satellite_layer)
    ):
        tile_url = overlay_url.replace("{layer}", key)
        folium.TileLayer(
            tiles=tile_url,
            attr="OpenWeatherMap",
            name=name,
            overlay=True
        ).add_to(m)

folium.Marker([lat, lon], tooltip=location).add_to(m)
folium.LayerControl().add_to(m)
st_folium(m, width=1000, height=500)

# ✅ SCENARIO REPORT DISPLAY (RESTORED)
st.subheader("📝 Scenario Report")
st.text(summary)

# Export PDF
def export_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "Climate Scenario Summary\n\n" + summary)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO()
    buffer.write(pdf_bytes)
    buffer.seek(0)
    return buffer

# Export PNG
def export_png():
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# ✅ EXPORT SECTION
st.subheader("📤 Export Scenario Report")
col1, col2 = st.columns(2)
with col1:
    st.download_button("Download PDF", data=export_pdf(), file_name="weathif_report.pdf")
with col2:
    st.download_button("Download Chart as PNG", data=export_png(), file_name="weathif_chart.png")
