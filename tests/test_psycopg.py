import unittest
from app.utils.psycopg_connection import PostgresConnection

class TestPostgresConnection(unittest.TestCase):

    def test_connection(self):
        db = PostgresConnection()
        try:
            conn = db.connect()
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                result = cursor.fetchone()
                print("PostgreSQL Version:", result)
                self.assertIsNotNone(result, "Connection to PostgreSQL failed.")
        except Exception as ex:
            self.fail(f"[ERROR] Something went wrong: {ex}")
        finally:
            db.close()

if __name__ == "__main__":
    unittest.main()
