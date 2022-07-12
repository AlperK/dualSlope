import PySimpleGUI as Sg
import RPi.GPIO as GPIO
import json
from pathlib import Path
import numpy as np


with open('default dds settings.json') as f:
    DEF_DDS_SETTINGS = json.load(f)
with open('default adc settings.json') as f:
    DEF_ADC_SETTINGS = json.load(f)


def dds_events(app, event, values):
    """
    Handles the events related to the DDS
    :param app: The MainWindow
    :param event: The event
    :param values: The values dictionary
    :return:
    """
    if event == '__DDS_P_DWN__':
        if values[event]:
            app.dds.shutdown()
            app['__LOG__'].update(f"DDS shutdown.\n", append=True)
        else:
            app.dds.wake_up()
            app['__LOG__'].update(f"DDS wakeup.\n", append=True)

    elif event == '__DDS_RST__':
        app.dds.reset()
        app.dds.load_settings(settings=DEF_DDS_SETTINGS)

        app['__DDS_RF__'].update(value=values['__DDS_RF__'])
        app['__DDS_IF__'].update(value=values['__DDS_IF__'])
        app['__DDS_PLL_MUL__'].update(values=['__DDS_PLL_MUL__'])
        app['__LOG__'].update(f"DDS reset.\n", append=True)

    elif event == '__DDS_PLL_MUL__':
        app.dds.set_freqmult(int(values[event]), ioupdate=True)
        app['__LOG__'].update(f'DDS PLL set to {values[event]}.\n', append=True)

    elif event in [f'__DDS_CHA_AMP__{channel}' for channel in range(4)]:
        channel = int(event[-1])
        value = values[f'__DDS_CHA_AMP__{channel}']
        app.dds.set_output(channels=channel, value=float(value), var='amplitude', io_update=True)

        app['__LOG__'].update(f'Channel {channel} amplitude set to {values[event]}.\n', append=True)

    elif event in [f'__DDS_CHA_PHA__{channel}' for channel in range(4)]:
        channel = int(event[-1])
        value = values[event]
        # print(value)
        app.dds.set_output(channels=channel, value=float(value), var='phase', io_update=True)

        app['__LOG__'].update(f'Channel {channel} phase set to {values[event]}.\n', append=True)

    elif event in [f'__DDS_CHA_EN__{channel}' for channel in range(4)]:
        channel = int(event[-1])

        if values[event]:
            app.dds.enable_channel(channel)
            app['__LOG__'].update(f'Channel {channel} enabled.\n', append=True)
        else:
            app.dds.disable_channel(channel)
            app['__LOG__'].update(f'Channel {channel} disabled.\n', append=True)

    elif event in [f'__DDS_CHA_DIV__{channel}' for channel in range(4)]:
        channel = int(event[-1])
        app.dds.set_current(channels=channel, divider=int(values[event]), ioupdate=True)

        app['__LOG__'].update(f'Channel {channel} divider set.\n', append=True)

    elif event in ['__DDS_RF__', '__DDS_IF__']:
        new_rf = values['__DDS_RF__']
        new_if = values['__DDS_IF__']

        if not new_rf.isnumeric():
            app['__LOG__'].update(f'Invalid RF.\n', append=True)
            app['__DDS_RF__'].update(background_color='orange')

            if not new_if.isnumeric():
                app['__LOG__'].update(f'Invalid IF.\n', append=True)
                app['__DDS_IF__'].update(background_color='orange')
                return
            else:
                app['__DDS_IF__'].update(background_color=Sg.theme_input_background_color())

            return
        else:
            app['__DDS_RF__'].update(background_color=Sg.theme_input_background_color())
        if not float(new_rf) <= 120:
            app['__LOG__'].update(f'Invalid RF.\n', append=True)
            app['__DDS_RF__'].update(background_color='orange')
            return
        else:
            app['__DDS_RF__'].update(background_color=Sg.theme_input_background_color())

        app.dds.set_rf_if(r_f=float(values['__DDS_RF__']),
                          i_f=float(values['__DDS_IF__']),
                          rf_channels=[0, 1],
                          lo_channels=[2, 3])
        app['__LOG__'].update('New RF and IF frequencies are set.\n', append=True)

    else:
        print(f'Event \'{event}\' unrecognized.')


