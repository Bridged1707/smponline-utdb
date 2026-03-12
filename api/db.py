import psycopg2
from psycopg2.extras import RealDictCursor
from .config import DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )


def execute_query(query, params=None, fetch=False):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(query, params)

    result = None
    if fetch:
        result = cursor.fetchall()

    conn.commit()

    cursor.close()
    conn.close()

    return result