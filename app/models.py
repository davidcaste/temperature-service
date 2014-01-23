import os
import csv
import datetime

try:
    import cPickle as pickle
except ImportError:
    import pickle

from config import LOGS_DIR


class NonExistantLogsError(Exception):
    pass


class GenericPeriodSamples(object):
    sample_data = None

    @property
    def max_indoor(self):
        return self.sample_data['max_indoor']

    @property
    def min_indoor(self):
        return self.sample_data['min_indoor']

    @property
    def average_indoor(self):
        return self.sample_data['average_indoor']

    @property
    def max_outdoor(self):
        return self.sample_data['max_outdoor']

    @property
    def average_outdoor(self):
        return self.sample_data['average_outdoor']

    @property
    def min_outdoor(self):
        return self.sample_data['min_outdoor']


class DaySample(GenericPeriodSamples):
    def __init__(self, year, month, day):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)

        samples_name = os.path.join(LOGS_DIR, '%04d-%02d-%02d' % (self.year, self.month, self.day))
        if not os.path.exists(samples_name):
            raise NonExistantLogsError()

        pickle_name = os.path.join('%s.dat' % samples_name)
        if os.path.exists(pickle_name):
            with open(pickle_name, 'rb') as pickle_file:
                try:
                    self.sample_data = pickle.load(pickle_file)
                except EOFError:
                    pass

        if self.sample_data is None:
            with open(pickle_name, 'wb') as pickle_file:
                self.__load_data(samples_name)

                sample_date = datetime.date(self.year, self.month, self.day)
                if datetime.date.today() != sample_date:
                    pickle.dump(self.sample_data, pickle_file)

    def __load_data(self, samples_name):
        self.sample_data = {}
        self.sample_data['indoor_samples'] = []
        self.sample_data['outdoor_samples'] = []

        indoor_samples = []
        outdoor_samples = []

        with open(samples_name, 'rb') as samples_file:
            samples_reader = csv.reader(samples_file, delimiter=',')
            for date, indoor, outdoor in samples_reader:
                self.sample_data['indoor_samples'].append({'x': int(date), 'y': float(indoor)})
                self.sample_data['outdoor_samples'].append({'x': int(date), 'y': float(outdoor)})

                indoor_samples.append(float(indoor))
                outdoor_samples.append(float(outdoor))

        self.sample_data['max_indoor'] = max(indoor_samples)
        self.sample_data['min_indoor'] = min(indoor_samples)
        self.sample_data['average_indoor'] = sum(indoor_samples) / float(len(indoor_samples))
        self.sample_data['max_outdoor'] = max(outdoor_samples)
        self.sample_data['min_outdoor'] = min(outdoor_samples)
        self.sample_data['average_outdoor'] = sum(outdoor_samples) / float(len(outdoor_samples))

    def next(self):
        day = datetime.timedelta(days=1)
        next_day = datetime.date(self.year, self.month, self.day) + day
        try:
            return DaySample(next_day.year, next_day.month, next_day.day)
        except NonExistantLogsError:
            return None

    def previous(self):
        day = datetime.timedelta(days=1)
        prev_day = datetime.date(self.year, self.month, self.day) - day
        try:
            return DaySample(prev_day.year, prev_day.month, prev_day.day)
        except NonExistantLogsError:
            return None

    @property
    def indoor_samples(self):
        return self.sample_data['indoor_samples']

    @property
    def outdoor_samples(self):
        return self.sample_data['outdoor_samples']


