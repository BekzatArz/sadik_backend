from app.utils.psycopg_connection import PostgresConnection

def get_server_version():
    connection_manager = PostgresConnection()
    try:
        conn = connection_manager.connect()
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            return cursor.fetchone()
    except Exception as ex:
        print("[ERROR] Error while executing query:", ex)
    finally:
        connection_manager.close()
