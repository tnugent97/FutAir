from machine import I2C
from machine import Pin
import time
import ads1115

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
sensor = ads1115.ADS1115(i2c)
time.sleep_ms(500)

while True:
    # print(sensor.read())
    print(sensor.read(4, 0))
    time.sleep_ms(20)
