import {
  Bar,
  BarChart,
  Cell,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import "../styles/climate-memory.css";


function formatDate(dateString) {
  const [year, month, day] = dateString
    .split("-")
    .map(Number);

  const date = new Date(
    Date.UTC(year, month - 1, day)
  );

  return date.toLocaleDateString("en-ZA", {
    day: "numeric",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  });
}


function signedValue(value, suffix = "") {
  if (value === null || value === undefined) {
    return "Unavailable";
  }

  const prefix = value > 0 ? "+" : "";

  return `${prefix}${value}${suffix}`;
}


function ClimateMemory({ data }) {
  if (!data) {
    return null;
  }

  const temperatureData = [
    {
      label: "Recent",
      value: data.recent.mean_temperature_c,
      type: "recent",
    },
    {
      label: `${data.historical_comparison.years_used}-year avg`,
      value:
        data.historical_comparison.mean_temperature_c,
      type: "historical",
    },
  ];

  const rainfallData = [
    {
      label: "Recent",
      value: data.recent.rainfall_total_mm,
      type: "recent",
    },
    {
      label: `${data.historical_comparison.years_used}-year avg`,
      value:
        data.historical_comparison.rainfall_total_mm,
      type: "historical",
    },
  ];

  return (
    <section className="climate-memory">
      <div className="page-shell">
        <div className="climate-memory__top">
          <div>
            <p className="eyebrow">
              Climate memory
            </p>

            <h2>
              Recent conditions,
              <br />
              in context.
            </h2>
          </div>

          <div className="climate-memory__period">
            <span>
              Comparing
            </span>

            <strong>
              {formatDate(data.period.start_date)}
              {" — "}
              {formatDate(data.period.end_date)}
            </strong>

            <small>
              against the same seasonal window from{" "}
              {data.historical_comparison.first_year}
              {"–"}
              {data.historical_comparison.last_year}
            </small>
          </div>
        </div>

        <div className="climate-memory__visuals">
          <article className="memory-panel memory-panel--temperature">
            <div className="memory-panel__header">
              <div>
                <span className="memory-panel__label">
                  Temperature
                </span>

                <h3>
                  {data.difference.temperature_context}
                </h3>
              </div>

              <strong className="memory-panel__change">
                {signedValue(
                  data.difference.temperature_c,
                  "°C"
                )}
              </strong>
            </div>

            <div className="memory-chart">
              <ResponsiveContainer
                width="100%"
                height="100%"
              >
                <BarChart
                  data={temperatureData}
                  margin={{
                    top: 24,
                    right: 12,
                    left: 0,
                    bottom: 0,
                  }}
                >
                  <XAxis
                    dataKey="label"
                    axisLine={false}
                    tickLine={false}
                    tick={{
                      fill: "#647069",
                      fontSize: 12,
                    }}
                  />

                  <YAxis hide />

                  <Tooltip
                    cursor={{
                      fill: "rgba(207, 113, 71, 0.06)",
                    }}
                    formatter={(value) => [
                      `${value}°C`,
                      "Mean temperature",
                    ]}
                  />

                  <Bar
                    dataKey="value"
                    radius={[10, 10, 0, 0]}
                    maxBarSize={92}
                  >
                    {temperatureData.map((entry) => (
                      <Cell
                        key={entry.type}
                        fill={
                          entry.type === "recent"
                            ? "#cf7147"
                            : "#b8aa95"
                        }
                      />
                    ))}

                    <LabelList
                      dataKey="value"
                      position="top"
                      formatter={(value) => `${value}°C`}
                      fill="#18221d"
                      fontSize={14}
                      fontWeight={700}
                    />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="memory-panel__footer">
              <span>
                Recent 30-day mean
              </span>

              <span>
                Historical seasonal comparison
              </span>
            </div>
          </article>

          <article className="memory-panel memory-panel--rainfall">
            <div className="memory-panel__header">
              <div>
                <span className="memory-panel__label">
                  Rainfall
                </span>

                <h3>
                  {data.difference.rainfall_context}
                </h3>
              </div>

              <strong className="memory-panel__change">
                {signedValue(
                  data.difference.rainfall_percent,
                  "%"
                )}
              </strong>
            </div>

            <div className="memory-chart">
              <ResponsiveContainer
                width="100%"
                height="100%"
              >
                <BarChart
                  data={rainfallData}
                  margin={{
                    top: 24,
                    right: 12,
                    left: 0,
                    bottom: 0,
                  }}
                >
                  <XAxis
                    dataKey="label"
                    axisLine={false}
                    tickLine={false}
                    tick={{
                      fill: "#647069",
                      fontSize: 12,
                    }}
                  />

                  <YAxis hide />

                  <Tooltip
                    cursor={{
                      fill: "rgba(63, 127, 152, 0.06)",
                    }}
                    formatter={(value) => [
                      `${value} mm`,
                      "Rainfall",
                    ]}
                  />

                  <Bar
                    dataKey="value"
                    radius={[10, 10, 0, 0]}
                    maxBarSize={92}
                  >
                    {rainfallData.map((entry) => (
                      <Cell
                        key={entry.type}
                        fill={
                          entry.type === "recent"
                            ? "#4f91aa"
                            : "#b8aa95"
                        }
                      />
                    ))}

                    <LabelList
                      dataKey="value"
                      position="top"
                      formatter={(value) => `${value} mm`}
                      fill="#18221d"
                      fontSize={14}
                      fontWeight={700}
                    />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="memory-panel__footer">
              <span>
                Recent 30-day total
              </span>

              <span>
                Historical seasonal comparison
              </span>
            </div>
          </article>
        </div>

        <div className="climate-memory__note">
          <span>
            Historical context only — not a forecast or formal climate normal.
          </span>

          <span>
            Source: {data.source}
          </span>
        </div>
      </div>
    </section>
  );
}

export default ClimateMemory;