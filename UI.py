import PySimpleGUI as Sg
import ADS8685
import Demodulator
import windows
import funcs
import json
from pathlib import Path as Path
import RPi.GPIO as GPIO


with open('settings.json', 'r') as f:
    settings = json.load(f)
    APP_SETTINGS = settings['APP_SETTINGS']
    DDS_SETTINGS = settings['DDS_SETTINGS']
    ADC_SETTINGS = settings['ADC_SETTINGS']
    MEA_SETTINGS = settings['MEA_SETTINGS']
    LAS_SETTINGS = settings['LAS_SETTINGS']
    PIN_SETTINGS = settings['PIN_SETTINGS']


_VARS = {

}
_VARS.update(settings)


def event_values(app, event, values):
    if event == Sg.WIN_CLOSED:
        return -1

    elif event == 'DDS_PDWN':
        print(values['DDS_PDWN'])
        if values['DDS_PDWN']:
            app.dds.shutdown()
        else:
            app.dds.wake_up()

    elif event == 'DDS_RST':
        app.dds.reset()
        funcs.load_dds_settings(device=app.dds, var_dict=_VARS, window=app)
        print(_VARS)

    elif event in ['CH_0_AMP_Enter', 'CH_1_AMP_Enter', 'CH_2_AMP_Enter', 'CH_3_AMP_Enter']:
        channel = int(event[3])
        value = float(values[event[:8]])

        app.dds.set_output(channel, value=value, var='amplitude', io_update=True)

        if 0.99*value <= app.dds.read_amplitude(channel) <= 1.01*value:
            update_vars('DDS_SETTINGS', 'channelAmplitudes', value, channel)
            funcs.update_event_log('Channel {} amplitude is set to {}.'.format(channel, value),
                                   _VARS, app)
        else:
            funcs.update_event_log('Channel amplitudes could not be set!', _VARS, app)

    elif event in ['CH_0_PHA_Enter', 'CH_1_PHA_Enter', 'CH_2_PHA_Enter', 'CH_3_PHA_Enter']:
        channel = int(event[3])
        value = float(values[event[:8]])

        app.dds.set_output(channel, value=value, var='phase', io_update=True)

        if 0.99*value < app.dds.read_phase(channel) < 1.01*value:
            update_vars('DDS_SETTINGS', 'channelPhases', value, channel)
            funcs.update_event_log('Channel {} phase is set to {}.'.format(channel, value), _VARS, app)
        else:
            funcs.update_event_log('Channel phases could not be set!', _VARS, app)

    elif event in ['RF_Enter', 'IF_Enter']:
        funcs.set_rf_if(r_f=float(values['RF']), i_f=float(values['IF']), dds=app.dds)

        check_0 = 0.99*(float(values['RF'])*1e6 + float(values['IF'])*1e3) < app.dds.read_frequency(0) < 1.01*(float(values['RF'])*1e6 + float(values['IF'])*1e3)
        check_1 = 0.99*(float(values['RF'])*1e6 + float(values['IF'])*1e3) < app.dds.read_frequency(1) < 1.01*(float(values['RF'])*1e6 + float(values['IF'])*1e3)
        check_2 = 0.99*(float(values['RF'])*1e6) < app.dds.read_frequency(2) < 1.01*(float(values['RF'])*1e6 + float(values['IF'])*1e3)
        check_3 = 0.99*(float(values['RF'])*1e6) < app.dds.read_frequency(3) < 1.01*(float(values['RF'])*1e6 + float(values['IF'])*1e3)

        if check_0 and check_1 and check_2 and check_3:
            update_vars('DDS_SETTINGS', 'RF', values['RF'])
            update_vars('DDS_SETTINGS', 'IF', values['IF'])
            update_vars('DDS_SETTINGS', 'channelFrequencies', [float(values['RF'])*1e6 + float(values['IF'])*1e3,
                                                               float(values['RF'])*1e6 + float(values['IF'])*1e3,
                                                               float(values['RF'])*1e6, float(values['RF'])*1e6])
            funcs.update_event_log('RF and IF frequencies are set to {} MHz and {} kHz.'.format(
                DDS_SETTINGS['RF'], DDS_SETTINGS['IF']),
                _VARS, app)
        else:
            funcs.update_event_log('Channel frequencies could not be set!', _VARS, app)

    elif event in ['CH_0_DIV', 'CH_1_DIV', 'CH_2_DIV', 'CH_3_DIV']:
        channel = int(event[3])
        value = int(values[event])

        app.dds.set_current(channel, value, ioupdate=True)
        update_vars('DDS_SETTINGS', 'channelDividers', value, channel)
        funcs.update_event_log('Channel current dividers are set to {}.'.format(DDS_SETTINGS['channelDividers']),
                               _VARS, app)

    elif event in ['MEAS_NAME', 'MEAS_NUM']:
        update_vars('MEA_SETTINGS', 'measurementFileName',
                    str(Path.joinpath(Path(values['MEAS_LOC']), Path(values['MEAS_DATE']),
                                      Path(values['MEAS_NAME']), Path(values['MEAS_NUM']))))

    elif event == "MEAS_FILE":
        print(MEA_SETTINGS['measurementFileName'])

    elif event == 'PLL_MUL':
        app.dds.set_freqmult(int(values[event]), ioupdate=True)

        if app.dds.get_freqmult() == int(values[event]):
            update_vars('DDS_SETTINGS', 'PLL_MUL', int(values[event]))
            funcs.set_rf_if(_VARS['DDS_SETTINGS']['RF'], _VARS['DDS_SETTINGS']['IF'], app.dds)
            funcs.update_event_log('PLL Multiplier is set to {}.'.format(int(values[event])), _VARS, app)
        else:
            funcs.update_event_log('Could not set PLL multiplier.', _VARS, app)

    elif event == 'DDS_DEFAULTS':
        funcs.load_defaults(app.dds, _VARS, window=app)
        funcs.update_event_log('Default DDS settings are loaded.', _VARS, app)

    elif event in ['ADC_1_RANGE', 'ADC_2_RANGE']:
        new_range = ADC_SETTINGS['range'].index(values[event])
        if new_range >= 5:
            new_range += 3

        channel = int(event[4])
        demodulator = getattr(app, f'Demodulator{channel}')

        adc = getattr(demodulator, f'ADC')
        adc.set_range(new_range)

    elif event in ['ADC_1_RESET', 'ADC_2_RESET']:
        channel = int(event[4])
        demod = getattr(app, f'Demodulator{channel}')
        adc = getattr(demod, f'ADC')
        adc.reset()

    elif event in ['ADC_1_MEAS', 'ADC_2_MEAS']:
        channel = int(event[4])
        demod = getattr(app, f'Demodulator{channel}')
        adc = getattr(demod, f'ADC')

        temp = []
        for i in range(256):
            temp.append(adc.convert())
        result = sum(temp)/len(temp)
        funcs.update_event_log(str(result), _VARS, app)
        # funcs.update_event_log(str(adc.convert()), _VARS, app)

    elif event == 'SW_TIME':
        if not values[event] == '':
            MEA_SETTINGS['laserOnTime'] = int(values[event])*1e-3
        else:
            MEA_SETTINGS['laserOnTime'] = 0
        app.Demodulator1.laser_on_time = MEA_SETTINGS['laserOnTime']
        app.Demodulator2.laser_on_time = MEA_SETTINGS['laserOnTime']
        update_vars('MEA_SETTINGS', 'laserOnTime', MEA_SETTINGS['laserOnTime'])

    elif event == 'MEAS_START':
        app['SW_TIME'].update(disabled=True)
        app['MEAS_NAME'].update(disabled=True)
        app['MEAS_NUM'].update(disabled=True)
        app['MEAS_DATE'].update(disabled=True)

        MEA_SETTINGS['measurementStarted'] = True
        MEA_SETTINGS['justStarted'] = True

        MEA_SETTINGS['amplitudeMeasurementFile'], MEA_SETTINGS['phaseMeasurementFile'] = funcs.create_base_files(_VARS)

    elif event == 'MEAS_STOP':
        app['SW_TIME'].update(disabled=False)
        app['MEAS_NAME'].update(disabled=False)
        app['MEAS_NUM'].update(disabled=False)
        app['MEAS_DATE'].update(disabled=False)

        MEA_SETTINGS['measurementStarted'] = False
        MEA_SETTINGS['justStarted'] = False

        app.reset_fills()
        app.active_laser_generator.send('restart')
        app.active_demod_generator.send('restart')

    elif event == 'PHA_CALIB_START':
        if values['Demodulator 1']:
            Demodulator = app.Demodulator1
        elif values['Demodulator 2']:
            Demodulator = app.Demodulator2
        else:
            return
        funcs.start_phase_calibration(Demodulator, values)

    elif event == 'AMP_CALIB_START':
        if values['Demodulator 1']:
            Demodulator = app.Demodulator1
        elif values['Demodulator 2']:
            Demodulator = app.Demodulator2
        else:
            return
        funcs.start_amplitude_calibration(Demodulator, values)

    elif event == 'LED_1_ON':
        GPIO.output(10, True)

    elif event == 'LED_1_OFF':
        GPIO.output(10, False)

    elif event == 'LED_2_ON':
        GPIO.output(13, True)

    elif event == 'LED_2_OFF':
        GPIO.output(13, False)

    elif event == 'LED_3_ON':
        GPIO.output(16, True)

    elif event == 'LED_3_OFF':
        GPIO.output(16, False)

    elif event == 'LED_4_ON':
        GPIO.output(15, True)

    elif event == 'LED_4_OFF':
        GPIO.output(15, False)

    elif event == "PHASE_1":
        funcs.set_adc2pha(app.Demodulator1.amp_pha)
    elif event == "AMPLITUDE_1":
        funcs.set_adc2amp(app.Demodulator1.amp_pha)

    elif event == "PHASE_2":
        funcs.set_adc2pha(app.Demodulator2.amp_pha)
    elif event == "AMPLITUDE_2":
        funcs.set_adc2amp(app.Demodulator2.amp_pha)

    if MEA_SETTINGS['measurementStarted']:
        if MEA_SETTINGS['justStarted']:
            app.reset_fills()
            MEA_SETTINGS['justStarted'] = False

            MEA_SETTINGS['activeDemod'] = next(app.active_demod_generator)
            MEA_SETTINGS['activeLaser'] = next(app.active_laser_generator)

        active_laser = MEA_SETTINGS['activeLaser']
        active_demod = MEA_SETTINGS['activeDemod']

        demodulator = getattr(app, f'Demodulator{active_demod+1}')
        app.update_fills(active_laser, active_demod)

        if active_laser == 0 and active_demod == 0:
            _VARS['amplitudes'] = []
            _VARS['phases'] = []

        funcs.turn_on_laser(active_laser)

        _VARS['amplitudes'].append(demodulator.measure_amplitude())
        _VARS['phases'].append(demodulator.measure_phase())

        if funcs.is_end_of_measurement_set(_VARS):
            funcs.save_measurement_set(_VARS)

        MEA_SETTINGS['activeDemod'] = next(app.active_demod_generator)
        if MEA_SETTINGS['activeDemod'] == 0:
            MEA_SETTINGS['activeLaser'] = next(app.active_laser_generator)


