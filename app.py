import streamlit as st
import pandas as pd
import requests
import urllib.parse
import folium
from streamlit_folium import st_folium

# --- CONFIG ---
API_KEY = "0af289b66a2d00d87f756b520df639df"

# --- Streamlit UI setup ---
st.set_page_config(page_title="Weathif", layout="wide")
st.title("🌍 Weathif: Local Climate Storyteller")
st.markdown("Type any location on Earth to simulate real climate shifts using live data.")

# --- Geocode user input using OpenStreetMap Nominatim ---
@st.cache_data(show_spinner=False)
def geocode_location(location_name):
    base_url = "https://nominatim.openstreetmap.org/search?"
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1
    }
    url = base_url + urllib.parse.urlencode(params)
    response = requests.get(url, headers={"User-Agent": "weathif-app"})
    results = response.json()

    if results:
        lat = float(results[0]["lat"])
        lon = float(results[0]["lon"])
        display_name = results[0]["display_name"]
        return lat, lon, display_name
    else:
        return None, None, None

# --- Generate AI-style summary ---
def generate_climate_summary(temp_change, rain_change, location, start, end):
    summary = f"🌍 **Climate Simulation Summary for {location}**\n\n"

    if temp_change == 0 and rain_change == 0:
        return summary + "No simulated changes were applied."

    if temp_change > 0:
        summary += f"- Temperatures increased by **{temp_change}%**, which could lead to longer heatwaves, crop stress, and energy demand surges.\n"
    elif temp_change < 0:
        summary += f"- Temperatures decreased by **{abs(temp_change)}%**, potentially reducing heat-related risks but increasing cold stress in some areas.\n"

    if rain_change < 0:
        summary += f"- Rainfall dropped by **{abs(rain_change)}%**, increasing chances of **droughts**, water restrictions, and wildfire risks.\n"
    elif rain_change > 0:
        summary += f"- Rainfall increased by **{rain_change}%**, which may lead to **flooding**, erosion, and disease outbreaks in vulnerable areas.\n"

    summary += f"\n📅 Time Period: **{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}**\n"
    summary += "\n⚠️ Always consider local context and adaptation strategies when interpreting climate shifts."
    return summary

# --- Location input ---
st.subheader("📍 Enter any location")
location_input = st.text_input("City, country, or landmark:", "Johannesburg")

lat, lon, display_name = geocode_location(location_input)

if not lat:
    st.error("❌ Location not found. Try a different name.")
    st.stop()

st.success(f"✅ Found: {display_name}")

# --- Map Overlay Toggles ---
st.subheader("🗺️ Live Weather Map Overlays")
show_rain = st.checkbox("🌧️ Rain", value=True)
show_clouds = st.checkbox("☁️ Clouds", value=True)
show_temp = st.checkbox("🌡️ Temperature", value=False)
show_satellite = st.checkbox("🛰️ Satellite View", value=False)

# --- Create Folium map ---
m = folium.Map(location=[lat, lon], zoom_start=6, tiles="OpenStreetMap")

# --- Overlay Layers ---
if show_rain:
    folium.TileLayer(
        tiles=f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
        attr="OpenWeatherMap Rain",
        name="Rain",
        overlay=True,
        control=True,
        opacity=0.6
    ).add_to(m)

if show_clouds:
    folium.TileLayer(
        tiles=f"https://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
        attr="OpenWeatherMap Clouds",
        name="Clouds",
        overlay=True,
        control=True,
        opacity=0.6
    ).add_to(m)

if show_temp:
    folium.TileLayer(
        tiles=f"https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
        attr="OpenWeatherMap Temp",
        name="Temperature",
        overlay=True,
        control=True,
        opacity=0.6
    ).add_to(m)

if show_satellite:
    folium.TileLayer(
        tiles="http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
        attr="Satellite",
        name="Satellite",
        overlay=True,
        control=True
    ).add_to(m)

folium.LayerControl().add_to(m)

# --- Display the map ---
st_folium(m, width=900, height=500)

# --- Date range selection ---
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start date", pd.to_datetime("2023-01-01"))
with col2:
    end_date = st.date_input("End date", pd.to_datetime("2023-12-31"))

# --- Fetch live weather data from Open-Meteo ---
url = (
    f"https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={lat}&longitude={lon}"
    f"&start_date={start_date}&end_date={end_date}"
    f"&daily=temperature_2m_max,precipitation_sum"
    f"&timezone=auto"
)

response = requests.get(url)
data = response.json()

# --- Climate simulation section ---
if "daily" in data:
    df = pd.DataFrame(data["daily"])
    df["time"] = pd.to_datetime(df["time"])

    st.subheader("🎛️ Climate Shift Simulation")
    col3, col4 = st.columns(2)
    with col3:
        temp_change = st.slider("🔺 Temperature change (%)", -50, 50, 0)
    with col4:
        rain_change = st.slider("💧 Rainfall change (%)", -50, 50, 0)

    df["Simulated Temp (°C)"] = df["temperature_2m_max"] * (1 + temp_change / 100)
    df["Simulated Rainfall (mm)"] = df["precipitation_sum"] * (1 + rain_change / 100)

    st.subheader("🌡️ Simulated Max Temperature")
    st.line_chart(df.set_index("time")[["Simulated Temp (°C)"]])

    st.subheader("🌧️ Simulated Rainfall")
    st.line_chart(df.set_index("time")[["Simulated Rainfall (mm)"]])

    st.subheader("🧠 AI-Style Climate Impact Summary")
    summary = generate_climate_summary(temp_change, rain_change, display_name, start_date, end_date)
    st.markdown(summary)
else:
    st.error("⚠️ No weather data found for this location and date range.")
