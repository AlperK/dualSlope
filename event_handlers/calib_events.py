import pyvisa
from functions import update_event_log
import time
from pathlib import Path
import ui.measurement


def calibration_events(app, event, values):
    if event == "__CAL_SIGGENCON__":
        app.sigGen = try_to_connect_to_device('USB0::6833::1601::DG4C141400166::0::INSTR',
                                 app=app)
    elif event == "__CAL_START_AMP_SWEEP__":
        # print(values['AMP_SWE_STA'])
        start_amplitude_sweep(app, event, values, app.sigGen)
    elif event == "__CAL_START_PHA_SWEEP__":
        start_phase_sweep(app, event, values, app.sigGen)
    elif event in ["__CAL_DEM__1", "__CAL_DEM__2"]:
        # channel = int(event[-3])
        demodulator = get_active_demodulator(app, event, values)
        
    
def try_to_connect_to_device(USB_ID, app):
    rm = pyvisa.ResourceManager('@py')
    try:
        # sigGen = rm.open_resource('USB0::6833::1601::DG4C141400166::0::INSTR')
        sigGen = rm.open_resource(USB_ID)
        app['__LOG__'].update('Connected to Rigol DG4162.\n', 
                              append=True)
        return sigGen
    except:
        app['__LOG__'].update(f'Could not connect to Rigol DG4162.\n',
                              append=True)
        return
   
    
def start_amplitude_sweep(app, event, values, sigGen):
    demodulator = get_active_demodulator(app, event, values)
    base_folder = ui.measurement.prepare_measurement_folder()
    
    calibration_folder = Path(base_folder, 
                              str(demodulator))
    calibration_folder.mkdir(parents=True, exist_ok=True)
    
    amp_sweep_start = int(values['AMP_SWE_STA'])
    amp_sweep_stop = int(values['AMP_SWE_STO'])
    amp_sweep_step = int(values['AMP_SWE_STE'])
    amp_sweep_range = range(amp_sweep_start, amp_sweep_stop, amp_sweep_step)
    
    
    fre_sweep_start = int(values['FRE_SWE_STA']) * 1000
    fre_sweep_stop = int(values['FRE_SWE_STO']) * 1000
    fre_sweep_step = int(values['FRE_SWE_STE']) * 1000
    fre_sweep_range = range(fre_sweep_start, fre_sweep_stop, fre_sweep_step)
    
    
    pha_sweep_start = int(values['PHA_SWE_STA'])
    pha_sweep_stop = int(values['PHA_SWE_STO'])
    pha_sweep_step = int(values['PHA_SWE_STE'])
    pha_sweep_range = range(pha_sweep_start, pha_sweep_stop, pha_sweep_step)
    
    
    app['__LOG__'].update(f"Amp sweep values: {amp_sweep_range}.\n",
                      append=True)
    app['__LOG__'].update(f"Fre sweep values: {fre_sweep_range}.\n",
                      append=True)
    
    sigGen.write("OUTP1 ON")
    sigGen.write("OUTP2 ON")
    for frequency in fre_sweep_range:
        file_path = Path.joinpath(calibration_folder,
                                        Path(f"{frequency}kHz.txt"))
        file_path.touch()
        
        for amplitude in amp_sweep_range:
            with open(str(file_path), 'a+') as f:
                source1_command = f"SOUR1:APPL:SIN {frequency}, {amplitude / 1000}, 0, 0"
                source2_command = f"SOUR2:APPL:SIN {frequency}, {amplitude / 1000}, 0, 0"
                
                sigGen.write(source1_command)
                sigGen.write(source2_command)
                
                sigGen.write('SOUR1:PHAS:INIT')
                
                time.sleep(0.1)
                f.write(f"{amplitude} {demodulator.measure_amplitude(raw=True)}\n")
    sigGen.write("OUTP1 OFF")
    sigGen.write("OUTP1 OFF")


def start_phase_sweep(app, event, values, sigGen):
    demodulator = get_active_demodulator(app, event, values)
    base_folder = ui.measurement.prepare_measurement_folder()
    
    calibration_folder = Path(base_folder, 
                              str(demodulator),
                              "Phase Calibration")
    calibration_folder.mkdir(parents=True, exist_ok=True)
    
    amp_sweep_start = int(values['AMP_SWE_STA'])
    amp_sweep_stop = int(values['AMP_SWE_STO'])
    amp_sweep_step = int(values['AMP_SWE_STE'])
    amp_sweep_range = range(amp_sweep_start, amp_sweep_stop, amp_sweep_step)
    
    
    fre_sweep_start = int(values['FRE_SWE_STA']) * 1000
    fre_sweep_stop = int(values['FRE_SWE_STO']) * 1000
    fre_sweep_step = int(values['FRE_SWE_STE']) * 1000
    fre_sweep_range = range(fre_sweep_start, fre_sweep_stop, fre_sweep_step)
    
    
    pha_sweep_start = int(values['PHA_SWE_STA'])
    pha_sweep_stop = int(values['PHA_SWE_STO'])
    pha_sweep_step = int(values['PHA_SWE_STE'])
    pha_sweep_range = range(pha_sweep_start, pha_sweep_stop, pha_sweep_step)
    
    sigGen.write("OUTP1 ON")
    sigGen.write("OUTP2 ON")
    
    for frequency in fre_sweep_range:
        
        for amplitude1 in amp_sweep_range:
            source1_command = f"SOUR1:APPL:SIN {frequency}, {amplitude1 / 1000}, 0, 0"
            sigGen.write(source1_command)
            time.sleep(0.1)
            
            for amplitude2 in amp_sweep_range:
                source2_command = f"SOUR2:APPL:SIN {frequency}, {amplitude2 / 1000}, 0, 0"
                sigGen.write(source2_command)
                time.sleep(0.1)
                
                for phase in pha_sweep_range:
                    file_path = Path.joinpath(calibration_folder,
                                              Path(f"{frequency}kHz_{amplitude1}mV_{amplitude2}mV.txt"))
                    file_path.touch(exist_ok=True)
                    with open(file_path, 'a+') as f:
                        source2_command = f"SOUR2:APPL:SIN {frequency}, {amplitude2 / 1000}, 0, {phase}"
                        sigGen.write(source2_command)
                        
                        sigGen.write('SOUR1:PHAS:INIT')
                        
                        time.sleep(0.1)
                        f.write(f"{phase} {demodulator.measure_phase(raw=True)}\n")
    sigGen.write("OUTP1 OFF")
    sigGen.write("OUTP2 OFF")
    
    
def get_active_demodulator(app, values, event):
    if app["__CAL_DEM__1"].get():
        return getattr(app, f"demodulator1")
    else:
        return getattr(app, f"demodulator2")
    
    print(app["__CAL_DEM__2"].get())
    # print(values['__CAL_DEM__2'])