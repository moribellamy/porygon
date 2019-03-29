from unittest.mock import patch, MagicMock

import porygon

@patch('porygon.bus')
def test_set_leftright(busfunc):
    bus = busfunc.return_value = MagicMock()
    porygon.set_leftright(100)
    print(bus.write_i2c_block_data.call_args_list)
