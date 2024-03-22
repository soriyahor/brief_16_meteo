from meteofrance_api import MeteoFranceClient

from functions.fetch_cities_data import fetch_cities_data
from functions.weather_table import create_weather_table,insert_weather_data
from functions.connection_postgres import connect_to_postgres, close_connection
from functions.delete_data_48h import delete_old_data_48h

# choix du département
department = 'hérault'

def main():
    conn = connect_to_postgres()
    if conn:
        delete_old_data_48h(conn)
        create_weather_table(conn)
        cities_data = fetch_cities_data(conn, department)
        if cities_data:
            meteo = MeteoFranceClient()
            for city_data in cities_data:
                longitude, latitude, label, department_name = city_data
                city_forecast = meteo.get_forecast(latitude, longitude)
                data = city_forecast.forecast
                for item in data:
                    dt = item['dt']
                    temperature = item['T']['value']
                    humidity = item['humidity']
                    sea_level = item['sea_level']
                    wind_speed = item['wind']['speed']
                    wind_gust = item['wind']['gust']
                    wind_direction = item['wind']['direction']
                    weather_icon = item['weather']['icon']
                    weather_desc = item['weather']['desc']
                    label_dt_key = f"{label}/{dt}"
                    insert_data = (longitude, latitude, label, department_name, label_dt_key, dt, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_icon, weather_desc)
                    insert_weather_data(conn, insert_data)
        close_connection(conn)
        print("Data transfer to PostgreSQL succeeded!")

if __name__ == "__main__":
    main()