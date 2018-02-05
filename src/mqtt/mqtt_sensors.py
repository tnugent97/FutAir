from umqtt.simple import MQTTClient
import time
import network
import machine
import ads1115
import mics4514
import si7021

def th_sensor_setup(_scl, _sda, _freq):
    print("Temperature/Humidity Sensor Setup")
    i2c = I2C(scl=Pin(_scl), sda=Pin(_sda), freq=_freq)
    s = si7021.SI7021(i2c)
    time.sleep_ms(500)
    return s

def adc_sensor_setup(_scl, _sda, _freq):
    print("Analogue to Digital Converter Sensor Setup")
    i2c = I2C(scl=Pin(_scl), sda=Pin(_sda), freq=_freq)
    s = ads1115.ADS1115(i2c)
    time.sleep_ms(500)
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
    time.sleep(20)
    return t, h

def gas_sensor_read(sensor):
    no2 = sensor.read_OX()
    co = sensor.read_RED()
    time.sleep(20)
    return no2, co

def main(server="192.168.0.10"):
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('EEERover','exhibition')

    c = MQTTClient(machine.unique_id(), server)
    c.connect()
    c.publish(b"esys/Thom&Doug/test", bytes("hello", 'utf-8'))
    c.disconnect()

if __name__ == "__main__":
    main()

