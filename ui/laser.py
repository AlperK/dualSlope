import PySimpleGUI as Sg
# import json
#
# with open(Path.joinpath(Path().resolve(), 'settings', 'app settings.json')) as f:
#     Sg.theme(json.load(f)['theme'])

_LAS_COL = Sg.Column(
    layout=[
        [Sg.Text(f"Laser-{i}: "), Sg.Checkbox(text='On/Off',
                                              default=False,
                                              key=f"__LAS__{i}",
                                              enable_events=True,
                                              )
         ]
        for i in range(1, 5)
    ],
    pad=(10, (10, 0)), )

laser_frame = Sg.Frame(
    title='Laser Controls',
    # background_color=Sg.theme_background_color(),
    layout=[
        [_LAS_COL],
    ],
    size=(300, 150),
)
