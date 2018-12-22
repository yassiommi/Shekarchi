import logging
import sys
import unittest
from astropy.coordinates import SkyCoord, Angle
from random import random
from time import sleep

from interfaces.mount.skyx import mount

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger(__name__)
logger = logging.getLogger()
MAX_ACCEPTABLE_ERROR = Angle('30 arcsec')


class MountPressureTest(unittest.TestCase):
    def test_random_targets(self):
        m = mount
        for i in range(1,30):
            target = SkyCoord(random()*360, random()*180 - 90, unit='deg')
            if m.is_above_horizon(target):
                m.meridian_tracking_correction()
                m.move(target)
                coord = m.get_position()
                sleep(1)
                logger.debug("pressure_tests:test_random_targets :: target:%s, current_position:%s, separation:%s" % (target, coord, target.separation(coord)))

        m.park()

if __name__ == '__main__':
    unittest.main()
