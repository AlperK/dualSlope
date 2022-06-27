import PySimpleGUI as Sg
import RPi.GPIO as GPIO
import json


with open('default dds settings.json') as f:
    DEF_DDS_SET = json.load(f)


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
        print(f'Event Value: {value}')

        if event_group == 'DDS':
            dds_events(app, event, values)


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
        app.dds.load_settings(settings=DEF_DDS_SET)

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
            app['__LOG__'].update(f'Channel {channel} enabled.\n', append=True)
        else:
            app['__LOG__'].update(f'Channel {channel} disabled.\n', append=True)

    else:
        print(f'Event \'{event}\' unrecognized.')
