import PySimpleGUI as sg
import AD9959
import ADS8685
import datetime
import RPi.GPIO as GPIO
from pathlib import Path
import shutil
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import matplotlib.pyplot as plt
import numpy as np
import threading


def the_thread(window: sg.Window):
    """
    The thread that communicates with the application through the window's events.
    Because the figure creation time is greater than the GUI drawing time, it's safe
    to send a non-regulated stream of events without fear of overrunning the communication queue
    """
    while True:
        fig = _VARS['pltFig']
        buf = draw_figure_threaded(fig)
        _VARS['window'].write_event_value('-THREAD-', buf)  # Data sent is a tuple of thread name and counter


def draw_figure_threaded(figure):
    """
    Draws the previously created "figure" in the supplied Image Element
    :param figure: a Matplotlib figure
    :return: BytesIO object
    """

    plt.close('all')  # erases previously drawn plots
    canv = FigureCanvasAgg(_VARS['pltFigure'])
    buf = io.BytesIO()
    canv.print_figure(buf, format='png')
    if buf is not None:
        buf.seek(0)
        # element.update(data=buf.read())
        return buf
    else:
        return None
        
        
def set_dds_channel_frequency(channel, frequency):
    print('Set Channel {} to {}MHz'.format(channel, frequency))
    
    
def set_dds_channel_amplitude(channel, amplitude):
    print('Set Channel {} to {} Amplitude'.format(channel, amplitude))
  
    
def update_event_log(message):
    t = datetime.datetime.now().strftime('%H:%M:%S')
    
    _VARS['eventLog'].append('{}: '.format(t)+message)
    _VARS['window']['EVE_LOG'].Update('\n'.join(_VARS['eventLog']), autoscroll=True)


def tick(period):
    # ~ t = time.time()
    # ~ while True:
        # ~ t += period
        # ~ yield max(t - time.time(), 0)
    def init():
            return time.time()
    t = init()
    while True:
            val = (yield max(t - time.time(), 0))
            if val == 'restart':
                    t = init()
            else:
                    t += period


def tickPha(period):
    # ~ t = time.time()
    # ~ while True:
        # ~ t += period
        # ~ yield max(t - time.time(), 0)
    def init():
            return time.time()
    t = init()
    while True:
            val = (yield max(t - time.time(), 0))
            if val == 'restart':
                    t = init()
            else:
                    t += period


def tickAmp(period):
    # ~ t = time.time()
    # ~ while True:
        # ~ t += period
        # ~ yield max(t - time.time(), 0)
    def init():
            return time.time()
    t = init()
    while True:
            val = (yield max(t - time.time(), 0))
            if val == 'restart':
                    t = init()
            else:
                    t += period


def switch_lasers(n):    
    n = format(n, '#06b')   # Format the number to 3 bits
    
    # Set the pins to switch the lasers
    GPIO.output(A_Pin, int(n[-1]))
    GPIO.output(B_Pin, int(n[-2]))
    GPIO.output(C_Pin, int(n[-3]))
    

def laser_count_generator():
        def init():
                return 0
        
        num = init()
        while True:
                val = (yield num % 8)
                if val=='restart':
                        i = init()
                else:
                        num += 1


