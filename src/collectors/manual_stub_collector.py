"""Manual public evidence registry collector.

Reads curated public observations from a CSV file and turns them into Observation records.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from src.models import Observation


def collect_manual_registry(path: str = "data/manual_evidence_registry.csv") -> List[Observation]:
    p = Path(path)
    if not p.exists():
        return []

    out: List[Observation] = []
    with p.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                out.append(
                    Observation(
                        indicator_id=row["indicator_id"],
                        date=row["date"],
                        value=float(row["value"]),
                        source_url=row.get("source_url") or None,
                        notes=row.get("notes") or "Manual public evidence registry",
                        confidence=float(row.get("confidence", 0.6)),
                        input_type=row.get("input_type", "manual"),
                    )
                )
            except Exception:
                continue
    return out
