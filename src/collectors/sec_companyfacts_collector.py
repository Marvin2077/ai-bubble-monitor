"""Optional SEC CompanyFacts collector.

Fetches one metric from SEC CompanyFacts JSON endpoint.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Optional

from src.models import Observation


def collect_sec_latest_observation(
    indicator_id: str,
    cik: str,
    taxonomy: str,
    tag: str,
    unit: str = "USD",
    confidence: float = 0.75,
) -> Optional[Observation]:
    """Fetch latest SEC fact for a given CIK/tag.

    Returns None on failure so dashboard never breaks.
    """
    cik10 = str(cik).zfill(10)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "ai-bubble-monitor/0.1 (local research)"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return None

    try:
        entries = payload["facts"][taxonomy][tag]["units"][unit]
        entries = [e for e in entries if "val" in e and ("end" in e or "fy" in e)]
        if not entries:
            return None
        latest = sorted(entries, key=lambda x: x.get("end", "0000-00-00"))[-1]
        end = latest.get("end", "")
        month = end[:7] if len(end) >= 7 else f"{latest.get('fy', 2000)}-12"
        return Observation(
            indicator_id=indicator_id,
            date=month,
            value=float(latest["val"]),
            source_url=url,
            notes=f"Auto-collected SEC {taxonomy}:{tag} {unit}",
            confidence=confidence,
            input_type="observed",
        )
    except (KeyError, TypeError, ValueError):
        return None
