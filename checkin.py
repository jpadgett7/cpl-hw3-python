from datetime import datetime
from pokeball import Pokeball


class CheckIn:
    """A check-in of a Team Rocket agent at a specific location/time.

    Represents a row of teh check-in spreadsheet.
    """

    def __init__(self, name, pokeball, location, time):
        """Constructor with the following parameters:

        :param str name: Name of agent checking in
        :param Pokeball pokeball: Type of Pokeball carried
        :param str location: The location where the agent checked in
        :param str time: Time the agent checked in

        :return: An object of the CheckIn type

        :raises ValueError: If a datetime.datetime object can not be created
            using the time parameter.
        """

        self.name = name
        if type(pokeball) is str:
            self.pokeball = Pokeball(int(pokeball))
        else:
            self.pokeball = pokeball
        self.location = location
        self.time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

    def __lt__(self, other):
        """Overloaded < operator

        :param CheckIn self: One CheckIn object
        :param CheckIn other: Another CheckIn object

        :return: True if self's time is less than other's time

        :rtype: bool
        """
        return self.time < other.time

    def __le__(self, other):
        """Overloaded <= operator

        :param CheckIn self: One CheckIn object
        :param CheckIn other: Another CheckIn object

        :return: True if self's time is less than or equal to other's time

        :rtype: bool
        """
        return self.time <= other.time

    def __gt__(self, other):
        """Overloaded > operator

        :param CheckIn self: One CheckIn object
        :param CheckIn other: Another CheckIn object

        :return: True if self's time is greater than other's time

        :rtype: bool
        """
        return self.time > other.time

    def __ge__(self, other):
        """Overloaded < operator

        :param CheckIn self: One CheckIn object
        :param CheckIn other: Another CheckIn object

        :return: True if self's time is greater than or equal to other's time

        :rtype: bool
        """
        return self.time >= other.time

    def __str__(self):
        """Called by str() to turn a CheckIn object into a str

        :param CheckIn self: A CheckIn object

        :return: The CheckIn object as a str

        :rtype: str
        """
        r = "{0} at {1} with {2} ({3})"
        return r.format(self.name, self.location, self.pokeball, self.time)
