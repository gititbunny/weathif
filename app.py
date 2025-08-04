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
st.markdown("Type or click a location to simulate real climate shifts using live data.")

# --- Geocoding Function ---
@st.cache_data(show_spinner=False)
def geocode_location(location_name):
    base_url = "https://nominatim.openstreetmap.org/search?"
    params = {"q": location_name, "format": "json", "limit": 1}
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

# --- Summary Generator ---
def generate_climate_summary(temp_change, rain_change, location, start, end):
    summary = f"🌍 **Climate Simulation Summary for {location}**\n\n"
    if temp_change == 0 and rain_change == 0:
        return summary + "No simulated changes were applied."
    if temp_change > 0:
        summary += f"- Temperatures increased by **{temp_change}%**, causing longer heatwaves, crop stress, and energy demand surges.\n"
    elif temp_change < 0:
        summary += f"- Temperatures decreased by **{abs(temp_change)}%**, possibly reducing heat risks but increasing cold stress.\n"
    if rain_change < 0:
        summary += f"- Rainfall dropped by **{abs(rain_change)}%**, raising drought, fire, and water scarcity risks.\n"
    elif rain_change > 0:
        summary += f"- Rainfall increased by **{rain_change}%**, which could cause flooding and erosion in vulnerable areas.\n"
    summary += f"\n📅 Time Period: **{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}**\n"
    summary += "\n⚠️ Consider local context and adaptation strategies when interpreting climate shifts."
    return summary

# --- Location Input ---
st.subheader("📍 Location Input")
location_input = st.text_input("Type a city, country, or landmark:", "Johannesburg")

typed_lat, typed_lon, display_name = geocode_location(location_input)
if not typed_lat:
    st.error("❌ Location not found. Try a different name.")
    st.stop()

st.success(f"✅ Found: {display_name}")

# --- Weather Overlay Toggles ---
st.subheader("🗺️ Weather Map (Click to change location)")
show_rain = st.checkbox("🌧️ Rain", value=True)
show_clouds = st.checkbox("☁️ Clouds", value=True)
show_temp = st.checkbox("🌡️ Temperature", value=False)
show_satellite = st.checkbox("🛰️ Satellite View", value=False)

# --- Create Map ---
map_center = [typed_lat, typed_lon]
m = folium.Map(location=map_center, zoom_start=6, tiles="OpenStreetMap")

# --- Add overlays ---
if show_rain:
    folium.TileLayer(
        f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
        attr="Rain", name="Rain", overlay=True, control=True, opacity=0.6
    ).add_to(m)

if show_clouds:
    folium.TileLayer(
        f"https://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
        attr="Clouds", name="Clouds", overlay=True, control=True, opacity=0.6
    ).add_to(m)

if show_temp:
    folium.TileLayer(
        f"https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
        attr="Temperature", name="Temperature", overlay=True, control=True, opacity=0.6
    ).add_to(m)

if show_satellite:
    folium.TileLayer(
        "http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
        attr="Satellite", name="Satellite", overlay=True, control=True
    ).add_to(m)

folium.LayerControl().add_to(m)
click_marker = folium.Marker(location=map_center, popup="Selected Location", draggable=False)
click_marker.add_to(m)

# --- Show map and get clicked location ---
map_data = st_folium(m, width=900, height=500)
clicked_coords = map_data.get("last_clicked")

if clicked_coords:
    lat, lon = clicked_coords["lat"], clicked_coords["lng"]
    display_name = f"Lat: {lat:.2f}, Lon: {lon:.2f}"
    st.info(f"📍 Map clicked at: {display_name}")
else:
    lat, lon = typed_lat, typed_lon

# --- Date Range Selection ---
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start date", pd.to_datetime("2023-01-01"))
with col2:
    end_date = st.date_input("End date", pd.to_datetime("2023-12-31"))

# --- Fetch Weather Data ---
url = (
    f"https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={lat}&longitude={lon}"
    f"&start_date={start_date}&end_date={end_date}"
    f"&daily=temperature_2m_max,precipitation_sum"
    f"&timezone=auto"
)

response = requests.get(url)
data = response.json()

# --- Simulation Charts + Summary ---
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
