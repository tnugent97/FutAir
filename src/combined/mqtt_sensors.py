from machine import I2C
gc.collect()
from machine import Pin
gc.collect()
import time
gc.collect()
import network
gc.collect()
import machine
gc.collect()
import mics4514
gc.collect()
import si7021
gc.collect()
import bmp180
gc.collect()

def th_sensor_setup(_scl, _sda):
    print("Temperature/Humidity Sensor Setup")
    i2c = I2C(-1, scl=Pin(_scl), sda=Pin(_sda))
    s = si7021.SI7021(i2c)
    return s

def pre_sensor_setup(_scl, _sda, _freq):
    print("Pressure Sensor Setup")
    i2c = I2C(scl=Pin(_scl), sda=Pin(_sda), freq=_freq)
    s = bmp180.BMP180(i2c)
    s.oversample_sett = 2
    return s

def gas_sensor_setup(_scl, _sda, _freq):
    print("Gas Sensor Setup")
    i2c = I2C(scl=Pin(_scl), sda=Pin(_sda), freq=_freq)
    s = mics4514.MICS4514(i2c)
    print("Preheating")
    s.preHeaterON()
    time.sleep_ms(10000)
    s.preHeaterOFF()
    return s

def pre_sensor_read(sensor):
    val = sensor.pressure
    time.sleep_ms(20)
    return val

def th_sensor_read(sensor):
    t = sensor.temperature()
    h = sensor.humidity()
    time.sleep_ms(20)
    return t, h

def gas_sensor_read(sensor):
    no2 = sensor.read_OX()
    co = sensor.read_RED()
    time.sleep_ms(20)
    return no2, co


# adc = adc_sensor_setup(13, 12, 100000)
gas = gas_sensor_setup(5, 4, 100000)
th = th_sensor_setup(5, 4)
pre = pre_sensor_setup(5, 4, 100000)

time.sleep_ms(500)

while True:
    # adc_val = adc_sensor_read(adc)
    gas_val = gas_sensor_read(gas)
    th_val = th_sensor_read(th)
    pre_val = pre_sensor_read(pre)

    print("Temp and Hum ", th_val)
    print("Gas ", gas_val,)
    print("Pressure", pre_val)
    # print("ADC ", adc_val)


