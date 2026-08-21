# Weathif 🌦️🌍

![Weathif Logo](./assets/logo.png)

**Weathif** is an interactive local climate scenario simulator built with Python and Streamlit. It allows users to explore how hypothetical changes in temperature and rainfall could affect a selected local environment.

Users can search for a location, view current weather information and interactive weather-map overlays, adjust temperature and rainfall scenarios, and compare the current conditions with the simulated future scenario.

## Features

* Search for locations worldwide
* Geocode locations using OpenStreetMap/Nominatim
* Retrieve current temperature data
* Estimate recent monthly rainfall using precipitation data
* Adjust temperature from **-5°C to +5°C**
* Adjust rainfall from **-100% to +100%**
* Compare current and simulated conditions
* Visualise climate scenarios with Matplotlib charts
* Interactive Folium weather map
* Rain, cloud and temperature map overlays
* Adjustable weather-overlay opacity
* Click directly on the map to change location
* Reverse geocoding for map-selected locations
* Generate a simple climate scenario report
* Display potential environmental consequences based on simulated conditions
* Responsive Streamlit interface

## Tech Stack

**Application**

* Python
* Streamlit

**Data & Visualisation**

* Pandas
* Matplotlib
* Folium
* Streamlit Folium

**Location & Geocoding**

* Geopy
* OpenStreetMap / Nominatim

**Weather Data**

* OpenWeatherMap API
* Open-Meteo Archive API

**Development**

* Git
* GitHub

## How It Works

The user begins by entering a location.

Weathif geocodes the location to obtain its latitude and longitude and retrieves weather information associated with those coordinates.

The simulator establishes baseline conditions using:

* Current temperature data
* Recent precipitation data used as a monthly rainfall proxy

Users can then change two scenario variables:

**Temperature**

* Between -5°C and +5°C from the baseline

**Rainfall**

* Between -100% and +100% from the baseline

Weathif calculates the simulated values and displays the current and future scenario side by side using a comparison chart.

Based on the simulated conditions, the application also provides simple rule-based environmental impact indicators for conditions such as:

* Heat stress
* Heatwave risk
* Wildfire risk
* Drought
* Reduced water availability
* Agricultural pressure
* Flood risk
* Waterlogging

## Interactive Weather Map

Weathif includes an interactive map built with **Folium**.

Depending on the available weather data, users can display map overlays including:

* Rain
* Clouds
* Temperature

Users can adjust overlay opacity and optionally click directly on the map to select a new location.

The selected coordinates are reverse-geocoded so the simulator can update the location and climate scenario.

## Climate Scenario Visualisation

Weathif uses **Matplotlib** to compare baseline and simulated values for:

* Temperature
* Monthly rainfall

This provides a quick visual representation of how the selected hypothetical changes alter local conditions.

## Project Structure

```text
weathif/
├── .streamlit/
│   └── config.toml
├── assets/
│   ├── icon.png
│   └── logo.png
├── data/
│   └── processed/
│       └── johannesburg_2023_weather.csv
├── app.py
├── fetch_weather.py
├── requirements.txt
├── setup.py
└── README.md
```

## Historical Weather Data

The project also contains `fetch_weather.py`, a supporting data utility that retrieves historical daily weather information from the **Open-Meteo Archive API**.

The included example dataset contains Johannesburg weather data for 2023, including:

* Daily maximum temperature
* Daily minimum temperature
* Daily precipitation

This supporting script demonstrates retrieving weather data from an external REST API, converting JSON responses into a Pandas DataFrame, and exporting processed data to CSV.

## Running the Project Locally

Clone the repository:

```bash
git clone https://github.com/gititbunny/weathif.git
```

Navigate into the project:

```bash
cd weathif
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.\.venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Create a local Streamlit secrets file:

```text
.streamlit/secrets.toml
```

Add your OpenWeatherMap API key:

```toml
OWM_API_KEY = "your_openweathermap_api_key"
```

Alternatively, `OWM_API_KEY` can be provided as an environment variable.

Run the application:

```bash
streamlit run app.py
```

## What This Project Demonstrates

Weathif demonstrates practical experience with:

* Python application development
* Interactive application development with Streamlit
* REST API integration
* JSON data processing
* Pandas data manipulation
* Data visualisation with Matplotlib
* Interactive maps with Folium
* Geocoding and reverse geocoding
* Working with latitude and longitude data
* Weather-data processing
* Scenario-based calculations
* User-controlled data visualisation
* Session state management
* API response caching
* Error handling and fallback behaviour
* Git and GitHub version control

## Important Note

Weathif is an **exploratory scenario simulator**, not a scientific climate forecasting model.

The rainfall baseline is based on recent precipitation data and is used as a simplified monthly rainfall proxy. Environmental consequences are generated using predefined scenario thresholds rather than a comprehensive climate model.

The results are intended to demonstrate climate-scenario exploration, data integration and visualisation rather than provide professional climate predictions.

## Author

Built by **Git It Bunny**

[GitHub](https://github.com/gititbunny)
