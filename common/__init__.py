
import logging

from logging.handlers import RotatingFileHandler

import sys

LOG_FILES = 'out/logs/shekarchi.log'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger(__name__)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename=LOG_FILES)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

