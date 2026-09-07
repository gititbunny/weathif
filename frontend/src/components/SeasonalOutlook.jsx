import {
  CartesianGrid,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import "../styles/seasonal-outlook.css";


function formatMonth(dateString) {
  const [year, month] = dateString
    .split("-")
    .map(Number);

  const date = new Date(
    Date.UTC(year, month - 1, 1)
  );

  return date.toLocaleDateString("en-ZA", {
    month: "short",
    timeZone: "UTC",
  });
}


function formatFullMonth(dateString) {
  const [year, month] = dateString
    .split("-")
    .map(Number);

  const date = new Date(
    Date.UTC(year, month - 1, 1)
  );

  return date.toLocaleDateString("en-ZA", {
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  });
}


function signedValue(value, suffix = "") {
  if (value === null || value === undefined) {
    return "—";
  }

  const prefix = value > 0 ? "+" : "";

  return `${prefix}${value}${suffix}`;
}


function findStrongestSignal(months, key) {
  const validMonths = months.filter(
    (month) =>
      month[key] !== null &&
      month[key] !== undefined
  );

  if (!validMonths.length) {
    return null;
  }

  return validMonths.reduce((strongest, month) => {
    if (
      Math.abs(month[key]) >
      Math.abs(strongest[key])
    ) {
      return month;
    }

    return strongest;
  });
}


function SeasonalOutlook({ data }) {
  if (!data?.months?.length) {
    return null;
  }

  const chartData = data.months.map((month) => ({
    month: formatMonth(month.month),
    fullMonth: formatFullMonth(month.month),

    temperature:
      month.temperature_anomaly_c,

    rainfall:
      month.precipitation_anomaly_mm,

    temperatureContext:
      month.temperature_context,

    rainfallContext:
      month.precipitation_context,
  }));

  const strongestTemperature = findStrongestSignal(
    data.months,
    "temperature_anomaly_c"
  );

  const strongestRainfall = findStrongestSignal(
    data.months,
    "precipitation_anomaly_mm"
  );

  return (
    <section className="seasonal-outlook">
      <div className="page-shell">
        <div className="seasonal-outlook__header">
          <div>
            <p className="eyebrow">
              Seasonal outlook
            </p>

            <h2>
              Looking beyond
              <br />
              today.
            </h2>
          </div>

          <div className="seasonal-outlook__summary">
            {strongestTemperature && (
              <div className="outlook-signal outlook-signal--temperature">
                <span>
                  Strongest temperature signal
                </span>

                <strong>
                  {formatFullMonth(
                    strongestTemperature.month
                  )}
                </strong>

                <p>
                  {signedValue(
                    strongestTemperature
                      .temperature_anomaly_c,
                    "°C"
                  )}
                  {" · "}
                  {
                    strongestTemperature
                      .temperature_context
                  }
                </p>
              </div>
            )}

            {strongestRainfall && (
              <div className="outlook-signal outlook-signal--rainfall">
                <span>
                  Strongest rainfall signal
                </span>

                <strong>
                  {formatFullMonth(
                    strongestRainfall.month
                  )}
                </strong>

                <p>
                  {signedValue(
                    strongestRainfall
                      .precipitation_anomaly_mm,
                    " mm"
                  )}
                  {" · "}
                  {
                    strongestRainfall
                      .precipitation_context
                  }
                </p>
              </div>
            )}
          </div>
        </div>

        <div className="seasonal-charts">
          <article className="seasonal-chart-card seasonal-chart-card--temperature">
            <div className="seasonal-chart-card__header">
              <div>
                <span>
                  Temperature tendency
                </span>

                <h3>
                  Warmer or cooler?
                </h3>
              </div>

              <div className="seasonal-chart-key">
                <i />
                anomaly °C
              </div>
            </div>

            <div
              className="seasonal-chart"
              aria-label="Monthly seasonal temperature anomaly chart"
            >
              <ResponsiveContainer
                width="100%"
                height="100%"
              >
                <LineChart
                  data={chartData}
                  margin={{
                    top: 18,
                    right: 18,
                    left: -12,
                    bottom: 4,
                  }}
                >
                  <CartesianGrid
                    vertical={false}
                    stroke="rgba(255,255,255,0.08)"
                  />

                  <XAxis
                    dataKey="month"
                    axisLine={false}
                    tickLine={false}
                    tick={{
                      fill: "rgba(255,255,255,0.56)",
                      fontSize: 12,
                    }}
                  />

                  <YAxis
                    axisLine={false}
                    tickLine={false}
                    width={46}
                    tick={{
                      fill: "rgba(255,255,255,0.42)",
                      fontSize: 11,
                    }}
                    tickFormatter={(value) =>
                      `${value}°`
                    }
                  />

                  <ReferenceLine
                    y={0}
                    stroke="rgba(255,255,255,0.38)"
                    strokeDasharray="4 4"
                  />

                  <Tooltip
                    contentStyle={{
                      background: "#10281e",
                      border:
                        "1px solid rgba(255,255,255,0.14)",
                      borderRadius: "12px",
                      color: "#ffffff",
                    }}
                    labelStyle={{
                      color:
                        "rgba(255,255,255,0.65)",
                    }}
                    formatter={(value) => [
                      signedValue(value, "°C"),
                      "Temperature anomaly",
                    ]}
                  />

                  <Line
                    type="monotone"
                    dataKey="temperature"
                    stroke="#df8a62"
                    strokeWidth={3}
                    dot={{
                      r: 5,
                      fill: "#df8a62",
                      stroke: "#23362f",
                      strokeWidth: 2,
                    }}
                    activeDot={{
                      r: 7,
                    }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="seasonal-chart-card__scale">
              <span>
                Cooler
              </span>

              <span>
                Model climatology
              </span>

              <span>
                Warmer
              </span>
            </div>
          </article>

          <article className="seasonal-chart-card seasonal-chart-card--rainfall">
            <div className="seasonal-chart-card__header">
              <div>
                <span>
                  Rainfall tendency
                </span>

                <h3>
                  Wetter or drier?
                </h3>
              </div>

              <div className="seasonal-chart-key">
                <i />
                anomaly mm
              </div>
            </div>

            <div
              className="seasonal-chart"
              aria-label="Monthly seasonal rainfall anomaly chart"
            >
              <ResponsiveContainer
                width="100%"
                height="100%"
              >
                <LineChart
                  data={chartData}
                  margin={{
                    top: 18,
                    right: 18,
                    left: -8,
                    bottom: 4,
                  }}
                >
                  <CartesianGrid
                    vertical={false}
                    stroke="rgba(255,255,255,0.08)"
                  />

                  <XAxis
                    dataKey="month"
                    axisLine={false}
                    tickLine={false}
                    tick={{
                      fill: "rgba(255,255,255,0.56)",
                      fontSize: 12,
                    }}
                  />

                  <YAxis
                    axisLine={false}
                    tickLine={false}
                    width={50}
                    tick={{
                      fill: "rgba(255,255,255,0.42)",
                      fontSize: 11,
                    }}
                    tickFormatter={(value) =>
                      `${value}`
                    }
                  />

                  <ReferenceLine
                    y={0}
                    stroke="rgba(255,255,255,0.38)"
                    strokeDasharray="4 4"
                  />

                  <Tooltip
                    contentStyle={{
                      background: "#10281e",
                      border:
                        "1px solid rgba(255,255,255,0.14)",
                      borderRadius: "12px",
                      color: "#ffffff",
                    }}
                    labelStyle={{
                      color:
                        "rgba(255,255,255,0.65)",
                    }}
                    formatter={(value) => [
                      signedValue(value, " mm"),
                      "Rainfall anomaly",
                    ]}
                  />

                  <Line
                    type="monotone"
                    dataKey="rainfall"
                    stroke="#8fc0d1"
                    strokeWidth={3}
                    dot={{
                      r: 5,
                      fill: "#8fc0d1",
                      stroke: "#23362f",
                      strokeWidth: 2,
                    }}
                    activeDot={{
                      r: 7,
                    }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="seasonal-chart-card__scale">
              <span>
                Drier
              </span>

              <span>
                Model climatology
              </span>

              <span>
                Wetter
              </span>
            </div>
          </article>
        </div>

        <div className="seasonal-months">
          {chartData.map((month) => (
            <div
              className="seasonal-month-summary"
              key={month.fullMonth}
            >
              <strong>
                {month.month}
              </strong>

              <span className="seasonal-month-summary__temperature">
                {signedValue(
                  month.temperature,
                  "°C"
                )}
              </span>

              <span className="seasonal-month-summary__rainfall">
                {signedValue(
                  month.rainfall,
                  " mm"
                )}
              </span>
            </div>
          ))}
        </div>

        <div className="seasonal-outlook__footer">
          <span>
            {data.model}
          </span>

          <p>
            Broad seasonal tendency only — not a precise
            local weather forecast.
          </p>

          <span>
            Source: {data.source}
          </span>
        </div>
      </div>
    </section>
  );
}

export default SeasonalOutlook;