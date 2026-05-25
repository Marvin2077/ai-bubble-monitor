from datetime import datetime

from src.models import Observation


def upsert_observation(conn, obs: Observation):
    conn.execute(
        """INSERT INTO observations(indicator_id,date,value,raw_value,source_url,notes,confidence,input_type,created_at)
    VALUES(?,?,?,?,?,?,?,?,?)
    ON CONFLICT(indicator_id,date) DO UPDATE SET value=excluded.value, raw_value=excluded.raw_value, source_url=excluded.source_url, notes=excluded.notes, confidence=excluded.confidence, input_type=excluded.input_type""",
        (
            obs.indicator_id,
            obs.date,
            obs.value,
            obs.raw_value,
            obs.source_url,
            obs.notes,
            obs.confidence,
            obs.input_type,
            datetime.utcnow().isoformat(),
        ),
    )
    conn.commit()


def bulk_upsert_observations(conn, observations: list[Observation]) -> int:
    count = 0
    for obs in observations:
        upsert_observation(conn, obs)
        count += 1
    return count
