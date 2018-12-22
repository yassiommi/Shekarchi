import requests

class Cloud():

    CLOUD_DETECTOR_URL = "http://127.0.0.1:5000"

    def is_observable(self,alt,az):
        r = requests.post(CLOUD_DETECTOR_URL, data = {'alt': alt, 'az': az})
        return bool(r.text)
