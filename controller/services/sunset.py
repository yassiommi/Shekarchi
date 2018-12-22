from interfaces.mount.skyx import mount
from controller import interrupt
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@periodic_task(run_every=timedelta(seconds=30))
def check_sunset():
    coord=mount.get_position()
    if mount.is_above_horizon(coord) :
        logger.warn('process interrupted. object is below horizon.')
        interrupt()
    logger.debug('sunset checked')


