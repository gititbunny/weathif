import { useState } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import {
  getClimateMemory,
  getEnsoContext,
  getEnvironment,
  getSeasonalOutlook,
  getWeather,
  reverseGeocode,
  runScenario,
  searchLocation,
} from "../services/api";
import ClimateMemory from "../components/ClimateMemory";
import ClimateMap from "../components/ClimateMap";
import SeasonalOutlook from "../components/SeasonalOutlook";
import EnsoContext from "../components/EnsoContext";
import "../styles/simulator.css";

function Simulator() {
  const [query, setQuery] = useState("");
  const [location, setLocation] = useState(null);
  const [weather, setWeather] = useState(null);
  const [environment, setEnvironment] = useState(null);
  const [climateMemory, setClimateMemory] = useState(null);
  const [seasonalOutlook, setSeasonalOutlook] = useState(null);
  const [ensoContext, setEnsoContext] = useState(null);
  const [temperatureChange, setTemperatureChange] = useState(0);
  const [rainfallChange, setRainfallChange] = useState(0);
  const [scenario, setScenario] = useState(null);
  const [loading, setLoading] = useState(false);
  const [scenarioLoading, setScenarioLoading] = useState(false);
  const [mapLoading, setMapLoading] = useState(false);
  const [error, setError] = useState("");
  const [scenarioError, setScenarioError] = useState("");
  async function handleSubmit(event) {
    event.preventDefault();

    const cleanQuery = query.trim();

    if (cleanQuery.length < 2) {
      setError("Enter a location to continue.");
      return;
    }

    setLoading(true);
    setError("");
    setScenarioError("");
    setLocation(null);
    setWeather(null);
    setEnvironment(null);
    setScenario(null);
    setClimateMemory(null);
    setSeasonalOutlook(null);
    setEnsoContext(null);
    setTemperatureChange(0);
    setRainfallChange(0);

    try {
      const locationData = await searchLocation(cleanQuery);

      const [
      weatherData,
      environmentData,
      climateMemoryData,
      seasonalOutlookData,
      ensoData,
    ] = await Promise.all([
      getWeather(
        locationData.latitude,
        locationData.longitude
      ),

      getEnvironment(
        locationData.latitude,
        locationData.longitude
      ),

      getClimateMemory(
        locationData.latitude,
        locationData.longitude
      ),

      getSeasonalOutlook(
        locationData.latitude,
        locationData.longitude
      ),

      getEnsoContext(),
    ]);

    setLocation(locationData);
    setWeather(weatherData);
    setEnvironment(environmentData);
    setClimateMemory(climateMemoryData);
    setSeasonalOutlook(seasonalOutlookData);
    setEnsoContext(ensoData);
      

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleMapLocationSelect(
    latitude,
    longitude
  ) {
    setMapLoading(true);
    setError("");
    setScenarioError("");

    setScenario(null);
    setTemperatureChange(0);
    setRainfallChange(0);

    try {
      const locationData = await reverseGeocode(
        latitude,
        longitude
      );

      const [
        weatherData,
        environmentData,
        climateMemoryData,
        seasonalOutlookData,
      ] = await Promise.all([
        getWeather(
          locationData.latitude,
          locationData.longitude
        ),

        getEnvironment(
          locationData.latitude,
          locationData.longitude
        ),

        getClimateMemory(
          locationData.latitude,
          locationData.longitude
        ),

        getSeasonalOutlook(
          locationData.latitude,
          locationData.longitude
        ),
      ]);

      setLocation(locationData);
      setWeather(weatherData);
      setEnvironment(environmentData);
      setClimateMemory(climateMemoryData);
      setSeasonalOutlook(seasonalOutlookData);
      setEnsoContext(ensoData);
      setQuery(locationData.name);
    } catch (err) {
      setError(err.message);
    } finally {
      setMapLoading(false);
    }
  }  
    
  async function handleScenario() {
    if (!weather) {
      return;
    }

    setScenarioLoading(true);
    setScenarioError("");

    try {
      const result = await runScenario({
        baselineTemperature:
          weather.baseline.temperature_c,

        baselineRainfall:
          weather.baseline.rainfall_mm,

        temperatureChange,

        rainfallChangePercent:
          rainfallChange,
      });

      setScenario(result);
    } catch (err) {
      setScenarioError(err.message);
    } finally {
      setScenarioLoading(false);
    }
  }

  return (
    <div className="simulator-page">
      <Header />

      <main>
        <section className="simulator-intro">
          <div className="page-shell simulator-intro__grid">
            <div>
              <p className="eyebrow">
                Scenario laboratory
              </p>

              <h1>
                Explore a changing environment.
              </h1>
            </div>

            <div className="simulator-intro__copy">
              Search a real location, establish its current
              environmental baseline and experiment with
              hypothetical changes in temperature and rainfall.
            </div>
          </div>
        </section>

        <section className="simulator-search">
          <div className="page-shell">
            <form
              onSubmit={handleSubmit}
              className="simulator-search__panel"
            >
              <div className="simulator-search__field">
                <label htmlFor="location">
                  Location
                </label>

                <input
                  id="location"
                  type="text"
                  value={query}
                  onChange={(event) =>
                    setQuery(event.target.value)
                  }
                  placeholder="e.g. Tzaneen, South Africa"
                  autoComplete="off"
                />
              </div>

              <button
                type="submit"
                className="simulator-search__button"
                disabled={loading}
              >
                {loading
                  ? "Loading climate data..."
                  : "Explore location"}
              </button>
            </form>

            {error && (
              <p
                className="simulator-error"
                role="alert"
              >
                {error}
              </p>
            )}
          </div>
        </section>

        {location && weather && (
          <>
            <section className="location-overview">
              <div className="page-shell">
                <div className="location-overview__top">
                  <div>
                    <p className="eyebrow">
                      Current environmental baseline
                    </p>

                    <h2>
                      {location.name}
                    </h2>
                  </div>

                  <p className="location-overview__coordinates">
                    {location.latitude},{" "}
                    {location.longitude}
                  </p>
                </div>

                <div className="conditions-grid">
                  <article className="condition-card condition-card--primary">
                    <div>
                      <p className="condition-card__label">
                        Current temperature
                      </p>

                      <h3 className="condition-card__value">
                        {weather.current.temperature_c}°C
                      </h3>

                      <p className="condition-card__subvalue">
                        Feels like{" "}
                        {weather.current.feels_like_c}°C
                      </p>
                    </div>

                    <div>
                      <p className="condition-card__label">
                        Conditions
                      </p>

                      <strong>
                        {weather.current.condition ||
                          "Unavailable"}
                      </strong>
                    </div>
                  </article>

                  <article className="condition-card">
                    <p className="condition-card__label">
                      Recent rainfall
                    </p>

                    <strong>
                      {weather.recent_rainfall.total_mm} mm
                    </strong>

                    <small>
                      Previous{" "}
                      {weather.recent_rainfall.period_days}{" "}
                      completed days
                    </small>
                  </article>

                  <article className="condition-card">
                    <p className="condition-card__label">
                      Humidity
                    </p>

                    <strong>
                      {weather.current.humidity_percent}%
                    </strong>
                  </article>

                  <article className="condition-card">
                    <p className="condition-card__label">
                      Cloud cover
                    </p>

                    <strong>
                      {weather.current.cloud_cover_percent}%
                    </strong>
                  </article>

                  <article className="condition-card">
                    <p className="condition-card__label">
                      Wind speed
                    </p>

                    <strong>
                      {weather.current.wind_speed_m_s} m/s
                    </strong>
                  </article>
                </div>

                <p className="conditions-source">
                  Temperature and atmospheric conditions:{" "}
                  {weather.current.source}
                  {" · "}
                  Rainfall:{" "}
                  {weather.recent_rainfall.source}
                </p>
              </div>
            </section>

            <ClimateMap
              location={location}
              onLocationSelect={handleMapLocationSelect}
              loading={mapLoading}
            />        

            <ClimateMemory data={climateMemory} />

            <SeasonalOutlook data={seasonalOutlook} />

            <EnsoContext data={ensoContext} />

            {environment && (
            <section className="land-water">
              <div className="page-shell">
                <div className="land-water__header">
                  <div>
                    <p className="eyebrow">
                      Land & water conditions
                    </p>

                    <h2>
                      Below the weather,
                      <br />
                      another system is moving.
                    </h2>
                  </div>

                  <p className="land-water__intro">
                    Explore modelled soil conditions, atmospheric
                    drying demand and reference evapotranspiration
                    around the selected location.
                  </p>
                </div>

                <div className="land-water__grid">
                  <article className="land-water-card land-water-card--soil">
                    <p className="land-water-card__label">
                      Surface soil moisture
                    </p>

                    <strong className="land-water-card__value">
                      {environment.soil.surface_moisture_m3_m3 ?? "—"}
                    </strong>

                    <span className="land-water-card__unit">
                      m³/m³
                    </span>

                    <p className="land-water-card__note">
                      Modelled volumetric moisture in the upper soil layer.
                    </p>
                  </article>

                  <article className="land-water-card">
                    <p className="land-water-card__label">
                      Root-zone moisture
                    </p>

                    <strong className="land-water-card__value">
                      {environment.soil.root_zone_moisture_m3_m3 ?? "—"}
                    </strong>

                    <span className="land-water-card__unit">
                      m³/m³
                    </span>

                    <p className="land-water-card__note">
                      Modelled moisture deeper below the surface.
                    </p>
                  </article>

                  <article className="land-water-card">
                    <p className="land-water-card__label">
                      Surface soil temperature
                    </p>

                    <strong className="land-water-card__value">
                      {environment.soil.surface_temperature_c ?? "—"}
                      {environment.soil.surface_temperature_c !== null
                        ? "°C"
                        : ""}
                    </strong>

                    <p className="land-water-card__note">
                      Estimated temperature at the land surface.
                    </p>
                  </article>

                  <article className="land-water-card">
                    <p className="land-water-card__label">
                      Soil temperature · 6 cm
                    </p>

                    <strong className="land-water-card__value">
                      {environment.soil.temperature_6cm_c ?? "—"}
                      {environment.soil.temperature_6cm_c !== null
                        ? "°C"
                        : ""}
                    </strong>

                    <p className="land-water-card__note">
                      Estimated soil temperature below the surface.
                    </p>
                  </article>

                  <article className="land-water-card land-water-card--vpd">
                    <p className="land-water-card__label">
                      Atmospheric drying demand
                    </p>

                    <div className="land-water-card__split">
                      <div>
                        <strong className="land-water-card__value">
                          {
                            environment.atmosphere
                              .vapour_pressure_deficit_kpa
                          }{" "}
                          kPa
                        </strong>
                      </div>

                      <span className="land-water-card__status">
                        {
                          environment.atmosphere
                            .vpd_context.label
                        }
                      </span>
                    </div>

                    <p className="land-water-card__note">
                      {
                        environment.atmosphere
                          .vpd_context.description
                      }
                    </p>
                  </article>

                  <article className="land-water-card land-water-card--et0">
                    <p className="land-water-card__label">
                      Reference evapotranspiration
                    </p>

                    <div className="land-water-card__split">
                      <div>
                        <strong className="land-water-card__value">
                          {
                            environment.reference_evapotranspiration
                              .average_mm_per_day
                          }{" "}
                          mm/day
                        </strong>

                        <span className="land-water-card__unit">
                          {
                            environment.reference_evapotranspiration
                              .total_mm
                          }{" "}
                          mm across the previous{" "}
                          {
                            environment.reference_evapotranspiration
                              .period_days
                          }{" "}
                          completed days
                        </span>
                      </div>
                    </div>

                    <p className="land-water-card__note">
                      A reference measure of atmospheric water demand.
                    </p>
                  </article>
                </div>

                <p className="land-water__source">
                  Source: {environment.source}. {environment.note}
                </p>
              </div>
            </section>
          )}              
            

            <section className="scenario-workspace">
              <div className="page-shell">
                <div className="scenario-workspace__header">
                  <div>
                    <p className="eyebrow">
                      Build your scenario
                    </p>

                    <h2>
                      Change the climate variables.
                      <br />
                      Watch the environment respond.
                    </h2>
                  </div>

                  <p className="scenario-workspace__intro">
                    Start from the observed local baseline, then adjust
                    temperature and rainfall to build a hypothetical
                    environmental scenario.
                  </p>
                </div>

                <div className="scenario-lab">
                  <div className="scenario-lab__controls">
                    <div className="scenario-control scenario-control--temperature">
                      <div className="scenario-control__top">
                        <div>
                          <span className="scenario-control__eyebrow">
                            Temperature shift
                          </span>

                          <label htmlFor="temperature-change">
                            Temperature
                          </label>
                        </div>

                        <strong className="scenario-control__value">
                          {temperatureChange > 0 ? "+" : ""}
                          {temperatureChange}°C
                        </strong>
                      </div>

                      <input
                        id="temperature-change"
                        type="range"
                        min="-5"
                        max="5"
                        step="0.5"
                        value={temperatureChange}
                        onChange={(event) => {
                          setTemperatureChange(
                            Number(event.target.value)
                          );

                          setScenario(null);
                        }}
                      />

                      <div className="scenario-control__range">
                        <span>-5°C</span>
                        <span>Current climate</span>
                        <span>+5°C</span>
                      </div>
                    </div>

                    <div className="scenario-control scenario-control--rainfall">
                      <div className="scenario-control__top">
                        <div>
                          <span className="scenario-control__eyebrow">
                            Precipitation shift
                          </span>

                          <label htmlFor="rainfall-change">
                            Rainfall
                          </label>
                        </div>

                        <strong className="scenario-control__value">
                          {rainfallChange > 0 ? "+" : ""}
                          {rainfallChange}%
                        </strong>
                      </div>

                      <input
                        id="rainfall-change"
                        type="range"
                        min="-100"
                        max="100"
                        step="5"
                        value={rainfallChange}
                        onChange={(event) => {
                          setRainfallChange(
                            Number(event.target.value)
                          );

                          setScenario(null);
                        }}
                      />

                      <div className="scenario-control__range">
                        <span>-100%</span>
                        <span>Current climate</span>
                        <span>+100%</span>
                      </div>
                    </div>
                  </div>

                  <div className="scenario-preview">
                    <div className="scenario-preview__header">
                      <div>
                        <span>
                          Live scenario preview
                        </span>

                        <h3>
                          Current → simulated
                        </h3>
                      </div>

                      <span className="scenario-preview__status">
                        Hypothetical
                      </span>
                    </div>

                    <div className="scenario-preview__comparison">
                      <div className="scenario-preview__column">
                        <span className="scenario-preview__column-label">
                          Current
                        </span>

                        <div className="scenario-preview__metric">
                          <span>
                            Temperature
                          </span>

                          <strong>
                            {weather.baseline.temperature_c}°C
                          </strong>
                        </div>

                        <div className="scenario-preview__metric">
                          <span>
                            Recent rainfall
                          </span>

                          <strong>
                            {weather.baseline.rainfall_mm} mm
                          </strong>
                        </div>
                      </div>

                      <div
                        className="scenario-preview__direction"
                        aria-hidden="true"
                      >
                        <span>→</span>
                      </div>

                      <div className="scenario-preview__column scenario-preview__column--future">
                        <span className="scenario-preview__column-label">
                          Scenario
                        </span>

                        <div className="scenario-preview__metric">
                          <span>
                            Temperature
                          </span>

                          <strong>
                            {(
                              weather.baseline.temperature_c +
                              temperatureChange
                            ).toFixed(1)}
                            °C
                          </strong>
                        </div>

                        <div className="scenario-preview__metric">
                          <span>
                            Rainfall
                          </span>

                          <strong>
                            {Math.max(
                              0,
                              weather.baseline.rainfall_mm *
                                (1 + rainfallChange / 100)
                            ).toFixed(1)}{" "}
                            mm
                          </strong>
                        </div>
                      </div>
                    </div>

                    <div className="scenario-preview__deltas">
                      <div>
                        <span>
                          Temperature
                        </span>

                        <strong>
                          {temperatureChange > 0 ? "+" : ""}
                          {temperatureChange}°C
                        </strong>
                      </div>

                      <div>
                        <span>
                          Rainfall
                        </span>

                        <strong>
                          {rainfallChange > 0 ? "+" : ""}
                          {rainfallChange}%
                        </strong>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="scenario-run">
                  <div>
                    <span>
                      Ready to calculate?
                    </span>

                    <p>
                      Run the scenario to evaluate Weathif&apos;s
                      environmental thresholds.
                    </p>
                  </div>

                  <button
                    type="button"
                    className="scenario-action"
                    onClick={handleScenario}
                    disabled={scenarioLoading}
                  >
                    {scenarioLoading
                      ? "Running scenario..."
                      : "Run climate scenario"}
                  </button>
                </div>

                {scenarioError && (
                  <p
                    className="simulator-error"
                    role="alert"
                  >
                    {scenarioError}
                  </p>
                )}
              </div>
            </section>
            
            {scenario && (
              <section className="scenario-results">
                <div className="page-shell">
                  <div className="scenario-results__inner">
                    <div className="scenario-results__header">
                      <div>
                        <p className="eyebrow">
                          Scenario result
                        </p>

                        <h2>
                          Your altered
                          <br />
                          climate state.
                        </h2>
                      </div>

                      <div className="scenario-results__summary">
                        <span>
                          Simulation complete
                        </span>

                        <strong>
                          {scenario.indicators.length}
                        </strong>

                        <small>
                          environmental{" "}
                          {scenario.indicators.length === 1
                            ? "indicator"
                            : "indicators"}
                        </small>
                      </div>
                    </div>

                    <div className="scenario-shift">
                      <article className="scenario-shift__item scenario-shift__item--temperature">
                        <div className="scenario-shift__label">
                          <span>
                            Temperature
                          </span>

                          <strong>
                            {scenario.changes.temperature > 0
                              ? "+"
                              : ""}
                            {scenario.changes.temperature}°C
                          </strong>
                        </div>

                        <div className="scenario-shift__values">
                          <div>
                            <span>
                              Current
                            </span>

                            <strong>
                              {scenario.baseline.temperature}°C
                            </strong>
                          </div>

                          <div
                            className="scenario-shift__arrow"
                            aria-hidden="true"
                          >
                            →
                          </div>

                          <div>
                            <span>
                              Scenario
                            </span>

                            <strong>
                              {scenario.scenario.temperature}°C
                            </strong>
                          </div>
                        </div>
                      </article>

                      <article className="scenario-shift__item scenario-shift__item--rainfall">
                        <div className="scenario-shift__label">
                          <span>
                            Rainfall
                          </span>

                          <strong>
                            {scenario.changes.rainfall_percent > 0
                              ? "+"
                              : ""}
                            {scenario.changes.rainfall_percent}%
                          </strong>
                        </div>

                        <div className="scenario-shift__values">
                          <div>
                            <span>
                              Current
                            </span>

                            <strong>
                              {scenario.baseline.rainfall} mm
                            </strong>
                          </div>

                          <div
                            className="scenario-shift__arrow"
                            aria-hidden="true"
                          >
                            →
                          </div>

                          <div>
                            <span>
                              Scenario
                            </span>

                            <strong>
                              {scenario.scenario.rainfall} mm
                            </strong>
                          </div>
                        </div>
                      </article>
                    </div>

                    <div className="scenario-indicators">
                      <div className="scenario-indicators__heading">
                        <span>
                          Threshold response
                        </span>

                        <h3>
                          What changed environmentally?
                        </h3>
                      </div>

                      <div className="scenario-indicators__list">
                        {scenario.indicators.map(
                          (indicator, index) => (
                            <article
                              className={`scenario-indicator scenario-indicator--${indicator.level}`}
                              key={`${indicator.type}-${index}`}
                            >
                              <div className="scenario-indicator__number">
                                {String(index + 1).padStart(
                                  2,
                                  "0"
                                )}
                              </div>

                              <div>
                                <p className="scenario-indicator__type">
                                  {indicator.type}
                                </p>

                                <h4>
                                  {indicator.title}
                                </h4>

                                <p>
                                  {indicator.description}
                                </p>
                              </div>
                            </article>
                          )
                        )}
                      </div>
                    </div>

                    <div className="scenario-disclaimer">
                      <span>
                        Exploratory scenario
                      </span>

                      <p>
                        {scenario.disclaimer}
                      </p>
                    </div>
                  </div>
                </div>
              </section>
            )}
          </>
        )}
        <Footer />
      </main>
    </div>
  );
}

export default Simulator;