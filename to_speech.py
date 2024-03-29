# Text To Speech

import json
import requests
import base64
from functions.connection_db import connect_db
from config import API_KEY

# info_meteo = """
# {'dt': 1711119600, 'T': {'value': 18.5, 'windchill': 20.6}, 'humidity': 65, 'sea_level': 1018.4, 'wind': {'speed': 4, 'gust': 0, 'direction': 165, 'icon': 'SSE'}, 'rain': {'1h': 0}, 'snow': {'1h': 0}, 'iso0': 3400, 'rain snow limit': 'Non pertinent', 'clouds': 70, 'weather': {'icon': 'p2j', 'desc': 'Eclaircies'}}

# """

# {'dt': 1711119600, 
#  'T': {'value': 18.5, 'windchill': 20.6}, 
#  'humidity': 65, 
#  'sea_level': 1018.4, 
#  'wind': {'speed': 4, 'gust': 0, 'direction': 165, 'icon': 'SSE'}, 
#  'rain': {'1h': 0}, 
#  'snow': {'1h': 0}, 
#  'iso0': 3400, 
#  'rain snow limit': 'Non pertinent',
#    'clouds': 70,
#      'weather': {'icon': 'p2j', 'desc': 'Eclaircies'}}

con = connect_db(dbname='postgres', user='postgres', password='soriya')
# print(con)
cur = con.cursor()

def fetch_forecast_for_city(city, date, hour=None):

    global con
    if con is None:
        print("La connexion à la base de données n'a pas été établie.")
        return "Erreur de connexion à la base de données."

    if hour is None:
        timestamp = date
        query = f"""
        SELECT dt, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_desc
            FROM weather
            WHERE label = %s AND date_trunc('day', dt) = %s
        """
        cur.execute(query, (city, timestamp))
    else:
        timestamp = f"{date} {hour:02}:00:00.000"
        cur.execute(
            f"""
            SELECT dt, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_desc
                FROM weather
                WHERE label = %s AND dt = %s
            """,
            (city, timestamp),
        )
    columns = [
        "Forecast date and hour",
        "Temperature",
        "Humidity",
        "Sea Level",
        "Wind Speed",
        "Wind Gust",
        "Wind Direction",
        "Weather Description",
    ]
    cities_data = cur.fetchall()
    result = ""
    for row in cities_data:
        result += (
            "\n".join([f"{column} {value}" for column, value in zip(columns, row)])
            + "\n"
        )
    return result.strip()

# info_meteo = print(fetch_forecast_for_city('jacou', '2024-03-26', '15'))

headers = {"Authorization": f"Bearer {API_KEY}"}

    
def get_text_from_forecast(city: str, date: str, hour=None) -> str:
    data = fetch_forecast_for_city(city, date, hour=hour)

    url = "https://api.edenai.run/v2/text/chat"
    providers = "openai"

    payload = {
    "providers": providers,
    "chatbot_global_action": "fais un résumé des infos metéo",
    "text": data,
    "previous_history": [],
    "temperature": 0.0,
    "max_tokens": 150,
    "fallback_providers": ""
    }


    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    rp = result[providers]
    generated_text = rp["generated_text"]
    return generated_text

print(get_text_from_forecast('jacou','2024-03-26','15'))


def get_speach_from_text(generated_text: str, city: str, date: str, hour=None) -> bytes:

    url_speech = "https://api.edenai.run/v2/audio/text_to_speech"

    providers_speech = "google"
    language_speech = "fr-FR"
    payload_speech = {
        "providers": providers_speech,
        "language": language_speech,
        "option": "MALE",
        "text": generated_text,
        "fallback_providers": ""
    }

    response = requests.post(url_speech, json=payload_speech, headers=headers)

    if response.status_code == 200:
        result = response.json()
        audio_data = result.get('google', {}).get('audio')
        if audio_data:
            audio_bytes = base64.b64decode(audio_data)
            with open("audio.mp3", "wb") as audio_file:
                audio_file.write(audio_bytes)
            print("Fichier audio généré avec succès : audio.mp3")
            return audio_bytes
        else:
            print("Aucune donnée audio disponible dans la réponse.")
    else:
        print(f"Erreur lors de la requête : {response.status_code} - {response.text}")


# text = get_text_from_forecast('jacou','2024-03-26','15')
# print(text)

# get_speach_from_text(text, 'jacou','2024-03-26','15')

