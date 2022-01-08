import csv


fields = ['RF', 'IF', 'Amplitudes']

data = [95e6+1e3, 1e3, [0.5, 0.6, 0.45, 0.45], [0, 90, 0, 180]]

filename = 'test.csv'

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    csvwriter.writerow(fields)
    csvwriter.writerow(data)
