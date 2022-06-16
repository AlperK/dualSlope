import RPi.GPIO as GPIO
import json
import datetime
import time
from pathlib import Path as Path
import shutil
import csv
import pyvisa
import AD9959_v2
import ADS8685


with open('settings.json', 'r') as f:
    settings = json.load(f)
    DDS_SETTINGS = settings['DDS_SETTINGS']
    MEA_SETTINGS = settings['MEA_SETTINGS']
    LAS_SETTINGS = settings['LAS_SETTINGS']


DDS_PINS = {
    'P_DWN': 33,
    'IO_UP': 36,
    'RESET': 37
}


def configure_dds(bus, device, pins):
    # Set DDS pins as outputs
    for pin in pins:
        GPIO.setup(pins[pin], GPIO.OUT)
        GPIO.output(pins[pin], False)

    dds = AD9959_v2.AD9959(bus=bus, device=device,
                           IO_UPDATE_PIN=pins['IO_UP'],
                           RST_PIN=pins['RESET'],
                           PWR_DWN_PIN=pins['P_DWN'],
                           ref_clk=25e6)

    dds.init_dds(channels=[0, 1])
    dds.set_freqmult(DDS_SETTINGS['PLL_MUL'], ioupdate=True)
    dds.set_refclock(25e6)
    dds.set_current([0, 1], 1)

    return dds


def initialize_dds(bus, device, pins=None):
    # Check if other pins were passed in
    if pins is None:
        pins = DDS_PINS

    # Set DDS pins as GPIO outputs
    for pin in pins:
        GPIO.setup(pins[pin], GPIO.OUT)
        GPIO.output(pins[pin], False)

    dds = AD9959_v2.AD9959(bus=bus, device=device,
                           IO_UPDATE_PIN=pins['IO_UP'],
                           RST_PIN=pins['RESET'],
                           PWR_DWN_PIN=pins['P_DWN'],
                           ref_clk=25e6)

    dds.init_dds(channels=[0, 1, 2, 3])
    dds.set_freqmult(DDS_SETTINGS['PLL_MUL'], ioupdate=True)
    dds.set_refclock(25e6)
    for i in range(4):
        dds.set_output(channels=i, value=DDS_SETTINGS['channelFrequencies'][i], var='frequency', io_update=True)
        dds.set_output(channels=i, value=DDS_SETTINGS['channelAmplitudes'][i], var='amplitude', io_update=True)
        dds.set_output(channels=i, value=DDS_SETTINGS['channelPhases'][i], var='phase', io_update=True)
        dds.set_current(channels=i, divider=DDS_SETTINGS['channelDividers'][i])

    return dds


def set_rf_if(r_f, i_f, dds):
    r_f = float(r_f) * 1000000
    i_f = float(i_f) * 1000

    dds.set_output([0, 1], value=r_f + i_f, var='frequency', io_update=True)
    dds.set_output([2, 3], value=r_f, var='frequency', io_update=True)


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


def initialize_lasers():
    for pin in LAS_SETTINGS['laserPins']:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)


def turn_on_laser(laser):
    for las in LAS_SETTINGS['laserPins']:
        GPIO.output(las, False)

    GPIO.output(LAS_SETTINGS['laserPins'][laser], True)


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


