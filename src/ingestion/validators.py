from src.models import Observation

def validate_row(row: dict, indicator_ids: set[str]) -> Observation:
    if row['indicator_id'] not in indicator_ids:
        raise ValueError(f"unknown indicator_id: {row['indicator_id']}")
    return Observation(
        indicator_id=row['indicator_id'], date=row['date'], value=float(row['value']),
        source_url=row.get('source_url') or None, notes=row.get('notes') or None,
        confidence=float(row['confidence']), input_type=row['input_type']
    )
