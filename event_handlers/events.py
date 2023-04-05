import PySimpleGUI as Sg
import RPi.GPIO as GPIO

from event_handlers.adc_events import adc_events
from event_handlers.dds_events import dds_events
from event_handlers.demodulator_events import dem_events
from event_handlers.laser_events import laser_events
from event_handlers.measurement_events import meas_events
from event_handlers.calib_events import calibration_events


def event_handler(app, event, values):
    if event == Sg.WIN_CLOSED:
        GPIO.cleanup()
        return -1
    else:
        event_group = event.split('__')[1].split('_')[0]
        # print(values)
        try:
            value = values[event]
        except KeyError:
            value = None
        # print(f'Event Group: {event_group}.')
        # print(f'Event : {event}.')
        # print(f'Event Value: {value}.')

        if event_group == 'DDS':
            dds_events(app, event, values)

        elif event_group == 'ADC':
            adc_events(app, event, values)

        elif event_group == 'DEM':
            dem_events(app, event, values)

        elif event_group == 'MEAS':
            meas_events(app, event, values)

        elif event_group == 'LAS' or event_group == 'LASER':
            laser_events(app, event, values)
            
        elif event_group == "CAL":
            calibration_events(app, event, values)
            print("CAL Event")
            
        else:
            print(f"Event group {event_group} is not recognized.")
