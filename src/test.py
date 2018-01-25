from machine import Pin, I2C
from time import sleep

ADDRESS = 0x29
REG_ACTIVATE = const(0x0)
COMMAND_BIT  = const(0x80)
REG_STATUS   = const(0x13)
REG_CDATA    = const(0x14)
REG_RDATA    = const(0x16)
REG_GDATA    = const(0x18)
REG_BDATA    = const(0x1a)

# Set up I2C thingy
i2cport = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

# Active the sensor
def activate_sensor():
  i2cport.writeto_mem(ADDRESS,REG_ACTIVATE,bytearray([0x1]))
  sleep(0.003)
  i2cport.writeto_mem(ADDRESS,REG_ACTIVATE,bytearray([0x3]))

# Read from sensor
def test_colours(n=2):
  r,g,b,c = tuple(int.from_bytes(i2cport.readfrom_mem(ADDRESS,reg,n),"big") for reg in (REG_RDATA,REG_GDATA,REG_BDATA,REG_CDATA))
  red,green,blue = tuple(int(pow((int((colour/c) * 256) / 255), 2.5) * 255) for colour in (r,g,b))
  print("Red: {0}, Green: {1}, Blue {2}".format(red,green,blue))
