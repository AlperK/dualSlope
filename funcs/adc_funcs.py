import json
from pathlib import Path

with open(Path.joinpath(Path().resolve(), 'settings', 'default adc settings.json'), 'r') as f:
    ADC_SETTINGS = json.load(f)


def range_from_range_list(range_word):
    if range_word >= 5:
        range_word -= 3

    return ADC_SETTINGS['rangeList'][range_word]
