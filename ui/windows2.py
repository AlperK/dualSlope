import PySimpleGUI as Sg
import json

with open('app settings.json', 'r') as f:
    APP_SETTINGS = json.load(f)
with open('dds settings.json', 'r') as f:
    DDS_SETTINGS = json.load(f)


class HardwareTab(Sg.Tab):
    def __init__(self):
        self.layout = [[DDSFrame()]]
        super(HardwareTab, self).__init__(title=f'Hardware \n Tab',
                                          layout=self.layout,)


class DDSFrame(Sg.Frame):
    def __init__(self):
        _CHA_FRE_ROW = [
            [Sg.Text(text='RF', size=(15, None)),
            Sg.Input(default_text=DDS_SETTINGS['RF'], size=(15, None), key='__DDS_RF__'),
            Sg.Text(text='IF', size=(15, None)),
            Sg.Input(default_text=DDS_SETTINGS['IF'], size=(15, None), key='__DDS_IF__'),
        ]
        ]
        _CHA_FRE_FRA = Sg.Frame(title='DDS Frequency Settings',
                                layout=_CHA_FRE_ROW)

        _CHA_AMP_ROW = [
            ([
                Sg.Text(text=f'Channel {channel}',
                        size=(15, None)),
                Sg.InputText(default_text=f'{channel}',
                             size=(15, None),
                             enable_events=True,
                             key=f'__DDS_CHA_AMP__{channel}')
            ])
            for channel in range(4)]
        _CHA_AMP_FRA = Sg.Frame(title='DDS Amplitude Settings',
                                layout=_CHA_AMP_ROW)

        _CHA_PHA_ROW = [
            ([
                Sg.Text(text=f'Channel {channel}',
                        size=(15, None)),
                Sg.InputText(default_text=f'{channel}',
                             size=(15, None),
                             enable_events=True,
                             key=f'__DDS_CHA_PHA__{channel}')
            ])
            for channel in range(4)]
        _CHA_PHA_FRA = Sg.Frame(title='DDS Phase Settings',
                                layout=_CHA_PHA_ROW)
        self.layout = [
            [
                Sg.Column(layout=[
                          [_CHA_FRE_FRA],
                          [_CHA_AMP_FRA,
                           _CHA_PHA_FRA]])
            ]
        ]

        super().__init__(title='DDS Settings', layout=self.layout)

