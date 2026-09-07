import requests


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def _round_or_none(value, digits=2):
    if value is None:
        return None

    return round(float(value), digits)


def _vpd_context(value):
    if value is None:
        return {
            "level": "unavailable",
            "label": "Unavailable",
            "description": (
                "Vapour pressure deficit data is not available "
                "for this location."
            ),
        }

    if value < 0.4:
        return {
            "level": "low",
            "label": "Low atmospheric drying demand",
            "description": (
                "The current vapour pressure deficit is below "
                "0.4 kPa, a range associated with lower plant "
                "transpiration demand."
            ),
        }

    if value > 1.6:
        return {
            "level": "high",
            "label": "Elevated atmospheric drying demand",
            "description": (
                "The current vapour pressure deficit is above "
                "1.6 kPa, a range associated with increased "
                "plant transpiration demand."
            ),
        }

    return {
        "level": "moderate",
        "label": "Moderate atmospheric drying demand",
        "description": (
            "The current vapour pressure deficit sits between "
            "Weathif's low and elevated VPD reference ranges."
        ),
    }


def fetch_land_water_conditions(
    latitude: float,
    longitude: float,
):
    try:
        response = requests.get(
            OPEN_METEO_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": ",".join(
                    [
                        "soil_temperature_0cm",
                        "soil_temperature_6cm",
                        "soil_moisture_0_to_1cm",
                        "soil_moisture_9_to_27cm",
                        "vapour_pressure_deficit",
                    ]
                ),
                "daily": "et0_fao_evapotranspiration",
                "past_days": 7,
                "forecast_days": 1,
                "timezone": "auto",
                "cell_selection": "land",
            },
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as exc:
        raise RuntimeError(
            "Land and water data is temporarily unavailable."
        ) from exc

    current = data.get("current", {})
    daily = data.get("daily", {})

    if not current:
        raise RuntimeError(
            "Land conditions were not returned by the environmental data service."
        )

    vpd = current.get("vapour_pressure_deficit")

    et0_dates = daily.get("time", [])
    et0_values = daily.get(
        "et0_fao_evapotranspiration",
        [],
    )

    # The final daily value represents the current day.
    # Use only completed recent days for the historical summary.
    completed_dates = et0_dates[:-1]
    completed_et0 = et0_values[:-1]

    completed_dates = completed_dates[-7:]
    completed_et0 = completed_et0[-7:]

    valid_et0 = [
        float(value)
        for value in completed_et0
        if value is not None
    ]

    et0_total = (
        sum(valid_et0)
        if valid_et0
        else None
    )

    et0_average = (
        et0_total / len(valid_et0)
        if valid_et0
        else None
    )

    return {
        "coordinates": {
            "latitude": latitude,
            "longitude": longitude,
        },
        "soil": {
            "surface_temperature_c": _round_or_none(
                current.get("soil_temperature_0cm"),
                1,
            ),
            "temperature_6cm_c": _round_or_none(
                current.get("soil_temperature_6cm"),
                1,
            ),
            "surface_moisture_m3_m3": _round_or_none(
                current.get("soil_moisture_0_to_1cm"),
                3,
            ),
            "root_zone_moisture_m3_m3": _round_or_none(
                current.get("soil_moisture_9_to_27cm"),
                3,
            ),
        },
        "atmosphere": {
            "vapour_pressure_deficit_kpa": _round_or_none(
                vpd,
                2,
            ),
            "vpd_context": _vpd_context(vpd),
        },
        "reference_evapotranspiration": {
            "period_days": len(valid_et0),
            "total_mm": (
                round(et0_total, 1)
                if et0_total is not None
                else None
            ),
            "average_mm_per_day": (
                round(et0_average, 2)
                if et0_average is not None
                else None
            ),
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
        },
        "source": "Open-Meteo",
        "note": (
            "Land and atmospheric values are weather-model estimates "
            "for the selected location."
        ),
    }