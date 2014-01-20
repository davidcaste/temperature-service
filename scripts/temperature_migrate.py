#!/usr/bin/env python

import csv
import datetime

dates = {}

def process_row(row):
    sample_datetime = datetime.datetime.fromtimestamp(float(row[0]))
    date = sample_datetime.strftime('%Y-%m-%d')

    if date not in dates:
        dates[date] = []
    dates[date].append(row)

def write_dates_to_files():
    for date in dates.keys():
        with open(date, 'wb') as newfile:
            temp_writer = csv.writer(newfile, delimiter=',')

            samples = dates[date]
            for sample in samples:
                temp_writer.writerow(sample)

def main():
    with open('temperature.txt', 'rb') as csvfile:
        temp_reader = csv.reader(csvfile, delimiter=',')
        for row in temp_reader:
            process_row(row)

    write_dates_to_files()


if __name__ == '__main__':
    main()
