import PySimpleGUI as Sg
import json
import numpy as np

with open('app settings.json', 'r') as f:
    APP_SETTINGS = json.load(f)
with open('dds settings.json', 'r') as f:
    DDS_SETTINGS = json.load(f)


class HardwareTab(Sg.Tab):
    def __init__(self):
        self.layout = [[DDSFrame()]]
        super(HardwareTab, self).__init__(title=f'Hardware \n Tab',
                                          layout=self.layout, )


class DDSFrame(Sg.Frame):
    def __init__(self):
        _CHA_FRE_ROW = [
            [Sg.Text(text='RF', size=(15, None)),
             Sg.Input(default_text=DDS_SETTINGS['RF'],
                      size=(15, None),
                      key='__DDS_RF__',
                      enable_events=False),
             Sg.Text('', size=(8, None)),
             Sg.Text(text='CF', size=(15, None)),
             Sg.Input(default_text=DDS_SETTINGS['IF'],
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
                      default_value=20,
                      enable_events=True,
                      key='__DDS_PLL_MUL__'), ]
        ]
        _DDS_SET_FRA = Sg.Frame(title='Misc',
                                layout=_DDS_SET_ROW,
                                size=(300, 50))

        _CHA_AMP_COL = [
            ([
                Sg.Text(text=f'Channel {channel}',
                        size=(15, None)),
                Sg.InputText(default_text=f'{channel}',
                             size=(15, None),
                             enable_events=False,
                             key=f'__DDS_CHA_AMP__{channel}')
            ])
            for channel in range(4)]
        _CHA_AMP_FRA = Sg.Frame(title='DDS Amplitude Settings',
                                layout=_CHA_AMP_COL,
                                size=(300, 135))

        _CHA_PHA_COL = [
            [
                Sg.Text(text=f'Channel {channel}',
                        size=(15, None)),
                Sg.InputText(default_text=f'{channel}',
                             size=(15, None),
                             enable_events=False,
                             key=f'__DDS_CHA_PHA__{channel}')
            ]
            for channel in range(4)]
        _CHA_PHA_FRA = Sg.Frame(title='DDS Phase Settings',
                                layout=_CHA_PHA_COL,
                                size=(300, 135))

        _CHA_EN_COL = [
            [
                Sg.Checkbox(text='Enable',
                            default=True,
                            key=f'__DDS_CHA_EN__{channel}',
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