def update_vars(setting, key, value, index=None):
    if index is None:
        _VARS[setting][key] = value
    else:
        _VARS[setting][key][index] = value


def fill_ele(ele, canvas, color):
    canvas.TKCanvas.itemconfig(ele, fill=color)


def unfill_ele(ele, canvas):
    canvas.TKCanvas.itemconfig(ele, fill='azure')


class MainApplication(windows.MainWindow):
    def __init__(self):
        windows.MainWindow.__init__(self)

        funcs.initialize_lasers()

        self.dds = funcs.initialize_dds(bus=1, device=0)

        self.ADC1 = ADS8685.ADS8685(bus=0, device=0, reset_pin=PIN_SETTINGS['adc_rst_1'])
        self.ADC1.set_range(0b100)
        self.Demodulator1 = Demodulator.Demodulator(self.ADC1, PIN_SETTINGS['amp_pha_1'],
                                                    MEA_SETTINGS['laserOnTime']*1e-3)

        self.ADC2 = ADS8685.ADS8685(bus=0, device=1, reset_pin=PIN_SETTINGS['adc_rst_2'])
        self.ADC2.set_range(0b100)
        self.Demodulator2 = Demodulator.Demodulator(self.ADC2, PIN_SETTINGS['amp_pha_2'],
                                                    MEA_SETTINGS['laserOnTime']*1e-3)

        self.R0 = self["-GRAPH-"].draw_rectangle((60, 40), (80, 60),
                                                 fill_color='deepskyblue', line_color='darkslateblue')
        self.R1 = self["-GRAPH-"].draw_rectangle((120, 40), (140, 60),
                                                 fill_color='deepskyblue', line_color='darkslateblue')

        self.S0 = self['-GRAPH-'].draw_arc((10, 60), (30, 40), extent=180, start_angle=90,
                                           fill_color='red', arc_color='darkred')
        self.S1 = self['-GRAPH-'].draw_arc((10, 60), (30, 40), extent=180, start_angle=-90,
                                           fill_color='red', arc_color='darkred')
        self.S2 = self['-GRAPH-'].draw_arc((170, 60), (190, 40), extent=180, start_angle=90,
                                           fill_color='red', arc_color='darkred')
        self.S3 = self['-GRAPH-'].draw_arc((170, 60), (190, 40), extent=180, start_angle=-90,
                                           fill_color='red', arc_color='darkred')

        self.reset_fills()

        self.active_laser_generator = funcs.laser_count_generator()
        self.active_demod_generator = funcs.demodulator_count_generator()

        for i in range(4):
            self['CH_{}_AMP'.format(i)].bind('<Return>', '_Enter')
            self['CH_{}_PHA'.format(i)].bind('<Return>', '_Enter')
        self['RF'].bind('<Return>', '_Enter')
        self['IF'].bind('<Return>', '_Enter')

    def fill_element(self, element, color):
        self['-GRAPH-'].TKCanvas.itemconfig(element, fill=color)

    def unfill_element(self, element):
        self['-GRAPH-'].TKCanvas.itemconfig(element, fill='azure')

    def reset_fills(self):
        self.unfill_element(self.R0)
        self.unfill_element(self.R1)
        self.unfill_element(self.S0)
        self.unfill_element(self.S1)
        self.unfill_element(self.S2)
        self.unfill_element(self.S3)

    def update_fills(self, laser, adc):
        self.reset_fills()
        semi = f'S{laser}'
        rect = f'R{adc}'

        self.fill_element(getattr(self, semi), 'deepskyblue')
        self.fill_element(getattr(self, rect), 'deepskyblue')
