import time
from pathlib import Path
import threading
import numpy as np


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


class Measurement:
    def __init__(self, laser_on_time, save_location=None, app=None):
        self.save_location = save_location
        self.amplitude_save_location = None
        self.phase_save_location = None

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
        self.demodulator_count_generator.send('restart')
        self.reset_arrays()

    def pause(self):
        self.paused = True
        self.started = False

    def unpause(self):
        self.paused = False
        self.started = True

    def create_measurement_files(self):
        base = self.save_location
        base.mkdir(parents=True, exist_ok=True)

        Path.joinpath(base, Path('amplitude.csv')).touch()
        Path.joinpath(base, Path('phase.csv')).touch()

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
