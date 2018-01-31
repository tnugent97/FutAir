import tcs34725
from machine import I2C, Pin
i2c = I2C(Pin(5), Pin(4))
sensor = tcs34725.TCS34725(i2c)
print(sensor.read())