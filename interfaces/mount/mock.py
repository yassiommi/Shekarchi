import astropy.units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time

from interfaces.common.estimator import EstimatorMixin
from interfaces.mount import AbsMount

# will be used in estimator

    # DEFAULTS
Location = EarthLocation(lat=35.6892*u.deg, lon=51.3890*u.deg, height= 1250*u.m)
time = Time.now()


class MockMount(AbsMount, EstimatorMixin):
    MOVE_SPEED = 5 # deg per seconds
    MAX_JOG_TIME = 1 # seconds
    MAX_PARK_TIME = 10
    current_coord = SkyCoord


    def move(self, coord):
        self.add_time(current_coord.seperation(coord).deg/self.MOVE_SPEED + 2*self.MAX_JOG_TIME)
        self.current_coord = coord


    def park(self):
        self.add_time(self.MAX_PARK_TIME)



    def celestial_to_horizontal(self, coord, time=time, location=Location):
        coord = coord.transform_to(AltAz(obstime=time, location=Location))
        return coord

