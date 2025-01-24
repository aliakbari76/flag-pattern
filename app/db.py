import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="flag_patterns",
        user="root",
        password="",
        host="localhost",
        port="5432",
    )
