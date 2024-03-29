def create_weather_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                id SERIAL PRIMARY KEY,
                loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                department_name VARCHAR(100),
                label_dt_key VARCHAR(100),
                label VARCHAR(100),
                longitude FLOAT,
                latitude FLOAT,                  
                dt TIMESTAMP,
                temperature FLOAT,
                humidity INT,
                sea_level FLOAT,
                wind_speed FLOAT,
                wind_gust FLOAT,
                wind_direction INT,
                weather_icon VARCHAR(10),
                weather_desc VARCHAR(100)
            );
        """)
        conn.commit()
        print("Weather table created successfully!")
    except Exception as e:
        conn.rollback()
        print(f"Error creating weather table: {e}")

def insert_weather_data(conn, data):
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO weather (longitude, latitude, label, department_name, label_dt_key, dt, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_icon, weather_desc)
            VALUES (%s, %s, %s, %s, %s, TO_TIMESTAMP(%s), %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, data)
        conn.commit()
        print("Data inserted successfully!")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting data: {e}")