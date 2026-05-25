import tempfile
from src.ingestion.csv_importer import import_csv_to_db
from src.storage.database import get_connection, init_db

def test_csv_validation():
    content='date,indicator_id,value,source_url,notes,confidence,input_type\n2026-03,BAD,1,x,n,0.7,manual\n'
    with tempfile.NamedTemporaryFile('w+', suffix='.csv') as f:
        f.write(content); f.flush()
        conn=get_connection(':memory:'); init_db(conn)
        c,e=import_csv_to_db(f.name, {'GOOD'}, conn)
        assert c==0 and e
