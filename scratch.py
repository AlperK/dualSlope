import csv


data = [[-0.1, 0.2, 1.0, -0.4, -0.43, 0.3, 0.2, -0.11],
        [0.1, -0.2, -1.0, 0.4, 0.43, -0.3, -0.2, 0.11]]


header = []
for laser in range(4):
    for apd in range(2):
        seq = ('L' + str(laser+1), 'APD' + str(apd+1))
        header.append('-'.join(seq))
print(header)

with open('csv_test.csv', 'w+') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows([header])

with open('csv_test.csv', 'a+') as f:
    writer = csv.writer(f, delimiter=',')
    for d in data:
        print(d)
        writer.writerows([d])