def configure_savefile_location():
        measurementFolder = Path.joinpath(
                Path(_VARS['measurementRoot']),
                Path(_VARS['measurementDate']), 
                Path(_VARS['measurementName']),
                Path(_VARS['measurementNumber'])
                )
        
        measurementFolder.mkdir(parents=True, exist_ok=True)
        
        phaseMeasurementFile = Path.joinpath(measurementFolder, 'phaseMeasurement.txt')
        if phaseMeasurementFile.exists():
                phaseMeasurementFile.unlink()
        phaseMeasurementFile.touch(exist_ok=True)
        
        amplitudeMeasurementFile = Path.joinpath(measurementFolder, 'amplitudeMeasurement.txt')
        if amplitudeMeasurementFile.exists():
                amplitudeMeasurementFile.unlink()
        amplitudeMeasurementFile.touch(exist_ok=True)
        
        phaseMeasurementFile.chmod(0o777)
        shutil.chown(phaseMeasurementFile, group = 'pi')
        shutil.chown(phaseMeasurementFile, user = 'pi')

        amplitudeMeasurementFile.chmod(0o777)
        shutil.chown(amplitudeMeasurementFile, group = 'pi')
        shutil.chown(amplitudeMeasurementFile, user = 'pi')
        
        _VARS['phaseMeasurementFile'] = phaseMeasurementFile
        _VARS['amplitudeMeasurementFile'] = amplitudeMeasurementFile
        
        update_event_log('Phase measurement location:     {}'.format(_VARS['phaseMeasurementFile']))
        update_event_log('Amplitude measurement location: {}'.format(_VARS['amplitudeMeasurementFile']))
                

def configure_dds(bus, device, io_update, rst, pwr_dwn, IF=1e3, RF=83e6):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pwr_dwn, GPIO.OUT)
    GPIO.output(pwr_dwn, False)
    
    dds = AD9959.AD9959(bus, device, IO_UPDATE_PIN=io_update, RST_PIN=rst, PWR_DWN_PIN = pwr_dwn)
    # ~ dds.init_dds()

    dds.set_freqmult(20, ioupdate=True)

    dds.set_output(0, RF+IF, 'frequency', io_update=True)
    dds.set_output(0, 1.0,  'amplitude', io_update=True)

    dds.set_output(1, RF+IF, 'frequency', io_update=True)
    dds.set_output(1, 0.2, 'amplitude', io_update=True)

    dds.set_output(2, RF, 'frequency', io_update=True)
    dds.set_output(2, 1, 'amplitude', io_update=True)
    dds.set_current(2, 1, ioupdate=True)


    dds.set_output(3, RF, 'frequency', io_update=True)
    dds.set_output(3, 1, 'amplitude', io_update=True)
    dds.set_current(1, 1, ioupdate=True)
    dds.set_output(3, 0, 'phase', io_update=True)
    
    
    
    # ~ dds._write('FR2', [0xA0, 0x00])
    # ~ dds._io_update()
    for ch in range(4):
        dds.set_current(ch, int(_VARS['ddsChannelDividers'][ch]), ioupdate=True)
                    
    return dds


def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg


def draw_subplot(update=False):
        _VARS['pltFig'], _VARS['pltAxes'] = plt.subplots(figsize=(8, 4))
                
        _VARS['pltAxes'].set_xlim([0, 8*_VARS['switchingPeriod']])
        _VARS['pltAxes'].set_ylim([0, 5])

        c = ['k', 'r', 'k', 'r', 'k', 'r', 'k', 'r',]
        for i in range(8):
                _VARS['pltAxes'].axhline(y=2.5 + i/10*_VARS['dataPoints'], xmin=i*0.125, xmax=(i+1)*0.125, c = c[i])
                _VARS['pltAxes'].axhline(y=2.5 - i/10*_VARS['dataPoints'], xmin=i*0.125, xmax=(i+1)*0.125, c = c[i])
        plt.grid()
        plt.tight_layout()
        
        _VARS['figAgg'] = draw_figure(_VARS['window']['MEAS_CANV'].TKCanvas, _VARS['pltFig'])
        _VARS['backgrounds'] = _VARS['pltFig'].canvas.copy_from_bbox(_VARS['pltAxes'].bbox)


