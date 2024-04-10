
import json
from connection_db import connect_db

def load_cities(conn):
    # conn = connect_db(dbname='postgres', user='postgres', password='soriya')
    if conn:

        try:
            # Create a cursor
            cur = conn.cursor()
            # Create table if not exists (moved outside the loop)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cities (
                    insee_code VARCHAR(10),
                    city_code VARCHAR(100),
                    zip_code VARCHAR(10),
                    label VARCHAR(100),
                    latitude FLOAT,
                    longitude FLOAT,
                    department_name VARCHAR(100),
                    department_number VARCHAR(10),
                    region_name VARCHAR(100),
                    region_geojson_name VARCHAR(100)
                )
            """)

            # Lecture du fichier JSON
            with open("cities.json", 'r') as fichier:
                data = json.load(fichier)
            
            for city in data:
                latitude = float(city['latitude']) if city['latitude'] else None
                longitude = float(city['longitude']) if city['longitude'] else None
                cur.execute("""
                    INSERT INTO cities (
                        insee_code, city_code, zip_code, label,
                        latitude, longitude, department_name,
                        department_number, region_name, region_geojson_name
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    city['insee_code'], city['city_code'], city['zip_code'], city['label'],
                    latitude, longitude,
                    city['department_name'], city['department_number'], city['region_name'], city['region_geojson_name']
                ))
                    
            # Commit the transaction
            conn.commit()
            print("Data cities transfer to PostgreSQL succeeded!")
        except Exception as e:
            conn.rollback()  # Rollback the transaction if an error occurs
            print(f"Error inserting data into PostgreSQL: {e}")

        # finally:
        #     # Close cursor and connection
        #     cur.close()
        #     conn.close()
