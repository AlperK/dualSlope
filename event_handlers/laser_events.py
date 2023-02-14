import PySimpleGUI as Sg


def laser_events(app, event, values):
    """
    Handles the events related to the Lasers
    :param app: The MainWindow
    :param event: The event
    :param values: The values dictionary
    :return:
    """
    # Turn on/off the selected Laser
    if event in [f'__LAS__{i}' for i in range(1, 5)]:
        channel = event[-1]
        if values[event]:
            getattr(app, f'laser{channel}').turn_on()
            app['__LOG__'].update(f"Laser-{channel} is turned on.\n", append=True)
        else:
            getattr(app, f'laser{channel}').turn_off()
            app['__LOG__'].update(f"Laser-{channel} is turned off.\n", append=True)

    elif event == '__LASER_ON_TIME__':
        if not values[event].isnumeric():
            app['__LOG__'].update('Invalid Laser On Time.\n', append=True)
            app[event].update(background_color='orange')
            return

        value = float(values[event])
        app['__LOG__'].update(f'Laser On Time set to {value} ms.\n', append=True)
        app[event].update(background_color=Sg.theme_input_background_color())
        app.laser_on_time = value / 1000
        # app['__LOG__'].update(f'laser on time {float(values[event])}\n', append=True)
