import requests

from src.api_base import ApiBase


class APIAdapter(ApiBase):
    def __init__(self) -> None:
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all?"
        self.aeroplanes = None

    def get_country_bounds(self, country):
        """Получает bounding box- координаты указанной страны"""
        if not country or not country.strip():
            raise ValueError("Название страны не может быть пустым")

        headers_nominatim = {
            'User-Agent': 'test-app'
        }

        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }
        response = requests.get(
            self.nominatim_url,
            params=params_nominatim,
            headers=headers_nominatim
        )
        response.raise_for_status()
        data = response.json()

        if not data:
            raise ValueError(f"Страна '{country}' не найдена")

        bounds = data[0].get('boundingbox')
        return bounds


    def get_aircraft(self, bounds):
        """Получает данные о самолетах в указанных границах"""
        if bounds is None:
            raise ValueError("Не указаны границы области")

        params_opensky = {
            'lamin': bounds[0],
            'lamax': bounds[1],
            'lomin': bounds[2],
            'lomax': bounds[3],
        }

        response = requests.get(
            self.opensky_url, params=params_opensky)
        response.raise_for_status()


        self.aeroplanes = response.json()
        return self.aeroplanes
