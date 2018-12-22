import sys
from os import path

from base.estimator import EstimatorMixin
from interfaces.ccd import AbsCCD

sys.path.append(path.abspath('../windi'))


class MockCCD(AbsCCD, EstimatorMixin):
    def capture(self, time, temperature, binning, interval, count, type):
        self.add_time(time+6)