def adc_events(app, event, values):
    """
    Handles the events related to the ADCs
    :param app: The MainWindow
    :param event: The event
    :param values: The values dictionary
    :return:
    """
    if event in [f'__ADC_RANGE__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        new_range = DEF_ADC_SETTINGS['rangeList'].index(values[event])
        if new_range >= 5:
            new_range += 3
        old_range = getattr(getattr(app, f'demodulator{channel}'), 'adc').get_range()
        getattr(getattr(app, f'demodulator{channel}'), 'adc').set_range(new_range)

        app['__LOG__'].update(f"Set ADC-{channel} range to {values[event]}.\n", append=True)
        app['__LOG__'].update(f"ADC-{channel} old range was {old_range}.\n", append=True)

    elif event in [f'__ADC_RST__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        getattr(getattr(app, f'demodulator{channel}'), 'adc').reset()

        app[f'__ADC_RANGE__{channel}'].update(DEF_ADC_SETTINGS['rangeList'][0])
        app['__LOG__'].update(f'ADC-{channel} is reset.\n', append=True)

    elif event in [f'__ADC_GET_RANGE__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        app['__LOG__'].update(f"ADC-{channel} range is {getattr(app, f'demodulator{channel}').adc.get_range()}.\n",
                              append=True)


def dem_events(app, event, values):
    """
    Handles the events related to the Demodulators
    :param app: The MainWindow
    :param event: The event
    :param values: The values dictionary
    :return:
    """
    if event in [f'__DEM_SET_AMP__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        getattr(app, f'demodulator{channel}').set2amp()
        app['__LOG__'].update(f'Demodulator-{channel} set to amplitude mode.\n',
                              append=True)

    elif event in [f'__DEM_SET_PHA__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        getattr(app, f'demodulator{channel}').set2pha()
        app['__LOG__'].update(f'Demodulator-{channel} set to phase mode.\n',
                              append=True)

    elif event in [f'__DEM_MEA__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        if values[f'__DEM_SET_AMP__{channel}']:
            result = getattr(app, f'demodulator{channel}').measure_amplitude(raw=values[f'__DEM_RAW__{channel}'])
            app['__LOG__'].update(f'Demodulator-{channel} measurement result: {result}.\n', append=True)
        elif values[f'__DEM_SET_PHA__{channel}']:
            result = getattr(app, f'demodulator{channel}').measure_phase(raw=values[f'__DEM_RAW__{channel}'])
            app['__LOG__'].update(f'Demodulator-{channel} measurement result: {result}.\n', append=True)


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
        app.measurement.save_location = Path.joinpath(Path(values['__MEAS_LOC__']),
                                                      Path(values['__MEAS_GRP__']),
                                                      Path(values['__MEAS_NUM__']))
        # measurement.save_loc = app.save_location
        app.measurement.amplitude_save_location = Path.joinpath(app.measurement.save_location, 'amplitude.csv')
        app.measurement.phase_save_location = Path.joinpath(app.measurement.save_location, 'phase.csv')

        print(app.measurement.save_location)

    elif event == '__MEAS_CRT__':
        app['__LOG__'].update(f"Save file location: {app.save_location}\n",
                              append=True)

        app.measurement.create_measurement_files()

    elif event == '__MEAS_START__':
        _amplitudes = np.array([])
        _phases = np.array([])
        app.measurement.start()
        app.measurement.start_measurement_on_a_thread()

    elif event == '__MEAS_LONG_DONE__':
        app['__LOG__'].update('Long operation done.\n', append=True)

    elif event == '__MEAS_STOP__':
        app.measurement.stop()
        app.measurement.started = False

        for rectangle, circle in zip(app.window_rectangles, app.window_circles):
            app.graph.TKCanvas.itemconfig(rectangle, fill='grey')
            app.graph.TKCanvas.itemconfig(circle, fill='grey')
        app['__LOG__'].update('Long operation stopped.\n', append=True)

    elif event == '__MEAS_PROGRESS__':
        laser_count = int(values[event][0]) % 2
        laser = getattr(app, f"laser{values[event][0]+1}")

        demodulator_count = int(values[event][1])
        demodulator = getattr(app, f"demodulator{values[event][1]+1}")
        for window_rectangle, window_circle, window_text in zip(app.window_rectangles, app.window_circles, app.window_texts):
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

        # app['__LOG__'].update(f'Amplitudes: {app.measurement.amplitudes}\n', append=True)
        # app['__LOG__'].update(f'Phases: {app.measurement.phases}\n', append=True)

        if app.measurement.amplitudes.size >= 8:
            app.measurement.save_arrays()
            app.measurement.reset_arrays()


def laser_events(app, event, values):
    """
    Handles the events related to the Lasers
    :param app: The MainWindow
    :param event: The event
    :param values: The values dictionary
    :return:
    """
    # Turn on/off the selected Laser
    if event in [f'__LAS__{i}' for i in range(1, 5)]:
        channel = event[-1]
        if values[event]:
            getattr(app, f'laser{channel}').turn_on()
            app['__LOG__'].update(f"Laser-{channel} is turned on.\n", append=True)
        else:
            getattr(app, f'laser{channel}').turn_off()
            app['__LOG__'].update(f"Laser-{channel} is turned off.\n", append=True)

    elif event == '__LASER_ON_TIME__':
        app.measurement.laser_on_time = float(values[event]) / 1000
        app['__LOG__'].update(f'laser on time {float(values[event])}\n', append=True)


def event_handler(app, event, values):
    if event == Sg.WIN_CLOSED:
        GPIO.cleanup()
        return -1
    else:
        event_group = event.split('__')[1].split('_')[0]
        print(values)
        try:
            value = values[event]
        except KeyError:
            value = None
        print(f'Event Group: {event_group}')
        print(f'Event : {event}')
        print(f'Event Value: {value}')

        if event_group == 'DDS':
            dds_events(app, event, values)

        elif event_group == 'ADC':
            adc_events(app, event, values)

        elif event_group == 'DEM':
            dem_events(app, event, values)

        elif event_group == 'MEAS':
            meas_events(app, event, values)

        elif event_group == 'LAS' or 'LASER':
            laser_events(app, event, values)
