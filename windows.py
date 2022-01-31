import PySimpleGUI as Sg
import json
import datetime


with open('defaults.json', 'r') as f:
    settings = json.load(f)

    APP_SETTINGS = settings['APP_SETTINGS']
    DDS_SETTINGS = settings['DDS_SETTINGS']
    ADC_SETTINGS = settings['ADC_SETTINGS']
    MEA_SETTINGS = settings['MEA_SETTINGS']

Sg.theme(APP_SETTINGS['theme'])
# Sg.set_options(font=("Courier New", 10))
Sg.set_options(font=("Tahoma", 10))


class MainWindow(Sg.Window):
    def __init__(self):

        self.theme = APP_SETTINGS['theme']
        self.title = APP_SETTINGS['title']
        self.win_size = (APP_SETTINGS['width'], APP_SETTINGS['height'])

        self.mea_tab = MEASTab()
        self.hardware_tab = HardwareTab()
        self.demod_tab = DemodulatorTab()
        self.layout = [
            [Sg.TabGroup([
                [self.hardware_tab],
                [self.mea_tab],
                [self.demod_tab],
            ]),
            ],
            [Log()]
        ]

        self.window = Sg.Window.__init__(self, title=self.title, layout=self.layout, size=self.win_size, resizable=True,
                                         grab_anywhere=True, keep_on_top=True, finalize=True)


class HardwareTab(Sg.Tab):
    def __init__(self):
        self.win_layout = [
            [DDSFrame()],
            [ADCFrame()],
        ]
        self.layout_keys = ['RF', 'IF',
                            'CH_0_AMP', 'CH_1_AMP', 'CH_2_AMP', 'CH_3_AMP',
                            'CH_0_DIV', 'CH_1_DIV', 'CH_2_DIV', 'CH_3_DIV',
                            'CH_0_PHA', 'CH_1_PHA', 'CH_2_PHA', 'CH_3_PHA',
                            'PLL_MUL', 'DDS_PDWN', 'SYNC_CLK']

        Sg.Tab.__init__(self, title='Hardware Details', layout=self.win_layout)


