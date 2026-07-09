from abc import ABC, abstractmethod

class ApiBase(ABC):
    """Абстрактный класс для работы с API"""
    @abstractmethod
    def get_country_bounds(self, country):
        """Получить границы страны через Nominatim"""
        pass

    @abstractmethod
    def get_aircraft(self, bounds):
        """Получить данные о самолетах через OpenSky"""
        pass