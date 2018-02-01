from machine import I2C
from machine import Pin
import time
import tcs34725
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
sensor = tcs34725.TCS34725(i2c)
sensor.active(True)
time.sleep_ms(500)
while True:
    # print(sensor.read()) 
    raw_data = sensor.read(True)
    print(tcs34725.html_rgb(raw_data))
    time.sleep_ms(20)