def update_subplot():
        fig, ax = _VARS['pltFig'], _VARS['pltAxes']
        # ~ _VARS['figAgg'].get_tk_widget().forget()
        _VARS['pltAxes'].clear()
        
        ax.set_xlim([0, 8*_VARS['switchingPeriod']])
        ax.set_ylim([0, 5])
        c = ['k', 'r', 'k', 'r', 'k', 'r', 'k', 'r',]
        for i in range(8):
                _VARS['pltAxes'].draw_artist
                # ~ _VARS['pltAxes'].axhline(y=2.5 + _VARS['pltAmp'][i], xmin=i*_VARS['switchingPeriod'], xmax=(i+1)*_VARS['switchingPeriod'], c = c[i])
                # ~ _VARS['pltAxes'].axhline(y=2.5 - _VARS['pltAmp'][i], xmin=i*_VARS['switchingPeriod'], xmax=(i+1)*_VARS['switchingPeriod'], c = c[i])
                
                ax.axhline(y=2.5 + _VARS['pltAmp'][i], xmin=i*0.125, xmax=(i+1)*0.125, c = c[i])
                ax.axhline(y=2.5 - _VARS['pltAmp'][i], xmin=i*0.125, xmax=(i+1)*0.125, c = c[i])

        plt.grid()
        plt.tight_layout()
        _VARS['figAgg'].draw()
        # ~ _VARS['figAgg'] = draw_figure(_VARS['window']['MEAS_CANV'].TKCanvas, _VARS['pltFig'])
        
        
        
