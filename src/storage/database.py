import sqlite3

def get_connection(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript('''
CREATE TABLE IF NOT EXISTS indicators (id TEXT PRIMARY KEY,name TEXT NOT NULL,category TEXT NOT NULL,unit TEXT,source_type TEXT,source_url TEXT,direction TEXT NOT NULL,weight REAL NOT NULL,description TEXT,manual_required INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS observations (id INTEGER PRIMARY KEY AUTOINCREMENT,indicator_id TEXT NOT NULL,date TEXT NOT NULL,value REAL NOT NULL,raw_value TEXT,source_url TEXT,notes TEXT,confidence REAL NOT NULL,input_type TEXT NOT NULL,created_at TEXT NOT NULL,UNIQUE(indicator_id,date));
CREATE TABLE IF NOT EXISTS indicator_scores (indicator_id TEXT NOT NULL,date TEXT NOT NULL,score REAL NOT NULL,reason TEXT,PRIMARY KEY(indicator_id,date));
CREATE TABLE IF NOT EXISTS category_scores (category TEXT NOT NULL,date TEXT NOT NULL,score REAL NOT NULL,reason TEXT,PRIMARY KEY(category,date));
CREATE TABLE IF NOT EXISTS scenario_results (date TEXT PRIMARY KEY,total_score REAL NOT NULL,s0_score REAL NOT NULL,s1_score REAL NOT NULL,s2_score REAL NOT NULL,s3_score REAL NOT NULL,final_label TEXT NOT NULL,explanation TEXT);
''')
    conn.commit()
