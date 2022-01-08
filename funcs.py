import RPi.GPIO as GPIO
import json
import datetime
import time
import AD9959_v2
import ADS8685


with open('settings.json', 'r') as f:
    settings = json.load(f)
    DDS_SETTINGS = settings['DDS_SETTINGS']
    MEA_SETTINGS = settings['MEA_SETTINGS']
    LAS_SETTINGS = settings['LAS_SETTINGS']


DDS_PINS = {
    'P_DWN': 22,
    'IO_UP': 29,
    'RESET': 13
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


        # vars['DDS_SETTINGS'] = dds_settings_def
    else:
        print('Is not instance.')


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