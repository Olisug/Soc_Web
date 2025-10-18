# import requests
# from typing import List, Dict

# my_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 YaBrowser/25.8.0.0 Safari/537.36'
# api_key = 'objkpuDQEy6GCdX2iArwrXnRB19wPs'
# countries_url = 'https://data-api.oxilor.com/rest/countries'


# class CityParser:
#     def __init__(self):
#         self.session = requests.Session()
#         self.headers = {'Accept': my_user_agent,
#                         'User-Agent': 'application/json',
#                         'Authorization': f'Bearer {api_key}',
#                         'X-API-Key': api_key}
#         self.session.headers.update(self.headers)

#     def get_countries(self) -> List[Dict]:
#         try:
#             response = self.session.get(countries_url)
#             response.raise_for_status()
#             return response.json()
#         except requests.exceptions.RequestException as error:
#             print(f"Ошибка при получении списка стран: {error}")
#             return []

#     def countries_tuple(self):
#         countries = self.get_countries()
#         countries_list = []
#         for country in countries:
#             countries_list.append((country['name'], country['name']))
#         return countries_list

#     def run(self):
#         self.countries_tuple()


# # if __name__ == "__main__":
# #     parser = CityParser()
# #     parser.run()

import requests
from django.conf import settings
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


if __name__ == "__main__":
    client = WeatherAPIClient()
    client.get_weather('Москва')