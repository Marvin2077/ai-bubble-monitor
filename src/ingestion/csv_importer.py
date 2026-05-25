import csv
from src.ingestion.validators import validate_row
from src.storage.repository import upsert_observation

REQUIRED_COLUMNS = {'date','indicator_id','value','source_url','notes','confidence','input_type'}

def import_csv_to_db(path:str, indicator_ids:set[str], conn):
    errors=[]; count=0
    with open(path, newline='', encoding='utf-8') as f:
        reader=csv.DictReader(f)
        if not REQUIRED_COLUMNS.issubset(reader.fieldnames or []):
            raise ValueError('missing required columns')
        for i,row in enumerate(reader, start=2):
            try:
                obs=validate_row(row, indicator_ids)
                upsert_observation(conn, obs)
                count += 1
            except Exception as e:
                errors.append(f'row {i}: {e}')
    return count, errors
