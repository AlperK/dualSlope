import ADS8685
import funcs
import time
import RPi.GPIO as GPIO


class Demodulator:
    def __init__(self, adc: ADS8685.ADS8685, amp_pha, laser_on_time):
        self.ADC = adc
        self.amp_pha = amp_pha
        GPIO.setup(amp_pha, GPIO.OUT)
        self.laser_on_time = laser_on_time

    def measure_amplitude(self):
        funcs.set_adc2amp(self.amp_pha)
        time.sleep(self.laser_on_time/2)
        return self.ADC.convert()

    def measure_phase(self):
        funcs.set_adc2pha(self.amp_pha)
        time.sleep(self.laser_on_time/2)
        return self.ADC.convert()

