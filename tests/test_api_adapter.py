import pytest
from unittest.mock import patch, Mock, MagicMock

from src.api_adapter import APIAdapter

class TestAPIAdapter:
    """Тесты для класса APIAdapter"""
    api = APIAdapter()

    @patch('src.api_adapter.requests.get')
    def test_get_country_bounds(self, mock_get):
        """Тест успешного получения границ страны"""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {'boundingbox': ['-55.3228175', '-9.0880125', '72.2461932', '168.2261259']}]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        bounds = self.api.get_country_bounds("Australia")

        assert len(bounds) == 4
        assert bounds[0] == '-55.3228175'
        assert bounds[1] == '-9.0880125'
        assert bounds[2] == '72.2461932'
        assert bounds[3] == '168.2261259'

    @patch('src.api_adapter.requests.get')
    def test_get_country_bounds_empty(self, mock_get):
        """Тест с пустой строкой"""
        api = APIAdapter()

        with pytest.raises(ValueError) as exc_info:
            api.get_country_bounds("")

        assert "Название страны не может быть пустым" in str(exc_info.value)
        mock_get.assert_not_called()

    @patch('src.api_adapter.requests.get')
    def test_get_country_bounds_not_found(self, mock_get):
        """Тест с несуществующей страной"""
        api = APIAdapter()

        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        with pytest.raises(ValueError) as exc_info:
            api.get_country_bounds("Zombieland")

        assert "Страна 'Zombieland' не найдена"

    @patch('src.api_adapter.requests.get')
    def test_get_aircraft(self, mock_get):
        """Тест успешного получения самолетов"""
        api = APIAdapter()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            'time': 1234567890,
            'states':[
                ['abc123',
                 'ABC123',
                 'Russia',
                 None,
                 None,
                 None,
                 None,
                 None,
                 None,
                 True,
                 None,
                 None,
                 None,
                 None,
                 None,
                 1234,
                 False,
                 0]
            ]
        }

        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        bounds = ['-55.3228175', '-9.0880125', '72.2461932', '168.2261259']
        result = api.get_aircraft(bounds)

        assert 'states' in result
        assert len(result['states']) == 1

    @patch('src.api_adapter.requests.get')
    def test_get_aircraft_with_none(self, mock_get):
        """Тест с None вместо границ"""
        api = APIAdapter()

        with pytest.raises(ValueError) as exc_info:
            api.get_aircraft(None)

        assert "Не указаны границы области" in str(exc_info.value)
        mock_get.assert_not_called()