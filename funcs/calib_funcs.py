import csv
from pathlib import Path as Path

import pyvisa

from functions import update_event_log, rmtree


def start_phase_calibration(demodulator, val_dict):
    start_freq = int(val_dict['PHA_CALIB_START_PHA'])
    stop_freq = int(val_dict['PHA_CALIB_STOP_PHA'])
    step_freq = int(val_dict['PHA_CALIB_STEP_PHA'])

    start_amp = int(val_dict['PHA_CALIB_START_AMP'])
    stop_amp = int(val_dict['PHA_CALIB_STOP_AMP'])
    step_amp = int(val_dict['PHA_CALIB_STEP_AMP'])

    rm = pyvisa.ResourceManager('@py')
    try:
        sigGen = rm.open_resource('USB0::6833::1601::DG4C141400166::0::INSTR')
    except:
        update_event_log('Could not find RIGOL DG4162', val_dict)
        return

    sigGen.write('SOUR1:APPL:SIN 1e3, 1, 0, 0')
    sigGen.write('SOUR2:APPL:SIN 1e3, 1, 0, 0')

    sigGen.write('OUTP1 ON')
    sigGen.write('OUTP2 ON')
    sigGen.write('SOUR1:PHAS:INIT')

    loc = Path.joinpath(Path(val_dict['MEAS_DATE'], Path('PhaseCalibration')))
    if loc.is_dir():
        rmtree(loc)

        loc.mkdir(parents=True, exist_ok=True)
        loc.chmod(511)

        loc.parent.chmod(511)
    else:
        loc.mkdir(parents=True, exist_ok=True)
        loc.chmod(511)
        loc.parent.chmod(511)

    for freq in range(start_freq, stop_freq + step_freq, step_freq):
        for amplitude1 in range(start_amp, stop_amp + step_amp, step_amp):
            root = 'SOUR1:APPL:SIN '
            t = ', '.join([str(freq*1e3), str(amplitude1*1e-3), '0', '0'])
            cmd = ''.join([root, t])
            sigGen.write(cmd)
            for amplitude2 in range(start_amp, stop_amp + step_amp, step_amp):
                # print(Path(''.join([str(amplitude2), 'mV'])))
                file = Path.joinpath(loc,
                                     Path(''.join([str(freq), 'kHz_',
                                                   str(amplitude1), 'mV_',
                                                   str(amplitude2), 'mV_',
                                                   'phase.csv'])))
                file.touch(mode=511)
                # loc.chmod(511)
                for phase in range(0, 181):
                    root = 'SOUR2:APPL:SIN '
                    t = ', '.join([str(freq*1e3), str(amplitude2*1e-3), '0', str(phase)])
                    cmd = ''.join([root, t])

                    sigGen.write(cmd)
                    sigGen.write('SOUR1:PHAS:INIT')

                    # print(phase, demodulator.measure_phase())
                    # time.sleep(0.1)
                    with open(file, 'a+') as csv_file:
                        writer = csv.writer(csv_file, delimiter=',')
                        writer.writerow([phase, demodulator.measure_phase_voltage()])


def start_amplitude_calibration(demodulator, val_dict):
    start_freq = int(val_dict['AMP_CALIB_START_PHA'])
    stop_freq = int(val_dict['AMP_CALIB_STOP_PHA'])
    step_freq = int(val_dict['AMP_CALIB_STEP_PHA'])

    start_amp = int(val_dict['AMP_CALIB_START_AMP'])
    stop_amp = int(val_dict['AMP_CALIB_STOP_AMP'])
    step_amp = int(val_dict['AMP_CALIB_STEP_AMP'])

    rm = pyvisa.ResourceManager('@py')
    try:
        sigGen = rm.open_resource('USB0::6833::1601::DG4C141400166::0::INSTR')
    except:
        update_event_log('Could not find RIGOL DG4162', val_dict)
        return

    sigGen.write('SOUR1:APPL:SIN 1e3, 1, 0, 0')
    sigGen.write('SOUR2:APPL:SIN 1e3, 1, 0, 0')

    sigGen.write('OUTP1 ON')
    sigGen.write('OUTP2 ON')
    sigGen.write('SOUR1:PHAS:INIT')

    loc = Path.joinpath(Path(val_dict['MEAS_DATE'], Path('AmplitudeCalibration')))
    if loc.is_dir():
        rmtree(loc)

        loc.mkdir(parents=True, exist_ok=True)
        loc.chmod(511)

        loc.parent.chmod(511)
    else:
        loc.mkdir(parents=True, exist_ok=True)
        loc.chmod(511)
        loc.parent.chmod(511)

    for freq in range(start_freq, stop_freq + step_freq, step_freq):
        file = Path.joinpath(loc,
                             Path(''.join([str(freq), 'kHz_',
                                           'amplitude.csv'])))
        file.touch(mode=511)
        for amplitude1 in range(start_amp, stop_amp + step_amp, step_amp):
            root = 'SOUR1:APPL:SIN '
            t = ', '.join([str(freq*1e3), str(amplitude1*1e-3), '0', '0'])
            cmd = ''.join([root, t])
            sigGen.write(cmd)

            root = 'SOUR2:APPL:SIN '
            t = ', '.join([str(freq*1e3), str(amplitude1*1e-3), '0', '0'])
            cmd = ''.join([root, t])
            sigGen.write(cmd)

            with open(file, 'a+') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow([amplitude1, demodulator.measure_amplitude_voltage()])
