import PySimpleGUI as Sg


def event_handler(app, event, values):
    if event == Sg.WIN_CLOSED:
        return -1
    else:
        event_group = event.split('__')[1].split('_')[0]
        value = values[event]
        print(f'Event Group: {event_group}')
        print(f'Event Value: {value}')

        if event_group == 'DDS':
            value = values[event]
            dds_events(app, event, value)


def dds_events(app, event, value):
    if event == '__DDS_P_DWN__':
        if value:
            app.dds.shutdown()
        else:
            app.dds.wake_up()

    elif event == '__DDS_RST__':
        app.dds.reset()
        app.dds.load_settings(settings=value)

        app['RF'].update(value=value)
        app['IF'].update(value=value)
        app['PLL_MUL'].update(value=value)

    else:
        print(f'Event: {event}')
