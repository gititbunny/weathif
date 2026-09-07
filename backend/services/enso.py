import re
from datetime import datetime, timedelta, timezone
import requests
from bs4 import BeautifulSoup


CPC_DISCUSSION_URL = (
    "https://www.cpc.ncep.noaa.gov/"
    "products/analysis_monitoring/"
    "enso_advisory/ensodisc.html"
)

PSL_DASHBOARD_URL = (
    "https://psl.noaa.gov/enso/dashboard.html"
)

REQUEST_HEADERS = {
    "User-Agent": (
        "Weathif Climate Scenario Simulator "
        "(environmental education project)"
    )
}

CACHE_DURATION = timedelta(hours=6)

_cache = {
    "data": None,
    "updated_at": None,
}


def _fetch_html(url: str):
    try:
        response = requests.get(
            url,
            headers=REQUEST_HEADERS,
            timeout=20,
        )

        response.raise_for_status()

        return response.text

    except requests.RequestException as exc:
        raise RuntimeError(
            "ENSO climate-driver data is temporarily unavailable."
        ) from exc


def _extract_metric(
    soup: BeautifulSoup,
    metric_name: str,
):
    heading = soup.find(
        lambda tag: (
            tag.name in {"h3", "h4"}
            and tag.get_text(
                " ",
                strip=True,
            ) == metric_name
        )
    )

    if heading is None:
        return None

    row = heading.find_parent("tr")

    if row is None:
        return None

    cells = row.find_all(["td", "th"])

    values = [
        cell.get_text(
            " ",
            strip=True,
        )
        for cell in cells
    ]

    date_pattern = re.compile(
        r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        r"\s+\d{4}$"
    )

    date_index = None
    date_value = None

    for index in range(
        len(values) - 1,
        -1,
        -1,
    ):
        if date_pattern.match(values[index]):
            date_index = index
            date_value = values[index]
            break

    if date_index is None:
        return None

    metric_value = None

    for index in range(
        date_index - 1,
        -1,
        -1,
    ):
        candidate = (
            values[index]
            .replace("−", "-")
            .replace("+", "")
            .strip()
        )

        try:
            metric_value = float(candidate)
            break

        except ValueError:
            continue

    if metric_value is None:
        return None

    return {
        "value": round(metric_value, 2),
        "date": date_value,
    }


def _fetch_indices():
    html = _fetch_html(
        PSL_DASHBOARD_URL
    )

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    return {
        "nino_34": _extract_metric(
            soup,
            "Niño 3.4",
        ),
        "oni": _extract_metric(
            soup,
            "ONI",
        ),
        "mei_v2": _extract_metric(
            soup,
            "MEI V2",
        ),
    }


def _extract_first_sentence(text: str):
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip(),
    )

    if not sentences:
        return None

    return sentences[0].strip()


def _fetch_official_discussion():
    html = _fetch_html(
        CPC_DISCUSSION_URL
    )

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    text = soup.get_text(
        " ",
        strip=True,
    )

    status_match = re.search(
        r"ENSO Alert System Status:\s*"
        r"(.*?)\s*Synopsis:",
        text,
        flags=re.IGNORECASE,
    )

    status = (
        status_match.group(1).strip()
        if status_match
        else None
    )

    synopsis = None

    if "Synopsis:" in text:
        synopsis_text = text.split(
            "Synopsis:",
            1,
        )[1]

        synopsis = _extract_first_sentence(
            synopsis_text
        )

    date_match = re.search(
        r"\b("
        r"\d{1,2}\s+"
        r"(?:January|February|March|April|May|June|"
        r"July|August|September|October|November|December)"
        r"\s+\d{4}"
        r")\b",
        text,
    )

    issued = (
        date_match.group(1)
        if date_match
        else None
    )

    combined_text = " ".join(
        item
        for item in [status, synopsis]
        if item
    )

    if "El Niño" in combined_text:
        phase = "El Niño"

    elif "La Niña" in combined_text:
        phase = "La Niña"

    else:
        phase = "ENSO-neutral"

    lowered = combined_text.lower()

    if "strengthening" in lowered:
        trend = "Strengthening"

    elif "weakening" in lowered:
        trend = "Weakening"

    elif "develop" in lowered:
        trend = "Developing"

    else:
        trend = "Current conditions"

    return {
        "phase": phase,
        "status": status,
        "trend": trend,
        "issued": issued,
        "summary": synopsis,
    }


def fetch_enso_context():
    now = datetime.now(timezone.utc)

    if (
        _cache["data"] is not None
        and _cache["updated_at"] is not None
        and now - _cache["updated_at"]
        < CACHE_DURATION
    ):
        return _cache["data"]

    discussion = _fetch_official_discussion()
    indices = _fetch_indices()

    nino_34 = indices.get("nino_34")
    oni = indices.get("oni")
    mei = indices.get("mei_v2")

    result = {
        "phase": {
            "name": discussion["phase"],
            "status": discussion["status"],
            "trend": discussion["trend"],
        },
        "official_outlook": {
            "issued": discussion["issued"],
            "summary": discussion["summary"],
        },
        "indices": {
            "nino_34": {
                "value_c": (
                    nino_34["value"]
                    if nino_34
                    else None
                ),
                "date": (
                    nino_34["date"]
                    if nino_34
                    else None
                ),
            },
            "oni": {
                "value_c": (
                    oni["value"]
                    if oni
                    else None
                ),
                "date": (
                    oni["date"]
                    if oni
                    else None
                ),
            },
            "mei_v2": {
                "value": (
                    mei["value"]
                    if mei
                    else None
                ),
                "date": (
                    mei["date"]
                    if mei
                    else None
                ),
            },
        },
        "context": (
            "ENSO is a large-scale interaction between the "
            "tropical Pacific Ocean and atmosphere that can "
            "influence seasonal climate patterns around the world."
        ),
        "location_note": (
            "ENSO does not determine weather at a specific "
            "location. Local impacts vary by region, season "
            "and individual event."
        ),
        "sources": {
            "advisory": (
                "NOAA Climate Prediction Center"
            ),
            "indices": (
                "NOAA Physical Sciences Laboratory"
            ),
        },
        "retrieved_at": (
            now.isoformat().replace("+00:00", "Z")
        ),
    }

    _cache["data"] = result
    _cache["updated_at"] = now

    return result
