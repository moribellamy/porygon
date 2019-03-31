#!/usr/bin/env python

import configparser
import os
import subprocess
import tempfile
import time

import PIL
import pytesseract
import smbus2

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    # If we're not running on a Pi, then we are running a test and
    # we can count on the test to stub out a mock GPIO module.
    GPIO = None

# <module_config>
__config = configparser.ConfigParser()
__config.read(os.path.join(
    os.path.dirname(__file__), 'config.ini'
))


def __make_button(name):
    return int(__config['buttons'][name], 0), name


Y = __make_button('Y')
B = __make_button('B')
X = __make_button('X')
A = __make_button('A')
HOME = __make_button('HOME')

I2C_WRITE_COMMAND = int(__config['joystick']['I2C_WRITE_COMMAND'], 0)
I2C_LEFTRIGHT_ADDR = int(__config['joystick']['I2C_LEFTRIGHT_ADDR'], 0)
I2C_UPDOWN_ADDR = int(__config['joystick']['I2C_UPDOWN_ADDR'], 0)
LR_NEUTRAL = int(__config['joystick']['LR_NEUTRAL'], 0)
UD_NEUTRAL = int(__config['joystick']['UD_NEUTRAL'], 0)
# </module_config>


__bus = None


def bus():
    global __bus
    if not __bus:
        __bus = smbus2.SMBus(1)
    return __bus


def init_pi():
    GPIO.setmode(GPIO.BOARD)
    for but in [A, B, X, Y, HOME]:
        GPIO.setup(but[0], GPIO.OUT)
        GPIO.output(but[0], False)
    still()


def press(but, hold_delay=.1, rest_delay=.1):
    print('pressing {}'.format(but[1]))
    GPIO.output(but[0], True)
    time.sleep(hold_delay)
    GPIO.output(but[0], False)
    time.sleep(rest_delay)


def set_leftright(level):
    level &= 0xfff
    msg = [(level & 0xff0) >> 4, (level & 0xf)]
    bus().write_i2c_block_data(I2C_LEFTRIGHT_ADDR, I2C_WRITE_COMMAND, msg)


def tilt_x(tilt):
    set_leftright(LR_NEUTRAL + tilt)


def set_updown(level):
    level &= 0xfff
    msg = [(level & 0xff0) >> 4, (level & 0xf)]
    bus().write_i2c_block_data(I2C_UPDOWN_ADDR, I2C_WRITE_COMMAND, msg)


def tilt_y(tilt):
    set_updown(UD_NEUTRAL + tilt)


def still():
    tilt_x(0)
    tilt_y(0)


def read_cropped_image(coords):
    try:
        fname = tempfile.NamedTemporaryFile(prefix='pokemon')
        subprocess.call(['fswebcam', '-r', '1280x720', fname.name])
        image = PIL.Image.open(fname.name)
        cropped = image.crop(coords)
        retval = pytesseract.image_to_string(cropped)
        return retval
    except Exception as e:
        print(e)
        return ''
