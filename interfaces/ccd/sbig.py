# import sys
# from os import path
import threading
import time
# sys.path.append(path.abspath('../windi'))
#
# from pywindi.scripts.capture import capturer
# from pywindi.scripts.config import config
# from pywindi.windrivers import *
# from pywindi.winclient import Winclient
from interfaces.ccd import AbsCCD
import requests
from time import sleep

DIRECTORY = 'out/images/'
HOSTS = '(172.18.1.30:7624)'

class __CCD(AbsCCD):
    def __init__(self):
        pass

    def capture(self, time, temperature, binning, interval, count, typee, idd):
        print(count)
        for i in range(int(count)):
            requests.post('http://172.18.1.30:5000/capture', json = {'binning' : str(binning), 'temperature' : str(temperature),
            'exposure_time' : str(time), 'interval' : str(interval), 'type' : typee, 'chiz': str(int(count) - i)}, 'id': str(idd))
            requests.post('http://172.18.1.31:5000/capture', json = {'binning' : str(binning), 'temperature' : str(temperature),
            'exposure_time' : str(time), 'interval' : str(interval), 'type' : typee, 'chiz': str(int(count) - i)}, 'id': str(idd))
            requests.post('http://172.18.1.32:5000/capture', json = {'binning' : str(binning), 'temperature' : str(temperature),
            'exposure_time' : str(time), 'interval' : str(interval), 'type' : typee, 'chiz': str(int(count) - i)}, 'id': str(idd))

    def get_temperature(self):
        pass

    def set_temperature(self):
        pass

    def get_ccd(self, host):
        pass


ccd = __CCD()
