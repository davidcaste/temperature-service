#!/usr/bin/env python

import glob
import time
import pywapi
import os
import sys
import csv
import datetime


BASE_DIR = '/sys/bus/w1/devices/'
DEVICE_FOLDER = glob.glob(BASE_DIR + '28*')[0]
DEVICE_FILE = DEVICE_FOLDER + '/w1_slave'

def get_yahoo_temp():
	result = pywapi.get_weather_from_yahoo('SPXX0050', 'metric')
	return float(result['condition']['temp'])

def read_temp_raw():
	f = open(DEVICE_FILE, 'r')
	lines = f.readlines()
	f.close()
	return lines

def get_data():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		epoch = int(time.time())
		temp_string = lines[1][equals_pos+2:]
		indoor_temp = float(temp_string) / 1000.0
		outdoor_temp = get_yahoo_temp()
		return epoch, indoor_temp, outdoor_temp

def register_temperature():
	epoch, indoor_temp, outdoor_temp = get_data()
	sample_datetime = datetime.datetime.fromtimestamp(epoch)
	date = sample_datetime.strftime('%Y-%m-%d')
	
	with open(os.path.join('logs', date), 'a') as output_file:
		temp_writer = csv.writer(output_file, delimiter=',')
		temp_writer.writerow([epoch,
							'%.02f' % indoor_temp,
							'%.02f' % outdoor_temp])

def main():
	while True:
		try:
			register_temperature()
		except Exception as inst:
			sys.stderr.write('%s: %s' % (type(inst), inst))
		time.sleep(600)

if __name__ == '__main__':
	main()