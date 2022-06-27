import PySimpleGUI as Sg
import json
import hardware.hardware as hw
import ui.windows2 as windows

with open('app settings.json', 'r') as f:
    APP_SETTINGS = json.load(f)
with open('dds settings.json', 'r') as f:
    DDS_SETTINGS = json.load(f)


class MainApplication(Sg.Window):
    def __init__(self):
        self.dds = hw.DDS(bus=0, device=0, pins=DDS_SETTINGS['pins'], max_speed=1_000_000)
        self.theme = APP_SETTINGS['theme']
        self.title = APP_SETTINGS['title']
        self.win_size = (APP_SETTINGS['width'], APP_SETTINGS['height'])
        self.layout = [
            [Sg.TabGroup(tab_location='left',
                         layout=[
                             [windows.HardwareTab()],
                                 ],)
             ]
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
