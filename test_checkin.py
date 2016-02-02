"""Tests for checkin module

Feel free to add more tests as you see fit.

"""
import datetime
import pytest

from checkin import CheckIn
from pokeball import Pokeball


def test_lt():
    """Test < operator"""
    o1 = CheckIn("Joe", Pokeball.poke_ball, "Pokemart", "2016-09-10 12:00:00")
    o2 = CheckIn("Jane", Pokeball.poke_ball, "Pokemart", "2016-09-10 12:30:00")
    assert o1 < o2
    assert not (o2 < o1)


def test_gt():
    """Test > operator"""
    o1 = CheckIn("Joe", Pokeball.poke_ball, "Pokemart", "2016-09-10 12:00:00")
    o2 = CheckIn("Jane", Pokeball.poke_ball, "Pokemart", "2016-09-10 12:30:00")
    assert not (o1 > o2)
    assert o2 > o1


def test_le():
    """Test <= operator"""
    o1 = CheckIn("Joe", Pokeball.poke_ball, "Pokemart", "2016-09-10 12:00:00")
    o2 = CheckIn("Jane", Pokeball.poke_ball, "Pokemart", "2016-09-10 12:30:00")
    assert o1 <= o2
    assert o1 <= o1
    assert o2 <= o2
    assert not (o2 <= o1)


def test_ge():
    """Test >= operator"""
    o1 = CheckIn("Joe", Pokeball.poke_ball, "Pokemart", "2016-09-10 12:00:00")
    o2 = CheckIn("Jane", Pokeball.poke_ball, "Pokemart", "2016-09-10 12:30:00")
    assert not (o1 >= o2)
    assert o1 >= o1
    assert o2 >= o2
    assert o2 >= o1


def test_datetime():
    """Test loading the :class:`datetime.datetime` from a string"""
    # Check the type
    o = CheckIn("Joe", Pokeball.poke_ball, "Pokemart", "2016-09-10 12:04:02")
    assert isinstance(o.time, datetime.datetime)

    # Bad time
    with pytest.raises(ValueError):
        CheckIn("Joe", Pokeball.poke_ball, "Pokemart", "2016-09-10 12:00:")

    # Bad date
    with pytest.raises(ValueError):
        CheckIn("Joe", Pokeball.poke_ball, "Pokemart", "2016-09- 12:00:00")

    # Good date/time
    o = CheckIn("Joe", Pokeball.poke_ball, "Pokemart", "2016-09-10 12:04:02")

    # Check that fields are assigned properly
    assert o.time.day == 10
    assert o.time.month == 9
    assert o.time.year == 2016
    assert o.time.hour == 12
    assert o.time.minute == 4
    assert o.time.second == 2
    assert o.time.microsecond == 0


def test_str():
    """Test str construction"""
    o = CheckIn("Tom", Pokeball.poke_ball, "Pokemart", "2016-09-10 12:04:02")
    assert str(o) == "Tom at Pokemart with a Poke Ball (2016-09-10 12:04:02)"
