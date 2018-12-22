import requests
from common import logger
from json import dumps

WEATHER_STATION_URL = 'http://172.18.1.27/__/usr/lambrecht/data/sensors'


class Weather:
    temp = 0
    wind_speed = 0
    rainy = 1
    humidity = 0

    def __init__(self, humidity, temp, wind_speed, rainy):
        self.temp = temp
        self.wind_speed = wind_speed
        self.humidity = humidity
        self.rainy = rainy


class WeatherStation:

    def check_weather(self):
        x = self.get_weather_json()
        print(x)
        if x is None:
            return False
        self.weather = Weather(humidity=x['values'][0], temp=x['values'][1], wind_speed=x['values'][2], rainy=x['values'][3])
        logger.info('WEATHER :: humidity = ' + str(self.weather.humidity))
        logger.info('WEATHER :: rainy = ' + str(self.weather.rainy == 0))
        logger.info('WEATHER :: temp = ' + str(self.weather.temp))
        logger.info('WEATHER :: wind = ' + str(self.weather.wind_speed))
        if self.weather.rainy == 0:
            return False
        if self.weather.humidity > 90:
            return False
        if self.weather.temp < -5:
            return False
        if self.weather.wind_speed > 100:
            return False
        return True

    def get_weather_json(self):
        try:
            r = requests.get(WEATHER_STATION_URL)
            return r.json()
        except requests.ConnectionError as exp:
            logger.error(exp)

    def get_weather_status(self):
        return dumps(vars(self.weather))
