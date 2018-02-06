import time
from machine import Pin
from micropython import const

LCD_CLEARDISPLAY        = const(0x01)
LCD_RETURNHOME          = const(0x02)
LCD_ENTRYMODESET        = const(0x04)
LCD_DISPLAYCONTROL      = const(0x08)
LCD_CURSORSHIFT         = const(0x10)
LCD_FUNCTIONSET         = const(0x20)
LCD_SETCGRAMADDR        = const(0x40)
LCD_SETDDRAMADDR        = const(0x80)

LCD_ENTRYRIGHT          = const(0x00)
LCD_ENTRYLEFT           = const(0x02)
LCD_ENTRYSHIFTINCREMENT = const(0x01)
LCD_ENTRYSHIFTDECREMENT = const(0x00)

LCD_DISPLAYON           = const(0x04)
LCD_DISPLAYOFF          = const(0x00)
LCD_CURSORON            = const(0x02)
LCD_CURSOROFF           = const(0x00)
LCD_BLINKON             = const(0x01)
LCD_BLINKOFF            = const(0x00)

LCD_DISPLAYMOVE         = const(0x08)
LCD_CURSORMOVE          = const(0x00)
LCD_MOVERIGHT           = const(0x04)
LCD_MOVELEFT            = const(0x00)

LCD_8BITMODE            = const(0x10)
LCD_4BITMODE            = const(0x00)
LCD_2LINE               = const(0x08)
LCD_1LINE               = const(0x00)
LCD_5X10DOTS            = const(0x04)
LCD_5X8DOTS             = const(0x00)

LCD_ROW_OFFSETS         = (0x00, 0x40, 0x14, 0x54)

_MCP23008_LCD_RS         = const(1)
_MCP23008_LCD_EN         = const(2)
_MCP23008_LCD_D4         = const(3)
_MCP23008_LCD_D5         = const(4)
_MCP23008_LCD_D6         = const(5)
_MCP23008_LCD_D7         = const(6)
_MCP23008_LCD_BACKLIGHT  = const(7)

_74HC595_LCD_RS          = const(1)
_74HC595_LCD_EN          = const(2)
_74HC595_LCD_D4          = const(6)
_74HC595_LCD_D5          = const(5)
_74HC595_LCD_D6          = const(4)
_74HC595_LCD_D7          = const(3)
_74HC595_LCD_BACKLIGHT   = const(7)

def _set_bit(byte_value, position, val):
    ret = None
    if val:
        ret = byte_value | (1 << position)
    else:
        ret = byte_value & ~(1 << position)

    return ret

class Character_LCD(object):
    def __init__(self, rs, en, d4, d5, d6, d7, cols, lines,
                 backlight=None
                ):

        self.cols = cols
        self.lines = lines
        #  save pin numbers
        self.reset = rs
        self.enable = en
        self.dl4 = d4
        self.dl5 = d5
        self.dl6 = d6
        self.dl7 = d7
        self.backlight = backlight
        self._write8(0x33)
        self._write8(0x32)
        self.displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.displayfunction = LCD_4BITMODE | LCD_1LINE | LCD_2LINE | LCD_5X8DOTS
        self.displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
        self._write8(LCD_DISPLAYCONTROL | self.displaycontrol)
        self._write8(LCD_FUNCTIONSET | self.displayfunction)
        self._write8(LCD_ENTRYMODESET | self.displaymode)
        self.clear()

    def home(self):
        self._write8(LCD_RETURNHOME)
        time.sleep(0.003)

    def clear(self):
        self._write8(LCD_CLEARDISPLAY)
        time.sleep(0.003)

    def show_cursor(self, show):
        if show:
            self.displaycontrol |= LCD_CURSORON
        else:
            self.displaycontrol &= ~LCD_DISPLAYON
        self._write8(LCD_DISPLAYCONTROL | self.displaycontrol)

    def set_cursor(self, col, row):
        if row > self.lines:
            row = self.lines - 1
        # Set location
        self._write8(LCD_SETDDRAMADDR | (col + LCD_ROW_OFFSETS[row]))

    def blink(self, blink):
        if blink is True:
            self.displaycontrol |= LCD_BLINKON
        else:
            self.displaycontrol &= ~LCD_BLINKON
        self._write8(LCD_DISPLAYCONTROL | self.displaycontrol)

    def move_left(self):
        self._write8(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)

    def move_right(self):
        self._write8(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)

    def set_left_to_right(self):
        self.displaymode |= LCD_ENTRYLEFT
        self._write8(LCD_ENTRYMODESET | self.displaymode)

    def set_right_to_left(self):
        self.displaymode |= LCD_ENTRYLEFT
        self._write8(LCD_ENTRYMODESET | self.displaymode)

    def enable_display(self, enable):
        if enable:
            self.displaycontrol |= LCD_DISPLAYON
        else:
            self.displaycontrol &= ~LCD_DISPLAYON
        self._write8(LCD_DISPLAYCONTROL | self.displaycontrol)

    def _write8(self, value, char_mode=False):
        # Sends 8b ``value`` in ``char_mode``.
        # :param value: bytes
        # :param char_mode: character/data mode selector. False (default) for
        # data only, True for character bits.
        #  one ms delay to prevent writing too quickly.
        time.sleep(0.001)
        #  set character/data bit. (charmode = False)
        self.reset.value(char_mode)
        # WRITE upper 4 bits
        self.dl4.value(((value >> 4) & 1) > 0)
        self.dl5.value(((value >> 5) & 1) > 0)
        self.dl6.value(((value >> 6) & 1) > 0)
        self.dl7.value(((value >> 7) & 1) > 0)
        #  send command
        self._pulse_enable()
        # WRITE lower 4 bits
        self.dl4.value((value & 1) > 0)
        self.dl5.value(((value >> 1) & 1) > 0)
        self.dl6.value(((value >> 2) & 1) > 0)
        self.dl7.value(((value >> 3) & 1) > 0)
        self._pulse_enable()

    def _pulse_enable(self):
        # Pulses (lo->hi->lo) to send commands.
        self.enable.value(0)
        # 1microsec pause
        time.sleep(0.0000001)
        self.enable.value(1)
        time.sleep(0.0000001)
        self.enable.value(0)
        time.sleep(0.0000001)

    def set_backlight(self, lighton):
        if lighton:
            self.backlight.value(0)
        else:
            self.backlight.value(1)


    def message(self, text):
        line = 0
        #  iterate thru each char
        for char in text:
            # if character is \n, go to next line
            if char == '\n':
                line += 1
                #  move to left/right depending on text direction
                col = 0 if self.displaymode & LCD_ENTRYLEFT > 0 else self.cols-1
                self.set_cursor(col, line)
            # Write character to display
            else:
                self._write8(ord(char), True)

    def create_char(self, location, pattern):
        location &= 0x7
        self._write8(LCD_SETCGRAMADDR | (location << 3))
        for i in range(8):
            self._write8(pattern[i], char_mode=True)

#pylint: enable-msg=too-many-instance-attributes
