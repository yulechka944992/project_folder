import pytest

from src.aeroplanes import Aeroplanes

class TestAeroplanes:
    """Тесты для класса Aeroplane"""

    def test_aeroplanes_creation(self, plane_number_one):
        """Тест создания объекта Aeroplane"""
        assert plane_number_one.callsign == "ABC123"
        assert plane_number_one.velocity == 500.0
        assert plane_number_one.baro_altitude == 10000.0

    def test_aeroplanes_velocity_error(self):
        """Тест с отрицательной скоростью"""
    with pytest.raises(ValueError) as e:
        Aeroplanes("ABC123", "Russia", -100, 10000.0)

    assert "Скорость не может быть отрицательной" in str(e.value)

    def test_aeroplanes_baro_altitude_error(self):
        """Тест с отрицательной высотой"""
        with pytest.raises(ValueError) as e:
            Aeroplanes("ABC123", "Russia", 500.0, -1000)

        assert "Высота не может быть отрицательной" in str(e.value)

    def test_lt_velocity(self, planes_data):
        """Тест сравнения скорости"""
        plane1 = planes_data[0]
        plane2 = planes_data[1]
        assert plane2 < plane1

    def test_gt_baro_altitude(self, planes_data):
        """Тест сравнения высоты"""
        plane1 = planes_data[0]
        plane2 = planes_data[1]
        assert plane1 > plane2

    def test_sort_by_velocity(self, planes_data):
        """Тест сортировки по скорости по возрастанию"""
        sorted_planes_data = sorted(planes_data)

        assert sorted_planes_data[0].callsign == "CHI678"
        assert sorted_planes_data[1].callsign == "AUR555"
        assert sorted_planes_data[2].callsign == "ABC123"

    def test_max_by_altitude(self, planes_data):
        """Тест поиска самолета с максимальной высотой"""
        highest = max(planes_data)
        assert highest.callsign == "ABC123"
        assert highest.baro_altitude == 10000.0

    def test_from_api_data(self, api_data):
        """"""
        planes = Aeroplanes.from_api_data(api_data)

        assert len(planes) == 4

        assert planes[0].callsign == "ABC123"
        assert planes[0].velocity == 500.0
        assert planes[0].baro_altitude == 10000.0

    def test_from_api_empty_value(self):
        """"""
        api_data = [
            ['abc123','ABC123','Russia', None, None, None, None, None, None, None]
        ]
        planes = Aeroplanes.from_api_data(api_data)
        assert len(planes) == 1
        assert planes[0].callsign == "ABC123"
        assert planes[0].velocity == 0.0
        assert planes[0].baro_altitude == 0.0

    def test_str_aeroplanes(self, plane_number_one):
        """"""
        message = "ABC123 (Russia) - Скорость:500.0 м/с, Высота:10000.0 м"
        assert str(plane_number_one) == message