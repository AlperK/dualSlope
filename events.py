import PySimpleGUI as Sg


def event_handler(app, event, values):
    if event == Sg.WIN_CLOSED:
        return -1
    else:
        event_group = event.split('_')[0]

        if event_group == 'DDS':
            values = values['DDS_SETTINGS']
            dds_events(app, event, values)


def dds_events(app, event, values):
    if event == 'DDS_P_DWN':
        if values['PDWN']:
            app.dds.shutdown()
        else:
            app.dds.wake_up()

    elif event == 'DDS_RST':
        app.dds.reset()
        app.dds.load_settings(settings=values)

        app['RF'].update(value=values['RF'])
        app['IF'].update(value=values['IF'])
        app['PLL_MUL'].update(value=values['PLL_MUL'])
