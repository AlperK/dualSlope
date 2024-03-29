import json
from pathlib import Path
import PySimpleGUI as Sg

with open(Path.joinpath(Path().resolve(), 'settings', 'default adc settings.json')) as f:
    DEF_ADC_SETTINGS = json.load(f)
with open(Path.joinpath(Path().resolve(), 'settings', 'default dem settings.json')) as f:
    DEF_DEM_SETTINGS = json.load(f)
with open(Path.joinpath(Path().resolve(), 'settings', 'app settings.json')) as f:
    Sg.theme(json.load(f)['theme'])

_DEM_COL_1 = Sg.Column(layout=[
    [
        Sg.Text('Range: ',
                size=(8, 1)),
        Sg.Combo(DEF_ADC_SETTINGS['rangeList'],
                 default_value=DEF_ADC_SETTINGS['rangeList'][4],
                 key='__ADC_RANGE__1',
                 size=(8, 1),
                 enable_events=True),
        Sg.Text('Integrate',
                size=(8, 1)),
        Sg.Input(DEF_DEM_SETTINGS['Demodulator-1']['integrationCount'],
                 size=(8, 1),
                 enable_events=False,
                 key='__DEM_INTEG__1'),
    ],
    [Sg.Text('Mode: ',
             size=(5, 1)),
     Sg.Checkbox('Raw', default=False, key='__DEM_RAW__1', enable_events=True),
     Sg.Radio('Amplitude',
              default=True,
              group_id='PHA_AMP_1',
              key='__DEM_SET_AMP__1',
              enable_events=True),
     Sg.Radio('Phase',
              default=False,
              group_id='PHA_AMP_1',
              key='__DEM_SET_PHA__1',
              enable_events=True),
     # Sg.Button('Get Range',
     #           key='__ADC_GET_RANGE__1',
     #           enable_events=True),
     ],
    [Sg.Text('Action:'),
     Sg.Button('Measure', key='__DEM_MEA__1', enable_events=True),
     Sg.Button('Reset', key='__ADC_RST__1', enable_events=True)
     ],
])
_DEM_FRA_1 = Sg.Frame(title='Demodulator-1 Settings',
                      layout=[
                          [_DEM_COL_1]
                      ],
                      size=(300, 150),
                      )
_DEM_COL_2 = Sg.Column(layout=[
    [
        Sg.Text('Range: ',
                size=(6, 1)),
        Sg.Combo(DEF_ADC_SETTINGS['rangeList'],
                 default_value=DEF_ADC_SETTINGS['rangeList'][4],
                 key='__ADC_RANGE__2',
                 enable_events=True),
        Sg.Text('Integrate',
                size=(8, 1)),
        Sg.Input(DEF_DEM_SETTINGS['Demodulator-2']['integrationCount'],
                 size=(8, 1),
                 enable_events=False,
                 key='__DEM_INTEG__2')
    ],
    [Sg.Text('Mode: ',
             size=(5, 1)),
     Sg.Checkbox('Raw', default=False, key='__DEM_RAW__2', enable_events=True),
     Sg.Radio('Amplitude',
              default=True,
              group_id='PHA_AMP_2',
              key='__DEM_SET_AMP__2',
              enable_events=True),
     Sg.Radio('Phase',
              default=False,
              group_id='PHA_AMP_2',
              key='__DEM_SET_PHA__2',
              enable_events=True),
     # Sg.Button('Get Range',
     #           key='__ADC_GET_RANGE__2',
     #           enable_events=True),
     ],
    [
        Sg.Text('Action: '),
        Sg.Button('Measure', key='__DEM_MEA__2', enable_events=True),
        Sg.Button('Reset', key='__ADC_RST__2', enable_events=True),
    ],
])
_DEM_FRA_2 = Sg.Frame(title='Demodulator-2 Settings',
                      layout=[
                          [_DEM_COL_2]
                      ],
                      size=(300, 150),
                      )
dem_layout = [
    [_DEM_FRA_1,
     # Sg.VerticalSeparator(),
     _DEM_FRA_2]
]
dem_frame = Sg.Frame(title='Demodulator Controls',
                     layout=dem_layout,
                     size=(620, 150)
                     )
