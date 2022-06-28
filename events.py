import PySimpleGUI as Sg
import RPi.GPIO as GPIO
import json


with open('default dds settings.json') as f:
    DEF_DDS_SETTINGS = json.load(f)
with open('default adc settings.json') as f:
    DEF_ADC_SETTINGS = json.load(f)


def event_handler(app, event, values):
    if event == Sg.WIN_CLOSED:
        GPIO.cleanup()
        return -1
    else:
        event_group = event.split('__')[1].split('_')[0]
        print(values)
        try:
            value = values[event]
        except KeyError:
            value = None
        print(f'Event Group: {event_group}')
        print(f'Event : {event}')
        print(f'Event Value: {value}')

        if event_group == 'DDS':
            dds_events(app, event, values)

        elif event_group == 'ADC':
            adc_events(app, event, values)

        elif event_group == 'DEM':
            dem_events(app, event, values)


def dds_events(app, event, values):
    if event == '__DDS_P_DWN__':
        if values[event]:
            app.dds.shutdown()
            app['__LOG__'].update(f"DDS shutdown.\n", append=True)
        else:
            app.dds.wake_up()
            app['__LOG__'].update(f"DDS wakeup.\n", append=True)

    elif event == '__DDS_RST__':
        app.dds.reset()
        app.dds.load_settings(settings=DEF_DDS_SETTINGS)

        app['__DDS_RF__'].update(value=values['__DDS_RF__'])
        app['__DDS_IF__'].update(value=values['__DDS_IF__'])
        app['__DDS_PLL_MUL__'].update(values=['__DDS_PLL_MUL__'])
        app['__LOG__'].update(f"DDS reset.\n", append=True)

    elif event == '__DDS_PLL_MUL__':
        app.dds.set_freqmult(int(values[event]), ioupdate=True)
        app['__LOG__'].update(f'DDS PLL set to {values[event]}.\n', append=True)

    elif event in [f'__DDS_CHA_AMP__{channel}' for channel in range(4)]:
        channel = int(event[-1])
        value = values[f'__DDS_CHA_AMP__{channel}']
        app.dds.set_output(channels=channel, value=float(value), var='amplitude', io_update=True)

        app['__LOG__'].update(f'Channel {channel} amplitude set to {values[event]}.\n', append=True)

    elif event in [f'__DDS_CHA_PHA__{channel}' for channel in range(4)]:
        channel = int(event[-1])
        value = values[f'__DDS_CHA_AMP__{channel}']
        app.dds.set_output(channels=channel, value=float(value), var='phase', io_update=True)

        app['__LOG__'].update(f'Channel {channel} phase set to {values[event]}.\n', append=True)

    elif event in [f'__DDS_CHA_EN__{channel}' for channel in range(4)]:
        channel = int(event[-1])

        if values[event]:
            app.dds.enable_channel(channel)
            app['__LOG__'].update(f'Channel {channel} enabled.\n', append=True)
        else:
            app.dds.disable_channel(channel)
            app['__LOG__'].update(f'Channel {channel} disabled.\n', append=True)

    elif event in [f'__DDS_CHA_DIV__{channel}' for channel in range(4)]:
        channel = int(event[-1])
        app.dds.set_current(channels=channel, divider=int(values[event]), ioupdate=True)

        app['__LOG__'].update(f'Channel {channel} divider set.\n', append=True)
    elif event in ['__DDS_RF__', '__DDS_IF__']:
        app.dds.set_rf_if(r_f=float(values['__DDS_RF__']),
                          i_f=float(values['__DDS_IF__']),
                          rf_channels=[0, 1],
                          lo_channels=[2, 3])
    else:
        print(f'Event \'{event}\' unrecognized.')


def adc_events(app, event, values):
    if event in [f'__ADC_RANGE__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        new_range = DEF_ADC_SETTINGS['rangeList'].index(values[event])
        if new_range >= 5:
            new_range += 3
        old_range = getattr(getattr(app, f'demodulator{channel}'), 'adc').get_range()
        getattr(getattr(app, f'demodulator{channel}'), 'adc').set_range(new_range)

        app['__LOG__'].update(f"Set ADC-{channel} range to {values[event]}.\n", append=True)
        app['__LOG__'].update(f"ADC-{channel} old range was {old_range}.\n", append=True)

    elif event in [f'__ADC_RST__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        getattr(getattr(app, f'demodulator{channel}'), 'adc').reset()

        app['__LOG__'].update(f'ADC-{channel} is reset.\n', append=True)


def dem_events(app, event, values):
    if event in [f'__DEM_SET_AMP__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        getattr(app, f'demodulator{channel}').set2amp()
        app['__LOG__'].update(f'Demodulator-{channel} set to amplitude mode.\n', append=True)

    elif event in [f'__DEM_SET_PHA__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        getattr(app, f'demodulator{channel}').set2pha()
        app['__LOG__'].update(f'Demodulator-{channel} set to phase mode.\n', append=True)

    elif event in [f'__DEM_MEA__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        if values[f'__DEM_SET_AMP__{channel}']:
            result = getattr(app, f'demodulator{channel}').measure_amplitude(raw=values[f'__DEM_RAW__{channel}'])
            app['__LOG__'].update(f'Demodulator-{channel} measurement result: {result}.\n', append=True)
            app['__LOG__'].update(f"Raw: {values[f'__DEM_RAW__{channel}']}.\n", append=True)
        elif values[f'__DEM_SET_PHA__{channel}']:
            result = getattr(app, f'demodulator{channel}').measure_phase(raw=values[f'__DEM_RAW__{channel}'])
            app['__LOG__'].update(f'Demodulator-{channel} measurement result: {result}.\n', append=True)
            app['__LOG__'].update(f"Raw: {values[f'__DEM_RAW__{channel}']}.\n", append=True)
