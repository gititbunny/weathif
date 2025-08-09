import os
import json
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# ----------------------- Config & Styles -----------------------
st.set_page_config(layout="wide", page_title="Weathif", page_icon="assets/icon.png")

PALETTE = {
    "alabaster": "#D2E1F9",
    "powder": "#A4C4E7",
    "persimmon": "#EB8316",
    "lion": "#C3A970",
    "obsidian": "#000000",
}
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@300;600;900&display=swap');
html, body, [class*="css"]  {{
  font-family: 'Nunito Sans', sans-serif;
  background: {PALETTE["alabaster"]} !important;
}}
.card {{
  background: linear-gradient(135deg, {PALETTE["powder"]}, {PALETTE["persimmon"]}20);
  padding: 1.25rem; border-radius: 20px;
  box-shadow: 0 4px 18px rgba(0,0,0,.08); color:{PALETTE["obsidian"]};
}}
.title-card {{
  background: linear-gradient(135deg, {PALETTE["lion"]}, {PALETTE["persimmon"]});
  padding: 1rem 1.25rem; border-radius: 16px; margin-bottom: 18px; color:white;
}}
.stButton > button {{
  background:{PALETTE["powder"]} !important; color: {PALETTE["obsidian"]};
  border-radius: 10px; border:0; padding:.6rem 1rem;
}}
</style>
""", unsafe_allow_html=True)


from pathlib import Path
import base64

def img_to_b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()

logo_b64 = img_to_b64(Path(__file__).parent / "assets" / "logo.png")

st.markdown(
    f"""
    <div style="text-align:center; margin-bottom:20px;">
        <img src="data:image/png;base64,{logo_b64}" width="200">
    </div>
    """,
    unsafe_allow_html=True
)



st.markdown('<div class="title-card"><h1 style="margin:0;">Weathif: Local Climate Storyteller 🌦️</h1></div>', unsafe_allow_html=True)

# ----------------------- Secrets & Globals -----------------------
OWM_KEY = st.secrets.get("OWM_API_KEY", os.environ.get("OWM_API_KEY", "").strip())
TILE_URL_TMPL = "https://tile.openweathermap.org/map/{layer}/{{z}}/{{x}}/{{y}}.png?appid=" + OWM_KEY if OWM_KEY else ""

OVERLAY_LAYERS = {
    "🌧️ Rain": "precipitation_new",
    "☁️ Clouds": "clouds_new",
    "🌡️ Temperature": "temp_new",
    "🛰️ Satellite View": "satellite",
}

# ----------------------- Geocoding -----------------------
@st.cache_resource(show_spinner=False)
def _geocoder():
    g = Nominatim(user_agent="weathif")
    # throttle to be nice to Nominatim
    g.geocode = RateLimiter(g.geocode, min_delay_seconds=1)
    g.reverse = RateLimiter(g.reverse, min_delay_seconds=1)
    return g

@st.cache_data(show_spinner=False, ttl=24*3600)
def geocode_place(q: str):
    g = _geocoder()
    loc = g.geocode(q, addressdetails=True, timeout=10)
    if not loc:
        return None
    return {"name": q, "lat": loc.latitude, "lon": loc.longitude}

@st.cache_data(show_spinner=False, ttl=24*3600)
def reverse_geocode(lat: float, lon: float):
    g = _geocoder()
    loc = g.reverse((lat, lon), language="en", timeout=10, zoom=12)
    return loc.address if loc else f"{lat:.4f}, {lon:.4f}"

# ----------------------- Live Weather -----------------------
def fetch_current_weather(lat: float, lon: float):
    """
    Returns (temp_c, rain_mm_hr) with graceful fallback if API key missing.
    """
    if not OWM_KEY:
        return 28.0, 0.0
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        r = requests.get(url, params={"lat": lat, "lon": lon, "appid": OWM_KEY, "units": "metric"}, timeout=10)
        r.raise_for_status()
        data = r.json()
        temp_c = data.get("main", {}).get("temp", 28.0)
        # OWM puts last-hour rain at rain["1h"]
        rain_1h = data.get("rain", {}).get("1h", 0.0)
        # Convert to a simple monthly proxy (rough illustrative): mm/month ~ 30 * 24 * (rain mm per hour when raining fraction)
        # Scale a bit so charts aren’t flat;.
        monthly_guess = min(200.0, rain_1h * 30)  # cap for display sanity
        return float(temp_c), float(monthly_guess)
    except Exception:
        return 28.0, 70.0

# ----------------------- UI: Location -----------------------
colL, colR = st.columns([2,1], vertical_alignment="center")
with colL:
    q = st.text_input("📍 Enter a location", "Tzaneen, South Africa")
with colR:
    use_click = st.toggle("Enable map click-to-update", value=True)

loc = geocode_place(q)
if not loc:
    st.error("Location not found. Please try another place.")
    st.stop()

if "loc" not in st.session_state:
    st.session_state.loc = loc
else:
    # update name but keep any click-updated coordinates if user edited the text field significantly
    st.session_state.loc.update({"name": q})

lat, lon = st.session_state.loc["lat"], st.session_state.loc["lon"]
place_name = st.session_state.loc.get("name", q)

# ----------------------- Sidebar: Scenario -----------------------
st.sidebar.header("🌧️ Climate Scenario Adjustments")
temp_change = st.sidebar.slider("Change in Temperature (°C)", -5.0, 5.0, 0.0, step=0.5)
rain_change = st.sidebar.slider("Change in Rainfall (%)", -100, 100, 0, step=5)

# Live current (fallback-safe)
current_temp, current_rain = fetch_current_weather(lat, lon)
future_temp = current_temp + temp_change
future_rain = max(0.0, current_rain * (1 + rain_change / 100))

# ----------------------- Charts -----------------------
st.subheader("🌡️ Climate Scenario Impact")
df = pd.DataFrame({
    "Metric": ["Avg Temperature (°C)", "Avg Rainfall (mm/month)"],
    "Current": [current_temp, current_rain],
    "Future": [future_temp, future_rain]
})

fig, ax = plt.subplots()
bar_width = 0.35
index = range(len(df))
ax.bar(index, df["Current"], bar_width, label="Current")
ax.bar([i + bar_width for i in index], df["Future"], bar_width, label="Future")
ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(df["Metric"], rotation=0)
ax.legend()
ax.set_ylabel("Value")
ax.set_title("Climate Scenario Comparison")
fig.tight_layout()
st.pyplot(fig)

# ----------------------- Map & Overlays -----------------------
st.subheader("🗺️ Weather Map Overlay")
st.markdown('<div class="card">', unsafe_allow_html=True)

layer_choices = st.multiselect(
    "Choose overlays",
    list(OVERLAY_LAYERS.keys()),
    default=["🌧️ Rain", "☁️ Clouds"]
)
opacity = st.slider("Overlay opacity", 0.1, 1.0, 0.7)

m = folium.Map(location=[lat, lon], zoom_start=8, control_scale=True, tiles="OpenStreetMap")
# Add selected overlays (skip if no key)
for name in layer_choices:
    layer_key = OVERLAY_LAYERS[name]
    if OWM_KEY and TILE_URL_TMPL:
        folium.TileLayer(
            tiles=TILE_URL_TMPL.format(layer=layer_key),
            attr="OpenWeatherMap",
            name=name,
            overlay=True,
            control=True,
            opacity=opacity,
        ).add_to(m)

folium.Marker([lat, lon], tooltip=place_name).add_to(m)
folium.LayerControl(collapsed=False).add_to(m)

m_state = st_folium(m, width=None, height=520)

st.markdown('</div>', unsafe_allow_html=True)

# Click-to-update location
if use_click and m_state and m_state.get("last_clicked"):
    new_lat = m_state["last_clicked"]["lat"]
    new_lon = m_state["last_clicked"]["lng"]
    st.session_state.loc["lat"] = new_lat
    st.session_state.loc["lon"] = new_lon
    # update display name via reverse geocode (non-blocking-ish)
    addr = reverse_geocode(new_lat, new_lon)
    st.session_state.loc["name"] = addr
    st.rerun()

# ----------------------- Scenario Report -----------------------
st.subheader("📝 Scenario Report")
summary = (
    f"Location: {st.session_state.loc['name']}\n"
    f"Current Avg Temp: {current_temp:.1f} °C\n"
    f"Future Avg Temp:  {future_temp:.1f} °C\n"
    f"Current Avg Rainfall (proxy): {current_rain:.1f} mm/month\n"
    f"Future Avg Rainfall (proxy):  {future_rain:.1f} mm/month\n"
)
st.text(summary)

# ----------------------- Impact Logic -----------------------
st.subheader("🌍 Projected Impact & Environmental Consequences")
implications = []
if future_temp >= 35:
    implications.append("🔥 High risk of heatwaves, crop failures, and wildfires.")
elif future_temp >= 32:
    implications.append("🌡️ Rising temperature may cause heat stress and alter local ecosystems.")
if future_rain < 30:
    implications.append("💧 Severe drought risk, low water availability, reduced agricultural productivity.")
elif future_rain > 100:
    implications.append("🌊 Increased flood risk, potential for water-logging and disease spread.")
if not implications:
    implications.append("✔ Conditions likely remain stable with minimal severe impacts.")

st.info("\n".join(f"- {x}" for x in implications))

# Footer
st.markdown(
    f"""
    <div class="footer" style="text-align:center; margin-top:2rem; opacity:.8;">
      Built by <a href="https://www.linkedin.com/in/ninankhwashu/" target="_blank">Nina Nkhwashu</a>.
    </div>
    """,
    unsafe_allow_html=True
)