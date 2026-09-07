import requests


SEASONAL_URL = "https://seasonal-api.open-meteo.com/v1/seasonal"


def _average_member_values(data, prefix):
    matching_keys = [
        key
        for key in data.keys()
        if key == prefix or key.startswith(f"{prefix}_member")
    ]

    if not matching_keys:
        return []

    series_list = [
        data[key]
        for key in matching_keys
        if isinstance(data.get(key), list)
    ]

    if not series_list:
        return []

    length = min(len(series) for series in series_list)

    averages = []

    for index in range(length):
        values = [
            float(series[index])
            for series in series_list
            if series[index] is not None
        ]

        averages.append(
            round(sum(values) / len(values), 2)
            if values
            else None
        )

    return averages


def _temperature_context(value):
    if value is None:
        return "Unavailable"

    if value > 0:
        return "Warmer than model climatology"

    if value < 0:
        return "Cooler than model climatology"

    return "Near model climatology"


def _rainfall_context(value):
    if value is None:
        return "Unavailable"

    if value > 0:
        return "Wetter than model climatology"

    if value < 0:
        return "Drier than model climatology"

    return "Near model climatology"


def fetch_seasonal_outlook(
    latitude: float,
    longitude: float,
):
    try:
        response = requests.get(
            SEASONAL_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "monthly": (
                    "temperature_2m_anomaly,"
                    "precipitation_anomaly"
                ),
                "models": "ecmwf_seas5",
                "forecast_days": 183,
                "timezone": "auto",
                "cell_selection": "land",
            },
            timeout=25,
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as exc:
        raise RuntimeError(
            "Seasonal outlook data is temporarily unavailable."
        ) from exc

    monthly = data.get("monthly", {})

    months = monthly.get("time", [])

    temperature_anomalies = _average_member_values(
        monthly,
        "temperature_2m_anomaly",
    )

    precipitation_anomalies = _average_member_values(
        monthly,
        "precipitation_anomaly",
    )

    if (
        not months
        or not temperature_anomalies
        or not precipitation_anomalies
    ):
        raise RuntimeError(
            "Seasonal outlook data was not returned."
        )

    count = min(
        len(months),
        len(temperature_anomalies),
        len(precipitation_anomalies),
    )

    outlook = []

    for index in range(count):
        temperature = temperature_anomalies[index]
        precipitation = precipitation_anomalies[index]

        outlook.append(
            {
                "month": months[index],
                "temperature_anomaly_c": temperature,
                "temperature_context": _temperature_context(
                    temperature
                ),
                "precipitation_anomaly_mm": precipitation,
                "precipitation_context": _rainfall_context(
                    precipitation
                ),
            }
        )

    return {
        "coordinates": {
            "latitude": latitude,
            "longitude": longitude,
        },
        "months": outlook,
        "source": "Open-Meteo / ECMWF SEAS5",
        "model": "ECMWF SEAS5 seasonal ensemble",
        "method": (
            "Monthly ensemble-member anomalies are averaged "
            "to provide a broad seasonal signal."
        ),
        "disclaimer": (
            "Seasonal forecasts describe broad area-scale tendencies. "
            "They are not precise local weather forecasts and are not "
            "bias-corrected."
        ),
    }