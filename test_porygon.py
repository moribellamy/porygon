from unittest.mock import patch, MagicMock

import porygon


@patch('porygon.bus')
def test_tilt_x(busfunc):
    busfunc.return_value = MagicMock()
    porygon.tilt_x(100)


@patch('porygon.bus')
def test_tilt_y(busfunc):
    busfunc.return_value = MagicMock()
    porygon.tilt_y(100)


@patch('porygon.GPIO')
@patch('porygon.bus')
def test_init_pi(_, __):
    porygon.init_pi()
