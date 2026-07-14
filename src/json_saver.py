import json
import os

from src.aeroplanes import Aeroplanes
from src.base_file import BaseFile


class JSONSaver(BaseFile):
    """Класс для сохранения информации о самолетах в JSON-файл"""

    def __init__(self, file_path: str = "aeroplanes.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Создает json файл если его нет"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

    def _read_data(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _write_data(self, data):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def _aeroplane_to_dict(self, aeroplane: Aeroplanes) -> dict:
        """Преобразует объект Aeroplanes в словарь"""
        return {
            "callsign": aeroplane.callsign,
            "country": aeroplane.country,
            "velocity": aeroplane.velocity,
            "baro_altitude": aeroplane.baro_altitude,
        }

    def _dict_to_aeroplane(self, data: dict) -> Aeroplanes:
        """Преобразует словарь в объект Aeroplanes"""
        return Aeroplanes(
            callsign=data.get("callsign", "N/A"),
            country=data.get("country", "Unknown"),
            velocity=data.get("velocity", 0.0),
            baro_altitude=data.get("baro_altitude", 0.0),
        )

    # абстрактные методы

    def add_aeroplane_to_file(self, aeroplane: Aeroplanes):
        data = self._read_data()

        for i, item in enumerate(data):
            if item.get("callsign") == aeroplane.callsign:
                data[i] = self._aeroplane_to_dict(aeroplane)
                self._write_data(data)
                return

        data.append(self._aeroplane_to_dict(aeroplane))
        self._write_data(data)

    def add_aeroplanes(self, aeroplanes: list[Aeroplanes]):
        for aeroplane in aeroplanes:
            self.add_aeroplane_to_file(aeroplane)

    def get_aeroplane(self, callsign):
        data = self._read_data()
        for item in data:
            if item.get("callsign") == callsign:
                return self._dict_to_aeroplane(item)
        return None

    def get_aeroplanes_by_country(self, country):
        data = self._read_data()
        result = []
        country_lower = country.lower()
        for item in data:
            item_country = item.get("country", "").lower()
            if country_lower in item_country:
                result.append(self._dict_to_aeroplane(item))
        return result

    def get_all_aeroplanes(self):
        data = self._read_data()
        return [self._dict_to_aeroplane(item) for item in data]

    def delete_aeroplane(self, callsign):
        data = self._read_data()
        for i, item in enumerate(data):
            if item.get("callsign") == callsign:
                del data[i]
                self._write_data(data)
                return True
        return False

    def delete_aeroplanes_by_country(self, country):
        data = self._read_data()
        all_count = len(data)
        new_data = [item for item in data if item.get("country", "").lower() != country.lower()]
        deleted_count = all_count - len(new_data)
        self._write_data(new_data)
        return deleted_count

    def clear_all(self):
        self._write_data([])

    def __str__(self):
        """Строковое представление о загрузке"""
        count_air = len(self.get_all_aeroplanes())
        return f"JSONSaver({self.file_path}) - {count_air} самолетов"
