from hardware.AD9959_v2 import AD9959 as AD9959
from hardware.ADS8685 import ADS8685 as ADS8685
import RPi.GPIO as GPIO
import time
import numpy as np


class DDS(AD9959):
    def __init__(self, bus, device, pins, max_speed):
        """Constructor for the DDS"""
        for pin in pins:
            GPIO.setup(pins[pin], GPIO.OUT)
        super().__init__(bus=bus, device=device, max_speed_hz=max_speed,
                         IO_UPDATE_PIN=pins['IO_UP'],
                         RST_PIN=pins['RESET'],
                         PWR_DWN_PIN=pins['P_DOWN'],
                         ref_clk=25e6)
        self.init_dds(channels=[0, 1, 2, 3])

    def initialize(self, settings):
        """Initializes the DDS by setting the PLL Multiplier and the Channel Outputs."""
        self.dds.set_freqmult(settings['PLL_MUL'], ioupdate=True)

        for channel in range(4):
            self.dds.set_output(channel, value=settings['channelFrequencies'][channel], var='frequency', io_update=True)
            self.dds.set_output(channel, value=settings['channelAmplitudes'][channel], var='amplitude', io_update=True)
            self.dds.set_output(channel, value=settings['channelPhases'][channel], var='phase', io_update=True)
            self.dds.set_current(channel, divider=settings['channelDividers'][channel])

    def set_rf_if(self, r_f, i_f, rf_channels=None, lo_channels=None):
        """Sets the channel frequencies for the RF and LO signals on the board."""
        if lo_channels is None:
            lo_channels = [2, 3]
        if rf_channels is None:
            rf_channels = [0, 1]
        r_f = float(r_f) * 1e6
        i_f = float(i_f) * 1e3

        self.set_output(rf_channels, value=r_f + i_f, var='frequency', io_update=True)
        self.set_output(lo_channels, value=r_f, var='frequency', io_update=True)

    def load_settings(self, settings):
        self.set_freqmult(settings['PLL_MUL'], ioupdate=True)
        self.set_rf_if(r_f=settings['RF'],
                       i_f=settings['IF'])
        for channel in range(4):
            self.set_output(channel,
                            value=settings['channelAmplitudes'][channel],
                            var='amplitude',
                            io_update=True)
            self.set_output(channel,
                            value=settings['channelPhases'][channel],
                            var='phase',
                            io_update=True)
            self.set_current(channel,
                             settings['channelDividers'][channel],
                             ioupdate=True)


class ADC:
    def __init__(self, bus, device, reset_pin, max_speed):
        """Constructor for the ADC"""
        self.adc = ADS8685.ADS8685(bus=bus, device=device, reset_pin=reset_pin, max_speed_hz=max_speed)

    def initialize(self, settings):
        """Initialize the ADC"""
        self.adc.set_range(settings['defaultRange'])


class Demodulator:
    def __str__(self):
        return f'Demodulator-{self.channel}'

    def __repr__(self):
        return f'Demodulator-{self.channel} based on AD630. The amp_pha_pin is {self.amp_pha_pin}.'

    def __init__(self, adc: ADS8685, laser_on_time, settings, channel=None):
        """Initialize the Demodulator"""
        if channel is None:
            self.channel = 0
        else:
            self.channel = channel

        self.adc = adc
        self.laser_on_time = laser_on_time
        self.integration_number = 1

        self.amp_pha_pin = settings[str(self)]['amp_pha_pin']
        GPIO.setup(self.amp_pha_pin, GPIO.OUT)

        self.amplitude_coefficients = settings[str(self)]['amplitude_coefficients']
        self.phase_coefficients = settings[str(self)]['phase_coefficients']

    def set_integration_number(self, n):
        """
        Sets the number of the measurements to be integrated
        :param n: The number of the measurements to be integrated
        :return: None
        """
        self.integration_number = n

    def set2amp(self):
        """
        Sets the Demodulator to amplitude measurement mode
        :return: None
        """
        GPIO.output(self.amp_pha_pin, True)

    def set2pha(self):
        """
        Sets the Demodulator to phase measurement mode
        :return: None
        """
        GPIO.output(self.amp_pha_pin, False)

    def measure_amplitude(self, raw=False):
        """
        Measures the amplitude of the IF signal  in mV
        :param raw: Whether to return to amplitude of the IF signal or the raw ADC result
        :return: The amplitude of the IF in mV.
        """
        self.set2amp()
        time.sleep(self.laser_on_time / 2)

        temp = np.zeros(self.integration_number)
        for i in range(temp):
            temp[i] = self.adc.convert()
        voltage = temp.mean() * 1000

        if not raw:
            amplitude = (voltage - self.amplitude_coefficients['intercept']) / self.amplitude_coefficients['slope']
            return amplitude
        else:
            return voltage

    def measure_phase(self, amplitude=None, raw=False):
        """
        Measures the amplitude of the IF signal  in mV
        :param amplitude: Amplitude information is needed for phase measurement
        :param raw: Whether to return to phase of the IF signal or the raw ADC result
        :return: The phase of the IF in degrees.
        """
        self.set2pha()
        time.sleep(self.laser_on_time / 2)

        temp = np.zeros(self.integration_number)
        for i in range(temp):
            temp[i] = self.adc.convert()
        voltage = temp.mean()

        if not raw:
            if amplitude is None:
                phase = self.voltage_to_phase(voltage, self.measure_amplitude())
            else:
                phase = self.voltage_to_phase(voltage, amplitude)

            return round(phase, 2)
        else:
            return voltage

    def voltage_to_phase(self, voltage, amplitude):
        """
        Converts the measured voltage that's a function of the phase and the amplitude of the IF signal in to phase
        :param voltage: Measured voltage
        :param amplitude: Amplitude of the IF
        :return: Phase of the IF in degrees
        """
        x = (voltage - np.log(amplitude) * self.phase_coefficients['offset']) / \
            (self.phase_coefficients['A'] * self.phase_coefficients['freq'])
        y = np.arcsin(x)
        phase = (y / (2 * np.pi * self.phase_coefficients['phi'])) - 90

        return -phase


class Laser:
    def __init__(self, wavelength, pin):
        self.wavelength = wavelength
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

        self.turn_off()

    def turn_on(self):
        GPIO.output(self.pin, True)

    def turn_off(self):
        GPIO.output(self.pin, False)
