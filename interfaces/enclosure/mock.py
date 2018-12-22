from interfaces.enclosure import AbsEnclosure
from interfaces.common.estimator import EstimatorMixin

CHANGE_STATE_TIME = 10
CLOSED = 0
OPEN = 1

class MockEnclosure(AbsEnclosure, EstimatorMixin):
    state = CLOSED

    def open(self):
        if state:
            self.add_time(CHANGE_STATE_TIME)
            state = OPEN


    def close(self):
        if not state:
            self.add_time(CHANGE_STATE_TIME)
            state = CLOSED

    def get_state(self):
        return state
