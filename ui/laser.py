import PySimpleGUI as Sg

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
    pad=(10, (10, 0)),)

laser_frame = Sg.Frame(
    title='Laser Controls',
    layout=[
        [_LAS_COL],
    ],
    size=(370, 150),
)
