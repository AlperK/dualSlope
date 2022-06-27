import PySimpleGUI as Sg
import json
import hardware.hardware as hw
import ui.windows2 as windows

with open('app settings.json', 'r') as f:
    APP_SETTINGS = json.load(f)
with open('default dds settings.json', 'r') as f:
    DEF_DDS_SETTINGS = json.load(f)


class MainApplication(Sg.Window):
    def __init__(self):
        self.dds = hw.DDS(bus=0, device=0, pins=DEF_DDS_SETTINGS['pins'], max_speed=1_000_000)
        self.theme = APP_SETTINGS['theme']
        self.title = APP_SETTINGS['title']
        self.win_size = (APP_SETTINGS['width'], APP_SETTINGS['height'])
        self.log = Sg.Frame(title='Event Log',
                            layout=[[Sg.Multiline(disabled=True,
                                                  key='__LOG__',
                                                  size=(610, 20),
                                                  autoscroll=True,
                                                  )]]
                            )
        self.hwTabGroup = Sg.TabGroup(tab_location='left',
                                      layout=[
                                          [windows.HardwareTab()],
                                      ],
                                      expand_x=True)
        self.layout = [
            [self.hwTabGroup],
            [Sg.Text('', size=(8, None)), self.log]
        ]
        super(MainApplication, self).__init__(title=self.title,
                                              size=self.win_size,
                                              layout=self.layout,
                                              finalize=True
                                              )
        for channel in range(4):
            self[f'__DDS_CHA_AMP__{channel}'].bind("<Return>", key_modifier='')
            self[f'__DDS_CHA_PHA__{channel}'].bind("<Return>", key_modifier='')
        self['__DDS_RF__'].bind("<Return>", key_modifier='')
        self['__DDS_IF__'].bind("<Return>", key_modifier='')