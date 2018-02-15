from machine import I2C
from machine import Pin
import time
import ads1115
import math
# D12 pin for the pre-heating element
PIN_HEATING_NO2 = 12


RED_SENSOR_CH = 1 #CO, Ammonia, H2S, Ethanol, Hydrogen...
OX_SENSOR_CH = 0 #NO2, NO, Hydrogen
ADC_RATE = 4

CALIB_R0_NO2 = 22000    #R0 calibration value for the NO2 sensor
CALIB_R0_CO = 47000   #R0 calibration value for the CO sensor

class MICS4514:
    def __init__(self, i2c):
        self.i2c = i2c
        self.adc = ads1115.ADS1115(i2c)
        self.heating_pin = Pin(PIN_HEATING_NO2, Pin.OUT)
        self.red_val = 0
        self.ox_val = 0

    def preHeaterON(self):
        self.heating_pin.on()

    def preHeaterOFF(self):
        self.heating_pin.off()

    def volt_RED(self):
        value = self.adc.read(ADC_RATE, RED_SENSOR_CH)
        volts = (value * 3.3) / 32768 # 2^15, max V is 3.3
        return volts

    def volt_OX(self):
        value = self.adc.read(ADC_RATE, OX_SENSOR_CH)
        volts = (value * 3.3) / 32768 # 2^15, max V is 3.3
        return volts

    def read_RED(self):
        value = self.adc.read(ADC_RATE, RED_SENSOR_CH)
        volts = (value * 3.3) / 32768 # 2^15, max V is 3.3
        fRes = (3.3 - volts) / volts

        #values measured from graph
        k = 0.5440680444
        m = -0.8480226815

        log_val = math.log(fRes) / math.log(10) #equivalent to log10

        #converts straight line from datasheet to equation
        conc = 10 ** ((log_val - k) / m)

        return conc



    def read_OX(self):
        value = self.adc.read(ADC_RATE, OX_SENSOR_CH)
        volts = (value * 3.3) / 32768 # 2^15, max V is 3.3
        fRes = (3.3 - volts) / volts

        #values measured from graph
        k = 0.7403626895
        m = 0.99673

        log_val = math.log(fRes) / math.log(10) #equivalent to log10

        #converts straight line from datasheet to equation
        conc = 10 ** ((log_val - k) / m)

        return conc
