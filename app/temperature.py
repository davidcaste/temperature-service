from config import DEVICE_FILE

import pywapi
import time


YAHOO_CODES_TO_IMG = {
    '0': 'Tornado.svg',  # tornado
    '1': 'Cloud-Wind.svg',  # tropical storm
    '2': 'Cloud-Wind.svg',  # hurricane
    '3': 'Cloud-Lightning.svg',  # severe thunderstorms
    '4': 'Cloud-Lightning.svg',  # thunderstorms
    '5': 'Cloud-Snow-Alt.svg',  # mixed rain and snow
    '6': 'Cloud-Snow.svg',  # mixed rain and sleet
    '7': 'Cloud-Snow.svg',  # mixed snow and sleet
    '8': 'Cloud-Snow.svg',  # freezing drizzle
    '9': 'Cloud-Drizzle.svg',  # drizzle
    '10': 'Cloud-Snow.svg',  # freezing rain
    '11': 'Cloud-Rain-Alt.svg',  # showers
    '12': 'Cloud-Rain.svg',  # showers
    '13': 'Cloud-Snow-Alt.svg',  # snow flurries
    '14': 'Cloud-Snow-Alt.svg',  # light snow showers
    '15': 'Snowflake.svg',  # blowing snow
    '16': 'Cloud-Snow-Alt.svg',  # snow
    '17': 'Cloud-Hail-Alt.svg',  # hail
    '18': 'Cloud-Snow.svg',  # sleet
    '19': 'Cloud-Fog-Alt.svg',  # dust
    '20': 'Cloud-Fog.svg',  # foggy
    '21': 'Cloud-Fog-Alt.svg',  # haze
    '22': 'Cloud-Fog-Alt.svg',  # smoky
    '23': 'Cloud-Wind.svg',  # blustery
    '24': 'Wind.svg',  # windy
    '25': 'Thermometer-Zero.svg',  # cold
    '26': 'Cloud.svg',  # cloudy
    '27': 'Cloud-Moon.svg', #  mostly cloudy (night)
    '28': 'Cloud-Sun.svg',  # mostly cloudy (day)
    '29': 'Cloud-Moon.svg',  # partly cloudy (night)
    '30': 'Cloud-Sun.svg',  # partly cloudy (day)
    '31': 'Moon.svg',  # clear (night)
    '32': 'Sun.svg',  # sunny
    '33': 'Moon.svg',  # fair (night)
    '34': 'Sun.svg',  # fair (day)
    '35': 'Cloud-Lightning.svg',  # mixed rain and hail
    '36': 'Thermometer-100.svg',  # hot
    '37': 'Cloud-Lightning.svg',  # isolated thunderstorms
    '38': 'Cloud-Lightning.svg',  # scattered thunderstorms
    '39': 'Cloud-Lightning.svg',  # scattered thunderstorms
    '40': 'Cloud-Rain.svg',  # scattered showers
    '41': 'Cloud-Snow-Alt.svg',  # heavy snow
    '42': 'Cloud-Snow.svg',  # scattered snow showers
    '43': 'Snowflake.svg',  # heavy snow
    '44': 'Cloud-Sun.svg',  # partly cloudy
    '45': 'Cloud-Lightning.svg',  # thundershowers
    '46': 'Cloud-Snow-Alt.svg',  # snow showers
    '47': 'Cloud-Lightning.svg',  # isolated thundershowers
}


class YahooTemp(object):
    def __init__(self):
        self.result = pywapi.get_weather_from_yahoo('SPXX0050', 'metric')
        icon = self.__code_to_something(self.result['condition']['code'])
        if icon:
            self.result['condition']['icon'] = icon
        if 'link' in self.result:
            self.result['condition']['link'] = self.result['link']

    def __code_to_something(self, code):
        if code in YAHOO_CODES_TO_IMG:
            return YAHOO_CODES_TO_IMG[code]

    @property
    def condition(self):
        return self.result['condition']

class IndoorTemp(object):
    def __init__(self):
        pass

    def temp(self):
        lines = self.__read_file()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.__read_file()()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp = float(temp_string) / 1000.0
            return temp

    def __read_file(self):
        with open(DEVICE_FILE, 'r') as device_file:
            return device_file.readlines()