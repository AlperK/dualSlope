import json
from pathlib import Path
import PySimpleGUI as Sg
import numpy as np

with open(Path.joinpath(Path().resolve(), 'settings', 'default dds settings.json')) as f:
    DEF_DDS_SETTINGS = json.load(f)
with open(Path.joinpath(Path().resolve(), 'settings', 'app settings.json')) as f:
    Sg.theme(json.load(f)['theme'])


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
                        size=(145, 135))


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
                       size=(145, 135))
dds_layout = [
    [
        Sg.Column(layout=[
            [_CHA_FRE_FRA, _DDS_SET_FRA],
            [_CHA_AMP_FRA, _CHA_PHA_FRA, _CHA_DIV_FRA, _CHA_EN_FRA]])
    ]
]
dds_frame = Sg.Frame(title='DDS Settings',
                     layout=dds_layout,
                     size=(930, 250),
                     )
