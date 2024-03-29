from meteofrance_api import MeteoFranceClient

def connect_meteo_france(latitude, longitude):
    meteo = MeteoFranceClient()
    city_forecast = meteo.get_forecast(latitude, longitude)
    data = city_forecast.forecast
    return data


# print(connect_meteo_france(43.663169698, 3.911878436))