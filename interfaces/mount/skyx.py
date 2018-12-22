
import re
import astropy.units as u
from astropy.coordinates import SkyCoord, AltAz

from interfaces.mount import AbsMount
from interfaces.common import call
from threading import Lock
from math import cos, sin, acos, asin, degrees
from common import logger

tracking_lock = Lock()
saghez_lock = Lock()


phi = 33.7485
l = 51.4257


POSITION_PATTERN = r'''RA: (?P<ra>\d+h \d+m \d+\.\d+s)''' + \
                   r'''\|Dec: (?P<dec>[+-]\d+° \d+' \d+\.\d+")''' + \
                   r'''\|Alt: (?P<alt>-?\d+\.?\d*)\|Az: (?P<az>\d+\.?\d*)''' + \
                   r'''\|HA: (?P<ha>-?\d+.\d+)\|Track: (?P<track>[01])'''

ALTAZ_PATTERN = r'Alt: (?P<alt>-?\d+.?\d*)\|Az: (?P<az>\d+\.?\d*)'

ERROR_PATTERN = 'Error = (\d+)'


class __Mount(AbsMount):
    def __init__(self):
        self.base_cmd = ['node', 'interfaces/mount/nodejs/mount.js', '-v']
        logger.debug('MOUNT :: init Mount')

    def go_home(self):
        # saghez_lock.acquire()
        call(self.base_cmd + ['home'])
        logger.debug('MOUNT :: went to home')
        # saghez_lock.release()

    def set_track(self, enabled):
        # saghez_lock.acquire()
        call(self.base_cmd + ['start' if enabled else 'stop'])
        logger.debug('MOUNT :: track %s' % 'enabled' if enabled else 'disabled')
        # saghez_lock.release()

    def get_position(self):
        # saghez_lock.acquire()
        exitcode, stdout, stderr = call(self.base_cmd + ['position'])
        positions = re.search(POSITION_PATTERN, stdout).groupdict()
        # saghez_lock.release()
        return SkyCoord(positions['ra'], positions['dec'])

    def celestical_to_horizontal(self, coord):
        # saghez_lock.acquire()
        exitcode, stdout, stderr = call(self.base_cmd + ['radec2altaz', '%s,%s' % (coord.ra.hour, coord.dec.deg)])
        positions = re.search(ALTAZ_PATTERN, stdout).groupdict()
        # saghez_lock.release()
        return AltAz(alt=float(positions['alt']) * u.deg, az=float(positions['az']) * u.deg)

    def move(self, coord):
        # saghez_lock.acquire()
        if not self.is_above_horizon(coord):
            raise Exception('Fuck off, its below the horizon')

        logger.debug('move :: move to %s' % coord)
        call(self.base_cmd + ['decimal', '%s,%s' % (coord.ra.hour, coord.dec.deg)])
        logger.debug('move :: goto completed')

        ccoord = self.get_position()

        ddec = coord.dec - ccoord.dec
        logger.debug('move :: start jogging in DEC (delta = %s)' % ddec)
        call(self.base_cmd + ['dither', 'N' if ddec > 0 else 'S', str(abs(ddec).arcmin)])

        dra = (coord.ra - ccoord.ra)
        logger.debug('move :: start jogging in RA (delta = %s)' % dra)
        call(self.base_cmd + ['dither', 'E' if dra > 0 else 'W', str(abs(dra).arcmin)])

        logger.debug('move :: jog completed')
        # saghez_lock.release()

    def park(self):
        # saghez_lock.acquire()
        call(self.base_cmd + ['park'])
        # saghez_lock.release()


    # SHOULD BE CHECKED BETWEEN EACH PHOTO
    def meridian_tracking_correction(self):
        # saghez_lock.acquire()
        alt = self.celestial_to_horizontal(self.get_position()).alt.deg
        dec = self.get_position().dec.deg
        hour_angle = degrees(acos((sin(alt) - sin(phi) * sin(dec)) / (cos(phi) * cos(dec))))
        if hour_angle > 10:
            tracking_lock.acquire()
            self.move(self.get_position())

        tracking_lock.release()
        # saghez_lock.release()


    def is_tracking(self):
        # saghez_lock.acquire()
        exitcode, stdout, stderr = call(self.base_cmd + ['position'])
        positions = re.search(POSITION_PATTERN, stdout).groupdict()
        if positions['track'] == 1:
            return 'On'
        else:
            return 'Off'
        # saghez_lock.release()
mount = __Mount()
