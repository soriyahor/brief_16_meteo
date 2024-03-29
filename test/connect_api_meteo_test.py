from functions.connect_api_meteo import connect_meteo_france

def test_connect_meteo_france():
    latitude = 45.018455673
    longitude = 4.856703914
    data = connect_meteo_france(latitude, longitude)

    assert data != None

    assert 'T' in data[0]  
    assert 'humidity' in data[0]  

    temperature = data[0]['T']['value']
    humidity = data[0]['humidity']
    assert isinstance(temperature, (int, float))  
    assert isinstance(humidity, (int, float))  
    assert -100 <= temperature <= 100  
    assert 0 <= humidity <= 100

test_connect_meteo_france()

