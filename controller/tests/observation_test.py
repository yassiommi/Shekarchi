import unittest

    # INSTANCES
from interfaces.mount.skyx import mount
from interfaces.enclosure.mock import MockEnclosure
from interfaces.ccd.sbig import ccd

    # LIBRARY
from astropy import SkyCoord
import astropy.units as u


class FinalTest(unittest.TestCase):
    def test_observe(self):
        coords = SkyCoord(10, 20, unit="deg")
        MockEnclosure.open()
        print(MockEnclosure.get_state())
        mount.move(coords)
        ccd.capture(10,-5,(1.0,1.0),5,2,'dark')
        mount.park()
        MockEnclosure.close()
        print(MockEnclosure.get_state())
        print('FINITO :D')


if __name__ == '__main__':
    unittest.main()
