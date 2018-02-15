#demo for lcd; cannot run with sensors because not enough memory on esp
import time
from machine import Pin
import character_lcd

lcd_columns = 16
lcd_rows = 2

lcd_rs = Pin(14, Pin.OUT)
lcd_en = Pin(12, Pin.OUT)
lcd_d7 = Pin(16, Pin.OUT)
lcd_d6 = Pin(0, Pin.OUT)
lcd_d5 = Pin(15, Pin.OUT)
lcd_d4 = Pin(13, Pin.OUT)

lcd = character_lcd.Character_LCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

while True:
    lcd.message('Temp: 20')
    lcd.message('\x00')
    lcd.message('C\n')
    lcd.message('Pressure: 1Bar')

    time.sleep(4)
    lcd.clear()

    lcd.message('NO2: 0.1ppm\n')
    lcd.message('CO: 1.3ppm')

    time.sleep(4)
    lcd.clear()

    lcd.message('Humidity: 42%')

    time.sleep(4)
    lcd.clear()
