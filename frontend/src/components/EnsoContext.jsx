import "../styles/enso-context.css";


function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}


function getScalePosition(value) {
  const minimum = -2.5;
  const maximum = 2.5;

  const safeValue = clamp(
    value ?? 0,
    minimum,
    maximum
  );

  return (
    ((safeValue - minimum) /
      (maximum - minimum)) *
    100
  );
}


function signedValue(value, suffix = "") {
  if (value === null || value === undefined) {
    return "—";
  }

  const prefix = value > 0 ? "+" : "";

  return `${prefix}${value}${suffix}`;
}


function EnsoContext({ data }) {
  if (!data) {
    return null;
  }

  const ninoValue =
    data.indices.nino_34.value_c;

  const markerPosition =
    getScalePosition(ninoValue);

  return (
    <section className="enso-context">
      <div className="page-shell">
        <div className="enso-context__header">
          <div>
            <p className="eyebrow">
              Global climate driver
            </p>

            <h2>
              The Pacific is
              <br />
              sending a signal.
            </h2>
          </div>

          <div className="enso-status">
            <span className="enso-status__label">
              Current ENSO phase
            </span>

            <strong>
              {data.phase.name}
            </strong>

            <div className="enso-status__meta">
              <span>
                {data.phase.status}
              </span>

              <span>
                {data.phase.trend}
              </span>
            </div>
          </div>
        </div>

        <div className="enso-field">
          <div
            className="enso-field__rings"
            aria-hidden="true"
          />

          <div className="enso-field__top">
            <div>
              <span>
                Tropical Pacific
              </span>

              <strong>
                ENSO signal
              </strong>
            </div>

            <div>
              <span>
                NOAA outlook
              </span>

              <strong>
                {data.official_outlook.issued ||
                  "Current advisory"}
              </strong>
            </div>
          </div>

          <div className="enso-scale">
            <div className="enso-scale__labels">
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

            <div className="enso-scale__track">
              <div className="enso-scale__cold" />
              <div className="enso-scale__neutral" />
              <div className="enso-scale__warm" />

              <div
                className="enso-scale__marker"
                style={{
                  left: `${markerPosition}%`,
                }}
              >
                <span>
                  Niño 3.4
                </span>

                <strong>
                  {signedValue(
                    ninoValue,
                    "°C"
                  )}
                </strong>
              </div>
            </div>

            <div className="enso-scale__range">
              <span>
                -2.5°C
              </span>

              <span>
                0
              </span>

              <span>
                +2.5°C
              </span>
            </div>
          </div>

          <div className="enso-indices">
            <article>
              <span>
                Niño 3.4
              </span>

              <strong>
                {signedValue(
                  data.indices.nino_34.value_c,
                  "°C"
                )}
              </strong>

              <small>
                {data.indices.nino_34.date}
              </small>
            </article>

            <article>
              <span>
                ONI
              </span>

              <strong>
                {signedValue(
                  data.indices.oni.value_c,
                  "°C"
                )}
              </strong>

              <small>
                {data.indices.oni.date}
              </small>
            </article>

            <article>
              <span>
                MEI V2
              </span>

              <strong>
                {signedValue(
                  data.indices.mei_v2.value
                )}
              </strong>

              <small>
                {data.indices.mei_v2.date}
              </small>
            </article>
          </div>
        </div>

        <div className="enso-outlook">
          <div className="enso-outlook__signal">
            <span>
              Official outlook
            </span>

            <p>
              {data.official_outlook.summary}
            </p>
          </div>

          <div className="enso-outlook__context">
            <span>
              What this means for Weathif
            </span>

            <p>
              ENSO provides global climate context,
              while Weathif&apos;s local conditions and
              seasonal outlook remain specific to the
              selected location.
            </p>
          </div>
        </div>

        <div className="enso-context__footer">
          <p>
            {data.location_note}
          </p>

          <span>
            {data.sources.advisory}
            {" · "}
            {data.sources.indices}
          </span>
        </div>
      </div>
    </section>
  );
}

export default EnsoContext;