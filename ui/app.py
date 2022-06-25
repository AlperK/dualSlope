import PySimpleGUI as Sg
import json
import ui.windows2 as windows

with open('app settings.json', 'r') as f:
    APP_SETTINGS = json.load(f)


class MainApplication(Sg.Window):
    def __init__(self):
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
