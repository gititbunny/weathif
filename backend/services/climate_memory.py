from datetime import date, datetime, timedelta

import requests


FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

COMPARISON_YEARS = 10
PERIOD_DAYS = 30


def _safe_date(year: int, month: int, day: int):
    try:
        return date(year, month, day)

    except ValueError:
        # Handles 29 February when the comparison year
        # is not a leap year.
        if month == 2 and day == 29:
            return date(year, 2, 28)

        raise


def _calculate_change(current, historical):
    if current is None or historical is None:
        return None

    return round(current - historical, 1)


def _calculate_percent_change(current, historical):
    if (
        current is None
        or historical is None
        or historical == 0
    ):
        return None

    return round(
        ((current - historical) / historical) * 100,
        1,
    )


def _temperature_context(change):
    if change is None:
        return "Historical temperature comparison unavailable."

    if change >= 1:
        return "Warmer than the recent historical comparison."

    if change <= -1:
        return "Cooler than the recent historical comparison."

    return "Close to the recent historical comparison."


def _rainfall_context(percent_change):
    if percent_change is None:
        return "Historical rainfall comparison unavailable."

    if percent_change >= 20:
        return "Wetter than the recent historical comparison."

    if percent_change <= -20:
        return "Drier than the recent historical comparison."

    return "Close to the recent historical comparison."


def fetch_recent_period(
    latitude: float,
    longitude: float,
):
    try:
        response = requests.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "daily": (
                    "temperature_2m_mean,"
                    "precipitation_sum"
                ),
                "past_days": PERIOD_DAYS,
                "forecast_days": 1,
                "timezone": "auto",
            },
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as exc:
        raise RuntimeError(
            "Recent climate context is temporarily unavailable."
        ) from exc

    daily = data.get("daily", {})

    dates = daily.get("time", [])
    temperatures = daily.get(
        "temperature_2m_mean",
        [],
    )
    precipitation = daily.get(
        "precipitation_sum",
        [],
    )

    if len(dates) < 2:
        raise RuntimeError(
            "Recent climate context was not returned."
        )

    # Remove the current / forecast day.
    dates = dates[:-1][-PERIOD_DAYS:]
    temperatures = temperatures[:-1][-PERIOD_DAYS:]
    precipitation = precipitation[:-1][-PERIOD_DAYS:]

    valid_temperatures = [
        float(value)
        for value in temperatures
        if value is not None
    ]

    valid_precipitation = [
        float(value)
        for value in precipitation
        if value is not None
    ]

    if not valid_temperatures or not valid_precipitation:
        raise RuntimeError(
            "Recent temperature or rainfall data is incomplete."
        )

    return {
        "start_date": dates[0],
        "end_date": dates[-1],
        "mean_temperature_c": round(
            sum(valid_temperatures)
            / len(valid_temperatures),
            1,
        ),
        "rainfall_total_mm": round(
            sum(valid_precipitation),
            1,
        ),
    }