def event_values(event, values):
        GPIO.setmode(GPIO.BOARD)
        
        # Gracefully close the GUI
        if event == sg.WIN_CLOSED:
            return -1
         
        # Measurement Save File Root
        elif event == 'MEAS_ROOT':  
                try:
                        _VARS['measurementRoot'] = values['MEAS_ROOT']
                except:
                        update_event_log('Save file location could not be set!')

        # Measurement Name
        elif event == 'MEAS_NAME':
                try:
                        _VARS['measurementName'] = values['MEAS_NAME']
                except:
                        update_event_log('Could not set Measurement Name!')
        
        # Measurement Number
        elif event == 'MEAS_NUM':
                try:
                        _VARS['measurementNumber'] = values['MEAS_NUM']
                except:
                        update_event_log('Could not set Measurement Number!')
        
        # Turn on/off the DDS
        elif event == 'DDS_PDWN':
                try:
                        GPIO.output(dds.PWR_DWN_PIN, values[event])
                        _VARS['window']['DDS_PDWN'].Update(disabled=True)
                        if values[event]:
                                update_event_log('DDS ON.')
                                for ch in range(4):
                                    dds._set_channels(ch)
                                    # ~ print('CFR BITS')
                                    asd = dds._read('CFR')
                                    # ~ print(cfr_bytes)
                                    asd[2] = 0x14
                                    dds._write('CFR', asd)
                                    dds._io_update()
                                dds._write('FR2', [0xA0, 0])
                                dds._io_update()

                                _VARS['window']['DDS_PDWN'].Update(disabled=False)
                        else:
                                update_event_log('DDS OFF.')

                                _VARS['window']['DDS_PDWN'].Update(disabled=False)
                except:
                        update_event_log('Something when wrong while turning ON of OFF the DDS!')
        
        # Set RF and IF Frequencies
        elif event == 'DDS_SET_FREQ':   
                try:
                    _VARS['RF'] = values['RF']
                    _VARS['IF'] = values['IF']
                    
                    RF = float(_VARS['RF'])*1e6
                    IF = float(_VARS['IF'])*1e3
                    # ~ set_dds_channel_frequency(0, RF+IF)
                    
                    dds.set_output(0, RF+IF, 'frequency', io_update=True)
                    dds.set_output(1, RF+IF, 'frequency', io_update=True)
                    dds.set_output(2, RF, 'frequency', io_update=True)
                    dds.set_output(3, RF, 'frequency', io_update=True)
                    update_event_log('Channel frequencies are set.')
                    for ch in range(4):
                        dds.set_current(ch, int(_VARS['ddsChannelDividers'][ch]), ioupdate=True)
                    
                except:
                    update_event_log('Could not set DDS Channel Frequencies!')

        # Turn on/off individual DDS Channels
        elif event in ['CH_0_EN', 'CH_1_EN', 'CH_2_EN', 'CH_3_EN']:
                ch = int(event[3])
                try:
                    _VARS['ddsActiveChannels'][ch] = values[event]
                    allEnabled = bool(values['CH_0_EN'] and values['CH_1_EN'] and values['CH_2_EN'] and values['CH_3_EN'])
                    _VARS['window']['CH_ALL_EN'].Update(value=allEnabled)
                    if values[event]:
                        update_event_log('Channel {} is turned on.'.format(ch))
                    elif not values[event]:
                        update_event_log('Channel {} is turned off.'.format(ch))
                    else:
                        update_event_log('Weird state for Channel {}'.format(ch))
                except:
                    update_event_log('Could not set the state of Channel {}!'.format(ch))
            
        # Turn on/all All DDS Channels
        elif event == 'CH_ALL_EN':
                try:
                    for ch in range(4):
                        _VARS['ddsActiveChannels'][ch] = values[event]
                        _VARS['window']['CH_{}_EN'.format(ch)]. Update (value = values[event])
                    if values[event]:
                        update_event_log('All channels are enabled.')
                    else:
                        update_event_log('All channels are disabled.')
                
                except:
                    update_event_log('Could not enable all channels!.')

        # Set DDS Channel Amplitudes
        elif event == 'DDS_SET_AMP':
                try:
                    for ch in range(4):
                        assert 0 <= float(values['CH_{}_AMP'.format(ch)]) <= 1.0
                        _VARS['ddsChannelAmplitudes'][ch] = float(values['CH_{}_AMP'.format(ch)])
                        dds.set_output(ch, float(values['CH_{}_AMP'.format(ch)]),  'amplitude', io_update=True)
                    update_event_log('Amplitudes for all channels are set.')                    
                    for ch in range(4):
                        dds.set_current(ch, int(_VARS['ddsChannelDividers'][ch]), ioupdate=True)
                except:
                    update_event_log('Could not set Channel Amplitudes!')
            
        # Set DDS Channel Dividers
        elif event in ['CH_0_DIV', 'CH_1_DIV', 'CH_2_DIV', 'CH_3_DIV']:
                ch = int(event[3])        
                try:
                    _VARS['ddsChannelDividers'][ch] = float(values[event])
                    dds.set_current(ch, int(values[event]), ioupdate=True)
                    update_event_log('CH {} Divider set to {}.'.format(ch, values[event]))
                except:
                    update_event_log('Could not set Ch {} Divider!'.format(ch))
                    print('Could not set Channel Dividers!')
        
        # Set DDS Channel Phases                
        elif event == 'DDS_SET_PHA':
                try:
                    for ch in range(4):
                        assert 0 <= float(values['CH_{}_PHA'.format(ch)]) <= 360
                        _VARS['ddsChannelPhases'][ch] = float(values['CH_{}_PHA'.format(ch)])
                        dds.set_output(ch, float(values['CH_{}_PHA'.format(ch)]), 'phase', io_update=True)
                    update_event_log('Phases for all channels are set.')
                    for ch in range(4):
                        dds.set_current(ch, int(_VARS['ddsChannelDividers'][ch]), ioupdate=True)
                    
                except:
                    update_event_log('Could not set Channel Phases!')
        
        # Active Laser Indicator
        elif event in ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8']:
                laser = int(event[1])-1
                try:
                    for i, l in enumerate(_VARS['activeLaser']):
                        _VARS['activeLaser'][i] = False
                        
                    _VARS['activeLaser'][laser] = True
                    switch_lasers(laser)
                    
                    update_event_log('Laser #{} turned on.'.format(laser+1))
                except:
                    update_event_log('Something went wrong with switching lasers!')
            
        # Test button to increment lasers -- Do not use
        elif event == 'TestButton':
                laser = _VARS['activeLaser'].index(True)
                for i, l in enumerate(_VARS['activeLaser']):
                    _VARS['activeLaser'][i] = False
                _VARS['activeLaser'][laser+1] = True
                _VARS['window']['L'+str(laser+2)].Update(value=True)

        # Start the measurement
        elif event == 'MEAS_START':
                _VARS['startMeasurement'] = True
                _VARS['window']['SWI_PER'].Update(disabled=True)
                _VARS['window']['MEAS_NAME'].Update(disabled=True)
                _VARS['window']['MEAS_NUM'].Update(disabled=True)
                
                
                configure_savefile_location()
                print(_VARS['phaseMeasurementFile'])
                print(_VARS['amplitudeMeasurementFile'])
                # ~ _VARS['phaseMeasurementFile'] = phaseMeasurementFile
                # ~ _VARS['amplitudeMeasurementFile'] = amplitudeMeasurementFile
                
                update_event_log('Measurement started.')
        
        # Stop the measurement        
        elif event == 'MEAS_STOP':
                _VARS['startMeasurement'] = False
                _VARS['window']['SWI_PER'].Update(disabled=False)
                _VARS['window']['MEAS_NAME'].Update(disabled=False)
                _VARS['window']['MEAS_NUM'].Update(disabled=False)
                
                _VARS['dataPoints'] = 0
                _VARS['window']['MEAS_PTS'].update(value=_VARS['dataPoints'])
                
                n.send('restart')
                # ~ g.send('restart')
                # ~ p.send('restart')
                # ~ a.send('restart')
                
                update_event_log('Measurement stopped.')
                            
        
        elif event == 'MEAS_RESTART':
            try:
                    pass
            except:
                    pass
                
        # Pause/Unpause the measurement
        elif event == 'MEAS_PAUS':
                try:
                    _VARS['measurementPaused'] = not _VARS['measurementPaused']
                    if _VARS['measurementPaused']:
                        update_event_log('Measurement paused.')
                    else:
                        update_event_log('Measurement unpaused.')
                except:
                    update_event_log('Could not (un)paused!')
            
        # Adjust the On Time for each laser
        elif event == 'SWI_PER':
                _VARS['switchingPeriod'] = float(values[event])*1e-3
                update_event_log('Switching period is set to {}ms.'.format(values[event]))
        
        
        elif event == 'MEAS_PTS':
                values[event] += 1
                values[event].Update()
        
        elif event == "PRNT_V":
            GPIO.output(Ph_Amp_Pin, True)
            time.sleep(0.5)
            update_event_log('Amplitude Meas: {}'.format(adc.convert()/0.209))
            
            GPIO.output(Ph_Amp_Pin, False)
            time.sleep(0.5)
            update_event_log('Phase Meas: {}'.format(adc.convert()))
            update_event_log('Phase Meas: {}'.format(adc.convert()))
            update_event_log('Phase Meas: {}'.format(adc.convert()))
            update_event_log('Phase Meas: {}'.format(adc.convert()))
            update_event_log('Phase Meas: {}'.format(adc.convert()))
        
        # Main measurement and Converting loop
        if (_VARS['startMeasurement']) and (not _VARS['measurementPaused']):
            if not _VARS['measurementPaused']:
                try:    # try to switch the lasers as usual and save the ADC readings
                    # ~ period = _VARS['switchingPeriod']  # On time for each laser
                    time.sleep(next(g))
                    laserNumber = next(n)
                    switch_lasers(laserNumber)
                    
                    if laserNumber == 0:
                        dds.set_output(0, 210, 'phase', io_update=True)
                    elif laserNumber == 4:
                        dds.set_output(0, 180, 'phase', io_update=True)    
                    for ch in range(4):
                        dds.set_current(ch, int(_VARS['ddsChannelDividers'][ch]), ioupdate=True)
                    
                    # Update the Radio elements
                    for i, l in enumerate(_VARS['activeLaser']):
                        _VARS['activeLaser'][i] = False
                    _VARS['activeLaser'][laserNumber] = True
                    _VARS['window']['L'+str(laserNumber+1)].Update(value=True)
    
                    # Start the Phase measurement
                    GPIO.output(Ph_Amp_Pin, False)
                    time.sleep(_VARS['switchingPeriod']*0.5) # Wait for the LPF to settle
                    _VARS['measPha'][laserNumber] = str(adc.convert())
        
                    # Start the Amplitude measurement
                    GPIO.output(Ph_Amp_Pin, True)
                    time.sleep(_VARS['switchingPeriod']*0.5) # Wait for the LPF to settle
                    # ~ _VARS['measAmp'][laserNumber] = str(adc.convert())
                    
                    _VARS['measAmp'][laserNumber] = str((adc.convert()-0.003808) / 0.209747)
                    _VARS['pltAmp'][laserNumber] = float(_VARS['measAmp'][laserNumber])

                    if laserNumber == 7:
                        with Path(_VARS['phaseMeasurementFile']).open('a+') as f:
                            for i, v in enumerate(_VARS['measPha']):
                                if i == 0:
                                    f.write('\n' + str(v))
                                else:
                                    f.write(', ' + str(v))
                            
                        with Path(_VARS['amplitudeMeasurementFile']).open('a+') as f:
                            for i , v in enumerate(_VARS['measAmp']):
                                if i == 0:
                                    f.write('\n' + str(v))
                                else:
                                    f.write(', ' + str(v))
                            
                        _VARS['window']['MEAS_PTS'].Update(value=_VARS['dataPoints'] + 1)
                        _VARS['dataPoints'] += 1

                        update_subplot()
                        
                except:
                    update_event_log('Something went wrong while switching or converting!')



