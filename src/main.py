# Simple demo of the TCS34725 color sensor.
# Will detect the color from the sensor and print it out every second.
import time
from machine import Pin,I2C

import esp


# Initialize I2C bus and sensor.
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
sensor = esp.TCS34725(i2c, 0x29)

# Main loop reading color and printing it every second.
while True:
    # Read the color as RGB bytes (0-255 values).
    r, g, b = sensor.color_rgb_bytes
    print('Detected color: #{0:02X}{1:02X}{2:02X}'.format(r, g, b))
    # Read the color temperature and lux of the sensor too.
    temp = sensor.temperature
    lux = sensor.lux
    print('Temperature: {0}K Lux: {1}'.format(temp, lux))
    # Delay for a second and repeat.
    time.sleep(1.0)
