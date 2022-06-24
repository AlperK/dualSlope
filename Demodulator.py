import ADS8685
import funcs
import time
import RPi.GPIO as GPIO
import numpy as np


def voltage2phase4sine(phase_voltage, p):
    x = (phase_voltage - np.log(p[0]) * p[3]) / (p[0] * p[1])
    y = np.arcsin(x)
    phase = (y / (2 * np.pi * p[2])) - 90
    return -phase


class Demodulator:
    def __init__(self, adc: ADS8685.ADS8685, amp_pha, laser_on_time):
        self.ADC = adc
        self.amp_pha = amp_pha
        GPIO.setup(amp_pha, GPIO.OUT)
        self.laser_on_time = laser_on_time

    def measure_amplitude(self, channel=None):
        if channel == 1:
            slope = 0.30148
            intercept = 3.199
        else:
            slope = 0.3009
            intercept = 2.488
        funcs.set_adc2amp(self.amp_pha)
        time.sleep(self.laser_on_time/2)

        temp = np.zeros(256)
        for i in range(256):
            temp[i] = self.ADC.convert()
        amplitude_voltage = temp.mean() * 1000
        amplitude = (amplitude_voltage - intercept) / slope
        return amplitude

    def measure_phase(self, channel=None):
        if channel == 1:
            a = 301.17
            b = 0.00277773
            c = -1.247
        elif channel == 2:
            a = 300.466
            b = 0.00277773
            c = -0.912
        else:
            a = 301.17
            b = 0.00277773
            c = 0
        funcs.set_adc2pha(self.amp_pha)
        time.sleep(self.laser_on_time/2)

        temp = np.zeros(256)
        for i in range(256):
            temp[i] = (self.ADC.convert())
        phase_voltage = temp.mean()

        amplitude = self.measure_amplitude(channel=channel) / 1000
        result = voltage2phase4sine(1000 * phase_voltage, [amplitude, a, b, c])
        return round(result, 2)

        # return self.ADC.convert()

    def measure_amplitude_voltage(self):
        funcs.set_adc2amp(self.amp_pha)
        time.sleep(self.laser_on_time/2)

        temp = np.zeros(256)
        for i in range(256):
            temp[i] = (self.ADC.convert())
        amplitude_voltage = temp.mean()

        return amplitude_voltage

    def measure_phase_voltage(self):
        funcs.set_adc2pha(self.amp_pha)
        time.sleep(self.laser_on_time/2)

        temp = np.zeros(256)
        for i in range(256):
            temp[i] = (self.ADC.convert())
        phase_voltage = temp.mean()

        return phase_voltage
