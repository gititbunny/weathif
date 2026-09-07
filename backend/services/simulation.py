from services.scenario import calculate_scenario
from services.weather import fetch_weather_baseline


def run_simulation(
    latitude: float,
    longitude: float,
    temperature_change: float,
    rainfall_change_percent: float,
):
    weather = fetch_weather_baseline(
        latitude,
        longitude,
    )

    scenario = calculate_scenario(
        baseline_temperature=weather["baseline"]["temperature_c"],
        baseline_rainfall=weather["baseline"]["rainfall_mm"],
        temperature_change=temperature_change,
        rainfall_change_percent=rainfall_change_percent,
    )

    return {
        "weather": weather,
        "simulation": scenario,
    }