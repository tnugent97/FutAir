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

degree = bytes([0x6,0x9,0x9,0x6,0x0,0x0,0x0,0x0])
lcd.create_char(0, degree)
