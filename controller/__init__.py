# PYTHON
import traceback
from threading import Lock

from datetime import datetime
import logging
import time
from math import cos, acos, sin, asin, tan, atan, degrees, radians, ceil, floor


# LIBRARY
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun
from astropy.io import fits
from astropy.time import Time
from celery.utils.log import get_task_logger

from app.celery import celery
from interfaces.weather import WeatherStation
from interfaces.mount.skyx import mount
from interfaces.ccd.sbig import  ccd
from interfaces.cloud_detector import Cloud
from interfaces.enclosure.plc import enclosure
from interfaces.ccd.sbig import DIRECTORY
from interfaces.focuser import Focuser

# GLOBALS
state_lock = Lock()

INTERRUPTING = 'INTERRUPTING'
OBSERVING = 'OBSERVING'
IDLE = 'IDLE'
observation_state = IDLE
observation_id = -1


perigee_equinox = 76.28992
astronomical_year = 365.25636
epsilon = 23.44

# EMERGENCY STOP
def interrupt():
    #   HODOR!
    global observation_state
    if observation_state != OBSERVING:
        return
    observation_state = INTERRUPTING
    enclosure.close()
    state_lock.acquire()
    observation_state = IDLE
    state_lock.release()

    # EXCEPTIONS


class InterruptionException(Exception):
    pass


class BadConditionsException(Exception):
    pass


from controller.services import interrupt_handle

logger = get_task_logger(__name__)

@celery.task
def observe(ra, dec, time, temperature, binning, interval, count, id, count2):
    global observation_state
    global state_lock
    global observation_id
    observation_id = id

    try:
        state_lock.acquire()
        if observation_state == IDLE:
            observation_state = OBSERVING
        state_lock.release()
#        log_handler.doRollover()
        weather_station = WeatherStation()
        if not weather_station.check_weather():
            raise BadConditionsException()

        target = SkyCoord(ra=ra, dec=dec, unit='deg')

        altaz = mount.celestical_to_horizontal(target)
            raise BadConditionsException()

        interruption_handling()
#        enclosure.open()
        logger.debug('OBSERVE :: enclosure opened')
        interruption_handling()
        mount.go_home()
        logger.debug('OBSERVE :: mount initiated')
        interruption_handling()
        logger.debug('OBSERVE :: Observation started.')
        interruption_handling()
        mount.move(target)
        mount.meridian_tracking_correction()

            #   CAPTURE BIASES BEFORE STARTING
        interruption_handling()
        logger.debug('Capturing bias images.')
        ccd.capture(time=time, temperature=temperature, binning = binning, interval=interval, count=count2, typee='bias')

         #   CAPTURE DARKS BEFORE STARTING
        interruption_handling()
        logger.debug('Capturing dark images.')
        ccd.capture(time=time, temperature=temperature, binning=binning, interval=interval,count=count2, typee='dark')

        interruption_handling()
        focusera = Focuser(A, 22006, 21960)
        focuserb = Focuser(B, 22006, 21960)
        focuserc = Focuser(C, 22120, 22054)
        ccd.capture(time=time, temperature=temperature, binning=binning, interval=interval, count=count, typee='light')

        logger.debug('Observation successfully ended.')
    finally:
        traceback.print_exc()
        logger.debug('Observation unsuccessfully ended.')

                #   CAPTURE BIASES AFTER FINISHING
        interruption_handling()
        bias_captures = {}
        logger.debug('Capturing bias images.')
        print(time, temperature, binning, interval, count2)
        ccd.capture(time=time, temperature=temperature, binning=binning, interval=interval,  count=count2, typee='bias')

               #   CAPTURE DARKS AFTER FINISHING
        interruption_handling()
        logger.debug('Capturing dark images.')
        dark_captures = {}
        ccd.capture(time=time, temperature=temperature, binning=binning, interval=interval, count=count2, typee='dark')

    mount.meridian_tracking_correction()
    mount.park()
 #   enclosure.close()

    state_lock.acquire()
    observation_state = IDLE
    state_lock.release()

    return "Man delam pari ro mikhad."



def sunset_time(a = -12):
    phi = 33.7485
    l = 51.4257
    now = datetime.datetime.now()
    t = Time(Time.now(), scale='utc', location = (str(l) + 'd', str(phi) + 'd'))
    ra, dec = get_sun(t).ra.deg, get_sun(t).dec.deg
    ST = t.sidereal_time('apparent').hour * 15
    H_now = ST - ra
    H_set = degrees(acos((sin(radians(a))-sin(radians(phi) * sin(radians(dec)))) / (cos(radians(phi)) * cos(radians(dec)))))
    delta = H_set - H_now
    return now.hour + now.minute / 60 + now.second / 3600 + delta / 15


def interruption_handling():
    if observation_state == INTERRUPTING:
        raise InterruptionException()


def set_header(ra, dec, id, captured):
    for img_name in captured.keys():
        now = captured[img_name]
        img = fits.open(DIRECTORY + str(img_name) + '/')
        header = img.header
        header.set('OBSERVATION_ID', id)
        header.set('SKY_COORD_RA', ra)
        header.set('SKY_COORD"DEC', dec)
        header.set('YEAR', now.year)
        header.set('MONTH', now.month)
        header.set('DAY', now.day)
        header.set('HOUR', now.hour)
        header.set('MINUTE', now.minute)
        header.set('SECOND', now.second)
        header.set('TIME_ZONE', 'UCT')
        weather_station = WeatherStation()
        ws_json = weather_station.get_weather_status()
        header.set('HUMIDITY', ws_json['humidity'])
        header.set('RAINY', ws_json['rainy'])
        header.set('WIND', ws_json['wind'])
        header.set('TEMP', ws_json['temp'])
        header.set('PIXEL_SCALE', 2.5)
        img.close()


def image_samples(captured):
    converted = []
    subprocess.call("cd " + DIRECTORY)
    for img_name in captured.keys():
        subprocess.call("magick" + " convert " + str(img_name) + ".fits " + str(img_name) + ".jpg", shell = True)
        converted.append(str(img_name) + ".jpg")
    return converted
