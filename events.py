import PySimpleGUI as Sg


def event_handler(app, event, values):
    if event == Sg.WIN_CLOSED:
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
        else:
            app.dds.wake_up()

    elif event == '__DDS_RST__':
        app.dds.reset()
        app.dds.load_settings(settings=values)

        app['__DDS_RF__'].update(value=values['__DDS_RF__'])
        app['__DDS_IF__'].update(value=values['__DDS_IF__'])
        app['__DDS_PLL_MUL__'].update(values=['__DDS_PLL_MUL__'])

    elif event == '__DDS_PLL_MUL__':
        app.dds.set_freqmult(int(values[event]), ioupdate=True)
        print('Here')

    elif event in [f'__DDS_CHA_AMP__{channel}' for channel in range(4)]:
        channel = int(event[-1])
        value = values[f'__DDS_CHA_AMP__{channel}']
        app.dds.set_output(channels=channel, value=float(value), var='amplitude', io_update=True)

    elif event in [f'__DDS_CHA_PHA__{channel}' for channel in range(4)]:
        channel = int(event[-1])
        value = values[f'__DDS_CHA_AMP__{channel}']
        app.dds.set_output(channels=channel, value=float(value), var='phase', io_update=True)

    else:
        print(f'Event \'{event}\' unrecognized.')
