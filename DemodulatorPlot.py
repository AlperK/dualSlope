import csv
from pathlib import Path as Path
import matplotlib.pyplot as plt


p0 = Path.joinpath(Path('2022-02-01'), Path('PhaseCalibration'), Path('1kHz_1000mV_500mV_phase.csv'))
pha0 = []
vol0 = []
with open(p0, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        pha0.append(int(row[0]))
        vol0.append(float(row[1])*1e3)


p1 = Path.joinpath(Path('2022-02-01'), Path('PhaseCalibration'), Path('1kHz_1000mV_1000mV_phase.csv'))
pha1 = []
vol1 = []
with open(p1, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        pha1.append(int(row[0]))
        vol1.append(float(row[1])*1e3)

p2 = Path.joinpath(Path('2022-02-01'), Path('PhaseCalibration'), Path('1kHz_1000mV_1500mV_phase.csv'))
pha2 = []
vol2 = []
with open(p2, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        pha2.append(int(row[0]))
        vol2.append(float(row[1])*1e3)

p3 = Path.joinpath(Path('2022-02-01'), Path('PhaseCalibration'), Path('1kHz_1000mV_2000mV_phase.csv'))
pha3 = []
vol3 = []
with open(p3, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        pha3.append(int(row[0]))
        vol3.append(float(row[1])*1e3)

a0 = Path.joinpath(Path('2022-02-01'), Path('AmplitudeCalibration'), Path('1kHz_amplitude.csv'))
amp0 = []
a_vol0 = []
with open(a0, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        amp0.append(int(row[0]))
        a_vol0.append(float(row[1])*1e3)

a1 = Path.joinpath(Path('2022-02-01'), Path('AmplitudeCalibration'), Path('4kHz_amplitude.csv'))
amp1 = []
a_vol1 = []
with open(a1, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        amp1.append(int(row[0]))
        a_vol1.append(float(row[1])*1e3)

a2 = Path.joinpath(Path('2022-02-01'), Path('AmplitudeCalibration'), Path('7kHz_amplitude.csv'))
amp2 = []
a_vol2 = []
with open(a2, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        amp2.append(int(row[0]))
        a_vol2.append(float(row[1])*1e3)

a3 = Path.joinpath(Path('2022-02-01'), Path('AmplitudeCalibration'), Path('10kHz_amplitude.csv'))
amp3 = []
a_vol3 = []
with open(a3, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        amp3.append(int(row[0]))
        a_vol3.append(float(row[1])*1e3)

# Phase Plot
plt.figure(figsize=(6, 6))
plt.scatter(pha0, vol0, s=5, label=r'$V_{ref} = 500 mV$')
plt.scatter(pha1, vol1, s=5, label=r'$V_{ref} = 1000 mV$')
plt.scatter(pha2, vol2, s=5, label=r'$V_{ref} = 1500 mV$')
plt.scatter(pha3, vol3, s=5, label=r'$V_{ref} = 2000 mV$')

plt.title(r'Phase Calibration /n$V_{sig} = 1000 mV$')
plt.legend()
plt.xticks([0, 30, 60, 90, 120, 150, 180])
plt.yticks([-500, -250, 0, 250, 500])
plt.grid()

# Amplitude Plot
plt.figure(figsize=(6, 6))
plt.scatter(amp0, a_vol0, s=5, label=r'$1 kHz')
plt.scatter(amp1, a_vol1, s=5, label=r'$4 kHz')
plt.scatter(amp2, a_vol2, s=5, label=r'$7 kHz')
plt.scatter(amp3, a_vol3, s=5, label=r'$10 kHz')

plt.title(r'Amplitude calibration')
plt.legend()
plt.xticks([0, 500, 1000, 1500, 2000])
plt.yticks([0, 100, 200, 300, 400])
plt.grid()
plt.show()
