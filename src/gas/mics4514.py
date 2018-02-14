from machine import I2C
from machine import Pin
import time
import ads1115

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
        volts = (value * 3.3) / 32768 # 2^16, max V is 3.3
        return volts

    def volt_OX(self):
        value = self.adc.read(ADC_RATE, OX_SENSOR_CH)
        volts = (value * 3.3) / 32768 # 2^16, max V is 3.3
        return volts

    def read_RED(self):
        value = self.adc.read(ADC_RATE, RED_SENSOR_CH)
        print("RED ADC: ", value)
        volts = (value * 3.3) / 32768 # 2^16, max V is 3.3
        print("RED VOLTS: ", volts)
        Rs = 3300 / volts
        print("RED Rs", Rs)
        fRes = Rs / CALIB_R0_CO # get Rs / R0 value
        print("RED fRes", fRes)
        thomnis_test = (3.3 - volts) / volts
        print("RED AGOM: ", thomnis_test)

        # convert to ppm
        # see datasheet graph
        # checking if in valid sensor detection range
        if fRes > 0.7:
            fRes = 0.7
        if fRes > 0.6:
            fConc = (0.711 - fRes) / 0.011
        elif fRes > 0.3:
            fConc = (0.7 - fRes) / 0.01
        else:
            fConc = (0.3233 - fRes) / 0.00058

        return fConc

    def read_OX(self):
        value = self.adc.read(ADC_RATE, OX_SENSOR_CH)
        print("OX ADC: ", value)
        volts = (value * 3.3) / 32768 # 2^16, max V is 3.3
        print("OX VOLTS: ", volts)
        Rs = 3300 / volts
        print("OX Rs", Rs)
        # fRes = Rs / CALIB_R0_NO2 #get Rs / R0 value
        # print("OX fRes: ", fRes)
        fRes = (3.3 - volts) / volts
        # print("OX AGOM: ", thomnis_test)
        print("OX fRes: ", fRes)

        k = 10**(5/599)
        conc = (fRes/k)**(1198/7985)
        print("OX CONC: ", conc)



        #print("ox",fRes)
        # convert to ppm
        # see datasheet graph
        # checking if in valid sensor detection range
        # if fRes < 3.0:
        #     fRes = 3.0
        # if fRes >= 3.0 and fRes < 8.0:
        #     fConc = (fRes - 0.5) / 0.25
        # else:
        #     fConc = (fRes + 129.655) / 4.589

        # return fConc
