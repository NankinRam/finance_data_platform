import psycopg2
from dotenv import load_dotenv
import os

from psycopg2._psycopg import OperationalError

from src.logger import log

load_dotenv()

def connect():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )

        log.info("Connect PostgreSQL DB:finance")

        return conn

    except OperationalError as e:
        log.info(f"Error connect PostgreSQL: {e}")