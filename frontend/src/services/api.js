const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(url, options = {}) {
  const response = await fetch(`${API_BASE_URL}${url}`, options);

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Something went wrong. Please try again."
    );
  }

  return data;
}

export function checkApiHealth() {
  return request("/api/health");
}

export function searchLocation(query) {
  const params = new URLSearchParams({
    query,
  });

  return request(`/api/geocode?${params.toString()}`);
}

export function reverseGeocode(latitude, longitude) {
  const params = new URLSearchParams({
    latitude,
    longitude,
  });

  return request(`/api/reverse-geocode?${params.toString()}`);
}

export function getWeather(latitude, longitude) {
  const params = new URLSearchParams({
    latitude,
    longitude,
  });

  return request(`/api/weather?${params.toString()}`);
}

export function getEnvironment(latitude, longitude) {
  const params = new URLSearchParams({
    latitude,
    longitude,
  });

  return request(`/api/environment?${params.toString()}`);
}

export function getClimateMemory(latitude, longitude) {
  const params = new URLSearchParams({
    latitude,
    longitude,
  });

  return request(`/api/climate-memory?${params.toString()}`);
}

export function getSeasonalOutlook(latitude, longitude) {
  const params = new URLSearchParams({
    latitude,
    longitude,
  });

  return request(`/api/seasonal-outlook?${params.toString()}`);
}

export function getEnsoContext() {
  return request("/api/enso");
}

export function runScenario({
  baselineTemperature,
  baselineRainfall,
  temperatureChange,
  rainfallChangePercent,
}) {
  return request("/api/scenario", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      baseline_temperature: baselineTemperature,
      baseline_rainfall: baselineRainfall,
      temperature_change: temperatureChange,
      rainfall_change_percent: rainfallChangePercent,
    }),
  });
}