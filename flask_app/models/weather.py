import requests
import json
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()
api_key=os.getenv('API_KEY') #Grabs the api key from the .env file and loads in the API_KEY

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    name: str
    real_feel: str
    temperature: float

def get_latitude_longitude(city_name, state_code, country_code, API_key):
    response= requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}').json()
    response_json = json.dumps(response, indent=4)
    if not response:
        return None, None
    data=response[0]
    lat, lon = data.get('lat'), data.get('lon')
    return lat, lon

def current_weather(lat,lon,API_key):
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=imperial').json()
    if 'weather' not in response: 
        return None
    weather_main=response.get('weather')[0].get('main')
    weather_main=weather_main.replace("Clouds", "Cloudy")
    data = WeatherData(
        main=weather_main,
        description = response.get('weather')[0].get('description'),
        icon=response.get('weather')[0].get('icon'),
        temperature=int(response.get('main').get('temp')),
        name=response.get('name'),
        real_feel=response.get('main').get('feels_like')
    )
    return data
    

def main(city_name, state_name, country_name):
    lat, lon = get_latitude_longitude({city_name}, {state_name}, {country_name}, api_key)
    WeatherData = current_weather(lat, lon, api_key)
    print(WeatherData)
    return WeatherData


if __name__ == "__main__":
    lat, lon = get_latitude_longitude('Dallas', 'TX', 'United States', api_key)
    print(current_weather(lat,lon,api_key))