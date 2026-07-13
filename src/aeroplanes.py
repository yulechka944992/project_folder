class Aeroplanes:
    """Класс для работы с информацией о самолетах"""
    def __init__(self, callsign, country, velocity, baro_altitude):
        """Конструктор с валидацией атрибутов"""
        if velocity is not None and velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")
        if baro_altitude is not None and baro_altitude < 0:
            raise ValueError("Высота не может быть отрицательной")

        self._callsign = callsign
        self._country = country
        self._velocity = velocity
        self._baro_altitude = baro_altitude


    @classmethod
    def from_api_data(cls, api_data):
        """Преобразует список данных из API в список объектов Aeroplane"""
        air_list = []

        for item in api_data:
            airplane = cls(
                callsign=item[1],
                country=item[2],
                velocity=item[9] if item[9] is not None else 0.0,
                baro_altitude=item[7] if item[7] is not None else 0.0
            )
            air_list.append(airplane)

        return air_list

    def __lt__(self, other):
        """Сравнение по скорости"""
        if not isinstance(other, Aeroplanes):
            return NotImplemented
        return self._velocity < other._velocity

    def __gt__(self, other):
        """Сравнение по высоте"""
        if not isinstance(other, Aeroplanes):
            return NotImplemented
        return self._baro_altitude > other._baro_altitude

    @property
    def callsign(self):
        return self._callsign

    @property
    def velocity(self):
        return self._velocity

    @property
    def baro_altitude(self):
        return self._baro_altitude

    def __str__(self):
        return f"{self._callsign} ({self._country}) - Скорость:{self._velocity} м/с, Высота:{self._baro_altitude} м"
