from abc import ABC, abstractmethod
from typing import Optional

from src.aeroplanes import Aeroplanes


class BaseFile(ABC):
    """Абстрактный класс обязывающий реализовать методы
    для добавления информациио самолете в файл,
    получения данных из файла и удаления информации о самолетах"""

    @abstractmethod
    def add_aeroplane_to_file(self, aeroplane: Aeroplanes):
        """Добавляет информацию о самолете в хранилище"""
        pass

    @abstractmethod
    def add_aeroplanes(self, aeroplanes: list[Aeroplanes]) -> None:
        """Добавляет список самолетов в хранилище"""
        pass

    @abstractmethod
    def get_aeroplane(self, callsign: str) -> Optional[Aeroplanes]:
        """Получает информацию о самолете по позывному"""
        pass

    @abstractmethod
    def get_aeroplanes_by_country(self, country: str) -> list[Aeroplanes]:
        """Получает список самолетов по стране регистрации"""
        pass

    @abstractmethod
    def get_all_aeroplanes(self):
        """Получает все самолеты из хранилища"""
        pass

    @abstractmethod
    def delete_aeroplane(self, callsign: str) -> bool:
        """Удаляет информацию о самолете по позывному"""
        pass

    @abstractmethod
    def delete_aeroplanes_by_country(self, country: str) -> int:
        """Удаляет все самолеты по стране регистрации."""
        pass

    @abstractmethod
    def clear_all(self) -> None:
        """Очищает все хранилище."""
        pass
