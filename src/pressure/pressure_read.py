from machine import I2C
from machine import Pin
import time
import bmp180

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
sensor = bmp180.BMP180(i2c)
sensor.oversample_sett = 2 #accuracy; 0-3, lower better, but slower

time.sleep_ms(500)

while True:
    print(sensor.pressure()) #apparently gives same value if <10s interval between calls
    time.sleep_ms(20)
