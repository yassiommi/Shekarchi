import requests
from controller import interrupt
from interfaces.cloud_detector import Cloud



def check_cloud(alt,az):
    cloud = Cloud()
    if not cloud.is_observable(alt, az):
        interrupt()


