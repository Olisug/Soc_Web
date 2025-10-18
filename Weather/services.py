import requests
import logging
import requests
from urllib.parse import quote


class WeatherAPIError(Exception):
    pass


class WeatherAPIClient:
    def __init__(self):
        self.base_url = 'https://wf-production-4367.up.railway.app'
    
    def get_weather(self, city: str) -> dict:
        try:
            encoded_city = quote(city)
            url = f"{self.base_url}/weather/current/?city={encoded_city}"
            print(f"Запрос к: {url}")
            response = requests.get(url)
            if response.status_code != 200:
                error_data = response.json()
                raise WeatherAPIError(f"Ошибка API: {error_data.get('detail', 'Unknown error')}")
            weather_data = response.json()
            print(weather_data)
            return weather_data
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"Ошибка соединения: {str(e)}")