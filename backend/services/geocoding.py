from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import Nominatim


geolocator = Nominatim(
    user_agent="weathif-climate-scenario-simulator"
)


def search_location(query: str):
    clean_query = query.strip()

    if not clean_query:
        return None

    try:
        location = geolocator.geocode(
            clean_query,
            exactly_one=True,
            addressdetails=True,
            timeout=10,
        )

    except (GeocoderTimedOut, GeocoderServiceError) as exc:
        raise RuntimeError(
            "The location service is temporarily unavailable."
        ) from exc

    if location is None:
        return None

    raw_data = location.raw

    return {
        "name": raw_data.get(
            "display_name",
            location.address,
        ),
        "latitude": round(float(location.latitude), 6),
        "longitude": round(float(location.longitude), 6),
        "type": raw_data.get("type"),
        "address": raw_data.get("address", {}),
    }


def reverse_location(latitude: float, longitude: float):
    try:
        location = geolocator.reverse(
            (latitude, longitude),
            exactly_one=True,
            addressdetails=True,
            timeout=10,
        )

    except (GeocoderTimedOut, GeocoderServiceError) as exc:
        raise RuntimeError(
            "The location service is temporarily unavailable."
        ) from exc

    if location is None:
        return None

    raw_data = location.raw

    return {
        "name": raw_data.get(
            "display_name",
            location.address,
        ),
        "latitude": round(float(location.latitude), 6),
        "longitude": round(float(location.longitude), 6),
        "type": raw_data.get("type"),
        "address": raw_data.get("address", {}),
    }