def start_phase_calibration(demodulator, val_dict):
    start_freq = int(val_dict['PHA_CALIB_START_PHA'])
    stop_freq = int(val_dict['PHA_CALIB_STOP_PHA'])
    step_freq = int(val_dict['PHA_CALIB_STEP_PHA'])

    start_amp = int(val_dict['PHA_CALIB_START_AMP'])
    stop_amp = int(val_dict['PHA_CALIB_STOP_AMP'])
    step_amp = int(val_dict['PHA_CALIB_STEP_AMP'])

    rm = pyvisa.ResourceManager('@py')
    try:
        sigGen = rm.open_resource('USB0::6833::1601::DG4C141400166::0::INSTR')
    except:
        update_event_log('Could not find RIGOL DG4162', val_dict)
        return

    sigGen.write('SOUR1:APPL:SIN 1e3, 1, 0, 0')
    sigGen.write('SOUR2:APPL:SIN 1e3, 1, 0, 0')

    sigGen.write('OUTP1 ON')
    sigGen.write('OUTP2 ON')
    sigGen.write('SOUR1:PHAS:INIT')

    loc = Path.joinpath(Path(val_dict['MEAS_DATE'], Path('PhaseCalibration')))
    if loc.is_dir():
        rmtree(loc)

        loc.mkdir(parents=True, exist_ok=True)
        loc.chmod(511)

        loc.parent.chmod(511)
    else:
        loc.mkdir(parents=True, exist_ok=True)
        loc.chmod(511)
        loc.parent.chmod(511)

    for freq in range(start_freq, stop_freq + step_freq, step_freq):
        for amplitude1 in range(start_amp, stop_amp + step_amp, step_amp):
            root = 'SOUR1:APPL:SIN '
            t = ', '.join([str(freq*1e3), str(amplitude1*1e-3), '0', '0'])
            cmd = ''.join([root, t])
            sigGen.write(cmd)
            for amplitude2 in range(start_amp, stop_amp + step_amp, step_amp):
                # print(Path(''.join([str(amplitude2), 'mV'])))
                file = Path.joinpath(loc,
                                     Path(''.join([str(freq), 'kHz_',
                                                   str(amplitude1), 'mV_',
                                                   str(amplitude2), 'mV_',
                                                   'phase.csv'])))
                file.touch(mode=511)
                # loc.chmod(511)
                for phase in range(0, 181):
                    root = 'SOUR2:APPL:SIN '
                    t = ', '.join([str(freq*1e3), str(amplitude2*1e-3), '0', str(phase)])
                    cmd = ''.join([root, t])

                    sigGen.write(cmd)
                    sigGen.write('SOUR1:PHAS:INIT')

                    # print(phase, demodulator.measure_phase())
                    # time.sleep(0.1)
                    with open(file, 'a+') as csv_file:
                        writer = csv.writer(csv_file, delimiter=',')
                        writer.writerow([phase, demodulator.measure_phase_voltage()])


def start_amplitude_calibration(demodulator, val_dict):
    start_freq = int(val_dict['AMP_CALIB_START_PHA'])
    stop_freq = int(val_dict['AMP_CALIB_STOP_PHA'])
    step_freq = int(val_dict['AMP_CALIB_STEP_PHA'])

    start_amp = int(val_dict['AMP_CALIB_START_AMP'])
    stop_amp = int(val_dict['AMP_CALIB_STOP_AMP'])
    step_amp = int(val_dict['AMP_CALIB_STEP_AMP'])

    rm = pyvisa.ResourceManager('@py')
    try:
        sigGen = rm.open_resource('USB0::6833::1601::DG4C141400166::0::INSTR')
    except:
        update_event_log('Could not find RIGOL DG4162', val_dict)
        return

    sigGen.write('SOUR1:APPL:SIN 1e3, 1, 0, 0')
    sigGen.write('SOUR2:APPL:SIN 1e3, 1, 0, 0')

    sigGen.write('OUTP1 ON')
    sigGen.write('OUTP2 ON')
    sigGen.write('SOUR1:PHAS:INIT')

    loc = Path.joinpath(Path(val_dict['MEAS_DATE'], Path('AmplitudeCalibration')))
    if loc.is_dir():
        rmtree(loc)

        loc.mkdir(parents=True, exist_ok=True)
        loc.chmod(511)

        loc.parent.chmod(511)
    else:
        loc.mkdir(parents=True, exist_ok=True)
        loc.chmod(511)
        loc.parent.chmod(511)

    for freq in range(start_freq, stop_freq + step_freq, step_freq):
        file = Path.joinpath(loc,
                             Path(''.join([str(freq), 'kHz_',
                                           'amplitude.csv'])))
        file.touch(mode=511)
        for amplitude1 in range(start_amp, stop_amp + step_amp, step_amp):
            root = 'SOUR1:APPL:SIN '
            t = ', '.join([str(freq*1e3), str(amplitude1*1e-3), '0', '0'])
            cmd = ''.join([root, t])
            sigGen.write(cmd)

            root = 'SOUR2:APPL:SIN '
            t = ', '.join([str(freq*1e3), str(amplitude1*1e-3), '0', '0'])
            cmd = ''.join([root, t])
            sigGen.write(cmd)

            with open(file, 'a+') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow([amplitude1, demodulator.measure_amplitude_voltage()])


def rmtree(root):

    for p in root.iterdir():
        if p.is_dir():
            rmtree(p)
        else:
            p.unlink()

    root.rmdir()
