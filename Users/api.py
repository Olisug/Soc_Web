import requests
from typing import List, Tuple

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

    def get_countries(self) -> List[Tuple[str, str]]:
        country_choices = []
        try:
            response = self.session.get(countries_url)
            response.raise_for_status()
            countries = response.json()
            for country in countries:
                name = country.get('name')
                country_choices.append((name, name))
            print(country_choices)
            return country_choices
        except requests.exceptions.RequestException as error:
            print(f"Ошибка при получении списка стран: {error}")
            return []

    def run(self):
        countries = self.get_countries()
        return countries


if __name__ == "__main__":
    parser = CityParser()
    parser.run()
