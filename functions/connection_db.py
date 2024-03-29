import psycopg2

def connect_db(dbname, user, password, host='localhost', port='5432'):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Successfully connected to db!")
        return conn
    except Exception as e:
        print(f"Error connecting to db: {e}")
        return None


def close_connection(conn):
    try:
        conn.close()
        print("Connection closed.")
    except Exception as e:
        print(f"Error closing connection: {e}")