class dds_tab(sg.Tab):
        def __init__(self, *args, **kwargs):
                
                _DDS_DES_COL = sg.Column([
                        [sg.Text('DDS Frequencies', size=(25, None))],
                        [sg.Text('DDS Channel Amplitudes', size=(25, None))],
                        [sg.Text('DDS Channel Dividers', size=(25, None))],
                        [sg.Text('DDS Channel Phases', size=(25, None))]
                        ])

                _DDS_FRE_ROW = [
                        sg.Text('RF (MHz)', size=(8, None), pad=5),
                        sg.InputText(default_text=_VARS['RF'], size=(3, None), pad=5, key='RF'),
                        sg.Text('IF (kHz)', size=(8, None), pad=5),
                        sg.InputText(default_text=_VARS['IF'], size=(3, None), pad=5, key='IF')
                        ]

                _DDS_BUT_COL = sg.Column([
                        [sg.Button('Set Frequencies', size=(20, None), enable_events=True, key='DDS_SET_FREQ')],
                        [sg.Button('Set Amplitudes', size=(20, None), enable_events=True, key='DDS_SET_AMP')],
                        [sg.Text('')],
                        [sg.Button('Set Phases', size=(20, None), enable_events=True, key='DDS_SET_PHA')]
                        ])
                        
                _DDS_CHN_COL_0 = sg.Column([
                    [sg.Text('Ch 0'), sg.InputText(size=(5, None), enable_events=True, default_text=_VARS['ddsChannelAmplitudes'][0], key='CH_0_AMP')],
                    [sg.Text('Ch 0'), sg.Combo([1, 2, 4, 8], default_value=_VARS['ddsChannelDividers'][0], size=(5, None), enable_events=True, key='CH_0_DIV')],
                    [sg.Text('Ch 0'), sg.InputText(size=(5, None), enable_events=False, default_text=_VARS['ddsChannelPhases'][0], key='CH_0_PHA')]
                    ])
                _DDS_CHN_COL_1 = sg.Column([
                    [sg.Text('Ch 1'), sg.InputText(size=(5, None), enable_events=True, default_text=_VARS['ddsChannelAmplitudes'][1], key='CH_1_AMP')],
                    [sg.Text('Ch 1'), sg.Combo([1, 2, 4, 8], default_value=_VARS['ddsChannelDividers'][1], size=(5, None), enable_events=True, key='CH_1_DIV')],
                    [sg.Text('Ch 1'), sg.InputText(size=(5, None), enable_events=False, default_text=_VARS['ddsChannelPhases'][1], key='CH_1_PHA')]
                    ])
                _DDS_CHN_COL_2 = sg.Column([
                    [sg.Text('Ch 2'), sg.InputText(size=(5, None), enable_events=True, default_text=_VARS['ddsChannelAmplitudes'][2], key='CH_2_AMP')],
                    [sg.Text('Ch 2'), sg.Combo([1, 2, 4, 8], default_value=_VARS['ddsChannelDividers'][2], size=(5, None), enable_events=True, key='CH_2_DIV')],
                    [sg.Text('Ch 2'), sg.InputText(size=(5, None), enable_events=False, default_text=_VARS['ddsChannelPhases'][2], key='CH_2_PHA')]
                    ])
                _DDS_CHN_COL_3 = sg.Column([
                    [sg.Text('Ch 3'), sg.InputText(size=(5, None), enable_events=True, default_text=_VARS['ddsChannelAmplitudes'][3], key='CH_3_AMP')],
                    [sg.Text('Ch 3'), sg.Combo([1, 2, 4, 8], default_value=_VARS['ddsChannelDividers'][3], size=(5, None), enable_events=True, key='CH_3_DIV')],
                    [sg.Text('Ch 3'), sg.InputText(size=(5, None), enable_events=False, default_text=_VARS['ddsChannelPhases'][3], key='CH_3_PHA')]
                    ])

                _DDS_CHN_COL =  sg.Column([
                        _DDS_FRE_ROW, 
                        [_DDS_CHN_COL_0,
                        _DDS_CHN_COL_1,
                        _DDS_CHN_COL_2,
                        _DDS_CHN_COL_3]
                        ])
        
                _DDS_PDR_COL = sg.Column([
                        [sg.Checkbox('DDS Power Down', default=False, enable_events=True, key='DDS_PDWN')],
                        ])
                
                self.win_layout = [[_DDS_DES_COL, _DDS_CHN_COL, _DDS_BUT_COL, _DDS_PDR_COL]]
                sg.Tab.__init__(self, title='DDS Details', layout=self.win_layout)
 
                
