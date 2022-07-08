import PySimpleGUI as Sg
import json

with open('default adc settings.json') as f:
    DEF_ADC_SETTINGS = json.load(f)

Sg.theme('DarkTeal6')

_DEM_COL_1 = Sg.Column(layout=[
    [
        Sg.Text('ADC-1 Range'),
        Sg.Combo(DEF_ADC_SETTINGS['rangeList'],
                 default_value=DEF_ADC_SETTINGS['rangeList'][4],
                 key='__ADC_RANGE__1',
                 enable_events=True),
        Sg.Button('Reset',
                  key='__ADC_RST__1',
                  enable_events=True)
    ],
    [
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
        Sg.Button('Get Range',
                  key='__ADC_GET_RANGE__1',
                  enable_events=True),
    ],
    [
        Sg.Button('Measure', key='__DEM_MEA__1', enable_events=True),
        Sg.Checkbox('Raw', default=False, key='__DEM_RAW__1', enable_events=True)
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
        Sg.Text('ADC-2 Range'),
        Sg.Combo(DEF_ADC_SETTINGS['rangeList'],
                 default_value=DEF_ADC_SETTINGS['rangeList'][4],
                 key='__ADC_RANGE__2',
                 enable_events=True),
        Sg.Button('Reset',
                  key='__ADC_RST__2',
                  enable_events=True),
    ],
    [
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
        Sg.Button('Get Range',
                  key='__ADC_GET_RANGE__2',
                  enable_events=True),
    ],
    [
        Sg.Button('Measure', key='__DEM_MEA__2', enable_events=True),
        Sg.Checkbox('Raw', default=False, key='__DEM_RAW__2', enable_events=True)
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