class DDSFrame(Sg.Frame):
    def __init__(self):
        _DDS_DES_COL = Sg.Column([
            [Sg.Text('Channel Frequencies', size=(20, 1))],
            [Sg.Text('Channel Amplitudes', size=(20, 1))],
            [Sg.Text('Channel Dividers', size=(20, 1))],
            [Sg.Text('Channel Phases', size=(20, 1))],
            # [Sg.Button('States', size=(20, 1), key='-ST-')],
        ])

        _DDS_CHN_COL_0 = Sg.Column([
            [Sg.Text('RF (MHz)', size=(10, 1)),
             Sg.InputText(default_text=DDS_SETTINGS['RF'],
                          size=(5, 1), justification='left', key='RF')],
            [Sg.Text('Channel 0', size=(10, 1)),
             Sg.InputText(default_text=DDS_SETTINGS['channelAmplitudes'][0],
                          size=(5, 1), justification='left', enable_events=True, key='CH_0_AMP')],
            [Sg.Text('Channel 0', size=(10, 1)),
             Sg.Combo([1, 2, 4, 8], default_value=DDS_SETTINGS['channelDividers'][0],
                      size=(5, 5), enable_events=True, key='CH_0_DIV')],
            [Sg.Text('Channel 0', size=(10, 1)),
             Sg.InputText(default_text=DDS_SETTINGS['channelPhases'][0],
                          size=(5, 1), enable_events=False, key='CH_0_PHA')],
            # [Sg.Button('Amplitudes', enable_events=True, key='-amplitudes-')]
        ])
        _DDS_CHN_COL_1 = Sg.Column([
            [Sg.Text('IF (kHz)', size=(10, 1)),
             Sg.InputText(default_text=DDS_SETTINGS['IF'],
                          size=(5, 1), justification='left', key='IF')],
            [Sg.Text('Channel 1', size=(10, 1)),
             Sg.InputText(default_text=DDS_SETTINGS['channelAmplitudes'][1],
                          size=(5, 1), justification='left', enable_events=True, key='CH_1_AMP')],
            [Sg.Text('Channel 1', size=(10, 1)),
             Sg.Combo([1, 2, 4, 8], default_value=DDS_SETTINGS['channelDividers'][1],
                      size=(5, 5), enable_events=True, key='CH_1_DIV')],
            [Sg.Text('Channel 1', size=(10, 1)),
             Sg.InputText(default_text=DDS_SETTINGS['channelPhases'][1],
                          size=(5, 1), enable_events=False, key='CH_1_PHA')],
            # [Sg.Button('Frequencies', enable_events=True, key='-freqs-')]
        ])
        _DDS_CHN_COL_2 = Sg.Column([
            [Sg.Text('PLL Multi', size=(10, 1)),
             Sg.Combo([x for x in range(4, 21)], default_value=DDS_SETTINGS['PLL_MUL'],
                      size=(5, 5), enable_events=True, key='PLL_MUL')],
            [Sg.Text('Channel 2', size=(10, 1)),
             Sg.InputText(default_text=DDS_SETTINGS['channelAmplitudes'][2],
                          size=(5, 1), justification='left', enable_events=True, key='CH_2_AMP')],
            [Sg.Text('Channel 2', size=(10, 1)),
             Sg.Combo([1, 2, 4, 8], default_value=DDS_SETTINGS['channelDividers'][2],
                      size=(5, 5), enable_events=True, key='CH_2_DIV')],
            [Sg.Text('Channel 2', size=(10, 1)),
             Sg.InputText(default_text=DDS_SETTINGS['channelPhases'][2],
                          size=(5, 1), enable_events=False, key='CH_2_PHA')],
            # [Sg.Button('Phases', enable_events=True, key='-phases-')]
        ])
        _DDS_CHN_COL_3 = Sg.Column([
            [Sg.Text('', size=(10, 1))],
            [Sg.Text('Channel 3', size=(10, 1)),
             Sg.InputText(default_text=DDS_SETTINGS['channelAmplitudes'][3],
                          size=(5, 1), justification='left', enable_events=True, key='CH_3_AMP')],
            [Sg.Text('Channel 3', size=(10, 1)),
             Sg.Combo([1, 2, 4, 8], default_value=DDS_SETTINGS['channelDividers'][3],
                      size=(5, 5), enable_events=True, key='CH_3_DIV')],
            [Sg.Text('Channel 3', size=(10, 1)),
             Sg.InputText(default_text=DDS_SETTINGS['channelPhases'][3],
                          size=(5, 1), enable_events=False, key='CH_3_PHA')],
            # [Sg.Button('Dividers', enable_events=True, key='-dividers-')]
        ])

        _DDS_CHN_COL = Sg.Column([
            [_DDS_CHN_COL_0,
             _DDS_CHN_COL_1,
             _DDS_CHN_COL_2,
             _DDS_CHN_COL_3]
        ])

        _DDS_PDR_COL = Sg.Column([
            # [Sg.Text()],
            [Sg.Checkbox('Power Down', default=False,
                         size=(10, 1), enable_events=True, key='DDS_PDWN')],
            [Sg.Checkbox('SYNC CLK', default=True,
                         size=(10, 1), enable_events=True, key='SYNC_CLK')],
            [Sg.Text()],
            # [Sg.Text()],
            [Sg.Button('Load', size=(5, 1), enable_events=True, key='DDS_LOAD', auto_size_button=False),
             Sg.Button('Read', size=(5, 1), enable_events=True, key='DDS_READ')],
            [Sg.Button('Load Default Settings', key='DDS_DEFAULTS')]
        ])

        self.win_layout = [
            [
            _DDS_DES_COL,
            _DDS_CHN_COL,
            _DDS_PDR_COL,
            ]
        ]

        Sg.Frame.__init__(self, title='DDS', layout=self.win_layout)


