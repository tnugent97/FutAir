# Import the required libraries
# Use Garbage collection for running on ESP8266
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

# Setups for the various sensors
# Temperature/Humidity Sensor Setup - SI7021
def th_sensor_setup(_scl, _sda):
    print("Temperature/Humidity Sensor Setup")
    i2c = I2C(-1, scl=Pin(_scl), sda=Pin(_sda))
    s = si7021.SI7021(i2c)
    return s

# Pressure Sensor Setup - BMP180
def pre_sensor_setup(_scl, _sda, _freq):
    print("Pressure Sensor Setup")
    i2c = I2C(scl=Pin(_scl), sda=Pin(_sda), freq=_freq)
    s = bmp180.BMP180(i2c)
    s.oversample_sett = 2
    return s

# Gas Sensor Setup - MiCS-4514
def gas_sensor_setup(_scl, _sda, _freq):
    print("Gas Sensor Setup")
    i2c = I2C(scl=Pin(_scl), sda=Pin(_sda), freq=_freq)
    s = mics4514.MICS4514(i2c)
    print("Preheating")
    s.preHeaterON()
    time.sleep_ms(10000)
    s.preHeaterOFF()
    return s

# Read fns for the sensors
# Pressure sensor read
def pre_sensor_read(sensor):
    val = sensor.pressure
    time.sleep_ms(20)
    return val

# Temperature/Humidity sensor read
def th_sensor_read(sensor):
    t = sensor.temperature()
    h = sensor.humidity()
    time.sleep_ms(20)
    return t, h

# Gas sensor read
def gas_sensor_read(sensor):
    no2 = sensor.read_OX()
    co = sensor.read_RED()
    time.sleep_ms(20)
    return no2, co

# Ip address needed for MQTT note: 192.168.0.10
# SSID: EEERover, Password: exhibition
def main(server="192.168.0.10"):
    # Setup the network
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('EEERover','exhibition')

    # init the sensors
    gas = gas_sensor_setup(5, 4, 100000)
    th = th_sensor_setup(5, 4)
    pre = pre_sensor_setup(5, 4, 100000)

    # Wait for i2c setup
    time.sleep_ms(500)

    c = MQTTClient(machine.unique_id(), server)
    c.connect()

    while True:
        # Gather readings
        no2_val, co_val = gas_sensor_read(gas)
        t_val, h_val = th_sensor_read(th)
        pre_val = pre_sensor_read(pre)
        year, month, day, hour, minute, second, ms, dayinyear = time.localtime() 

        # Create JSON message to be sent
        # Dummy Long and Lat for Imperial
        send_msg = {
            'id': "1"
            'time': [year, month, day, hour, minute, second, ms, dayinyear],
            'long': 0.1749,
            'lat': 51.4988,
            'no2': no2_val,
            'co': co_val,
            'temp': t_val,
            'hum': h_val,
            'pre': pre_val
        }

        # Print out readings for debugging
        print("Temp ", t_val)
        print("no2 ", no2_val)
        print("Pressure ", pre_val)
        print("hum ", h_val)
        print("co", co_val)

        # MQTT publish the readings
        c.publish(b"esys/Thom&Doug/test", bytes(json.dumps(send_msg), 'utf-8'))

        time.sleep_ms(10000)

    c.disconnect()

if __name__ == "__main__":
    main()





