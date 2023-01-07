import time
from pathlib import Path
import threading
import numpy as np
import json


def demodulator_count_generator():
    def init():
        return 0

    num = init()
    while True:
        val = (yield num % 2)
        if val == 'restart':
            i = init()
        else:
            num += 1


def laser_count_generator():
    def init():
        return 0

    num = init()
    while True:
        val = (yield num % 4)
        if val == 'restart':
            i = init()
        else:
            num += 1


def _linearize_amplitudes(amplitudes, separations, average=False):
    if average:
        return np.average(np.log(np.square(separations) * amplitudes), axis=1)
    else:
        return np.log(np.square(separations)*amplitudes)


def _get_slope(arr, separations, average=False, is_phase=False):
    # if is_phase:
    #
    #     if average:
    #         print(np.diff(separations))
    #         return np.average((np.diff(arr) % (np.pi/2)) / np.diff(separations), axis=2)
    #     else:
    #         print(np.diff(separations))
    #         return np.diff(arr) / np.diff(separations)
    #
    # else:
    if average:
        # print(np.diff(separations))
        return np.average(np.diff(arr) / np.diff(separations), axis=2)
    else:
        # print(np.diff(separations))
        return np.diff(arr) / np.diff(separations)


class Measurement:
    def __init__(self, laser_on_time, save_location=None, app=None):
        self.save_location = save_location
        if self.save_location is not None:
            self.amplitude_save_location = Path.joinpath(self.save_location,
                                                         'amplitude.csv')
            self.phase_save_location = Path.joinpath(self.save_location,
                                                     'phase.csv')

        self.started = False
        self.paused = False
        self.laser_on_time = laser_on_time

        self.laser_count_generator = laser_count_generator()
        self.laser_count = next(self.laser_count_generator)

        self.demodulator_count_generator = demodulator_count_generator()
        self.demodulator_count = next(self.demodulator_count_generator)

        self.r1 = 25
        self.r2 = 10

        self.amplitudes = np.array([])
        self.phases = np.array([])

        self.app = app

    def start(self):
        self.started = True
        self.paused = False

    def stop(self):
        self.started = False
        self.paused = False

        self.laser_count_generator.send('restart')
        self.laser_count = 0

        self.demodulator_count_generator.send('restart')
        self.demodulator_count = 0

        self.reset_arrays()

    def pause(self):
        self.paused = True
        self.started = False

    def unpause(self):
        self.paused = False
        self.started = True

    def create_measurement_files(self, app_save_location):
        self.base = app_save_location
        self.base.mkdir(parents=True, exist_ok=True)

        Path.joinpath(self.base, Path('amplitude.csv')).touch()
        Path.joinpath(self.base, Path('phase.csv')).touch()
        Path.joinpath(self.base, Path('measurement settings.json')).touch()

    def take_measurement(self):

        while self.started:
            self.app.write_event_value('__MEAS_PROGRESS__', [self.laser_count, self.demodulator_count])

            self.demodulator_count = next(self.demodulator_count_generator)
            if self.demodulator_count == 0:
                self.laser_count = next(self.laser_count_generator)
            time.sleep(self.laser_on_time)

        return f't'

    def start_measurement_on_a_thread(self):
        threading.Thread(target=self.take_measurement, daemon=True).start()

    def reset_arrays(self):
        self.amplitudes = np.array([])
        self.phases = np.array([])

    def save_arrays(self):
        with open(self.amplitude_save_location, 'a+') as f:
            np.savetxt(f, X=[self.amplitudes], delimiter=',', fmt='%4.2f')
        with open(self.phase_save_location, 'a+') as f:
            np.savetxt(f, X=[self.phases], delimiter=',', fmt='%3.2f')

    def get_slopes(self, average=False):
        """
        Calculates the amplitude and phase slopes.
        :return: ([amplitude_slope_1, amplitude_slope_2], [phase_slope_1, phase_slope_2])
        """

        separations = np.array([[[self.r1, self.r1 + self.r2], [self.r1 + self.r2, self.r1]],
                                [[self.r1, self.r1 + self.r2], [self.r1 + self.r2, self.r1]]])
        amplitudes = self.amplitudes.reshape((2, 2, 2))
        linearized_amplitudes = _linearize_amplitudes(amplitudes, separations)

        phases = np.deg2rad(self.phases.reshape((2, 2, 2)))

        if average:
            amplitude_slopes = np.average(_get_slope(linearized_amplitudes, separations, average, is_phase=False), axis=1)
            # print(linearized_amplitudes)
            # print(amplitude_slopes)
            phase_slopes = np.average(_get_slope(phases, separations, average, is_phase=False), axis=1)
        else:
            amplitude_slopes = _get_slope(linearized_amplitudes, separations, average, is_phase=False)
            phase_slopes = _get_slope(phases, separations, average, is_phase=False)

        # print(amplitude_slopes)
        # print(phase_slopes)
        return amplitude_slopes, phase_slopes

    def _get_optical_parameters(self, frequency, wavelength):
        # print(frequency)
        if wavelength == 830:
            i = 0
        if wavelength in [685, 690]:
            i = 1
        else:
            print("ERROR")
            return
        separations = np.array([[[self.r1, self.r2], [self.r2, self.r1]],
                                [[self.r1, self.r2], [self.r2, self.r1]]])
        # amplitudes = self.amplitudes.reshape((2, 2, 2))[i]
        amplitudes = self.amplitudes.reshape((2, 2, 2))
        # amplitudes *= np.array([[[1, 1], [1, 1]],
        #                         [[1, 1], [1.109*1, 1.04]]])
        # amplitudes *= np.array([[[1, 1], [1, 1]],
        #                         [[1, 1.1157], [1, 1.1157]]])
        # phases = self.phases.reshape((2, 2, 2))[i]
        phases = self.phases.reshape((2, 2, 2))
        # phases += np.array([[[0, 0], [0, 0]],
        #                     [[0, 0], [2.4, 6.9]]])
        # phases += np.array([[[0, 0], [0, 0]],
        #                     [[15.75, 0], [15.75, 0]]])

        linearized_amplitudes = _linearize_amplitudes(amplitudes, separations)
        amplitude_slopes = _get_slope(linearized_amplitudes, separations, average=True, is_phase=False)
        phase_slopes = _get_slope(phases, separations, average=True, is_phase=False)
        c = 2.998e11
        n = 1.4
        mod_frequency = 2 * np.pi * frequency
        amplitude_slope, phase_slope = self.get_slopes(average=True)
        # print(f'Sac: {amplitude_slope}, average: {np.average(amplitude_slope)}')
        # print(f'Sp: {phase_slope}, average: {np.average(phase_slope)}')

        absorption_coefficient = (mod_frequency * n) / (2 * c)
        absorption_coefficient *= (phase_slope / amplitude_slope) - (amplitude_slope / phase_slope)

        scattering_coefficient = (amplitude_slope ** 2 - phase_slope ** 2) / (3 * absorption_coefficient)

        return absorption_coefficient, scattering_coefficient

    def save_measurement_settings(self, app):
        measurement_settings = {
            'RF': str(app['__DDS_RF__'].get()),
            'IF': str(app['__DDS_IF__'].get()),
            'channelAmplitudes': [str(app[f'__DDS_CHA_AMP__{i}'].get()) for i in range(4)]
        }
        # print(measurement_settings)
        self.measurement_settings_location = Path.joinpath(self.base,
                                                           Path('measurement settings.json'))
        with open(self.measurement_settings_location, 'w') as f:
            json.dump(measurement_settings, f)
