import os
import glob
import csv

from config import LOGS_DIR


def read_logs(year=None, month=None, day=None):
    if year is None:
        year = '*'
    else:
        year = '%04d' % int(year)
    if month is None:
        month = '*'
    else:
        month = '%02d' % int(month)
    if day is None:
        day = '*'
    else:
        day = '%02d' % int(day)

    name_pattern = '%s-%s-%s' % (year, month, day)
    files = sorted(glob.glob(os.path.join(LOGS_DIR, name_pattern)))

    indoor_samples = []
    outdoor_samples = []
    for foo in files:
        with open(foo, 'rb') as sample_file:
            samples_reader = csv.reader(sample_file, delimiter=',')
            for date, indoor, outdoor in samples_reader:
                indoor_samples.append({'x': int(date), 'y': float(indoor)})
                outdoor_samples.append({'x': int(date), 'y': float(outdoor)})

    return indoor_samples, outdoor_samples

if __name__ == '__main__':
    print read_logs(2014,1)