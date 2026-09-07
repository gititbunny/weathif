def calculate_scenario(
    baseline_temperature: float,
    baseline_rainfall: float,
    temperature_change: float,
    rainfall_change_percent: float,
):
    scenario_temperature = baseline_temperature + temperature_change

    scenario_rainfall = baseline_rainfall * (
        1 + rainfall_change_percent / 100
    )

    scenario_rainfall = max(0, scenario_rainfall)

    indicators = []

    # Temperature indicators
    if scenario_temperature >= 35:
        indicators.append(
            {
                "type": "temperature",
                "level": "high",
                "title": "Extreme heat conditions",
                "description": (
                    "The scenario crosses the 35°C threshold used by "
                    "Weathif to indicate increased heat, crop stress "
                    "and wildfire concerns."
                ),
            }
        )

    elif scenario_temperature >= 32:
        indicators.append(
            {
                "type": "temperature",
                "level": "moderate",
                "title": "Heat stress conditions",
                "description": (
                    "The scenario crosses the 32°C threshold used by "
                    "Weathif to indicate potential heat stress and "
                    "ecosystem pressure."
                ),
            }
        )

    # Rainfall indicators
    if scenario_rainfall < 30:
        indicators.append(
            {
                "type": "rainfall",
                "level": "high",
                "title": "Low rainfall conditions",
                "description": (
                    "The scenario falls below the 30 mm rainfall "
                    "threshold used by Weathif to indicate drought-related "
                    "conditions."
                ),
            }
        )

    elif scenario_rainfall > 100:
        indicators.append(
            {
                "type": "rainfall",
                "level": "high",
                "title": "High rainfall conditions",
                "description": (
                    "The scenario exceeds the 100 mm rainfall threshold "
                    "used by Weathif to indicate possible flooding or "
                    "waterlogging conditions."
                ),
            }
        )

    if not indicators:
        indicators.append(
            {
                "type": "general",
                "level": "stable",
                "title": "No scenario threshold crossed",
                "description": (
                    "The selected temperature and rainfall values remain "
                    "within Weathif's current scenario thresholds."
                ),
            }
        )

    return {
        "baseline": {
            "temperature": round(baseline_temperature, 2),
            "rainfall": round(baseline_rainfall, 2),
        },
        "changes": {
            "temperature": round(temperature_change, 2),
            "rainfall_percent": round(rainfall_change_percent, 2),
        },
        "scenario": {
            "temperature": round(scenario_temperature, 2),
            "rainfall": round(scenario_rainfall, 2),
        },
        "indicators": indicators,
        "disclaimer": (
            "These are exploratory scenario indicators based on Weathif's "
            "defined thresholds. They are not climate forecasts."
        ),
    }