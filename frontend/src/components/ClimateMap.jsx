import { useEffect } from "react";
import {
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  useMap,
  useMapEvents,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";
import "../styles/climate-map.css";


function RecenterMap({ latitude, longitude }) {
  const map = useMap();

  useEffect(() => {
    map.flyTo(
      [latitude, longitude],
      10,
      {
        duration: 1.2,
      }
    );
  }, [latitude, longitude, map]);

  return null;
}


function MapClickHandler({
  onLocationSelect,
  disabled,
}) {
  useMapEvents({
    click(event) {
      if (disabled) {
        return;
      }

      onLocationSelect(
        event.latlng.lat,
        event.latlng.lng
      );
    },
  });

  return null;
}


function ClimateMap({
  location,
  onLocationSelect,
  loading = false,
}) {
  if (!location) {
    return null;
  }

  const position = [
    location.latitude,
    location.longitude,
  ];

  return (
    <section className="climate-map-section">
      <div className="page-shell">
        <div className="climate-map-section__header">
          <div>
            <p className="eyebrow">
              Geographic context
            </p>

            <h2>
              Climate begins
              <br />
              with place.
            </h2>
          </div>

          <div className="climate-map-section__intro">
            <p>
              Explore the geographic setting of the selected
              location. Weathif uses these coordinates to
              retrieve its environmental data.
            </p>

            <p>
              <strong>
                Click anywhere on the map
              </strong>{" "}
              to explore conditions at another location.
            </p>
          </div>
        </div>

        <div className="climate-map-shell">
          <div className="climate-map__wrapper">
            <MapContainer
              center={position}
              zoom={10}
              scrollWheelZoom
              className="climate-map"
            >
              <TileLayer
                attribution="&copy; OpenStreetMap contributors"
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />

              <Marker position={position}>
                <Popup>
                  <strong>
                    {location.name}
                  </strong>

                  <br />

                  {location.latitude},{" "}
                  {location.longitude}
                </Popup>
              </Marker>

              <RecenterMap
                latitude={location.latitude}
                longitude={location.longitude}
              />

              <MapClickHandler
                onLocationSelect={onLocationSelect}
                disabled={loading}
              />
            </MapContainer>

            {loading && (
              <div
                className="climate-map__loading"
                role="status"
              >
                <span>
                  Loading environmental data…
                </span>
              </div>
            )}
          </div>

          <div className="climate-map-meta">
            <div>
              <span>
                Latitude
              </span>

              <strong>
                {location.latitude}
              </strong>
            </div>

            <div>
              <span>
                Longitude
              </span>

              <strong>
                {location.longitude}
              </strong>
            </div>

            <div>
              <span>
                Map interaction
              </span>

              <strong>
                Click to explore
              </strong>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default ClimateMap;