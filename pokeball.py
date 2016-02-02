from enum import Enum


class Pokeball(Enum):
    """An enumeration of different Pokeballs used by Team Rocket Delivery
    agents.

    Refer to the Python 3.4 `enum docs`_

    .. _enum link: https://docs.python.org/3.4/library/enum.html

    """
    poke_ball = 1
    great_ball = 2
    ultra_ball = 3

    def __str__(self):
        """Returns the string representation of a Pokeball"""
        name = ""
        if self.value == 1:
            name = "a Poke Ball"
        if self.value == 2:
            name = "a Great Ball"
        if self.value == 3:
            name = "an Ultra Ball"
        return name
