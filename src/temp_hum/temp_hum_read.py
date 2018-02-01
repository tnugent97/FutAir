from machine import I2C, Pin
import time
import si7021
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
sensor = si7021.SI7021(i2c)
time.sleep_ms(500)
while True:
    print("Temperature: ", sensor.temperature())
    print("Humidity: ", sensor.humidity())
    time.sleep_ms(20)