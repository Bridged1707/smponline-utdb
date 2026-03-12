import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("UTDB_HOST", "localhost")
DB_NAME = os.getenv("UTDB_NAME", "utdb")
DB_USER = os.getenv("UTDB_USER", "utdb_api")
DB_PASS = os.getenv("UTDB_PASS", "password")
DB_PORT = os.getenv("UTDB_PORT", "5432")