import PySimpleGUI as Sg
from pathlib import Path


def prepare_measurement_folder():
    # Prepare the folder the measurements will be saved in
    home = Path('').home()
    base_folder = Path.joinpath(home, 'Documents', 'Dual Slope Data')
    base_folder.mkdir(parents=True, exist_ok=True)
    return base_folder


baseFolder = prepare_measurement_folder()
_FILE_LOC_ROW = [
    [Sg.Text('Measurement Save File Location: ',
             size=(30, 1)),
     Sg.Input(Path(baseFolder),
              size=(50, None),
              readonly=True,
              key='__MEAS_LOC__',
              enable_events=True,
              ),
     Sg.FolderBrowse('Browse',
                     initial_folder=str(baseFolder),
                     enable_events=True,
                     key='__MEAS_FOL__',
                     ),
     ],
    [Sg.Text('Measurement group:',
             size=(30, 1)),
     Sg.Input('', key='__MEAS_GRP__',
              size=(50, 1),
              enable_events=True,
              ),

     ],
    [Sg.Text('Measurement number',
             size=(30, 1)),
     Sg.Input('', key='__MEAS_NUM__',
              size=(5, 1),
              enable_events=True,
              )],
    [Sg.Text('Laser on time (ms):',
             size=(30, 1)),
     Sg.Input(default_text=100,
              size=(5, 1),
              key='__LASER_ON_TIME__')],
    [Sg.Button('Create', size=(10, 1), key='__MEAS_CRT__', enable_events=True),],
    [Sg.Button('Start', size=(10, 1), key='__MEAS_START__', enable_events=True),],
]

measurement_tab = Sg.Tab(title='Measurement',
                         layout=_FILE_LOC_ROW)
