from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from services.geocoding import reverse_location, search_location
from services.scenario import calculate_scenario
from services.weather import fetch_weather_baseline
from services.simulation import run_simulation
from services.environment import fetch_land_water_conditions
from services.climate_memory import fetch_climate_memory
from services.seasonal_outlook import fetch_seasonal_outlook
from services.enso import fetch_enso_context


app = FastAPI(
    title="Weathif API",
    description="Backend API for the Weathif climate scenario simulator.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://weathif-web.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScenarioRequest(BaseModel):
    baseline_temperature: float = Field(
        ...,
        ge=-100,
        le=100,
    )
    baseline_rainfall: float = Field(
        ...,
        ge=0,
    )
    temperature_change: float = Field(
        ...,
        ge=-5,
        le=5,
    )
    rainfall_change_percent: float = Field(
        ...,
        ge=-100,
        le=100,
    )

class SimulationRequest(BaseModel):
    latitude: float = Field(
        ...,
        ge=-90,
        le=90,
    )
    longitude: float = Field(
        ...,
        ge=-180,
        le=180,
    )
    temperature_change: float = Field(
        0,
        ge=-5,
        le=5,
    )
    rainfall_change_percent: float = Field(
        0,
        ge=-100,
        le=100,
    )

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "Weathif API",
    }


@app.get("/api/geocode")
def geocode_location(
    query: str = Query(
        ...,
        min_length=2,
        max_length=150,
    ),
):
    try:
        location = search_location(query)

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    if location is None:
        raise HTTPException(
            status_code=404,
            detail="Location not found.",
        )

    return location


@app.get("/api/reverse-geocode")
def reverse_geocode_location(
    latitude: float = Query(
        ...,
        ge=-90,
        le=90,
    ),
    longitude: float = Query(
        ...,
        ge=-180,
        le=180,
    ),
):
    try:
        location = reverse_location(
            latitude,
            longitude,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    if location is None:
        raise HTTPException(
            status_code=404,
            detail="No location could be identified for these coordinates.",
        )

    return location

@app.get("/api/weather")
def get_weather(
    latitude: float = Query(
        ...,
        ge=-90,
        le=90,
    ),
    longitude: float = Query(
        ...,
        ge=-180,
        le=180,
    ),
):
    try:
        return fetch_weather_baseline(
            latitude,
            longitude,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

@app.get("/api/enso")
def get_enso_context():
    try:
        return fetch_enso_context()

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

@app.get("/api/seasonal-outlook")
def get_seasonal_outlook(
    latitude: float = Query(
        ...,
        ge=-90,
        le=90,
    ),
    longitude: float = Query(
        ...,
        ge=-180,
        le=180,
    ),
):
    try:
        return fetch_seasonal_outlook(
            latitude,
            longitude,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

@app.get("/api/climate-memory")
def get_climate_memory(
    latitude: float = Query(
        ...,
        ge=-90,
        le=90,
    ),
    longitude: float = Query(
        ...,
        ge=-180,
        le=180,
    ),
):
    try:
        return fetch_climate_memory(
            latitude,
            longitude,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

@app.get("/api/environment")
def get_environment(
    latitude: float = Query(
        ...,
        ge=-90,
        le=90,
    ),
    longitude: float = Query(
        ...,
        ge=-180,
        le=180,
    ),
):
    try:
        return fetch_land_water_conditions(
            latitude,
            longitude,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

@app.post("/api/simulate")
def simulate_climate(request: SimulationRequest):
    try:
        return run_simulation(
            latitude=request.latitude,
            longitude=request.longitude,
            temperature_change=request.temperature_change,
            rainfall_change_percent=request.rainfall_change_percent,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

@app.post("/api/scenario")
def create_scenario(request: ScenarioRequest):
    return calculate_scenario(
        baseline_temperature=request.baseline_temperature,
        baseline_rainfall=request.baseline_rainfall,
        temperature_change=request.temperature_change,
        rainfall_change_percent=request.rainfall_change_percent,
    )