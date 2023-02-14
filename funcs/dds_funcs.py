from RPi import GPIO as GPIO
from hardware import AD9959_v2
from pathlib import Path
import json

with open(Path.joinpath(Path().resolve(), 'settings', 'settings.json'), 'r') as f:
    settings = json.load(f)
    DDS_SETTINGS = settings['DDS_SETTINGS']

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
