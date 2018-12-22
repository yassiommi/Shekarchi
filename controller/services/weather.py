from interfaces.weather import WeatherStation
from controller import interrupt
from datetime import timedelta
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

weather_station = WeatherStation()
logger = get_task_logger(__name__)

@periodic_task(run_every=timedelta(seconds=30))
def check_weather():
    if not weather_station.check_weather():
        logger.warn('process interrupted. weather is not appropriate for observing.')
        interrupt()
    logger.debug('weather checked')

