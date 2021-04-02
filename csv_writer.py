import csv

def write(path, data):
    file = open(path, 'a', newline='')
    writer = csv.writer(file)

    writer.writerow(data)

    file.close()
