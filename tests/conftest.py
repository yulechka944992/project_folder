import pytest

from src.aeroplanes import Aeroplanes


@pytest.fixture
def plane_number_one():
    """"""
    return Aeroplanes(
        callsign="ABC123",
        country="Russia",
        velocity=500.0,
        baro_altitude=10000.0
    )
@pytest.fixture
def planes_data():
    """"""
    return [
        Aeroplanes(callsign="ABC123", country="Russia", velocity=500.0, baro_altitude=10000.0),
        Aeroplanes(callsign="CHI678", country="China", velocity=450.0, baro_altitude=8000.0),
        Aeroplanes(callsign="AUR555", country="Australia", velocity=480.0, baro_altitude=9000.0)
    ]

@pytest.fixture
def api_data():
    """"""
    return [
        ['abc123','ABC123','Russia', None, None, None, None, 10000, None, 500.0],
        ['jbl333','JBL333','Korea', None, None, None, None, 8000, None, 450.0],
        ['nhl911','NHL911','Spain', None, None, None, None, 9000, None, 480.0],
        ['usa602','USA602','USA', None, None, None, None, 10000, None, 400.0]
    ]