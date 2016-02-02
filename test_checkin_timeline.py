"""Tests for checkin_timeline module

Feel free to add more tests as you see fit.

"""
import random

from datetime import datetime, timedelta

from checkin import CheckIn
from checkin_timeline import CheckInTimeline
from pokeball import Pokeball


def random_timed_checkins(count=100):
    """A helper function that returns CheckIns with random times

    Note that the names and locations will all be the same.

    :param int count: The number of CheckIns to return

    :return: a list of CheckIn instances in a random order.
    """
    # Generate a list of random, unique CheckIns
    checkins = []
    time = datetime.fromtimestamp(0)
    for _ in range(count):
        time += timedelta(minutes=random.randint(1, 59))
        c = CheckIn("Bob", Pokeball.poke_ball, "Pokemart", str(time))
        checkins.append(c)

    # Shuffle up the CheckIns
    random.shuffle(checkins)

    return checkins


def random_timed_checkin_timeline(count=100):
    """A helper function that returns an CheckInTimeline that contains
    CheckIns with random times.

    Note that the names and locations will all be the same.

    :param int count: The number of CheckIns in the CheckInTimeline

    :return: An CheckInTimeline with ``count`` CheckIns with
        random times.

    """
    # Generate some checkins
    checkins = random_timed_checkins(count)

    # Add the checkins to our timeline
    timeline = CheckInTimeline()
    for t in checkins:
        timeline.add(t)

    return timeline


def test_add():
    """Test that adding more CheckIns keeps them in order."""
    # Generate checkins with random times
    timeline = random_timed_checkin_timeline()

    # Check that our checkins are in order
    # (Go look up zip())
    for prev, current in zip(timeline.checkins, timeline.checkins[1:]):
        assert prev.time < current.time


def test_window():
    """Test that our window generator respects window_size."""
    # Generate checkins with random times
    timeline = random_timed_checkin_timeline()

    # Defaults to one hour
    for window in timeline.windows():
        # Gotta be a tuple, though we don't know the length
        assert isinstance(window, tuple)
        assert len(window) > 0

        # Check the types
        for o in window:
            assert isinstance(o, CheckIn)

        # Double check that CheckIns in the window are sorted (for fun)
        for o1, o2 in zip(window, window[1:]):
            assert o1 < o2

        # Make sure each member is within an hour of the first.
        # We know they're sorted, so just check first and last.
        assert (window[0].time + timedelta(hours=1)) > window[-1].time


def test_rendezvous():
    """Test our rendezvous generator"""
    timeline = CheckInTimeline()
    timeline.add(CheckIn("Alice",
                         Pokeball.poke_ball,
                         "Pokemart",
                         "1970-01-02 02:53:00"))

    timeline.add(CheckIn("Bob",
                         Pokeball.poke_ball,
                         "Pokemart",
                         "1970-01-02 03:52:00"))

    for i, agent_pair in enumerate(timeline.rendezvous()):
        # Gotta be a tuple of length 2
        assert isinstance(agent_pair, tuple)
        assert len(agent_pair) == 2

        # Unpack 'em
        a1, a2 = agent_pair

        # Check the types
        assert isinstance(a1, CheckIn)
        assert isinstance(a2, CheckIn)

        # Check that we've got our agents
        assert "Alice" in (a1.name, a2.name)
        assert "Bob" in (a1.name, a2.name)

    # We only looped one time, so 'i' was set to zero, and that's it.
    assert i == 0
