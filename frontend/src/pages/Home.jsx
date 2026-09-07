import { Link } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";

import lushEnvironment from "../assets/images/environment-lush.jpg";
import droughtEnvironment from "../assets/images/environment-drought.jpg";
import rainEnvironment from "../assets/images/environment-rain.jpg";

import "../styles/home.css";

function Home() {
  return (
    <div className="home">
      <Header />

      <main>
        {/* =========================
            Hero
        ========================= */}

        <section className="home-hero">
          <div className="page-shell">
            <div className="home-hero__heading">
              <div className="home-hero__content">
                <p className="eyebrow">
                  Climate scenario simulator
                </p>

                <h1>
                  See a place.
                  <br />
                  Understand its climate.
                  <br />
                  Change the variables.
                </h1>
              </div>

              <div className="home-hero__aside">
                <p>
                  Weathif brings weather, historical climate
                  context, seasonal modelling and environmental
                  data into one interactive experience.
                </p>

                <div className="home-hero__actions">
                  <Link
                    to="/simulator"
                    className="primary-action"
                  >
                    Explore climate
                  </Link>

                  <a
                    href="#climate-layers"
                    className="secondary-action"
                  >
                    Discover Weathif
                  </a>
                </div>
              </div>
            </div>

            <div className="climate-cinema">
              <video
                className="climate-cinema__video"
                autoPlay
                muted
                loop
                playsInline
                preload="metadata"
                poster="/images/climate-hero-poster.jpg"
                aria-hidden="true"
              >
                <source
                  src="/videos/climate-hero.mp4"
                  type="video/mp4"
                />
              </video>

              <div className="climate-cinema__wash" />

              <div className="climate-cinema__top">
                <div>
                  <span className="climate-cinema__kicker">
                    Environmental observatory
                  </span>

                  <strong>
                    Place → Context → Scenario
                  </strong>
                </div>

                <span className="climate-cinema__status">
                  Interactive climate exploration
                </span>
              </div>

              <div className="climate-cinema__statement">
                <span>
                  Weather is the present.
                </span>

                <strong>
                  Climate gives it context.
                </strong>
              </div>

              <div className="climate-cinema__metrics">
                <div>
                  <span>
                    Observe
                  </span>

                  <strong>
                    Local conditions
                  </strong>
                </div>

                <div>
                  <span>
                    Compare
                  </span>

                  <strong>
                    Climate context
                  </strong>
                </div>

                <div>
                  <span>
                    Simulate
                  </span>

                  <strong>
                    Environmental change
                  </strong>
                </div>
              </div>

              <div
                className="climate-cinema__rings"
                aria-hidden="true"
              >
                <span />
                <span />
                <span />
              </div>
            </div>

            <div className="home-hero__foot">
              <span>
                Weather
              </span>

              <span>
                Climate memory
              </span>

              <span>
                Seasonal outlook
              </span>

              <span>
                ENSO
              </span>

              <span>
                Land + water
              </span>

              <span>
                Scenario modelling
              </span>
            </div>
          </div>
        </section>

        {/* =========================
            What Weathif does
        ========================= */}

        <section
          className="home-intro"
          id="how-it-works"
        >
          <div className="page-shell">
            <div className="home-intro__header">
              <div>
                <p className="eyebrow">
                  Observe. Understand. Simulate.
                </p>

                <h2>
                  More than a weather forecast.
                </h2>
              </div>

              <div className="home-intro__copy">
                <p>
                  Weather tells you what is happening now.
                  Weathif adds historical, environmental and
                  seasonal context around that observation.
                </p>

                <p>
                  Then it lets you alter temperature and rainfall
                  to explore a transparent hypothetical climate
                  scenario.
                </p>
              </div>
            </div>

            <div className="home-intro__steps">
              <article className="home-step">
                <span className="home-step__number">
                  01
                </span>

                <h3>
                  Begin with place
                </h3>

                <p>
                  Search a real location or explore directly
                  through the interactive map.
                </p>
              </article>

              <article className="home-step">
                <span className="home-step__number">
                  02
                </span>

                <h3>
                  Build climate context
                </h3>

                <p>
                  Compare current conditions with recent,
                  historical, seasonal and environmental data.
                </p>
              </article>

              <article className="home-step">
                <span className="home-step__number">
                  03
                </span>

                <h3>
                  Ask what if
                </h3>

                <p>
                  Change temperature and rainfall to explore
                  defined environmental scenario thresholds.
                </p>
              </article>
            </div>
          </div>
        </section>

        {/* =========================
            Climate layers
        ========================= */}

        <section
          className="climate-layers"
          id="climate-layers"
        >
          <div className="page-shell">
            <div className="climate-layers__header">
              <div>
                <p className="eyebrow">
                  Inside the simulator
                </p>

                <h2>
                  Climate is not
                  <br />
                  one number.
                </h2>
              </div>

              <p>
                Weathif assembles multiple environmental layers
                around a location so you can move from a single
                weather observation toward a broader picture.
              </p>
            </div>

            <div className="climate-layers__grid">
              {/* Map */}

              <article className="climate-layer climate-layer--map">
                <div className="climate-layer__top">
                  <span>
                    Geographic context
                  </span>

                  <strong>
                    01
                  </strong>
                </div>

                <div
                  className="map-visual"
                  aria-hidden="true"
                >
                  <div className="map-visual__road map-visual__road--one" />
                  <div className="map-visual__road map-visual__road--two" />
                  <div className="map-visual__road map-visual__road--three" />

                  <span className="map-visual__pin" />
                </div>

                <div className="climate-layer__copy">
                  <h3>
                    Climate begins with place.
                  </h3>

                  <p>
                    Search, map and reverse-geocode real
                    locations.
                  </p>
                </div>
              </article>

              {/* Climate memory */}

              <article className="climate-layer climate-layer--memory">
                <div className="climate-layer__top">
                  <span>
                    Climate memory
                  </span>

                  <strong>
                    02
                  </strong>
                </div>

                <div
                  className="memory-visual"
                  aria-hidden="true"
                >
                  <div className="memory-visual__group">
                    <div className="memory-visual__bar memory-visual__bar--recent" />

                    <span>
                      Recent
                    </span>
                  </div>

                  <div className="memory-visual__group">
                    <div className="memory-visual__bar memory-visual__bar--history" />

                    <span>
                      Historical
                    </span>
                  </div>
                </div>

                <div className="climate-layer__copy">
                  <h3>
                    Recent conditions, in context.
                  </h3>

                  <p>
                    Compare the recent period with the same
                    seasonal window across previous years.
                  </p>
                </div>
              </article>

              {/* Seasonal outlook */}

              <article className="climate-layer climate-layer--seasonal">
                <div className="climate-layer__top">
                  <span>
                    Seasonal outlook
                  </span>

                  <strong>
                    03
                  </strong>
                </div>

                <div
                  className="seasonal-visual"
                  aria-hidden="true"
                >
                  <svg
                    viewBox="0 0 520 170"
                    preserveAspectRatio="none"
                  >
                    <path
                      className="seasonal-visual__grid"
                      d="M0 45 H520 M0 85 H520 M0 125 H520"
                    />

                    <path
                      className="seasonal-visual__temperature"
                      d="M0 132 C70 125 90 102 145 91 C210 76 246 42 315 52 C375 60 418 32 520 44"
                    />

                    <path
                      className="seasonal-visual__rain"
                      d="M0 38 C68 48 105 56 155 76 C205 96 230 132 300 129 C363 126 407 94 520 106"
                    />
                  </svg>
                </div>

                <div className="climate-layer__copy">
                  <h3>
                    Looking beyond today.
                  </h3>

                  <p>
                    Explore monthly temperature and rainfall
                    anomaly signals from seasonal modelling.
                  </p>
                </div>
              </article>

              {/* ENSO */}

              <article className="climate-layer climate-layer--enso">
                <div className="climate-layer__top">
                  <span>
                    Global climate driver
                  </span>

                  <strong>
                    04
                  </strong>
                </div>

                <div className="enso-visual">
                  <div className="enso-visual__labels">
                    <span>
                      La Niña
                    </span>

                    <span>
                      Neutral
                    </span>

                    <span>
                      El Niño
                    </span>
                  </div>

                  <div
                    className="enso-visual__scale"
                    aria-hidden="true"
                  >
                    <span />
                  </div>

                  <p>
                    Live Pacific climate context is retrieved
                    in the simulator.
                  </p>
                </div>

                <div className="climate-layer__copy">
                  <h3>
                    The Pacific sends a signal.
                  </h3>

                  <p>
                    Follow NOAA ENSO advisories and major
                    Pacific climate indices.
                  </p>
                </div>
              </article>

              {/* Land and water */}

              <article className="climate-layer climate-layer--land">
                <div className="climate-layer__top">
                  <span>
                    Land + water
                  </span>

                  <strong>
                    05
                  </strong>
                </div>

                <div
                  className="soil-visual"
                  aria-hidden="true"
                >
                  <div className="soil-visual__surface">
                    <span>
                      Surface
                    </span>
                  </div>

                  <div className="soil-visual__root">
                    <span>
                      Root zone
                    </span>
                  </div>

                  <div className="soil-visual__deep">
                    <span>
                      Soil
                    </span>
                  </div>
                </div>

                <div className="climate-layer__copy">
                  <h3>
                    Below the weather.
                  </h3>

                  <p>
                    Explore soil moisture, soil temperature,
                    atmospheric drying demand and
                    evapotranspiration.
                  </p>
                </div>
              </article>

              {/* Scenario lab */}

              <article className="climate-layer climate-layer--scenario">
                <div className="climate-layer__top">
                  <span>
                    Scenario lab
                  </span>

                  <strong>
                    06
                  </strong>
                </div>

                <div
                  className="scenario-visual"
                  aria-hidden="true"
                >
                  <div className="scenario-visual__metric">
                    <span>
                      Temperature
                    </span>

                    <div className="scenario-visual__track">
                      <span className="scenario-visual__temperature" />
                    </div>
                  </div>

                  <div className="scenario-visual__metric">
                    <span>
                      Rainfall
                    </span>

                    <div className="scenario-visual__track">
                      <span className="scenario-visual__rain" />
                    </div>
                  </div>

                  <div className="scenario-visual__flow">
                    <span>
                      Current
                    </span>

                    <strong>
                      →
                    </strong>

                    <span>
                      Scenario
                    </span>
                  </div>
                </div>

                <div className="climate-layer__copy">
                  <h3>
                    Change the variables.
                  </h3>

                  <p>
                    Build a hypothetical temperature and rainfall
                    scenario from the observed baseline.
                  </p>
                </div>
              </article>
            </div>

            <div className="climate-layers__footer">
              <p>
                Each layer provides context. None is presented
                as a deterministic prediction of local future
                weather.
              </p>

              <Link
                to="/simulator"
                className="climate-layers__link"
              >
                Open the full simulator →
              </Link>
            </div>
          </div>
        </section>

        {/* =========================
            Environmental story
        ========================= */}

        <section className="environment-story">
          <div className="page-shell">
            <div className="environment-story__header">
              <div>
                <p className="eyebrow">
                  Environmental change
                </p>

                <h2>
                  One place.
                  <br />
                  Different environmental futures.
                </h2>
              </div>

              <div className="environment-story__copy">
                <p>
                  Temperature and rainfall help shape the
                  landscapes, water systems and vegetation
                  around us.
                </p>

                <p>
                  Weathif lets you experiment with those
                  variables and observe how a hypothetical
                  scenario crosses defined environmental
                  thresholds.
                </p>
              </div>
            </div>

            <div className="environment-gallery">
              <figure className="environment-image environment-image--lush">
                <img
                  src={lushEnvironment}
                  alt="Green agricultural landscape surrounding a river"
                />

                <figcaption>
                  <span>
                    Water + vegetation
                  </span>

                  <strong>
                    Landscapes under wetter conditions
                  </strong>
                </figcaption>
              </figure>

              <figure className="environment-image environment-image--drought">
                <img
                  src={droughtEnvironment}
                  alt="Cracked dry earth in a drought-affected landscape"
                />

                <figcaption>
                  <span>
                    Dryness + heat
                  </span>

                  <strong>
                    Landscapes under water stress
                  </strong>
                </figcaption>
              </figure>

              <figure className="environment-image environment-image--rain">
                <img
                  src={rainEnvironment}
                  alt="Heavy rainfall and storm clouds over agricultural land"
                />

                <figcaption>
                  <span>
                    Rainfall + saturation
                  </span>

                  <strong>
                    Landscapes under intense rainfall
                  </strong>
                </figcaption>
              </figure>
            </div>

            <div className="environment-story__footer">
              <p>
                These photographs are illustrative environmental
                references. They are not generated predictions of
                Weathif scenarios.
              </p>

              <Link
                to="/methodology"
                className="environment-story__link"
              >
                Read the methodology →
              </Link>
            </div>
          </div>
        </section>

        {/* =========================
            Final CTA
        ========================= */}

        <section className="home-final">
          <div className="page-shell">
            <div className="home-final__inner">
              <div>
                <p className="eyebrow">
                  Enter the simulator
                </p>

                <h2>
                  Change the climate variables.
                  <br />
                  See what shifts.
                </h2>
              </div>

              <div className="home-final__action">
                <p>
                  Choose a real place, understand its
                  environmental context and build your own
                  hypothetical scenario.
                </p>

                <Link
                  to="/simulator"
                  className="home-final__button"
                >
                  Explore climate
                  <span aria-hidden="true">
                    →
                  </span>
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export default Home;