from machine import I2C
from machine import Pin
import time
import adc1115

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
sensor = adc1115.ADS1115(i2c)
sensor.active(True)
time.sleep_ms(500)

while True:
    # print(sensor.read())
    print(sensor.read(4, 0))
    time.sleep_ms(20)