class PeriodWithMaxMinAverageSample(GenericPeriodSamples):
    def _load_data(self, samples):
        self.sample_data = {}
        self.sample_data['max_indoor_samples'] = []
        self.sample_data['min_indoor_samples'] = []
        self.sample_data['average_indoor_samples'] = []
        self.sample_data['max_outdoor_samples'] = []
        self.sample_data['min_outdoor_samples'] = []
        self.sample_data['average_outdoor_samples'] = []

        max_indoor_samples = []
        min_indoor_samples = []
        average_indoor_samples = []
        max_outdoor_samples = []
        min_outdoor_samples = []
        average_outdoor_samples = []

        for i in sorted(samples.keys()):
            sample = samples[i]

            max_indoor = sample.max_indoor
            min_indoor = sample.min_indoor
            average_indoor = sample.average_indoor
            max_outdoor = sample.max_outdoor
            min_outdoor = sample.min_outdoor
            average_outdoor = sample.average_outdoor

            self.sample_data['max_indoor_samples'].append({'x': i, 'y': max_indoor})
            self.sample_data['min_indoor_samples'].append({'x': i, 'y': min_indoor})
            self.sample_data['average_indoor_samples'].append({'x': i, 'y': average_indoor})
            self.sample_data['max_outdoor_samples'].append({'x': i, 'y': max_outdoor})
            self.sample_data['min_outdoor_samples'].append({'x': i, 'y': min_outdoor})
            self.sample_data['average_outdoor_samples'].append({'x': i, 'y': average_outdoor})

            max_indoor_samples.append(max_indoor)
            min_indoor_samples.append(min_indoor)
            average_indoor_samples.append(average_indoor)
            max_outdoor_samples.append(max_outdoor)
            min_outdoor_samples.append(min_outdoor)
            average_outdoor_samples.append(average_outdoor)

        self.sample_data['max_indoor'] = max(max_indoor_samples)
        self.sample_data['min_indoor'] = min(min_indoor_samples)
        self.sample_data['max_outdoor'] = max(max_outdoor_samples)
        self.sample_data['min_outdoor'] = min(min_outdoor_samples)
        self.sample_data['average_indoor'] = sum(average_indoor_samples) / float(len(average_indoor_samples))
        self.sample_data['average_outdoor'] = sum(average_outdoor_samples) / float(len(average_outdoor_samples))

    @property
    def max_indoor_samples(self):
        return self.sample_data['max_indoor_samples']

    @property
    def min_indoor_samples(self):
        return self.sample_data['min_indoor_samples']

    @property
    def average_indoor_samples(self):
        return self.sample_data['average_indoor_samples']

    @property
    def max_outdoor_samples(self):
        return self.sample_data['max_outdoor_samples']

    @property
    def min_outdoor_samples(self):
        return self.sample_data['min_outdoor_samples']

    @property
    def average_outdoor_samples(self):
        return self.sample_data['average_outdoor_samples']


class MonthSample(PeriodWithMaxMinAverageSample):
    def __init__(self, year, month):
        self.year = int(year)
        self.month = int(month)

        pickle_name = os.path.join(LOGS_DIR, '%04d-%02d.dat' % (self.year, self.month))
        if os.path.exists(pickle_name):
            with open(pickle_name, 'rb') as pickle_file:
                try:
                    self.sample_data = pickle.load(pickle_file)
                except EOFError:
                    pass

        if self.sample_data is None:
            with open(pickle_name, 'wb') as pickle_file:
                samples = {}
                for i in range(1, 32):
                    try:
                        sample = DaySample(self.year, self.month, i)
                        samples[i] = sample
                    except NonExistantLogsError:
                        continue

                if len(samples) == 0:
                    raise NonExistantLogsError()

                self._load_data(samples)

                today = datetime.date.today()
                if (today.year != self.year) or (today.month != self.month):
                    pickle.dump(self.sample_data, pickle_file)

    def next(self):
        date = datetime.date(self.year, self.month, 15)
        next_month = date + datetime.timedelta(days=31)
        try:
            return MonthSample(next_month.year, next_month.month)
        except:
            return None

    def previous(self):
        date = datetime.date(self.year, self.month, 15)
        next_month = date - datetime.timedelta(days=31)
        try:
            return MonthSample(next_month.year, next_month.month)
        except:
            return None


class YearSample(PeriodWithMaxMinAverageSample):
    def __init__(self, year):
        self.year = int(year)

        pickle_name = os.path.join(LOGS_DIR, '%04d.dat' % self.year)
        if os.path.exists(pickle_name):
            with open(pickle_name, 'rb') as pickle_file:
                try:
                    self.sample_data = pickle.load(pickle_file)
                except EOFError:
                    pass

        if self.sample_data is None:
            with open(pickle_name, 'wb') as pickle_file:
                samples = {}
                for i in range(1, 13):
                    try:
                        sample = MonthSample(self.year, i)
                        samples[i] = sample
                    except NonExistantLogsError:
                        continue

                if len(samples) == 0:
                    raise NonExistantLogsError()

                self._load_data(samples)

                today = datetime.date.today()
                if today.year != self.year:
                    pickle.dump(self.sample_data, pickle_file)

    def next(self):
        date = datetime.date(self.year, 6, 15)
        next_year = date + datetime.timedelta(days=365)
        try:
            return YearSample(next_year.year)
        except:
            return None

    def previous(self):
        date = datetime.date(self.year, 6, 15)
        next_year = date - datetime.timedelta(days=365)
        try:
            return YearSample(next_year.year)
        except:
            return None