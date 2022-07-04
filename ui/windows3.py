import PySimpleGUI as Sg
import json
import numpy as np
from pathlib import Path

from ui.dds import dds_frame
from ui.demodulator import dem_frame
from ui.measurement import prepare_measurement_folder

with open('app settings.json', 'r') as f:
    APP_SETTINGS = json.load(f)
with open('default dds settings.json', 'r') as f:
    DEF_DDS_SETTINGS = json.load(f)
with open('default adc settings.json', 'r') as f:
    DEF_ADC_SETTINGS = json.load(f)


class HardwareTab(Sg.Tab):
    """
    The tab that includes all the Frames related to the hardware
    """

    def __init__(self):
        self.layout = [[DDSFrame()],
                       [DemodulatorFrame()]]
        super(HardwareTab, self).__init__(title=f"Hardware \nTab",
                                          layout=self.layout, )


dem_title = 'Demodulator Controls'

hardware_layout = [
    [dds_frame],
    [dem_frame],
]

hardware_tab = Sg.Tab(title='Hardware',
                      layout=hardware_layout)


class DDSFrame(Sg.Frame):
    """
    The Frame that includes all the Elements related to the DDS
    """

    def __init__(self):
        # RF and IF frequency settings
        _CHA_FRE_ROW = [
            [Sg.Text(text='RF (Mhz)', size=(15, None)),
             Sg.Input(default_text=DEF_DDS_SETTINGS['RF'],
                      size=(15, None),
                      key='__DDS_RF__',
                      enable_events=False),
             Sg.Text('', size=(8, None)),
             Sg.Text(text='IF (kHz)', size=(15, None)),
             Sg.Input(default_text=DEF_DDS_SETTINGS['IF'],
                      size=(15, None),
                      key='__DDS_IF__',
                      enable_events=False),
             ]
        ]
        _CHA_FRE_FRA = Sg.Frame(title='DDS Frequency Settings',
                                layout=_CHA_FRE_ROW,
                                size=(610, 50))

        # Miscellaneous DDS settings
        _DDS_SET_ROW = [
            [Sg.Button(button_text='Reset',
                       size=(10, 5),
                       enable_events=True,
                       key='__DDS_RST__'),
             Sg.Text('PLL Mul'),
             Sg.Combo(values=list(np.arange(4, 21)),
                      default_value=DEF_DDS_SETTINGS['PLL_MUL'],
                      enable_events=True,
                      key='__DDS_PLL_MUL__'), ]
        ]
        _DDS_SET_FRA = Sg.Frame(title='Misc',
                                layout=_DDS_SET_ROW,
                                size=(300, 50))

        # Channel amplitude settings
        _CHA_AMP_COL = [
            ([
                Sg.Text(text=f"Channel {channel}",
                        size=(15, None)),
                Sg.InputText(default_text=f"{DEF_DDS_SETTINGS['channelAmplitudes'][channel]}",
                             size=(15, None),
                             enable_events=False,
                             key=f"__DDS_CHA_AMP__{channel}")
            ])
            for channel in range(4)]
        _CHA_AMP_FRA = Sg.Frame(title='DDS Amplitude Settings',
                                layout=_CHA_AMP_COL,
                                size=(300, 135))

        # Channel phase settings
        _CHA_PHA_COL = [
            [
                Sg.Text(text=f"Channel {channel} (°)",
                        size=(15, None)),
                Sg.InputText(default_text=f"{DEF_DDS_SETTINGS['channelPhases'][channel]}",
                             size=(15, None),
                             enable_events=False,
                             key=f"__DDS_CHA_PHA__{channel}")
            ]
            for channel in range(4)]
        _CHA_PHA_FRA = Sg.Frame(title='DDS Phase Settings',
                                layout=_CHA_PHA_COL,
                                size=(300, 135))

        # Channel divider settings
        _CHA_DIV_COL = [
            [Sg.Text(f'Channel {channel}'),
             Sg.Combo(values=[1, 2, 4, 8],
                      default_value=DEF_DDS_SETTINGS['channelDividers'][channel],
                      key=f'__DDS_CHA_DIV__{channel}',
                      enable_events=True), ]
            for channel in range(4)
        ]
        _CHA_DIV_FRA = Sg.Frame(title='Channel Dividers',
                                layout=_CHA_DIV_COL,
                                size=(146, 135))

        # Channel enable/disable settings
        _CHA_EN_COL = [
            [
                Sg.Checkbox(text='Enable',
                            default=DEF_DDS_SETTINGS['activeChannels'][channel],
                            key=f"__DDS_CHA_EN__{channel}",
                            enable_events=True)
            ]
            for channel in range(4)
        ]
        _CHA_EN_FRA = Sg.Frame(title='Channel Enable',
                               layout=_CHA_EN_COL,
                               size=(146, 135))

        self.layout = [
            [
                Sg.Column(layout=[
                    [_CHA_FRE_FRA, _DDS_SET_FRA],
                    [_CHA_AMP_FRA, _CHA_PHA_FRA, _CHA_DIV_FRA, _CHA_EN_FRA]])
            ]
        ]

        super().__init__(title='DDS Settings', layout=self.layout)