class ADCFrame(Sg.Frame):
    def __init__(self):
        _ADC_COL_0 = Sg.Column([
            [Sg.Text('')],
            [Sg.Text('Range')],
        ])
        _ADC_COL_1 = Sg.Column([
            [Sg.Text('ADC 1', size=(10, 1))],
            [Sg.Combo([u'\u00B1 12.288 V', u'\u00B1 10.24 V', u'\u00B1 6.144 V', u'\u00B1 5.12 V', u'\u00B1 2.56 V',
                       '0-12.288 V', '0-10.24 V', '0-6.144 V', '0-5.12 V'],
                      default_value=ADC_SETTINGS['range'][4], enable_events=True, key='ADC_1_RANGE')],
            [Sg.Button('Reset', size=(10, 1), key='ADC_1_RESET')],
            [Sg.Button('Measure', size=(10, 1), key='ADC_1_MEAS')],
        ])
        _ADC_COL_2 = Sg.Column([
            [Sg.Text('ADC 2', size=(20, 1))],
            [Sg.Combo([u'\u00B1 12.288 V', u'\u00B1 10.24 V', u'\u00B1 6.144 V', u'\u00B1 5.12 V', u'\u00B1 2.56 V',
                       '0-12.288 V', '0-10.24 V', '0-6.144 V', '0-5.12 V'],
                      default_value=ADC_SETTINGS['range'][4], enable_events=True, key='ADC_2_RANGE')],
            [Sg.Button('Reset', size=(10, 1), key='ADC_2_RESET')],
            [Sg.Button('Measure', size=(10, 1), key='ADC_2_MEAS')],
        ])

        self.win_layout = [[_ADC_COL_0, _ADC_COL_1, Sg.VerticalSeparator(), _ADC_COL_2]]
        Sg.Frame.__init__(self, title='ADC', layout=self.win_layout)


class MEASTab(Sg.Tab):
    def __init__(self):
        graph = Sg.Graph(
                canvas_size=MEA_SETTINGS['canvasSize'],
                graph_bottom_left=(0, 0),
                graph_top_right=MEA_SETTINGS['canvasSize'],
                key="-GRAPH-",
                enable_events=True,
                background_color='dimgrey',
                drag_submits=True)
        data = [[1, 2], [2, 1], [1, 2], [2, 1], [1, 2], [2, 1], [1, 2], [2, 1]]

        amp_matrix = Sg.Table(values=data, headings=['APD 1', 'APD 2'], auto_size_columns=False, col_widths=[6, 6],
                          num_rows=8, justification='center', display_row_numbers=True, alternating_row_color='black')
        _MEAS_ROW_1 = [Sg.Text('Measurement Location:', size=(30, 1)),
                       Sg.InputText(size=(30, 1), key='MEAS_LOC', readonly=True,
                                    disabled_readonly_background_color=Sg.theme_element_background_color(),
                                    disabled_readonly_text_color=Sg.theme_element_text_color()),
                       Sg.FolderBrowse(target='MEAS_LOC'),
                       Sg.Stretch(),
                       Sg.Button('Start', size=(10, 1), key='MEAS_START'),
                       Sg.Button('Stop', size=(10, 1), key='MEAS_STOP')]
        _MEAS_ROW_2 = [Sg.Text('Measurement Name:', size=(30, 1)),
                       Sg.InputText(key='MEAS_NAME', enable_events=True,
                                    disabled_readonly_background_color=Sg.theme_element_background_color(),
                                    disabled_readonly_text_color=Sg.theme_element_text_color()),
                       Sg.Text('Measurement Number:', size=(20, 1)),
                       Sg.InputText(key='MEAS_NUM', size=(5, 1), enable_events=True,
                                    disabled_readonly_background_color=Sg.theme_element_background_color(),
                                    disabled_readonly_text_color=Sg.theme_element_text_color())]
        _MEAS_ROW_3 = [Sg.Text('Measurement Date (YYYY-MM-DD):', size=(30, 1)),
                       Sg.InputText(default_text=datetime.date.today(), key='MEAS_DATE', enable_events=True,
                                    disabled_readonly_background_color=Sg.theme_element_background_color(),
                                    disabled_readonly_text_color=Sg.theme_element_text_color()),
                       Sg.CalendarButton('Calendar', target='MEAS_DATE', format='%Y-%m-%d', key='ASD',
                                         default_date_m_d_y=(1, None, 2022)),
                       # Sg.Button('File Name', key='MEAS_FILE'),
                       ]
        _MEAS_ROW_4 = [Sg.Text('_'*150)]
        _MEAS_ROW_5 = [Sg.Text('Switching Period (ms):', size=(30, 1)),
                       Sg.InputText(key='SW_TIME', default_text=MEA_SETTINGS['laserOnTime'], enable_events=True,
                                    disabled_readonly_background_color=Sg.theme_element_background_color(),
                                    disabled_readonly_text_color=Sg.theme_element_text_color())]

        _MEAS_COL_2 = Sg.Column(
            [_MEAS_ROW_1, _MEAS_ROW_2, _MEAS_ROW_3, _MEAS_ROW_4, _MEAS_ROW_5]
        )
        _MEAS_COL_1 = Sg.Column([
            [graph, amp_matrix]
        ])

        self.tab_layout = [[_MEAS_COL_2], [_MEAS_COL_1]]
        Sg.Tab.__init__(self, title='Measurement Details', layout=self.tab_layout)


