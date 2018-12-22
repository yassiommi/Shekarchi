class EstimatorMixin():
    def __init__(self):
        self._time = 0.0
        
    def get_time(self):
        return self._time
        
    def reset(self):
        self._time = 0.0
    
    def add_time(self, time):
        self._time += time
