import requests
import json
from typing import List, Dict


my_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 YaBrowser/25.8.0.0 Safari/537.36'
api_key = 'objkpuDQEy6GCdX2iArwrXnRB19wPs'
countries_url = 'https://data-api.oxilor.com/rest/countries'


class CityParser:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'Accept': my_user_agent,
                        'User-Agent': 'application/json',
                        'Authorization': f'Bearer {api_key}',
                        'X-API-Key': api_key}
        self.session.headers.update(self.headers)

    def get_countries(self) -> List[Dict]:
        try:
            response = self.session.get(countries_url)
            response.raise_for_status()
            print(response.json())
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Ошибка при получении списка стран: {error}")
            return []

    def print_countries(self, countries):
        if not countries:
            print("Список стран пуст")
            return
        for i, country in enumerate(countries, 1):
            name = country.get('name', 'N/A')
            code = country.get('code', country.get('countryCode', 'N/A'))
            print(f"{i:3d}. {name} ({code})")

    def run(self):
        countries = self.get_countries()
        self.print_countries(countries)
    # def get_cities_by_country(self, country_code: str, max_results: int = 1000) -> List[Dict]:
    #     try:
    #         params = {'country': country_code,
    #                   'limit': max_results}
    #         response = self.session.get(f"{self.url}/rest/regions/cities", params=params)
    #         response.raise_for_status()
    #         data = response.json()
    #         return data.get('cities', []) or data.get('items', []) or data
    #     except requests.exceptions.RequestException as error:
    #         print(f"Ошибка при получении городов для страны {country_code}: {error}")
    #         return []
    
    # def parse_all_cities(self) -> pd.DataFrame:
    #     """Основной метод для парсинга всех городов"""
    #     print("Начинаем парсинг базы городов...")
        
    #     # Получаем список стран
    #     countries = self.get_countries()
    #     print(f"Найдено стран: {len(countries)}")
        
    #     all_cities = []
        
    #     for country in countries:
    #         country_code = country.get('code') or country.get('countryCode')
    #         country_name = country.get('name') or country.get('countryName')
            
    #         if not country_code:
    #             continue
                
    #         print(f"Обрабатываем страну: {country_name} ({country_code})")
            
    #         cities = self.get_cities_by_country(country_code)
            
    #         for city in cities:
    #             city_data = {
    #                 'city_name': city.get('name') or city.get('cityName'),
    #                 'country_code': country_code,
    #                 'country_name': country_name,
    #                 'latitude': city.get('latitude') or city.get('lat'),
    #                 'longitude': city.get('longitude') or city.get('lon'),
    #                 'population': city.get('population'),
    #                 'timezone': city.get('timezone'),
    #                 'region': city.get('region') or city.get('state')
    #             }
    #             all_cities.append(city_data)
            
    #         print(f"Найдено городов в {country_name}: {len(cities)}")
            
    #         # Пауза между запросами чтобы не перегружать сервер
    #         time.sleep(0.5)
        
    #     # Создаем DataFrame
    #     df = pd.DataFrame(all_cities)
    #     print(f"Всего собрано городов: {len(df)}")
        
    #     return df
    
    # def save_to_csv(self, df: pd.DataFrame, filename: str = "world_cities.csv"):
    #     """Сохраняем данные в CSV файл"""
    #     df.to_csv(filename, index=False, encoding='utf-8')
    #     print(f"Данные сохранены в файл: {filename}")
    
    # def save_to_json(self, df: pd.DataFrame, filename: str = "world_cities.json"):
    #     """Сохраняем данные в JSON файл"""
    #     df.to_json(filename, orient='records', force_ascii=False, indent=2)
    #     print(f"Данные сохранены в файл: {filename}")


if __name__ == "__main__":
    parser = CityParser()
