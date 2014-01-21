import os
import glob
import csv
import datetime

from config import LOGS_DIR


class DaySample(object):
    def __init__(self, year, month, day):
        samples_name = os.path.join(LOGS_DIR, '%s-%s-%s' % (year, month, day))
        if not os.path.exists(samples_name):
            raise Exception()

        self.date = datetime.date(int(year), int(month), int(day))

        self._indoor_samples = []
        self._outdoor_samples = []

        self.max_indoor = None
        self.min_indoor = None
        self.max_outdoor = None
        self.min_outdoor = None

        with open(samples_name, 'rb') as samples_file:
            samples_reader = csv.reader(samples_file, delimiter=',')
            for date, indoor, outdoor in samples_reader:
                self._indoor_samples.append({'x': int(date), 'y': float(indoor)})
                self._outdoor_samples.append({'x': int(date), 'y': float(outdoor)})

                if (self.max_indoor == None) or (self.max_indoor < indoor):
                    self.max_indoor = indoor
                if (self.min_indoor == None) or (self.min_indoor > indoor):
                    self.min_indoor = indoor
                if (self.max_outdoor == None) or (self.max_outdoor < outdoor):
                    self.max_outdoor = outdoor
                if (self.min_outdoor == None) or (self.min_outdoor > outdoor):
                    self.min_outdoor = outdoor


    @property
    def indoor(self):
        return self._indoor_samples


    @property
    def outdoor(self):
        return self._outdoor_samples


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