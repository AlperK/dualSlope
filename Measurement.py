import time
from pathlib import Path


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
    def __init__(self, laser_on_time, save_location=None):
        self.save_location = save_location
        self.started = False
        self.paused = False
        self.laser_on_time = laser_on_time

    def start(self):
        self.started = True

    def stop(self):
        self.started = False

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def create_measurement_files(self):
        base = self.save_location
        base.mkdir(parents=True, exist_ok=True)

        Path.joinpath(base, Path('amplitudes.csv')).touch()
        Path.joinpath(base, Path('phases.csv')).touch()

    def dummy_long_operation(self, t):
        time.sleep(t)
        return f't'
