from celery.task import periodic_task
from datetime import timedelta
from controller.services.weather import check_weather

from controller import observation_state, OBSERVING
from threading import Lock

lock = Lock()


@periodic_task(run_every=timedelta(seconds=30))
def interrupt_handle():
    lock.acquire()

    if observation_state != OBSERVING:
        return
    check_weather()
    lock.release()
