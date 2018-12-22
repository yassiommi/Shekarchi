import unittest
from interfaces.weather import WeatherStation


class WeatherStationTest(unittest.TestCase):

    def weather_station_test(self):
        weather_station = WeatherStation()
        weather_station.check_weather()
