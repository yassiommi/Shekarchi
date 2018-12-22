from interfaces.enclosure import AbsEnclosure
from interfaces.common import call
from threading import Lock
from interfaces.common import logger

class __Enclosure(AbsEnclosure):
    state = 'Closed'
    enclosure_lock = Lock()

    def __init__(self):
        self.base_cmd = ['node', 'interfaces/enclosure/nodejs/plc.js']
        logger.debug('ENCLOSURE :: init enclosure')

    def open(self):
        state = 'Opening'
        self.enclosure_lock.acquire()
        logger.debug('ENCLOSURE :: open')
        self.enclosure_lock.release()
        state = 'Open'

    def close(self):
        state = 'Closing'
        self.enclosure_lock.acquire()
        logger.debug('ENCLOSURE :: close')
        self.enclosure_lock.release()
        state = 'Closed'

    def get_enclosure_state(self):
        return self.state

enclosure = __Enclosure()
