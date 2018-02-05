from umqtt.simple import MQTTClient
from machine import I2C
from machine import Pin
import time
import network
import machine
import ads1115
import mics4514
import si7021

def th_sensor_setup(_scl, _sda):
    print("Temperature/Humidity Sensor Setup")
    i2c = I2C(-1, scl=Pin(_scl), sda=Pin(_sda))
    s = si7021.SI7021(i2c)
    return s

def adc_sensor_setup(_scl, _sda, _freq):
    print("Analogue to Digital Converter Sensor Setup")
    i2c = I2C(scl=Pin(_scl), sda=Pin(_sda), freq=_freq)
    s = ads1115.ADS1115(i2c)
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

def adc_sensor_read(sensor):
    val = sensor.read(4, 0)
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


adc = adc_sensor_setup(13, 12, 100000)
# gas = gas_sensor_setup(7, 6, 100000)
th = th_sensor_setup(5, 4)

time.sleep_ms(500)

while True:
    adc_val = adc_sensor_read(adc)
    # gas_val = gas_sensor_read(gas)
    th_val = th_sensor_read(th)

    print("Temp and Hum ", th_val)
    # print("Gas ", gas_val,)
    print("ADC ", adc_val)

# def main(server="192.168.0.10"):
#     ap_if = network.WLAN(network.AP_IF)
#     ap_if.active(False)

#     sta_if = network.WLAN(network.STA_IF)
#     sta_if.active(True)
#     sta_if.connect('EEERover','exhibition')

#     adc = adc_sensor_setup(5, 4, 100000)
#     gas = gas_sensor_setup(7, 6, 100000)
#     th = th_sensor_setup(9, 8, 100000)

#     adc_val = adc_sensor_read(adc)
#     gas_val = gas_sensor_read(gas)
#     th_val = th_sensor_read(th)

#     print(adc_val, gas_val, th_val)

#     c = MQTTClient(machine.unique_id(), server)
#     c.connect()
#     c.publish(b"esys/Thom&Doug/test", bytes("hello", 'utf-8'))
#     c.disconnect()

