import datetime
import sys


class DataError(Exception):
    """ Custom error with base class Exception.

    Thrown by methods of CheckInTimeline
    """
    pass


class CheckInTimeline:
    """A timeline of check-ins.

    Represents a timeline of recorded check-ins: ordered chronologically from
    least recent to most recent.
    """

    def __init__(self):
        self.checkins = []

    def add(self, checkin):
        """Appends a CheckIn object to checkins list attribute

        :param CheckInTimeLine self: The CheckInTimeLine object being called
        :param CheckIn checkin: An object of type CheckIn

        :return: None
        """
        self.checkins.append(checkin)
        self.checkins = sorted(self.checkins)

    def windows(self, window_size=datetime.timedelta(0, 3600)):
        """Generator function for iterating over windows of given size

        :param CheckInTimeline self: The object being called
        :param timedelta window_size: Size of window, defaults to 3600 seconds

        """
        p1_loops = 0  # first index of slice
        for pivot1 in self.checkins:
            p2_loops = 0  # second index of slice
            for pivot2 in self.checkins:
                if pivot2.time >= pivot1.time + window_size:
                    break
                p2_loops = p2_loops + 1
            yield tuple(self.checkins[p1_loops:p2_loops])
            p1_loops = p1_loops + 1

    def rendezvous(self, window_size=datetime.timedelta(0, 3600)):
        for w in self.windows(window_size):
            meeting = ()
            first_check = w[0]
            for tup in w:
                if tup.location == first_check.location:
                    meeting = meeting + (tup, )
            try:
                if len(meeting) == 2:
                    yield meeting
                elif len(meeting) < 2:  # Not a rendezvous
                    pass
                else:  # Size of tuple
                    raise DataError
            except DataError:
                print("DataError: More than two agents at one rendezvous.")
                sys.exit(1)
