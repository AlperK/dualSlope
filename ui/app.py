import PySimpleGUI as Sg
import json
import hardware.hardware as hw
import Measurement
from ui.dds import dds_frame
from ui.demodulator import dem_frame
from ui.laser import laser_frame
from ui.measurement import measurement_tab
import ui.drawings

with open('app settings.json', 'r') as f:
    APP_SETTINGS = json.load(f)
with open('default dds settings.json', 'r') as f:
    DEF_DDS_SETTINGS = json.load(f)
with open('default adc settings.json', 'r') as f:
    DEF_ADC_SETTINGS = json.load(f)
with open('default dem settings.json', 'r') as f:
    DEF_DEM_SETTINGS = json.load(f)

Sg.theme('DarkTeal6')


class MainApplication(Sg.Window):
    """
    The main application. All the hardware is an attribute of this
    """

    def __init__(self):
        # General window settings
        Sg.change_look_and_feel(APP_SETTINGS['theme'])
        self.theme = APP_SETTINGS['theme']
        self.title = APP_SETTINGS['title']
        self.win_size = (APP_SETTINGS['width'], APP_SETTINGS['height'])

        # Instantiating the Log
        self.log = Sg.Frame(title='Event Log',
                            layout=[[Sg.Multiline(disabled=True,
                                                  key='__LOG__',
                                                  autoscroll=True,
                                                  size=(1200, 100),
                                                  # expand_x=True,
                                                  # expand_y=True,
                                                  )]]
                            )

        self.hardware_tab = Sg.Tab(title='Hardware',
                                   layout=[
                                       [dds_frame],
                                       [dem_frame, laser_frame]
                                   ])
        self.measurement_tab = measurement_tab

        # Instantiating the TabGroup
        self.tabGroup = Sg.TabGroup(tab_location='topleft',
                                    layout=[
                                        [self.hardware_tab],
                                        [self.measurement_tab],
                                    ],
                                    expand_x=True)

        self.layout = [
            [self.tabGroup],
            [self.log],
        ]
        super(MainApplication, self).__init__(title=self.title,
                                              size=self.win_size,
                                              layout=self.layout,
                                              finalize=True
                                              )

        # Binding the Return key to a few InputText elements so that they trigger events when Return is hit
        for channel in range(4):
            self[f'__DDS_CHA_AMP__{channel}'].bind("<Return>", key_modifier='')
            self[f'__DDS_CHA_PHA__{channel}'].bind("<Return>", key_modifier='')
        self['__DDS_RF__'].bind("<Return>", key_modifier='')
        self['__DDS_IF__'].bind("<Return>", key_modifier='')

        # Instantiating and initializing the DDS
        self.dds = hw.DDS(bus=1, device=0, pins=DEF_DDS_SETTINGS['pins'], max_speed=1_000_000)
        self.dds.initialize(settings=DEF_DDS_SETTINGS)

        # Instantiating and initializing the Demodulators
        self.demodulator1 = hw.Demodulator(adc=hw.ADC(bus=0, device=0,
                                                      reset_pin=DEF_ADC_SETTINGS['RST_PIN'][0],
                                                      max_speed=1_000_000),
                                           channel=1,
                                           settings=DEF_DEM_SETTINGS)
        self.demodulator2 = hw.Demodulator(adc=hw.ADC(bus=0, device=1,
                                                      reset_pin=DEF_ADC_SETTINGS['RST_PIN'][1],
                                                      max_speed=1_000_000),
                                           channel=2,
                                           settings=DEF_DEM_SETTINGS)

        self.demodulator1.adc.initialize(settings=DEF_ADC_SETTINGS)
        self.demodulator2.adc.initialize(settings=DEF_ADC_SETTINGS)

        # Instantiating and initializing the Lasers
        self.laser1 = hw.Laser(wavelength=685, pin=13)
        self.laser2 = hw.Laser(wavelength=685, pin=10)
        self.laser3 = hw.Laser(wavelength=830, pin=15)
        self.laser4 = hw.Laser(wavelength=830, pin=16)

        # Drawing the Laser and Demodulator indicators
        self.graph = self.Element('__GRAPH__')
        self.graph, self.window_rectangles, self.window_circles, self.window_texts = ui.drawings.draw_the_things(self.graph)

        # Instantiating the measurement
        self.save_location = None
        self.laser_on_time = float(self['__LASER_ON_TIME__'].get()) / 1000

        self.measurement = Measurement.Measurement(laser_on_time=self.laser_on_time,
                                                   save_location=self.save_location,
                                                   app=self)

