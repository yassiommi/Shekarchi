import unittest
from astropy.coordinates import SkyCoord, Angle

from interfaces.mount.skyx import mount

MAX_ACCEPTABLE_ERROR = Angle('30 arcsec')

class MountFunctionalTest(unittest.TestCase):

    def test_polar(self):
        m = mount
        target = SkyCoord('0h43m44s', '40d58\'06"')
        m.move(target)
        coord = m.get_celestial_coords()
        m.park()
        self.assertTrue(coord.separation(target) <= MAX_ACCEPTABLE_ERROR)

if __name__ == '__main__':
    unittest.main()
