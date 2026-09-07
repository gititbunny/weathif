import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_PATH)

OWM_API_KEY = os.getenv("OWM_API_KEY", "").strip()

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_current_conditions(latitude: float, longitude: float):
    if not OWM_API_KEY:
        raise RuntimeError(
            "OpenWeatherMap API key is not configured."
        )

    try:
        response = requests.get(
            OPENWEATHER_URL,
            params={
                "lat": latitude,
                "lon": longitude,
                "appid": OWM_API_KEY,
                "units": "metric",
            },
            timeout=10,
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as exc:
        raise RuntimeError(
            "Current weather data is temporarily unavailable."
        ) from exc

    main = data.get("main", {})
    weather = data.get("weather", [])
    wind = data.get("wind", {})
    clouds = data.get("clouds", {})

    temperature = main.get("temp")

    if temperature is None:
        raise RuntimeError(
            "Current temperature was not returned by the weather service."
        )

    description = None

    if weather:
        description = weather[0].get("description")

    return {
        "temperature_c": round(float(temperature), 1),
        "feels_like_c": (
            round(float(main["feels_like"]), 1)
            if main.get("feels_like") is not None
            else None
        ),
        "humidity_percent": main.get("humidity"),
        "pressure_hpa": main.get("pressure"),
        "wind_speed_m_s": wind.get("speed"),
        "cloud_cover_percent": clouds.get("all"),
        "condition": description,
        "source": "OpenWeatherMap",
    }


def fetch_recent_rainfall(latitude: float, longitude: float):
    try:
        response = requests.get(
            OPEN_METEO_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "daily": "precipitation_sum",
                "past_days": 30,
                "forecast_days": 1,
                "timezone": "auto",
            },
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as exc:
        raise RuntimeError(
            "Recent rainfall data is temporarily unavailable."
        ) from exc

    daily = data.get("daily", {})

    dates = daily.get("time", [])
    precipitation = daily.get("precipitation_sum", [])

    if len(precipitation) < 2:
        raise RuntimeError(
            "Recent rainfall data was not returned by the weather service."
        )

    # The final value is the current/forecast day.
    # We only want completed recent days.
    completed_dates = dates[:-1]
    completed_precipitation = precipitation[:-1]

    # Keep the most recent 30 completed days.
    completed_dates = completed_dates[-30:]
    completed_precipitation = completed_precipitation[-30:]

    valid_values = [
        float(value)
        for value in completed_precipitation
        if value is not None
    ]

    if not valid_values:
        raise RuntimeError(
            "Recent rainfall data was not available for this location."
        )

    rainfall_total = sum(valid_values)

    return {
        "period_days": len(valid_values),
        "total_mm": round(rainfall_total, 1),
        "start_date": (
            completed_dates[0]
            if completed_dates
            else None
        ),
        "end_date": (
            completed_dates[-1]
            if completed_dates
            else None
        ),
        "source": "Open-Meteo",
    }


def fetch_weather_baseline(latitude: float, longitude: float):
    current = fetch_current_conditions(
        latitude,
        longitude,
    )

    rainfall = fetch_recent_rainfall(
        latitude,
        longitude,
    )

    return {
        "coordinates": {
            "latitude": latitude,
            "longitude": longitude,
        },
        "current": current,
        "recent_rainfall": rainfall,
        "baseline": {
            "temperature_c": current["temperature_c"],
            "rainfall_mm": rainfall["total_mm"],
        },
        "retrieved_at": datetime.utcnow().isoformat() + "Z",
    }