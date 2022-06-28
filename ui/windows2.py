import PySimpleGUI as Sg
import json
import numpy as np

with open('app settings.json', 'r') as f:
    APP_SETTINGS = json.load(f)
with open('default dds settings.json', 'r') as f:
    DEF_DDS_SETTINGS = json.load(f)
with open('default adc settings.json', 'r') as f:
    DEF_ADC_SETTINGS = json.load(f)


class HardwareTab(Sg.Tab):
    def __init__(self):
        self.layout = [[DDSFrame()],
                       [DemodulatorFrame()]]
        super(HardwareTab, self).__init__(title=f"Hardware \n Tab",
                                          layout=self.layout, )


class DDSFrame(Sg.Frame):
    def __init__(self):
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
                               size=(300, 135))

        self.layout = [
            [
                Sg.Column(layout=[
                    [_CHA_FRE_FRA, _DDS_SET_FRA],
                    [_CHA_AMP_FRA, _CHA_PHA_FRA, _CHA_EN_FRA]])
            ]
        ]

        super().__init__(title='DDS Settings', layout=self.layout)


class DemodulatorFrame(Sg.Frame):
    def __init__(self):
        self.title = 'Demodulator Controls'

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
            ]
        )
        _DEM_FRA_2 = Sg.Frame(title='Demodulator-2 Settings',
                              layout=[
                                  [_DEM_COL_2]
                              ])
        self.layout = [
            [_DEM_FRA_1, Sg.VerticalSeparator(), _DEM_FRA_2]
        ]
        super(DemodulatorFrame, self).__init__(title=self.title,
                                               layout=self.layout)
