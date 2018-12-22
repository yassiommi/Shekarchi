import unittest
from time import sleep
from interfaces.enclosure.plc import enclosure

class EnclosureFunctionalTest(unittest.TestCase):
    def test(self):
        enclosure.open()
        sleep(60)
        enclosure.close()

if __name__ == '__main__':
    unittest.main()
