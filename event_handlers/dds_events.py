import json
from pathlib import Path

import PySimpleGUI as Sg

import funcs.dds_funcs

with open(Path.joinpath(Path().resolve(), 'settings', 'default dds settings.json')) as f:
    DEF_DDS_SETTINGS = json.load(f)


def dds_events(app, event, values):
    """
    Handles the events related to the DDS
    :param app: The MainWindow
    :param event: The event
    :param values: The values dictionary
    :return:
    """
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

        # Put the default settings back into the UI.
        app['__DDS_RF__'].update(value=DEF_DDS_SETTINGS['RF'])
        app['__DDS_IF__'].update(value=DEF_DDS_SETTINGS['IF'])
        app['__DDS_PLL_MUL__'].update(value=DEF_DDS_SETTINGS['PLL_MUL'])

        for channel in range(4):
            app[f'__DDS_CHA_AMP__{channel}'].update(value=DEF_DDS_SETTINGS['channelAmplitudes'][channel])
            app[f'__DDS_CHA_PHA__{channel}'].update(value=DEF_DDS_SETTINGS['channelPhases'][channel])
            app[f'__DDS_CHA_DIV__{channel}'].update(value=DEF_DDS_SETTINGS['channelDividers'][channel])

        app['__LOG__'].update(f"DDS reset.\n", append=True)

    elif event == '__DDS_PLL_MUL__':
        app.dds.set_freqmult(int(values[event]), ioupdate=True)
        app['__LOG__'].update(f'DDS PLL set to {values[event]}.\n', append=True)

    elif event in [f'__DDS_CHA_AMP__{channel}' for channel in range(4)]:
        #   Check if the input can be a float, then between 0 and 1, then apply.

        channel = int(event[-1])
        for i in range(4):
            try:
                value = float(values[f'__DDS_CHA_AMP__{i}'])

                if not value <= 1.0:
                    app['__LOG__'].update(f'Invalid amplitude for Channel {i}.\n', append=True)
                    app[f'__DDS_CHA_AMP__{i}'].update(background_color='orange')
                    # break
                else:
                    app.dds.set_output(channels=i, value=float(value), var='amplitude', io_update=True)
                    if i == channel:
                        app['__LOG__'].update(f'Channel {i} amplitude set.\n', append=True)
                    app[f'__DDS_CHA_AMP__{i}'].update(background_color=Sg.theme_input_background_color())
            except ValueError:
                app['__LOG__'].update(f'Invalid amplitude for Channel {i}.\n', append=True)
                app[f'__DDS_CHA_AMP__{i}'].update(background_color='orange')

    elif event in [f'__DDS_CHA_PHA__{channel}' for channel in range(4)]:
        #   Check if the input can be a float, then between 0 and 360, then apply.

        channel = int(event[-1])
        for i in range(4):
            try:
                value = float(values[f'__DDS_CHA_PHA__{i}'])

                if not 0 <= value <= 360:
                    app['__LOG__'].update(f'Invalid phase for Channel {i}.\n', append=True)
                    app[f'__DDS_CHA_PHA__{i}'].update(background_color='orange')
                else:
                    app.dds.set_output(channels=i, value=value, var='phase', io_update=True)
                    app[f'__DDS_CHA_PHA__{i}'].update(background_color=Sg.theme_input_background_color())
                    if i == channel:
                        app['__LOG__'].update(f'Channel {i} phase set.\n', append=True)
            except ValueError:
                app['__LOG__'].update(f'Invalid phase for Channel {i}.\n', append=True)
                app[f'__DDS_CHA_PHA__{i}'].update(background_color='orange')

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
        new_rf = values['__DDS_RF__']
        new_if = values['__DDS_IF__']

        if not new_rf.isnumeric():
            app['__LOG__'].update(f'Invalid RF.\n', append=True)
            app['__DDS_RF__'].update(background_color='orange')

            if not new_if.isnumeric():
                app['__LOG__'].update(f'Invalid IF.\n', append=True)
                app['__DDS_IF__'].update(background_color='orange')
                return
            else:
                app['__DDS_IF__'].update(background_color=Sg.theme_input_background_color())

            return
        else:
            app['__DDS_RF__'].update(background_color=Sg.theme_input_background_color())
        if not float(new_rf) <= 120:
            app['__LOG__'].update(f'Invalid RF.\n', append=True)
            app['__DDS_RF__'].update(background_color='orange')
            return
        else:
            app['__DDS_RF__'].update(background_color=Sg.theme_input_background_color())

        # funcs.dds_funcs.set_rf_if(r_f=float(values['__DDS_RF__']),
        #                           i_f=float(values['__DDS_IF__']),
        #                           rf_channels=[0, 1],
        #                           lo_channels=[2, 3])
        funcs.dds_funcs.set_rf_if(r_f=float(values['__DDS_RF__']),
                                  i_f=float(values['__DDS_IF__']),
                                  dds=app.dds)
        app['__LOG__'].update('New RF and IF frequencies are set.\n', append=True)

    else:
        print(f'Event \'{event}\' unrecognized.')
