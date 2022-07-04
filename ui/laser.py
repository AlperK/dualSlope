import PySimpleGUI as Sg

_LAS_COL = [
    [Sg.Text(f"Laser-{i}: "), Sg.Checkbox(text='On/Off',
                                          default=False,
                                          key=f"__LAS__{i}",
                                          enable_events=True,
                                          )]
    for i in range(1, 5)
]

laser_frame = Sg.Frame(
    title='Laser Controls',
    layout=_LAS_COL,
    expand_y=True,
    expand_x=True,
)
