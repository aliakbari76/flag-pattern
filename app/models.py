import psycopg2
from .db import get_db_connection


CREATE_FLAG_PATTERN_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS flag_patterns (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    price NUMERIC NOT NULL,
    pattern TEXT NOT NULL
);
"""

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_FLAG_PATTERN_TABLE_QUERY)
    conn.commit()
    conn.close()
