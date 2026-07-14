import os
from src.json_saver import JSONSaver
from src.aeroplanes import Aeroplanes


class TestJSONSaver:
    def test_add_aeroplane(self, temp_file, plane_number_one):
        """Тест добавления одного самолета"""
        temp_file.add_aeroplane_to_file(plane_number_one)
        all_planes = temp_file.get_all_aeroplanes()

        assert len(all_planes) == 1
        assert all_planes[0].callsign == "ABC123"
        assert all_planes[0].country == "Russia"
        assert all_planes[0].velocity == 500.0
        assert all_planes[0].baro_altitude == 10000.0

    def test_add_aeroplanes(self, temp_file, planes_data):
        """Тест добавления нескольких самолетов."""
        temp_file.add_aeroplanes(planes_data)
        all_planes = temp_file.get_all_aeroplanes()

        assert len(all_planes) == 3
        assert all_planes[0].callsign == "ABC123"
        assert all_planes[1].callsign == "CHI678"
        assert all_planes[2].callsign == "AUR555"

    def test_add_aeroplane_update(self, temp_file, plane_number_one):
        """Тест обновления существующего самолета"""
        temp_file.add_aeroplane_to_file(plane_number_one)

        updated_plane = Aeroplanes("ABC123", "Russia", 600.0, 15000.0)
        temp_file.add_aeroplane_to_file(updated_plane)

        all_planes = temp_file.get_all_aeroplanes()
        assert len(all_planes) == 1
        assert all_planes[0].velocity == 600.0
        assert all_planes[0].baro_altitude == 15000.0

    def test_get_aeroplane(self, temp_file, planes_data):
        """Тест получения самолета по позывному"""
        temp_file.add_aeroplanes(planes_data)

        plane = temp_file.get_aeroplane("AUR555")
        assert plane.country == "Australia"

    def test_get_aeroplanes_not_found(self, temp_file, planes_data):
        """Тест получения несуществующего самолета"""
        temp_file.add_aeroplanes(planes_data)

        plane = temp_file.get_aeroplane("Самолетик")
        assert plane is None

    def test_get_aeroplanes_by_country(self, temp_file, planes_data):
        """Тест получения самолетов по стране"""
        temp_file.add_aeroplanes(planes_data)
        russian_planes = temp_file.get_aeroplanes_by_country("Russia")
        assert len(russian_planes) == 1
        assert russian_planes[0].callsign == "ABC123"

    def test_get_aeroplanes_by_country_not_found(self, temp_file, planes_data):
        """Тест получения самолетов по несуществующей стране"""
        temp_file.add_aeroplanes(planes_data)
        italy_planes = temp_file.get_aeroplanes_by_country("Italy")
        assert len(italy_planes) == 0

    def test_delete_aeroplane(self, temp_file, planes_data):
        """Тест удаления самолета по позывному"""
        temp_file.add_aeroplanes(planes_data)
        result = temp_file.delete_aeroplane("ABC123")
        assert result is True

        all_planes = temp_file.get_all_aeroplanes()
        assert len(all_planes) == 2

    def test_delete_aeroplane_by_country(self, temp_file, planes_data):
        """Тест удаления всех самолетов по стране"""
        temp_file.add_aeroplanes(planes_data)
        result = temp_file.delete_aeroplanes_by_country("Russia")
        assert result == 1
        all_planes = temp_file.get_all_aeroplanes()
        assert len(all_planes) == 2

    def test_clear_all(self, temp_file, planes_data):
        """Тест полной очистки хранилища"""
        temp_file.add_aeroplanes(planes_data)
        assert len(temp_file.get_all_aeroplanes()) == 3
        temp_file.clear_all()
        assert len(temp_file.get_all_aeroplanes()) == 0

    def test_str(self, temp_file, planes_data):
        """Тест строкового представления"""
        temp_file.add_aeroplanes(planes_data)

        expected = f"JSONSaver({temp_file.file_path}) - 3 самолетов"
        assert str(temp_file) == expected

    def test_file_creation(self, tmp_path):
        """Тест создания файла при инициализации"""
        file_path = tmp_path / "test.json"
        saver = JSONSaver(str(file_path))

        assert os.path.exists(str(file_path))
