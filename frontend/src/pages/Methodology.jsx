import Header from "../components/Header";
import Footer from "../components/Footer";
import "../styles/methodology.css";

function Methodology() {
  return (
    <div className="methodology-page">
      <Header />

      <main>
        <section className="methodology-hero">
          <div className="page-shell methodology-hero__grid">
            <div>
              <p className="eyebrow">
                Methodology
              </p>

              <h1>
                Transparent by design.
              </h1>
            </div>

            <p className="methodology-hero__intro">
              Weathif combines observed, modelled and
              historical environmental data with simple,
              visible scenario calculations. It is designed
              for exploration — not as a climate forecast
              or scientific prediction model.
            </p>
          </div>
        </section>

        <section className="methodology-process">
          <div className="page-shell">
            <div className="methodology-process__grid">
              <article className="methodology-step">
                <span className="methodology-step__number">
                  01
                </span>

                <div>
                  <p className="methodology-step__label">
                    Location
                  </p>

                  <h2>
                    Start with place.
                  </h2>

                  <p>
                    A searched or map-selected location is
                    converted into latitude and longitude.
                    Those coordinates become the geographic
                    reference for the environmental requests
                    that follow.
                  </p>
                </div>
              </article>

              <article className="methodology-step">
                <span className="methodology-step__number">
                  02
                </span>

                <div>
                  <p className="methodology-step__label">
                    Baseline
                  </p>

                  <h2>
                    Observe current conditions.
                  </h2>

                  <p>
                    Weathif retrieves current atmospheric
                    conditions together with recent rainfall
                    to establish the local baseline used by
                    the simulator.
                  </p>
                </div>
              </article>

              <article className="methodology-step">
                <span className="methodology-step__number">
                  03
                </span>

                <div>
                  <p className="methodology-step__label">
                    Context
                  </p>

                  <h2>
                    Look backward and forward.
                  </h2>

                  <p>
                    Recent conditions are compared against
                    the same seasonal period across previous
                    years, while seasonal ensemble anomalies
                    provide broader forward-looking context.
                  </p>
                </div>
              </article>

              <article className="methodology-step">
                <span className="methodology-step__number">
                  04
                </span>

                <div>
                  <p className="methodology-step__label">
                    Scenario
                  </p>

                  <h2>
                    Change the variables.
                  </h2>

                  <p>
                    Temperature changes are applied directly
                    to the baseline temperature. Rainfall
                    changes are calculated as a percentage
                    of the recent rainfall baseline.
                  </p>
                </div>
              </article>

              <article className="methodology-step">
                <span className="methodology-step__number">
                  05
                </span>

                <div>
                  <p className="methodology-step__label">
                    Indicators
                  </p>

                  <h2>
                    Cross transparent thresholds.
                  </h2>

                  <p>
                    Scenario results are evaluated against
                    Weathif&apos;s defined environmental
                    thresholds to surface exploratory
                    indicators such as heat or rainfall
                    conditions.
                  </p>
                </div>
              </article>
            </div>
          </div>
        </section>

        <section className="methodology-sources">
          <div className="page-shell">
            <div className="methodology-sources__header">
              <div>
                <p className="eyebrow">
                  Data sources
                </p>

                <h2>
                  Where the information comes from.
                </h2>
              </div>

              <p>
                Weathif does not invent environmental
                observations. Its displayed values originate
                from external weather, climate and geographic
                data services.
              </p>
            </div>

            <div className="methodology-sources__grid">
              <article>
                <span>
                  Current weather
                </span>

                <strong>
                  OpenWeatherMap
                </strong>

                <p>
                  Current temperature, humidity, cloud cover,
                  wind and general weather conditions.
                </p>
              </article>

              <article>
                <span>
                  Environmental data
                </span>

                <strong>
                  Open-Meteo
                </strong>

                <p>
                  Rainfall, soil conditions, historical
                  weather context and reference
                  evapotranspiration.
                </p>
              </article>

              <article>
                <span>
                  Seasonal modelling
                </span>

                <strong>
                  ECMWF SEAS5 via Open-Meteo
                </strong>

                <p>
                  Broad monthly temperature and precipitation
                  anomaly signals from a seasonal ensemble.
                </p>
              </article>

              <article>
                <span>
                  Global climate driver
                </span>

                <strong>
                  NOAA
                </strong>

                <p>
                  ENSO advisory information and Pacific
                  climate indices including Niño 3.4, ONI
                  and MEI V2.
                </p>
              </article>

              <article>
                <span>
                  Mapping
                </span>

                <strong>
                  OpenStreetMap
                </strong>

                <p>
                  Geographic map tiles used for interactive
                  spatial exploration.
                </p>
              </article>

              <article>
                <span>
                  Location search
                </span>

                <strong>
                  Nominatim / geocoding
                </strong>

                <p>
                  Converts place names to coordinates and
                  coordinates back into geographic locations.
                </p>
              </article>
            </div>
          </div>
        </section>

        <section className="methodology-boundaries">
          <div className="page-shell methodology-boundaries__grid">
            <div>
              <p className="eyebrow">
                Scientific boundaries
              </p>

              <h2>
                What Weathif is not.
              </h2>
            </div>

            <div className="methodology-boundaries__content">
              <p>
                Weathif is an exploratory climate scenario
                simulator. It is not a numerical climate
                model, agricultural decision system,
                meteorological warning service or substitute
                for professional scientific analysis.
              </p>

              <p>
                Seasonal anomalies describe broad model
                tendencies rather than precise local weather.
                Historical comparisons are contextual
                comparisons rather than formal climate
                normals.
              </p>

              <p>
                Scenario indicators use transparent,
                application-defined thresholds and should
                not be interpreted as forecasts.
              </p>
            </div>
          </div>
        </section>
        <Footer />
      </main>
    </div>
  );
}

export default Methodology;