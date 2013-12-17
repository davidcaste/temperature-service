#!/usr/bin/env python

import glob
import time
import pywapi
import sys


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def get_yahoo_temp():
	result = pywapi.get_weather_from_yahoo('SPXX0050', 'metric')
	return float(result['condition']['temp'])

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
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

def write_temp(line):
	with open('temperature.txt', 'a') as output_file:
		output_file.write(line + '\n')

while True:
	try:
		write_temp('%d,%0.2f,%0.2f' % read_temp())
	except Exception as inst:
		sys.stderr.write('%s: %s' % (type(inst), inst))
	time.sleep(600)

