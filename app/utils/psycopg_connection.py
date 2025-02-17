import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import Config


class PostgresConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                cursor_factory=RealDictCursor
            )
            return self.connection
        except Exception as ex:
            print("[ERROR] Failed to connect to the database:", ex)
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            print("[INFO] PostgreSQL connection closed")
