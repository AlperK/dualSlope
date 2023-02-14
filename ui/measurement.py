from datetime import date
from pathlib import Path
import PySimpleGUI as Sg
from ui.drawings import measurement_graph
from ui.plot import canvas
import json


def prepare_measurement_folder():
    # Prepare the folder the measurements will be saved in
    home = Path('').home()
    base_folder = Path.joinpath(home, 'Documents', 'Dual Slope Data',
                                date.today().strftime('%Y-%m-%d'))
    base_folder.mkdir(parents=True, exist_ok=True)
    return base_folder


with open(Path.joinpath(Path().resolve(), 'settings', 'app settings.json')) as f:
    Sg.theme(json.load(f)['theme'])

baseFolder = prepare_measurement_folder()
_FILE_LOC_GRP = [
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
]

_FILE_LOC_FRA = Sg.Frame(title='Save file location',
                         layout=_FILE_LOC_GRP)

_MEAS_CNT_GRP = [
    [Sg.Text('Laser on time (ms):',
             size=(30, 1)),
     Sg.Input(default_text=100,
              size=(5, 1),
              key='__LASER_ON_TIME__', enable_events=False), ],
    [Sg.Button('Start', size=(10, 1),
               key='__MEAS_START__', enable_events=True),
     Sg.Button('Stop', size=(10, 1),
               key='__MEAS_STOP__', enable_events=True),
     ],
]

_DIS_ROW = [
    [measurement_graph],
    [Sg.Text('r1 (mm):'), Sg.Input(default_text='25', size=(5, 1),
                                   key='__MEAS_r__1', enable_events=False),
     Sg.Text('r2 (mm)'), Sg.Input(default_text='10', size=(5, 1),
                                  key='__MEAS_r__2', enable_events=False),
     ]
]
_MEAS_CNT_FRA = Sg.Frame(title='Measurement Controls',
                         layout=_MEAS_CNT_GRP + _DIS_ROW)

_GRAPH_ROW = [
    [canvas]
]
_GRAPH_COL = Sg.Column(layout=_GRAPH_ROW)


measurement_tab = Sg.Tab(title='Measurement',
                         layout=[
                             [_FILE_LOC_FRA],
                             [_MEAS_CNT_FRA, _GRAPH_COL],
                             # [_DIS_FRA],
                         ]
                         )
