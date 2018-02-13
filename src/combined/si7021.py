from micropython import const
import ustruct
import sys


_HUMID_NOHOLD = const(0xf5)
_TEMP_NOHOLD = const(0xf3)
_RESET = const(0xfe)
_READ_USER1 = const(0xe7)
_USER1_VAL = const(0x3a)

# The el' classico cyclic redundancy code
def _crc(data):
    crc = 0
    for byte in data:
        crc ^= byte
        for i in range(8):
            if crc & 0x80:
                crc <<= 1
                crc ^= 0x131
            else:
                crc <<= 1
    return crc


class SI7021:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.init()
        self._measurement = 0

    def init(self):
        self.reset()
        # make sure settings correct
        while True:
            # whilst restarting sensor doesn't respond
            try:
                if hasattr(self.i2c, 'readfrom_mem'):
                    value = self.i2c.readfrom_mem(
                        self.address, _READ_USER1, 1)[0]
                else:
                    data = bytearray([_READ_USER1])
                    self.i2c.writeto(self.address, data, stop=False)
                    self.i2c.readfrom_into(self.address, data)
                    value = data[0]
            except OSError as e:
                if e.args[0] not in ('I2C bus error', 19): # errno 19 ENODEV (triggered)
                    raise
            else:
                break
        if value != _USER1_VAL:
            raise RuntimeError("bad USER1 register (%x!=%x)" % (
                value, _USER1_VAL))

    def _command(self, command):
        self.i2c.writeto(self.address, ustruct.pack('B', command))

    def _data(self):
        data = bytearray(3)
        data[0] = 0xff
        while True:
            # while it is busy the sensor won't respond to reads
            try:
                self.i2c.readfrom_into(self.address, data)
            except OSError as e:
                if e.args[0] not in ('I2C bus error', 19): # errno 19 ENODEV
                    raise
            else:
                if data[0] != 0xff: # read success?
                    break
        value, checksum = ustruct.unpack('>HB', data)
        if checksum != _crc(data[:2]):
            raise ValueError("CRC mismatch")
        return value

    def reset(self):
        self._command(_RESET)

    def humidity(self, raw=False, block=True):
        # humidity read
        if not self._measurement:
            self._command(_HUMID_NOHOLD)
        elif self._measurement != _HUMID_NOHOLD:
            raise RuntimeError("other measurement in progress")
        # if block is true, block until ready and return the
        # measured value, if false return none.
        if not block:
            self._measurement = _HUMID_NOHOLD
            return None
        self._measurement = 0
        value = self._data()
        # if raw is true, return measured value as 16-bit int
        # else convert it to percentage and return float
        if raw:
            return value
        return value * 125 / 65536 - 6

    def temperature(self, raw=False, block=True):
        # temp read
        if not self._measurement:
            self._command(_TEMP_NOHOLD)
        elif self._measurement != _TEMP_NOHOLD:
            raise RuntimeError("other measurement in progress")
        # if block is true, block until ready and return the
        # measured value, if false return none.
        if not block:
            self._measurement = _TEMP_NOHOLD
            return None
        self._measurement = 0
        value = self._data()
        # if raw is true, return measured value as 16-bit int
        # else convert it to Celsius return float
        if raw:
            return value
        return value * 175.72 / 65536 - 46.85
