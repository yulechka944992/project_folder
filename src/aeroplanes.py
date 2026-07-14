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
            velocity = item[9]
            if velocity is None or velocity < 0:
                velocity = 0.0

            baro_altitude = item[7]
            if baro_altitude is None or baro_altitude < 0:
                baro_altitude = 0.0

            airplane = cls(
                callsign=item[1],
                country=item[2],
                velocity=velocity,
                baro_altitude=baro_altitude
            )
            air_list.append(airplane)

        return air_list

    def __lt__(self, other):
        """Сравнение по скорости"""
        if not isinstance(other, Aeroplanes):
            return NotImplemented

        self_v = self._velocity if self._velocity is not None else 0.0
        other_v = other._velocity if other._velocity is not None else 0.0

        return self_v < other_v

    def __gt__(self, other):
        """Сравнение по высоте"""
        if not isinstance(other, Aeroplanes):
            return NotImplemented

        self_a = self._baro_altitude if self._baro_altitude is not None else 0.0
        other_a = other._baro_altitude if other._baro_altitude is not None else 0.0

        return self_a > other_a

    @property
    def callsign(self):
        return self._callsign

    @property
    def country(self):
        return self._country

    @property
    def velocity(self):
        return self._velocity

    @property
    def baro_altitude(self):
        return self._baro_altitude

    def __str__(self):
        return f"{self._callsign} ({self._country}) - Скорость:{self._velocity} м/с, Высота:{self._baro_altitude} м"
