from umqtt.simple import MQTTClient
gc.collect()
import network
gc.collect()
import machine
gc.collect()
import json
gc.collect()
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

def main(server="192.168.0.10"):
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('EEERover','exhibition')

    gas = gas_sensor_setup(5, 4, 100000)
    th = th_sensor_setup(5, 4)
    pre = pre_sensor_setup(5, 4, 100000)

    time.sleep_ms(500)

    c = MQTTClient(machine.unique_id(), server)
    c.connect()

    while True:
        no2_val, co_val = gas_sensor_read(gas)
        t_val, h_val = th_sensor_read(th)
        pre_val = pre_sensor_read(pre)

        send_msg = {
            'NO2': no2_val,
            'Temperature': t_val,
            'Humidity': h_val,
            'Pressure': pre_val,
            'CO': co_val
        }

        print("Temp ", t_val)
        print("no2 ", no2_val)
        print("Pressure ", pre_val)
        print("hum ", h_val)
        print("co", co_val)

        c.publish(b"esys/Thom&Doug/test", bytes(json.dumps(send_msg), 'utf-8'))

        time.sleep_ms(5000)

    c.disconnect()

if __name__ == "__main__":
    main()
