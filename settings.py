import json
import pathlib

app_settings = {
    'theme': 'DarkGrey14',
    'width': 1200,
    'height': 800,
    'title': 'Dual Slope'
}

dds_settings = {
    'RF': 100,
    'IF': 1,
    'refClk': 25e6,
    'PLL_MUL': 20,
    'channelFrequencies': [100.001e6, 100.001e6, 100e6, 100e6],
    'channelAmplitudes': [0.15, 0.1, 0.5, 0.5],
    'channelPhases': [0, 0, 0, 180],
    'channelDividers': [4, 4, 1, 1],

}

adc_settings = {
    'range': [u'\u00B1 12.288 V', u'\u00B1 10.24 V', u'\u00B1 6.144 V', u'\u00B1 5.12 V', u'\u00B1 2.56 V',
              '0-12.288 V', '0-10.24 V', '0-6.144 V', '0-5.12 V'],
}

mea_settings = {
    'canvasSize': (200, 100),
    'measurementFileName': '',
    'laserOnTime': 500,
    'measurementStarted': False,
    'justStarted': False,
    'activeLaser': None,
    'activeDemod': None,
}

las_settings = {
    'laserPins': [10, 13, 15, 16],
}

pin_settings = {
    'adc_rst_1': 22,
    'amp_pha_1': 29,
    'adc_rst_2': 18,
    'amp_pha_2': 31,
}

settings = {
    'APP_SETTINGS': app_settings,
    'DDS_SETTINGS': dds_settings,
    'ADC_SETTINGS': adc_settings,
    'MEA_SETTINGS': mea_settings,
    'LAS_SETTINGS': las_settings,
    'PIN_SETTINGS': pin_settings,
}
with open('settings.json', 'w') as f:
    json.dump(settings, f)

with open('defaults.json', 'w') as f:
    json.dump(settings, f)


# with open('settings.json', 'r') as f:
#     settings = json.load(f)
#     APP_SETTINGS = settings['APP_SETTINGS']
#     DDS_SETTINGS = settings['DDS_SETTINGS']
# print(APP_SETTINGS)
# print(DDS_SETTINGS)

