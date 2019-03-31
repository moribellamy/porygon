Porygon consists of two parts: a digital circuit that is wired between a RasPi and a JoyCon, as well as a script
to run that circuit.

For a video of it in action, and some tips on how to put this together, see the announcement post at 
https://invoked.net/2019-03-26-joycon-circuit/

# Circuit

* [A circuit diagram](docs/circuit.png?raw=true)
* [An example implementation](docs/breadboard.jpg?raw=true)

The parts listed in the circuit:

| Component | Link | Function |
| :------ |:--- | :--- |
| PI-IO | [raspi](https://www.raspberrypi.org/products/raspberry-pi-1-model-b-plus/) |Array of GPIO pins on the raspi, used to toggle analog switches and to drive an I2C bus.| 
| DG333A Analog Switch (x2)| [digikey](https://www.digikey.com/product-detail/en/DG333ADJ-E3/DG333ADJ-E3-ND/2621669?utm_campaign=buynow&WT.z_cid=ref_octopart_dkc_buynow&utm_medium=aggregator&curr=usd&site=us&utm_source=octopart) | Single Pole, Double Throw switches. To bridge points to COL, emulating a button press.| 
|MCP4725 (x2)| [sparkfun](https://www.sparkfun.com/products/12918)| Digital Analog Converters. The pi sends a signal here to output a variable voltage, which will emulate what the joystick does. I bought breakout boards instead of the chip itself to make soldering easier.|

# Script

To actually get the inputs going, you'll need shell access to the PI in your circuit. Then,

```bash
git clone https://github.com/moribellamy/porygon.git
cd porygon
python3 -m virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

If your circuit diagram varies from the one documented here, there are some settings you can put in
`config.ini`. This is if you didn't use the same pin numbers on your PI GPIO array, or if your
power source isn't a clean five volts.

Then you are in control!

```python
from porygon import *
import time

tilt_x(100)  # Go left a while!
time.sleep(1)
still()  # Zero out the joystick.

press(A)
press(X)  # And so forth.
```

For an example end to end script, which takes input from a webcam, read `pokemon_lets_go.py`.
