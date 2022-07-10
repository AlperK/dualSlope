import time
from pathlib import Path
import threading


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
        self.started = False
        self.paused = False
        self.laser_on_time = laser_on_time

        self.laser_count_generator = laser_count_generator()
        self.laser_count = next(self.laser_count_generator)
        self.demodulator_count_generator = demodulator_count_generator()
        self.demodulator_count = next(self.demodulator_count_generator)

        self.app = app
        # self.graph = app.graph
        # self.graph_elements = app.elements

    def start(self):
        self.started = True
        self.paused = False

    def stop(self):
        self.started = False
        self.paused = False
        self.laser_count_generator.send('restart')
        self.demodulator_count_generator.send('restart')

    def pause(self):
        self.paused = True
        self.started = False

    def unpause(self):
        self.paused = False
        self.started = True

    def create_measurement_files(self):
        base = self.save_location
        base.mkdir(parents=True, exist_ok=True)

        Path.joinpath(base, Path('amplitudes.csv')).touch()
        Path.joinpath(base, Path('phases.csv')).touch()

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