class Log(Sg.Frame):
    def __init__(self):
        self.win_layout = [[
            Sg.Multiline(disabled=True, key='EVE_LOG', size=(400, 25), enable_events=True)
        ]]
        Sg.Frame.__init__(self, title='Event Log', layout=self.win_layout)


class DemodulatorTab(Sg.Tab):
    def __init__(self):
        _DEMOD_ROW = [
                Sg.Radio('Demodulator 1', 'Demodulator', enable_events=True, default=False, size=(15, 1)),
                Sg.Radio('Demodulator 2', 'Demodulator', enable_events=True, default=False, size=(15, 1)),
             ]
        _DEMOD_FRAME = Sg.Frame(title='', layout=[
            _DEMOD_ROW
        ])

        _PHA_ROW_0 = [
            Sg.Text('Start Frequency (kHz): ', size=(20, 1)),
            Sg.Input(size=(5, 1), default_text='1', key='PHA_CALIB_START_PHA'),
            Sg.Text('Stop Frequency (kHz): ', size=(20, 1)),
            Sg.Input(size=(5, 1), default_text='10', key='PHA_CALIB_STOP_PHA'),
            Sg.Text('Step (kHz):', size=(20, 1)),
            Sg.Input(size=(5, 1), default_text='3', key='PHA_CALIB_STEP_PHA'),
        ]
        _PHA_ROW_1 = [
            Sg.Text('Start Amplitude (V): ', size=(20, 1)),
            Sg.Input(size=(5, 1), default_text='0.5', key='PHA_CALIB_START_AMP'),
            Sg.Text('Stop Amplitude (V): ', size=(20, 1)),
            Sg.Input(size=(5, 1), default_text='2', key='PHA_CALIB_STOP_AMP'),
            Sg.Text('Step (V):', size=(20, 1)),
            Sg.Input(size=(5, 1), default_text='0.5', key='PHA_CALIB_STEP_AMP'),
        ]
        _PHA_ROW_2 = [
            Sg.Button('Start', key='PHA_CALIB_START'),
            Sg.Button('Stop', key='PHA_CALIB_STOP'),
        ]

        _PHA_FRAME = Sg.Frame(title='Phase Calibration', layout=[
            _PHA_ROW_0,
            _PHA_ROW_1,
            _PHA_ROW_2,
        ])

        _AMP_ROW_0 = [
            Sg.Text('Start Amplitude (mV): ', size=(20, 1)),
            Sg.Input(size=(5, 1), default_text='20', key='AMP_CALIB_START_AMP'),
            Sg.Text('Stop Amplitude (mV): ', size=(20, 1)),
            Sg.Input(size=(5, 1), default_text='2000', key='AMP_CALIB_STOP_AMP'),
            Sg.Text('Step (mV):', size=(20, 1)),
            Sg.Input(size=(5, 1), default_text='10', key='AMP_CALIB_STEP_AMP'),
        ]
        _AMP_ROW_1 = [
            Sg.Text('Start Frequency (kHz): ', size=(20, 1)),
            Sg.Input(size=(5, 1), default_text='1', key='AMP_CALIB_START_PHA'),
            Sg.Text('Stop Frequency (kHz): ', size=(20, 1)),
            Sg.Input(size=(5, 1), default_text='10', key='AMP_CALIB_STOP_PHA'),
            Sg.Text('Step (kHz):', size=(20, 1)),
            Sg.Input(size=(5, 1), default_text='3', key='AMP_CALIB_STEP_PHA')
        ]
        _AMP_ROW_2 = [
            Sg.Button('Start', key='AMP_CALIB_START'),
            Sg.Button('Stop', key='AMP_CALIB_STOP'),
        ]

        _AMP_FRAME = Sg.Frame(title='Amplitude Calibration', layout=[
            _AMP_ROW_0,
            _AMP_ROW_1,
            _AMP_ROW_2,
        ])

        self.layout = [
            [_DEMOD_FRAME],
            [_PHA_FRAME],
            [_AMP_FRAME],
        ]

        Sg.Tab.__init__(self, title='Demodulator Calibration', layout=self.layout)
