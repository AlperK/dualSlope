import csv
import datetime
import json
import time
from pathlib import Path as Path

from RPi import GPIO as GPIO

from funcs.dds_funcs import set_rf_if
from hardware import AD9959_v2, ADS8685

with open(Path.joinpath(Path().resolve(), 'settings', 'settings.json'), 'r') as f:
    settings = json.load(f)
    DDS_SETTINGS = settings['DDS_SETTINGS']
    MEA_SETTINGS = settings['MEA_SETTINGS']
    LAS_SETTINGS = settings['LAS_SETTINGS']


def load_defaults(device, var_dict, window):
    # Load defaults.json
    with open('defaults.json', 'r') as f:
        default_settings = json.load(f)
        app_settings_def = default_settings['APP_SETTINGS']
        dds_settings_def = default_settings['DDS_SETTINGS']
        adc_settings_def = default_settings['ADC_SETTINGS']
        mea_settings_def = default_settings['MEA_SETTINGS']

    # Load DDS defaults and update the UI
    if isinstance(device, AD9959_v2.AD9959):
        for key, value in dds_settings_def.items():
            var_dict['DDS_SETTINGS'][key] = value

        device.set_refclock(dds_settings_def['refClk'])
        device.set_freqmult(dds_settings_def['PLL_MUL'], ioupdate=True)
        set_rf_if(r_f=dds_settings_def['RF'], i_f=dds_settings_def['IF'], dds=device)

        for ch in range(4):
            device.set_output(ch, value=dds_settings_def['channelAmplitudes'][ch], var='amplitude')
            device.set_output(ch, value=dds_settings_def['channelPhases'][ch], var='phase')
            device.set_current(ch, dds_settings_def['channelDividers'][ch], ioupdate=True)

        for ch in range(4):
            window['CH_{}_AMP'.format(ch)].Update(value=dds_settings_def['channelAmplitudes'][ch])
            window['CH_{}_PHA'.format(ch)].Update(value=dds_settings_def['channelPhases'][ch])
            window['CH_{}_DIV'.format(ch)].Update(value=dds_settings_def['channelDividers'][ch])

        window['RF'].update(value=dds_settings_def['RF'])
        window['IF'].update(value=dds_settings_def['IF'])
        window['PLL_MUL'].update(value=dds_settings_def['PLL_MUL'])

    else:
        print('Is not instance.')


def load_dds_settings(device, var_dict, window):
    # for key, value in dds_settings_def.items():
    #     var_dict['DDS_SETTINGS'][key] = value

    device.set_refclock(var_dict['DDS_SETTINGS']['refClk'])
    device.set_freqmult(var_dict['DDS_SETTINGS']['PLL_MUL'], ioupdate=True)
    set_rf_if(r_f=var_dict['DDS_SETTINGS']['RF'], i_f=var_dict['DDS_SETTINGS']['IF'], dds=device)

    for ch in range(4):
        device.set_output(ch, value=var_dict['DDS_SETTINGS']['channelAmplitudes'][ch], var='amplitude')
        device.set_output(ch, value=var_dict['DDS_SETTINGS']['channelPhases'][ch], var='phase')
        device.set_current(ch, var_dict['DDS_SETTINGS']['channelDividers'][ch], ioupdate=True)

    for ch in range(4):
        window['CH_{}_AMP'.format(ch)].Update(value=var_dict['DDS_SETTINGS']['channelAmplitudes'][ch])
        window['CH_{}_PHA'.format(ch)].Update(value=var_dict['DDS_SETTINGS']['channelPhases'][ch])
        window['CH_{}_DIV'.format(ch)].Update(value=var_dict['DDS_SETTINGS']['channelDividers'][ch])

    window['RF'].update(value=var_dict['DDS_SETTINGS']['RF'])
    window['IF'].update(value=var_dict['DDS_SETTINGS']['IF'])
    window['PLL_MUL'].update(value=var_dict['DDS_SETTINGS']['PLL_MUL'])


def update_event_log(message, var_dict, window):
    t = datetime.datetime.now().strftime('%H:%M:%S')
    if 'eventLog' not in var_dict:
        var_dict.update({'eventLog': []})
    if 'window' not in var_dict:
        var_dict.update({'window': window})
    var_dict['eventLog'].append('{}: '.format(t) + message)
    var_dict['window']['EVE_LOG'].Update('\n'.join(var_dict['eventLog']), autoscroll=True)


def set_adc2amp(pin):
    GPIO.output(pin, True)


def set_adc2pha(pin):
    GPIO.output(pin, False)


def get_amp_pha_measurement_from_adc(adc: ADS8685.ADS8685, amp_pha_pin):
    set_adc2amp(amp_pha_pin)
    time.sleep(MEA_SETTINGS['laserOneTime']/2)
    measured_amplitude_voltage = adc.convert()

    set_adc2pha(amp_pha_pin)
    time.sleep(MEA_SETTINGS['laserOneTime']/2)
    measured_phase_voltage = adc.convert()

    return measured_amplitude_voltage, measured_phase_voltage


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


def create_base_files(var_dict):
    loc = Path(var_dict['MEA_SETTINGS']['measurementFileName'])

    measurement_conditions = {}
    measurement_conditions.update(var_dict['DDS_SETTINGS'])
    measurement_conditions.update(var_dict['ADC_SETTINGS'])
    measurement_conditions.update(var_dict['MEA_SETTINGS'])

    save_measurement_settings(loc, measurement_conditions)
    amplitude_file, phase_file = initialize_csv_files(loc)
    return str(amplitude_file), str(phase_file)


def save_measurement_settings(loc, measurement_conditions):

    Path(loc).mkdir(parents=True, exist_ok=True)
    json_file = Path.joinpath(loc, Path('measurement conditions.json'))

    with json_file.open(mode='w+') as file:
        json.dump(measurement_conditions, file)


def initialize_csv_files(loc):
    header = []
    for laser in range(4):
        for apd in range(2):
            seq = ('L' + str(laser + 1), 'APD' + str(apd + 1))
            header.append('-'.join(seq))

    phase_file = Path.joinpath(loc, Path('phase.csv'))
    with open(phase_file, 'w+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows([header])

    amplitude_file = Path.joinpath(loc, Path('amplitude.csv'))
    with open(amplitude_file, 'w+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows([header])

    return amplitude_file, phase_file


def is_end_of_measurement_set(var_dict):
    return len(var_dict['amplitudes']) == 8 and len(var_dict['phases']) == 8


def save_measurement_set(var_dict):
    with open(Path(var_dict['MEA_SETTINGS']['amplitudeMeasurementFile']), 'a+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows([var_dict['amplitudes']])

    with open(Path(var_dict['MEA_SETTINGS']['phaseMeasurementFile']), 'a+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows([var_dict['phases']])


def rmtree(root):

    for p in root.iterdir():
        if p.is_dir():
            rmtree(p)
        else:
            p.unlink()

    root.rmdir()