def fetch_historical_comparison(
    latitude: float,
    longitude: float,
    recent_start: str,
    recent_end: str,
):
    recent_start_date = datetime.strptime(
        recent_start,
        "%Y-%m-%d",
    ).date()

    recent_end_date = datetime.strptime(
        recent_end,
        "%Y-%m-%d",
    ).date()

    current_year = recent_end_date.year

    comparison_windows = []

    for years_back in range(
        COMPARISON_YEARS,
        0,
        -1,
    ):
        comparison_year = current_year - years_back

        start = _safe_date(
            comparison_year,
            recent_start_date.month,
            recent_start_date.day,
        )

        end_year = comparison_year

        # Handle windows crossing New Year.
        if (
            recent_end_date.month,
            recent_end_date.day,
        ) < (
            recent_start_date.month,
            recent_start_date.day,
        ):
            end_year += 1

        end = _safe_date(
            end_year,
            recent_end_date.month,
            recent_end_date.day,
        )

        comparison_windows.append(
            {
                "year": comparison_year,
                "start": start,
                "end": end,
            }
        )

    archive_start = comparison_windows[0]["start"]
    archive_end = comparison_windows[-1]["end"]

    try:
        response = requests.get(
            ARCHIVE_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "start_date": archive_start.isoformat(),
                "end_date": archive_end.isoformat(),
                "daily": (
                    "temperature_2m_mean,"
                    "precipitation_sum"
                ),
                "timezone": "auto",
                "cell_selection": "land",
            },
            timeout=25,
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as exc:
        raise RuntimeError(
            "Historical climate data is temporarily unavailable."
        ) from exc

    daily = data.get("daily", {})

    dates = daily.get("time", [])
    temperatures = daily.get(
        "temperature_2m_mean",
        [],
    )
    precipitation = daily.get(
        "precipitation_sum",
        [],
    )

    records = {}

    for index, date_string in enumerate(dates):
        records[date_string] = {
            "temperature": temperatures[index],
            "precipitation": precipitation[index],
        }

    yearly_results = []

    for window in comparison_windows:
        current_day = window["start"]

        window_temperatures = []
        window_precipitation = []

        while current_day <= window["end"]:
            record = records.get(
                current_day.isoformat()
            )

            if record:
                temperature = record.get("temperature")
                rainfall = record.get("precipitation")

                if temperature is not None:
                    window_temperatures.append(
                        float(temperature)
                    )

                if rainfall is not None:
                    window_precipitation.append(
                        float(rainfall)
                    )

            current_day += timedelta(days=1)

        if (
            window_temperatures
            and window_precipitation
        ):
            yearly_results.append(
                {
                    "year": window["year"],
                    "mean_temperature_c": (
                        sum(window_temperatures)
                        / len(window_temperatures)
                    ),
                    "rainfall_total_mm": sum(
                        window_precipitation
                    ),
                }
            )

    if not yearly_results:
        raise RuntimeError(
            "Historical comparison data could not be calculated."
        )

    historical_temperature = sum(
        item["mean_temperature_c"]
        for item in yearly_results
    ) / len(yearly_results)

    historical_rainfall = sum(
        item["rainfall_total_mm"]
        for item in yearly_results
    ) / len(yearly_results)

    return {
        "years_used": len(yearly_results),
        "first_year": yearly_results[0]["year"],
        "last_year": yearly_results[-1]["year"],
        "mean_temperature_c": round(
            historical_temperature,
            1,
        ),
        "rainfall_total_mm": round(
            historical_rainfall,
            1,
        ),
    }


def fetch_climate_memory(
    latitude: float,
    longitude: float,
):
    recent = fetch_recent_period(
        latitude,
        longitude,
    )

    historical = fetch_historical_comparison(
        latitude,
        longitude,
        recent["start_date"],
        recent["end_date"],
    )

    temperature_change = _calculate_change(
        recent["mean_temperature_c"],
        historical["mean_temperature_c"],
    )

    rainfall_percent_change = (
        _calculate_percent_change(
            recent["rainfall_total_mm"],
            historical["rainfall_total_mm"],
        )
    )

    return {
        "period": {
            "days": PERIOD_DAYS,
            "start_date": recent["start_date"],
            "end_date": recent["end_date"],
        },
        "recent": {
            "mean_temperature_c": (
                recent["mean_temperature_c"]
            ),
            "rainfall_total_mm": (
                recent["rainfall_total_mm"]
            ),
        },
        "historical_comparison": {
            **historical,
            "description": (
                "Average conditions for the same seasonal "
                "30-day window across the previous completed years."
            ),
        },
        "difference": {
            "temperature_c": temperature_change,
            "rainfall_percent": rainfall_percent_change,
            "temperature_context": (
                _temperature_context(
                    temperature_change
                )
            ),
            "rainfall_context": (
                _rainfall_context(
                    rainfall_percent_change
                )
            ),
        },
        "source": "Open-Meteo",
        "method": (
            "Recent completed 30-day conditions are compared "
            "with the average of the same calendar window "
            f"across the previous {COMPARISON_YEARS} years."
        ),
        "disclaimer": (
            "This is a historical context comparison, not a "
            "formal climate normal or climate forecast."
        ),
    }