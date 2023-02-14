import json
from pathlib import Path
from funcs.adc_funcs import range_from_range_list

with open(Path.joinpath(Path().resolve(), 'settings', 'default adc settings.json')) as f:
    DEF_ADC_SETTINGS = json.load(f)


def adc_events(app, event, values):
    """
    Handles the events related to the ADCs
    :param app: The MainWindow
    :param event: The event
    :param values: The values dictionary
    :return:
    """
    if event in [f'__ADC_RANGE__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        new_range = DEF_ADC_SETTINGS['rangeList'].index(values[event])

        if new_range >= 5:  # Check if the new range is bipolar or not.
            new_range += 3
        old_range = getattr(getattr(app, f'demodulator{channel}'), 'adc').get_range()
        getattr(getattr(app, f'demodulator{channel}'), 'adc').set_range(new_range)

        app['__LOG__'].update(f"Set ADC-{channel} range to {values[event]}.\n",
                              append=True)
        app['__LOG__'].update(f"ADC-{channel} old range was "
                              f"{range_from_range_list(old_range)}.\n",
                              append=True)

    elif event in [f'__ADC_RST__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        getattr(getattr(app, f'demodulator{channel}'), 'adc').reset()

        app[f'__ADC_RANGE__{channel}'].update(DEF_ADC_SETTINGS['rangeList'][0])
        app['__LOG__'].update(f'ADC-{channel} is reset.\n', append=True)

    elif event in [f'__ADC_GET_RANGE__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        app['__LOG__'].update(f"ADC-{channel} range is {getattr(app, f'demodulator{channel}').adc.get_range()}.\n",
                              append=True)
