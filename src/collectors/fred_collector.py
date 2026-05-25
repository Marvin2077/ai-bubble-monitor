"""Optional FRED collector (no API key required).

Uses public CSV endpoint:
https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES_ID
"""

from __future__ import annotations

import csv
import io
import urllib.error
import urllib.request
from typing import Optional

from src.models import Observation


def _to_yyyymm(date_str: str) -> str:
    return date_str[:7]


def collect_fred_latest_observation(indicator_id: str, series_id: str, confidence: float = 0.7) -> Optional[Observation]:
    """Fetch latest valid value from FRED CSV and map to one Observation.

    Returns None on network/source failure to keep app resilient.
    """
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            content = resp.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError, ValueError):
        return None

    rows = list(csv.DictReader(io.StringIO(content)))
    rows = [r for r in rows if r.get(series_id) not in (None, "", ".")]
    if not rows:
        return None
    last = rows[-1]
    return Observation(
        indicator_id=indicator_id,
        date=_to_yyyymm(last["DATE"]),
        value=float(last[series_id]),
        source_url=url,
        notes=f"Auto-collected from FRED series {series_id}",
        confidence=confidence,
        input_type="observed",
    )
