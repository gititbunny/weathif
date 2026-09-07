import Header from "../components/Header";
import Footer from "../components/Footer";
import "../styles/technology.css";

function Technology() {
  return (
    <div className="technology-page">
      <Header />

      <main>
        <section className="technology-hero">
          <div className="page-shell technology-hero__grid">
            <div>
              <p className="eyebrow">
                Technology
              </p>

              <h1>
                Climate data,
                <br />
                engineered into
                <br />
                an experience.
              </h1>
            </div>

            <div className="technology-hero__aside">
              <p>
                Weathif separates its React interface from
                its Python climate and data logic through a
                REST API architecture.
              </p>

              <div className="technology-hero__stack">
                <span>React</span>
                <span>JavaScript</span>
                <span>FastAPI</span>
                <span>Python</span>
                <span>REST</span>
                <span>Recharts</span>
              </div>
            </div>
          </div>
        </section>

        <section className="technology-architecture">
          <div className="page-shell">
            <div className="technology-section-heading">
              <div>
                <p className="eyebrow">
                  Application architecture
                </p>

                <h2>
                  From interaction
                  <br />
                  to environmental data.
                </h2>
              </div>

              <p>
                The browser never needs direct access to
                private service credentials. React talks to
                Weathif&apos;s FastAPI backend, which handles
                calculations and external data requests.
              </p>
            </div>

            <div className="architecture-flow">
              <article className="architecture-node architecture-node--frontend">
                <div className="architecture-node__number">
                  01
                </div>

                <span>
                  Frontend
                </span>

                <h3>
                  React + Vite
                </h3>

                <p>
                  Interface, routing, maps, charts, loading
                  states and user interaction.
                </p>

                <div className="architecture-node__tags">
                  <span>React</span>
                  <span>Vite</span>
                  <span>CSS</span>
                  <span>React Router</span>
                </div>
              </article>

              <div
                className="architecture-connection"
                aria-hidden="true"
              >
                <span>
                  REST
                </span>

                <div>
                  →
                </div>
              </div>

              <article className="architecture-node architecture-node--backend">
                <div className="architecture-node__number">
                  02
                </div>

                <span>
                  Backend
                </span>

                <h3>
                  FastAPI + Python
                </h3>

                <p>
                  API orchestration, environmental logic,
                  scenario calculations and server-side
                  service requests.
                </p>

                <div className="architecture-node__tags">
                  <span>FastAPI</span>
                  <span>Python</span>
                  <span>Requests</span>
                  <span>Beautiful Soup</span>
                </div>
              </article>

              <div
                className="architecture-connection"
                aria-hidden="true"
              >
                <span>
                  DATA
                </span>

                <div>
                  →
                </div>
              </div>

              <article className="architecture-node architecture-node--services">
                <div className="architecture-node__number">
                  03
                </div>

                <span>
                  External services
                </span>

                <h3>
                  Weather + climate sources
                </h3>

                <p>
                  Live, historical, seasonal, geographic and
                  global climate-driver information.
                </p>

                <div className="architecture-node__tags">
                  <span>OpenWeatherMap</span>
                  <span>Open-Meteo</span>
                  <span>NOAA</span>
                  <span>OpenStreetMap</span>
                </div>
              </article>
            </div>
          </div>
        </section>

        <section className="technology-stack">
          <div className="page-shell">
            <div className="technology-stack__header">
              <p className="eyebrow">
                Technical stack
              </p>

              <h2>
                Built across the full application flow.
              </h2>
            </div>

            <div className="technology-stack__grid">
              <article className="stack-panel stack-panel--frontend">
                <span className="stack-panel__index">
                  FRONTEND
                </span>

                <h3>
                  Interface
                </h3>

                <ul>
                  <li>
                    React component architecture
                  </li>

                  <li>
                    React Router navigation
                  </li>

                  <li>
                    Responsive custom CSS
                  </li>

                  <li>
                    Recharts data visualisation
                  </li>

                  <li>
                    React Leaflet interactive mapping
                  </li>

                  <li>
                    Loading and error states
                  </li>
                </ul>
              </article>

              <article className="stack-panel stack-panel--backend">
                <span className="stack-panel__index">
                  BACKEND
                </span>

                <h3>
                  Logic
                </h3>

                <ul>
                  <li>
                    FastAPI REST endpoints
                  </li>

                  <li>
                    Python scenario calculations
                  </li>

                  <li>
                    Server-side API requests
                  </li>

                  <li>
                    Input validation
                  </li>

                  <li>
                    Response error handling
                  </li>

                  <li>
                    Short-lived ENSO response caching
                  </li>
                </ul>
              </article>

              <article className="stack-panel stack-panel--data">
                <span className="stack-panel__index">
                  DATA
                </span>

                <h3>
                  Environmental sources
                </h3>

                <ul>
                  <li>
                    Current atmospheric conditions
                  </li>

                  <li>
                    Recent rainfall
                  </li>

                  <li>
                    Historical weather comparison
                  </li>

                  <li>
                    Soil and evapotranspiration data
                  </li>

                  <li>
                    Seasonal ensemble anomalies
                  </li>

                  <li>
                    Live ENSO climate indices
                  </li>
                </ul>
              </article>
            </div>
          </div>
        </section>

        <section className="technology-request">
          <div className="page-shell">
            <div className="technology-request__heading">
              <div>
                <p className="eyebrow">
                  Request lifecycle
                </p>

                <h2>
                  One location.
                  <br />
                  Multiple data layers.
                </h2>
              </div>

              <span className="technology-request__endpoint">
                /api/*
              </span>
            </div>

            <div className="request-sequence">
              <div className="request-step">
                <span>
                  01
                </span>

                <strong>
                  Search
                </strong>

                <p>
                  The user chooses a location by text search
                  or map interaction.
                </p>
              </div>

              <div className="request-step">
                <span>
                  02
                </span>

                <strong>
                  Geocode
                </strong>

                <p>
                  Weathif resolves the location into usable
                  latitude and longitude coordinates.
                </p>
              </div>

              <div className="request-step">
                <span>
                  03
                </span>

                <strong>
                  Request
                </strong>

                <p>
                  React requests weather, environmental,
                  historical and seasonal context from
                  FastAPI.
                </p>
              </div>

              <div className="request-step">
                <span>
                  04
                </span>

                <strong>
                  Process
                </strong>

                <p>
                  Python normalises responses and performs
                  Weathif&apos;s calculations.
                </p>
              </div>

              <div className="request-step">
                <span>
                  05
                </span>

                <strong>
                  Visualise
                </strong>

                <p>
                  React turns the returned data into maps,
                  comparisons, charts and scenario controls.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="technology-decisions">
          <div className="page-shell">
            <div className="technology-decisions__grid">
              <div>
                <p className="eyebrow">
                  Engineering decisions
                </p>

                <h2>
                  Built to separate concerns.
                </h2>
              </div>

              <div className="technology-decisions__list">
                <article>
                  <span>
                    01
                  </span>

                  <div>
                    <h3>
                      Streamlit removed from the final interface
                    </h3>

                    <p>
                      The existing Python functionality was
                      preserved while the user interface was
                      rebuilt as a dedicated React application.
                    </p>
                  </div>
                </article>

                <article>
                  <span>
                    02
                  </span>

                  <div>
                    <h3>
                      Python stays responsible for Python logic
                    </h3>

                    <p>
                      Environmental processing and scenario
                      calculations remain in the backend rather
                      than being recreated in JavaScript.
                    </p>
                  </div>
                </article>

                <article>
                  <span>
                    03
                  </span>

                  <div>
                    <h3>
                      External data is normalised behind one API
                    </h3>

                    <p>
                      The frontend receives predictable Weathif
                      responses instead of managing several
                      unrelated third-party APIs directly.
                    </p>
                  </div>
                </article>

                <article>
                  <span>
                    04
                  </span>

                  <div>
                    <h3>
                      No database added without a reason
                    </h3>

                    <p>
                      The current application does not require
                      stored user accounts or persistent
                      application data, so no database layer is
                      artificially included.
                    </p>
                  </div>
                </article>
              </div>
            </div>
          </div>
        </section>
        <Footer />
      </main>
    </div>
  );
}

export default Technology;