import json
from pathlib import Path

app_settings = {
    'theme': 'Dark Black',
    'width': 960,
    'height': 800,
    'title': 'Dual Slope'
}

default_dds_settings = {
    'RF': 80,
    'IF': 1,
    'refClk': 25e6,
    'PLL_MUL': 20,
    'activeChannels': [True, True, True, True],
    'channelFrequencies': [80.001e6, 80.001e6, 80e6, 80e6],
    'channelAmplitudes': [0.5, 0.02, 0.5, 0.5],
    'channelPhases': [0, 0, 0, 180],
    'channelDividers': [4, 8, 1, 1],
    'pins': {
        'IO_UP': 36,
        'RESET': 37,
        'P_DOWN': 33,
    }
}

default_adc_settings = {
    'rangeList': [u'\u00B1 12.288 V', u'\u00B1 10.24 V', u'\u00B1 6.144 V', u'\u00B1 5.12 V', u'\u00B1 2.56 V',
                  '0-12.288 V', '0-10.24 V', '0-6.144 V', '0-5.12 V'],
    'defaultRange': 4,
    'RST_PIN': [22, 18]
}

default_dem_settings = {
    'laserOnTime': 100e-3,
    'Demodulator-1': {
        'PHA_AMP_PIN': 29,
        'amplitudeCoefficients': {'slope': 3.0,
                                  'intercept': 50.0,
                                  'offset': 8.12,
                                  },
        'phaseCoefficients': {'A': 0.3006,
                              'freq': 0.0027722,
                              # 'phi': 0.01447449,
                              'phi': 0.0136,
                              'offset': 0.478},
        'integrationCount': 16,
    },
    'Demodulator-2': {
        'PHA_AMP_PIN': 31,
        'amplitudeCoefficients': {'slope': 2.95,
                                  'intercept': 19.06,
                                  'offset': 7.4,
                                  },
        'phaseCoefficients': {'A': 0.3003,
                              'freq': 0.002767,
                              'phi': 0.01447449,
                              'offset': 0.3491,
                              },
        'integrationCount': 16,
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

with open(Path.joinpath(Path().resolve(), 'settings', 'settings.json'), 'w') as f:
    json.dump(settings, f)
with open(Path.joinpath(Path().resolve(), 'settings', 'defaults.json'), 'w') as f:
    json.dump(settings, f)
with open(Path.joinpath(Path().resolve(), 'settings', 'app settings.json'), 'w') as f:
    json.dump(app_settings, f)
with open(Path.joinpath(Path().resolve(), 'settings', 'default dds settings.json'), 'w') as f:
    json.dump(default_dds_settings, f)
with open(Path.joinpath(Path().resolve(), 'settings', 'default adc settings.json'), 'w') as f:
    json.dump(default_adc_settings, f)
with open(Path.joinpath(Path().resolve(), 'settings', 'default dem settings.json'), 'w') as f:
    json.dump(default_dem_settings, f)