class measurement_tab(sg.Tab):
        def __init__(self, *args, **kwargs):
                _MEA_ROW = [
                        [sg.Button('Start', key='MEAS_START') 
                        ,sg.Button('Stop', key='MEAS_STOP') 
                        ,sg.Button('Pause/Unpause', key='MEAS_PAUS') 
                        ,sg.Button('Restart', key='MEAS_RESTART')
                        ,sg.Text('Period (ms)')
                        ,sg.InputText(default_text=str(float(_VARS['switchingPeriod'])*1000), size=(5, 1), enable_events=True, key='SWI_PER')
                        ,sg.Text('# of Data Points:')
                        ,sg.Text(_VARS['dataPoints'], size=(3, 1), key='MEAS_PTS')],
                    
                        [sg.Text('Amplitude and Phase Results Save Location', size=(20, None))
                        ,sg.Input(size=(50, 1), enable_events=True, key='MEAS_ROOT', change_submits=True)
                        ,sg.FolderBrowse()
                        ,sg.Text('Measurement Name')
                        ,sg.InputText(size=(10, None), enable_events=True, key='MEAS_NAME')
                        ,sg.Text('Measurement Num')
                        ,sg.InputText(size=(3, None), enable_events=True, key='MEAS_NUM')],
                        
                        [sg.Button('Change Settings (Does Nothing!!)', enable_events=True, key="PRNT_V")],
                        [sg.Text('Measurement Date')
                        ,sg.InputText(default_text = datetime.datetime.now().strftime('%d-%B-%Y'), key='MEAS_DATE')],
                        ]

                self.win_layout = _MEA_ROW
                sg.Tab.__init__(self, title='Measurement Details', layout = self.win_layout)
                        

