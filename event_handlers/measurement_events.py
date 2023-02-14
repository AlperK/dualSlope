import random
from pathlib import Path

import PySimpleGUI as Sg
import numpy as np

import Measurement


def meas_events(app, event, values):
    """
    Handles the events related to the Measurement
    :param app: The MainWindow
    :param event: The event
    :param values: The values dictionary
    :return:
    """
    # Creates and updates the save file location

    if event in ['__MEAS_LOC__', '__MEAS_GRP__', '__MEAS_NUM__']:
        app.save_location = Path.joinpath(Path(values['__MEAS_LOC__']),
                                                      Path(values['__MEAS_GRP__']),
                                                      Path(values['__MEAS_NUM__']))
        # measurement.save_loc = app.save_location
        app.amplitude_save_location = Path.joinpath(app.save_location, 'amplitude.csv')
        app.phase_save_location = Path.joinpath(app.save_location, 'phase.csv')

        print(app.save_location)

    elif event == '__MEAS_CRT__':
        app['__LOG__'].update(f"Save file location: {app.save_location}\n",
                              append=True)

        app.measurement.create_measurement_files(app.save_location)

    elif event == '__MEAS_START__':
        app.measurement = Measurement.Measurement(laser_on_time=app.laser_on_time,
                                                  save_location=app.save_location,
                                                  app=app)
        app.measurement.create_measurement_files(app_save_location=app.save_location)
        app.measurement.save_measurement_settings(app)
        _amplitudes = np.array([])
        _phases = np.array([])
        app.measurement.start()
        app.measurement.start_measurement_on_a_thread()

    elif event == '__MEAS_LONG_DONE__':
        app['__LOG__'].update('Long operation done.\n', append=True)

    elif event == '__MEAS_STOP__':
        app.measurement.stop()
        app.measurement.started = False
        app.measurement.amplitudes = np.array([])
        app.measurement.phases = np.array([])

        for rectangle, circle in zip(app.window_rectangles, app.window_circles):
            app.graph.TKCanvas.itemconfig(rectangle, fill='grey')
            app.graph.TKCanvas.itemconfig(circle, fill='grey')
        for channel in range(1, 5):
            getattr(app, f'laser{channel}').turn_off()
        app['__LOG__'].update('Long operation stopped.\n', append=True)

    elif event == '__MEAS_PROGRESS__':

        laser_count = int(values[event][0]) % 2
        laser = getattr(app, f"laser{values[event][0]+1}")

        demodulator_count = int(values[event][1])
        demodulator = getattr(app, f"demodulator{values[event][1]+1}")
        for window_rectangle, window_circle, window_text in \
                zip(app.window_rectangles, app.window_circles, app.window_texts):
            app.graph.TKCanvas.itemconfig(window_rectangle, fill='grey')
            app.graph.TKCanvas.itemconfig(window_circle, fill='grey')

        app.graph.TKCanvas.itemconfig(app.window_rectangles[laser_count], fill='red')
        app.graph.TKCanvas.itemconfig(app.window_circles[demodulator_count], fill='white')

        for i in range(1, 5):
            getattr(app, f"laser{i}").turn_off()

        laser.turn_on()
        amplitude = demodulator.measure_amplitude()
        app.measurement.amplitudes = np.append(app.measurement.amplitudes, amplitude)
        app.measurement.phases = np.append(app.measurement.phases, demodulator.measure_phase())

        # app.plot.plot(x=values[event][0] + 1, y=values[event][1])
        if app.measurement.amplitudes.size >= 8:
            a, s = app.measurement._get_optical_parameters(frequency=1e6*float(app['__DDS_RF__'].get()) +
                                                                     1e3*float(app['__DDS_IF__'].get()),
                                                           wavelength=690)
            if random.uniform(0, 1) > 0:
                app['__LOG__'].update(f'Absorption: {np.round(a, 4)}, ', append=True)
                app['__LOG__'].update(f'Error: {np.round((a[1] - 0.0081) / 0.0081 * 100, 2)}\n', append=True)
                app['__LOG__'].update(f'Scattering: {np.round(s, 4)}, ', append=True)
                app['__LOG__'].update(f'Error: {np.round((s[1] - 0.761) / 0.761 * 100, 2)}\n', append=True)
                app['__LOG__'].update(f'\n', append=True)
                # print_counter = 0
            app.measurement.save_arrays()
            app.measurement.reset_arrays()
            # print_counter += 1

    elif event in ['__MEAS_r__1', '__MEAS_r__2']:
        for i in range(1, 3):
            try:
                value = float(values[f'__MEAS_r__{i}'])
                if not value > 0:
                    app['__LOG__'].update(f'Invalid input for r{i}.\n', append=True)
                    app[event].update(background_color='orange')
                else:
                    setattr(app.measurement, f'r{i}', value)
                    app['__LOG__'].update(f"r{i} set to {getattr(app.measurement, f'r{i}')}mm.\n", append=True)
                    app[f'__MEAS_r__{i}'].update(background_color=Sg.theme_input_background_color())
            except ValueError:
                app['__LOG__'].update(f'Invalid input for r{i}.\n', append=True)
                app[f'__MEAS_r__{i}'].update(background_color='orange')
