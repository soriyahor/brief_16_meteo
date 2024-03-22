import psycopg2

def connect_to_postgres():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='soriya',
            host='localhost',
            port='5432'
        )
        print("Successfully connected to PostgreSQL!")
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None


def close_connection(conn):
    try:
        conn.close()
        print("Connection closed.")
    except Exception as e:
        print(f"Error closing connection: {e}")