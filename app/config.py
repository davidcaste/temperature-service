import glob

LOGS_DIR = 'logs'

BASE_DIR = '/sys/bus/w1/devices/'
try:
    DEVICE_FOLDER = glob.glob(BASE_DIR + '28*')[0]
    DEVICE_FILE = DEVICE_FOLDER + '/w1_slave'
except IndexError:
    DEVICE_FILE = None