class DemodulatorFrame(Sg.Frame):
    """
    The Frame that includes all the Elements related to the Demodulators
    """

    def __init__(self):
        self.title = 'Demodulator Controls'

        # Demodulator Settings
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
            ],
            [
                Sg.Button('Measure', key='__DEM_MEA__1', enable_events=True),
                Sg.Checkbox('Raw', default=False, key='__DEM_RAW__1', enable_events=True)
            ],
        ])
        _DEM_FRA_1 = Sg.Frame(title='Demodulator-1 Settings',
                              layout=[
                                  [_DEM_COL_1]
                              ])

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
            ],
            [
                Sg.Button('Measure', key='__DEM_MEA__2', enable_events=True),
                Sg.Checkbox('Raw', default=False, key='__DEM_RAW__2', enable_events=True)
            ],
        ])
        _DEM_FRA_2 = Sg.Frame(title='Demodulator-2 Settings',
                              layout=[
                                  [_DEM_COL_2]
                              ])
        self.layout = [
            [_DEM_FRA_1, Sg.VerticalSeparator(), _DEM_FRA_2]
        ]
        super(DemodulatorFrame, self).__init__(title=self.title,
                                               layout=self.layout)


class MeasurementTab(Sg.Tab):
    def __init__(self):
        self.base_folder = prepare_measurement_folder()
        # Path(str(datetime.today().date()))
        _FILE_LOC_ROW = [
            [Sg.Text('Measurement Save File Location: ',
                     size=(30, 1)),
             Sg.Input(Path(self.base_folder),
                      size=(50, None),
                      readonly=True,
                      key='__MEAS_LOC__',
                      # enable_events=True
                      ),
             Sg.FolderBrowse('Browse',
                             initial_folder=str(self.base_folder),
                             enable_events=True,
                             key='__MEAS_FOL__'
                             ),
             ],
            [Sg.Text('Measurement group:',
                     size=(30, 1)),
             Sg.Input('', key='__MEAS_GRP__',
                      size=(50, 1),
                      enable_events=True),

             ],
            [Sg.Text('Measurement number',
                     size=(30, 1)),
             Sg.Input('', key='__MEAS_NUM__',
                      size=(5, 1),
                      enable_events=True)],
            [Sg.Text('Laser on time (ms):',
                     size=(30, 1)),
             Sg.Input(default_text=100,
                      size=(5, 1),
                      key='__LASER_ON_TIME__')],
        ]

        super(MeasurementTab, self).__init__(title='Measurement \nTab',
                                             layout=_FILE_LOC_ROW,
                                             )
