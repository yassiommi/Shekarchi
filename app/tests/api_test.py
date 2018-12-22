import unittest
import requests

class TestAPI(unittest.TestCase):

    # def test_observation(self):
    #     r = requests.post('http://172.18.1.47:5000/observation', json={'RA': '13h38m40s','DEC': '-5d27\'50"', 'Exposure Time': 0.01, \
    #         'Binning': 1, 'Interval': 3, 'Number': 2, 'ID': '003435672', 'IP': 'call me :**'})
    #     print(r.text)


    def test_position(self):
        r = requests.get('http://172.18.1.47:5000/position')
        print(r.text)


    def test_enclosure(self):
        r = requests.get('http://172.18.1.47:5000/enclosure')
        print(r.text)


    def test_tracking(self):
        r = requests.get('http://172.18.1.47:5000/tracking')
        print(r.text)


    def test_status(self):
        r = requests.get('http://172.18.1.47:5000/status')
        print(r.text)


    def test_id(self):
        r = requests.get('http://172.18.1.47:5000/id')
        print(r.text)


if __name__ == '__main__':
    unittest.main()
