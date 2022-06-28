import json

app_settings = {
    'theme': 'DarkGrey14',
    'width': 1200,
    'height': 800,
    'title': 'Dual Slope'
}

default_dds_settings = {
    'RF': 100,
    'IF': 1,
    'refClk': 25e6,
    'PLL_MUL': 20,
    'activeChannels': [True, False, False, True],
    'channelFrequencies': [100.001e6, 100.001e6, 100e6, 100e6],
    'channelAmplitudes': [0.15, 0.1, 0.5, 0.5],
    'channelPhases': [0, 0, 0, 180],
    'channelDividers': [4, 4, 1, 1],
    'pins': {
        'IO_UP': 36,
        'RESET': 37,
        'P_DOWN': 33,
    }
}

default_adc_settings = {
    'rangeList': [u'\u00B1 12.288 V', u'\u00B1 10.24 V', u'\u00B1 6.144 V', u'\u00B1 5.12 V', u'\u00B1 2.56 V',
                  '0-12.288 V', '0-10.24 V', '0-6.144 V', '0-5.12 V'],
    'RST_PIN': [22, 18]
}

default_dem_settings = {
    'laserOnTime': 100e-3,
    'Demodulator-1': {
        'PHA_AMP_PIN': 29,
        'amplitudeCoefficients': {'slope': 0.3009,
                                  'intercept': 2.488},
        'phaseCoefficients': {'A': 300.466,
                              'freq': 0.00277773,
                              'phi': 0,
                              'offset': -0.912},
    },
    'Demodulator-2': {
        'PHA_AMP_PIN': 31,
        'amplitudeCoefficients': {'slope': 0.3009,
                                  'intercept': 2.488},
        'phaseCoefficients': {'A': 300.466,
                              'freq': 0.00277773,
                              'phi': 0,
                              'offset': -0.912},
    }
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
    'DDS_SETTINGS': default_dds_settings,
    'ADC_SETTINGS': default_adc_settings,
    'MEA_SETTINGS': mea_settings,
    'LAS_SETTINGS': las_settings,
    'PIN_SETTINGS': pin_settings,
}
with open('settings.json', 'w') as f:
    json.dump(settings, f)

with open('defaults.json', 'w') as f:
    json.dump(settings, f)

with open('app settings.json', 'w') as f:
    json.dump(app_settings, f)

with open('default dds settings.json', 'w') as f:
    json.dump(default_dds_settings, f)
with open('default adc settings.json', 'w') as f:
    json.dump(default_adc_settings, f)
with open('default dem settings.json', 'w') as f:
    json.dump(default_dem_settings, f)
# with open('settings.json', 'r') as f:
#     settings = json.load(f)
#     APP_SETTINGS = settings['APP_SETTINGS']
#     DDS_SETTINGS = settings['DDS_SETTINGS']
# print(APP_SETTINGS)
# print(DDS_SETTINGS)
