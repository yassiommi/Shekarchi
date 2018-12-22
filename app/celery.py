from celery import Celery
celery = Celery('Shekarchi', broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['app.api', 'controller'])

import logging

from celery.signals import after_setup_logger, after_setup_task_logger

def handle_logs(logger=None,loglevel=logging.DEBUG, **kwargs):
    from common import handler
    logger.addHandler(handler)
    return logger


after_setup_task_logger.connect(handle_logs)
after_setup_logger.connect(handle_logs)
