from machine import I2C
from machine import Pin
import time
import mics4514

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
sensor = mics4514.MICS4514(i2c)
time.sleep_ms(500)

while True:
    print("CO: ", sensor.read_RED())
    print("NO: ", sensor.read_OX())
    time.sleep_ms(20)