class log(sg.Frame):
        def __init__(self, *args, **kwargs):
                self.win_layout = [[
                        sg.Multiline(disabled=True, key='EVE_LOG', size=(400,25), enable_events=True)
                        ]]
                sg.Frame.__init__(self, title = 'Event Log', layout = self.win_layout)


class laser_indicator(sg.Frame):
        def __init__(self, *args, **kwargs):
                self.win_layout = [
                    [sg.Text('Active Laser:')
                    ,sg.Radio('#1', 'LASERS', enable_events=True, key='L1')
                    ,sg.Radio('#2', 'LASERS', enable_events=True, key='L2')
                    ,sg.Radio('#3', 'LASERS', enable_events=True, key='L3')
                    ,sg.Radio('#4', 'LASERS', enable_events=True, key='L4')
                    ,sg.Radio('#5', 'LASERS', enable_events=True, key='L5')
                    ,sg.Radio('#6', 'LASERS', enable_events=True, key='L6')
                    ,sg.Radio('#7', 'LASERS', enable_events=True, key='L7')
                    ,sg.Radio('#8', 'LASERS', enable_events=True, key='L8')],
                    
                    [sg.Button('Incerement', enable_events=True, key='TestButton')]]
                    
                sg.Frame.__init__(self, title='', layout = self.win_layout)
                        

