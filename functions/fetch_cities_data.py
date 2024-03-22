
def fetch_cities_data(conn, department_number):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT longitude, latitude, label, department_number
            FROM cities
            WHERE department_name = %s;
        """, (department_number,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching cities data: {e}")
        return None