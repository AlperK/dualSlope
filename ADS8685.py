import spidev
import numpy as np
import RPi.GPIO as GPIO
import time

_registers = {
    'DEVICE_ID_REG': 0x00,
    'RST_PWRCTL_REG': 0x04,
    'SDI_CTL_REG': 0x08,
    'SDO_CTL_REG': 0x0C,
    'DATAOUT_CTL_REG': 0x10,
    'RANGE_SEL_REG': 0x14,
    'ALARM_REG': 0x20,
    'ALARM_H_TH_REG': 0x24,
    'ALARM_L_TH_REG': 0x28
}

_ranges = {
    0b0000: (+3.0, -3.0),
    0b0001: (+2.5, -2.5),
    0b0010: (+1.5, -1.5),
    0b0011: (+1.25, -1.25),
    0b0100: (+0.625, -0.625),
    0b1000: (+3.0, 0),
    0b1001: (+2.5, 0),
    0b1010: (+1.5, 0),
    0b1011: (+1.25, 0)}

READ = 0xC8
WRITE = 0xD0


class ADS8685:
    def __init__(self, bus, device, reset_pin):
        self.pos_full_scale = None
        self.neg_full_scale = None
        self.full_scale = None
        self.range = None
        self.LSB = None
        
        self.init_adc()

        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000

        self.reset_pin = reset_pin
        GPIO.setup(reset_pin, GPIO.OUT)
        GPIO.output(reset_pin, True)

    def __del__(self):
        GPIO.cleanup()

    def init_adc(self):
        self.pos_full_scale = +3 * 4.096
        self.neg_full_scale = -3 * 4.096
        self.range = self.pos_full_scale - self.neg_full_scale
        self.LSB = self.range / 2 ** 16

        # self.DATA_VAL = 0b000
        # self.RANGE_INCL = 0b0

        # self.value = bytearray(2)

    def reset(self):
        GPIO.output(self.reset_pin, False)
        time.sleep(10e-6)
        GPIO.output(self.reset_pin, True)
        time.sleep(20e-6)

        self.pos_full_scale = _ranges[0b000][0] * 4.096
        self.neg_full_scale = _ranges[0b000][1] * 4.096
        self.full_scale = self.pos_full_scale - self.neg_full_scale
        self.LSB = self.full_scale / 2 ** 16

    def get_range(self):
        mask = 0b00001111
        content = self._read('RANGE_SEL_REG')
        range_sel = content[1] & mask
        print(range_sel)
        return 'Full Scale Range: {0}V to {1}V'.format(_ranges[range_sel][1] * 4.096, _ranges[range_sel][0] * 4.096)

    def set_range(self, range_sel):
        assert range_sel in _ranges, '%i is not a valid range.' % range_sel
        self._write('RANGE_SEL_REG', range_sel)

        self.pos_full_scale = _ranges[range_sel][0] * 4.096
        self.neg_full_scale = _ranges[range_sel][1] * 4.096
        self.full_scale = self.pos_full_scale - self.neg_full_scale
        self.LSB = self.full_scale / 2 ** 16
        print('Positive Full Scale: {0}V, Negative Full Scale: {1}'.format(self.pos_full_scale, self.neg_full_scale))

    def _create_message(self, op_code, reg_address, message_0=0x0, message_1=0x0):
        return [op_code, reg_address, message_0, message_1]

    def _read(self, register):
        assert register in _registers, '%r is not a valid register. Register must be passed as string.' % register

        reg = bytearray(2)
        message = self._create_message(READ, _registers[register])
        # ~ self.spi.write(message)
        self.spi.xfer(message)
        reg = self.spi.xfer(message)
        # ~ reg = self.spi.readbytes(2)
        return reg

    def _write(self, register, data):
        assert register in _registers, '%r is not a valid register. Register must be passed as string.' % register

        message = self._create_message(WRITE, _registers[register], 0x00, data)
        a = self.spi.xfer(message)

    def convert(self):
        self.spi.xfer([0x0, 0x0])
        value = self.spi.xfer([0x0, 0x0])
        # ~ return value
        return value[0] * self.LSB * 2 ** 8 + value[1] * self.LSB + self.neg_full_scale