class measurement_signals(sg.Frame):
        def __init__(self, *args, **kwargs):
                self.win_layout = [
                [sg.Canvas(size = (800, 400), key='MEAS_CANV')]
                ]
                
                sg.Frame.__init__(self, title='Measurement Signals', layout=self.win_layout)


class main_window(sg.Window):
        
        def __init__(self, *args, **kwargs):
                self.win_title = 'Main Window'
                self.win_size = (1050, 800)
                self.win_layout = [[sg.TabGroup([[measurement_tab()], [dds_tab()], ])], 
                                        [laser_indicator()], [measurement_signals()], [log()]]
                sg.Window.__init__(self, title=self.win_title, layout=self.win_layout, size=self.win_size, resizable=True, finalize=True)
                

sg.theme ('DarkGrey 13')


_VARS = {
    'window': False,
    'figAgg': False,
    'pltFig': False,
    'pltAmp': [0, 0, 0, 0, 0, 0, 0, 0],
    'measAmp': [0, 0, 0, 0, 0, 0, 0, 0],
    'measPha': [0, 0, 0, 0, 0, 0, 0, 0],
    'RF': 90,
    'IF': 1,
    'ddsActiveChannels': [0, 0, 0, 0],
    'ddsChannelAmplitudes': [0.2, 0.4, 1.0, 1.0],      
    'ddsChannelDividers': [4, 1, 1, 1],
    'ddsChannelPhases': [120, 0, 0, 0],
    'ddsPowerDown': False,
    'eventLog': [],
    'activeLaser': [False, False, False, False, False, False, False, False],
    'startMeasurement': False,
    'measurementPaused': False,
    'switchingPeriod': 300e-3,
    'dataPoints': 0,
    'measurementDate': datetime.datetime.now().strftime('%d-%B-%Y'),
    'measurementRoot': '',
    'measurementName': '',
    'measurementNumber': '',
    'measurementLocation': '',
    'phaseMeasurementFile': '',
    'amplitudeMeasurementFile': '',
    }


GPIO.setmode(GPIO.BOARD)
# Select the control pins for the Decoder
A_Pin = 31
B_Pin = 33
C_Pin = 37
GPIO.setup(A_Pin, GPIO.OUT)
GPIO.setup(B_Pin, GPIO.OUT)
GPIO.setup(C_Pin, GPIO.OUT)

# Select the Phase/Amplitude Measurement Control pin
Ph_Amp_Pin = 7
GPIO.setup(Ph_Amp_Pin, GPIO.OUT)
GPIO.output(Ph_Amp_Pin, False) # True for Amplitude measurement of Sig A, False for phase measurement

# Initialize and set the range of ADC
adc = ADS8685.ADS8685(bus=1, device=2, RST_PIN=32)
adc.set_range(4)

# Initialize and set the channels of DDS
dds = configure_dds(bus=0, device=0, pwr_dwn = 22, IF=1e3, RF=83e6, io_update=29, rst=13)

# Set up timings
g = tick(_VARS['switchingPeriod'])
n = laser_count_generator()





