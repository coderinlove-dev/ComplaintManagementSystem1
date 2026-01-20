# config/db.py

import os
import mysql.connector
from mysql.connector import pooling

# IMPORTANT:
# Do NOT use load_dotenv() in production (Render)
# Render already injects environment variables

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))

# Safety validation (prevents silent failures)
if not DB_HOST or not DB_USER or not DB_NAME:
    raise RuntimeError("Database environment variables are missing")

dbconfig = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "port": DB_PORT,

    # REQUIRED for Railway MySQL
    "ssl_disabled": True
}

# Create connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,          # 32 is too high for Render free tier
    pool_reset_session=True,
    **dbconfig
)

def get_connection():
    return connection_pool.get_connection()