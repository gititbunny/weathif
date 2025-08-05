import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from fpdf import FPDF
from io import BytesIO

# Page setup
st.set_page_config(layout="wide", page_title="Weathif", page_icon="🌦️")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@300;600;900&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Nunito Sans', sans-serif;
        background-color: #EBEEDF;
    }
    .card {
        background: linear-gradient(135deg, #A4C4E7, #EB8316);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        color: #000;
    }
    .title-card {
        background: linear-gradient(135deg, #C3A970, #EB8316);
        padding: 1rem 2rem;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .stButton > button {
        background-color: #A4C4E7 !important;
        color: black;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-card"><h1 style="margin:0;">Weathif: Local Climate Storyteller 🌦️</h1></div>', unsafe_allow_html=True)

location = st.text_input("📍 Enter a location", "Tzaneen, South Africa")
geolocator = Nominatim(user_agent="weathif")
geo = geolocator.geocode(location)

if geo is None:
    st.error("Location not found. Please enter a valid location.")
    st.stop()

lat, lon = geo.latitude, geo.longitude

st.sidebar.header("🌧️ Climate Scenario Adjustments")
temp_change = st.sidebar.slider("Change in Temperature (°C)", -5.0, 5.0, 0.0)
rain_change = st.sidebar.slider("Change in Rainfall (%)", -100, 100, 0)

current_temp = 28.0
current_rain = 70.0
future_temp = current_temp + temp_change
future_rain = current_rain * (1 + rain_change / 100)

summary = (
    f"Location: {location}\n"
    f"Current Avg Temp: {current_temp}°C\n"
    f"Future Avg Temp: {future_temp}°C\n"
    f"Current Avg Rainfall: {current_rain} mm/month\n"
    f"Future Avg Rainfall: {future_rain:.1f} mm/month\n"
)

st.subheader("🌡️ Climate Scenario Impact")
df = pd.DataFrame({
    "Metric": ["Avg Temperature (°C)", "Avg Rainfall (mm/month)"],
    "Current": [current_temp, current_rain],
    "Future": [future_temp, future_rain]
})

fig, ax = plt.subplots()
bar_width = 0.35
index = range(len(df))
bars_current = ax.bar(index, df["Current"], bar_width, label="Current", color="#A4C4E7")
bars_future = ax.bar([i + bar_width for i in index], df["Future"], bar_width, label="Future", color="#EB8316")

ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(df["Metric"], rotation=0)
ax.legend()
ax.set_ylabel("Value")
ax.set_title("Climate Scenario Comparison")
fig.tight_layout()
st.pyplot(fig)

# Weather Overlay
st.subheader("🗺️ Weather Map Overlay")
st.markdown('<div class="card">', unsafe_allow_html=True)

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
st.markdown('</div>', unsafe_allow_html=True)

# Scenario Report
st.subheader("📝 Scenario Report")
st.text(summary)

# Environmental Impact Section
st.subheader("🌍 Projected Impact & Environmental Consequences")
implications = ""
if future_temp >= 35:
    implications += "- 🔥 High risk of heatwaves, crop failures, and wildfires.\n"
elif future_temp >= 32:
    implications += "- 🌡️ Rising temperature may cause heat stress and alter local ecosystems.\n"
if future_rain < 30:
    implications += "- 💧 Severe drought risk, low water availability, reduced agricultural productivity.\n"
elif future_rain > 100:
    implications += "- 🌊 Increased flood risk, potential for water-logging and disease spread.\n"
if implications == "":
    implications = "- ✔ Conditions likely remain stable with minimal severe impacts."

st.info(implications)

# PDF Export
def export_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title (short, no symbols or emojis)
    pdf.set_text_color(59, 59, 59)
    pdf.cell(0, 10, txt="Weathif Report", ln=True, align="L")
    pdf.ln(10)

    # Climate details (short lines, no special chars)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, f"Location: {location}")
    pdf.multi_cell(0, 10, f"Current Temp: {current_temp} C")
    pdf.multi_cell(0, 10, f"Future Temp: {future_temp:.1f} C")
    pdf.multi_cell(0, 10, f"Current Rain: {current_rain} mm")
    pdf.multi_cell(0, 10, f"Future Rain: {future_rain:.1f} mm")
    pdf.ln(5)

    # Implications header
    pdf.set_font("Arial", style='B', size=11)
    pdf.cell(0, 10, "Environmental Effects:", ln=True)

    # Remove emojis/symbols from implications
    clean_implications = implications.replace("🔥", "").replace("🌡️", "").replace("💧", "").replace("🌊", "").replace("✅", "").replace("-", "").strip().split("\n")

    pdf.set_font("Arial", size=10)
    for line in clean_implications:
        if line.strip():
            pdf.multi_cell(0, 8, f"- {line.strip()}")

    return pdf.output(dest="S").encode("latin1")


def export_png():
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Export Options
st.subheader("📤 Export Scenario Report")
col1, col2 = st.columns(2)
with col1:
    st.download_button("Download PDF", data=export_pdf(), file_name="weathif_report.pdf")
with col2:
    st.download_button("Download Chart as PNG", data=export_png(), file_name="weathif_chart.png")
