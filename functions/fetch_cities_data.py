
def fetch_cities_data(conn, department_name):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT longitude, latitude, label, department_name
            FROM cities
            WHERE department_name = %s;
        """, (department_name,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching cities data: {e}")
        return None