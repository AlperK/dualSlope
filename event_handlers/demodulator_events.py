def dem_events(app, event, values):
    """
    Handles the events related to the Demodulators
    :param app: The MainWindow
    :param event: The event
    :param values: The values dictionary
    :return:
    """
    if event in [f'__DEM_SET_AMP__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        getattr(app, f'demodulator{channel}').set2amp()
        app['__LOG__'].update(f'Demodulator-{channel} set to amplitude mode.\n',
                              append=True)

    elif event in [f'__DEM_SET_PHA__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        getattr(app, f'demodulator{channel}').set2pha()
        app['__LOG__'].update(f'Demodulator-{channel} set to phase mode.\n',
                              append=True)

    elif event in [f'__DEM_MEA__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        separations = [25, 35]
        if values[f'__DEM_SET_AMP__{channel}']:
            result = getattr(app, f'demodulator{channel}').measure_amplitude(raw=values[f'__DEM_RAW__{channel}'])
            app['__LOG__'].update(f'Demodulator-{channel} measurement result: {result}.\n', append=True)
        elif values[f'__DEM_SET_PHA__{channel}']:
            result = getattr(app, f'demodulator{channel}').measure_phase(raw=values[f'__DEM_RAW__{channel}'])
            app['__LOG__'].update(f'Demodulator-{channel} measurement result: {result}.\n', append=True)

    elif event in [f'__DEM_INTEG__{channel}' for channel in range(1, 3)]:
        channel = int(event[-1])
        getattr(app, f'demodulator{channel}').integration_number = int(values[event])
        app['__LOG__'].update(f"{getattr(app, f'demodulator{channel}')} integration count set to "
                              f"{getattr(app, f'demodulator{channel}').integration_number}.\n",
                              append=True)
