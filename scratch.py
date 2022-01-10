import json


with open('settings.json', 'r') as f:
    settings = json.load(f)
    APP_SETTINGS = settings['APP_SETTINGS']
    DDS_SETTINGS = settings['DDS_SETTINGS']
    ADC_SETTINGS = settings['ADC_SETTINGS']
    MEA_SETTINGS = settings['MEA_SETTINGS']
    LAS_SETTINGS = settings['LAS_SETTINGS']
    PIN_SETTINGS = settings['PIN_SETTINGS']


fileName = 'measurement conditions.json'


measurement_conditions = {}
measurement_conditions.update(DDS_SETTINGS)
measurement_conditions.update(ADC_SETTINGS)

print(measurement_conditions)

with open('measurement conditions.json', 'w') as f:
    json.dump(measurement_conditions, f)
