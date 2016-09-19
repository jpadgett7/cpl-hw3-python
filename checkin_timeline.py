from checkin import CheckIn
from datetime import timedelta

class DataError(Exception):
    pass
    
class CheckInTimeLine:
    """A timeline of check-ins.
    
    Represents a timeline of recorded check-ins: ordered chronologically from
        least recent to most recent.
    """

    def __init__(self):
        self.checkins = ()
        
    def add(self, checkin):
        self.checkins.append(checkin)
        self.checkisn.sort()
        
    def windows(window_size=datetime.timedelta(0, 3600)):
        for i in window_size:
            if self.time == i:
                yield i