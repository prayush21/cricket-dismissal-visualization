import os
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "my-dummy-cricket-db"),
        user=os.getenv("DB_USER", "prayushdave"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost")
    )