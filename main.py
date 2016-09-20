import argparse
import csv
import pprint
import sys

from checkin import CheckIn
from checkin_timeline import CheckInTimeline


def load_timeline(filename):
    """Loads a CSV file of Team Rocket agent checkins.

    :param str filename: The name of the CSV file to read

    :returns: A tuple with the following pokemon:

                - A dictionary that maps an agent's name to the
                  Pokemon they stored in their initial Pokeball
                  (based on data in the CSV file).

                - A CheckInTimeline that contains the check-in
                  data loaded from the CSV file.

    :rtype: tuple

    :raises ValueError: If there is an issue unpacking the values of a
        row into name, pokeball type, location, time, and
        pokemon. Note that this is thrown when unpacking too few or
        two many values into a tuple of variables.

    :raises ValueError: If there is an issue loading the time (fourth
        column in each row) into a datetime object.

    :raises ValueError: If there is an issue loading the type of
        Pokeball (second column in each row, stored as the integer
        value of a :class:`Pokeball <pokeball.Pokeball>` enum)

    :raises OSError: If there is an issue finding or opening the
        file. Note that this is thrown by the open() function.

    """
    rocket_data = CheckInTimeline()  # stores empty timeline in rocket_data
    grunt_poke = {}  # stores dict of pokemon indexed by agent names
    try:
        with open(filename) as mew:  # file opened
            rocket_rows = csv.reader(mew)
            for row in rocket_rows:
                try:
                    grunt_row = CheckIn(row[0], row[1], row[2], row[3])
                except ValueError:
                    print("Invalid data! CheckIn could not be created!")
                    sys.exit(1)
                rocket_data.add(grunt_row)
                if row[4] != "":  # i.e. if there's a Pokemon listed
                    grunt_poke[row[0]] = row[4]  # add to dict
    except OSError:
        print("Couldn't find or open the file")
        sys.exit(1)
    return(grunt_poke, rocket_data)


def main(args):
    """Program entry point.

    - Loads a CSV file of checkins

    - Determines how Pokemon were exchanged during various rendezvous

    - Outputs information to the console

      - Prints the exchanges as they happen if desired.

      - Prints the latest agent to be in posession of a *specific*
        pokemon if desired.

      - Otherwise, neatly prints a dictionary mapping agents to the
        pokemon they have carried most recently.

    This program will return an exit code of ``1`` in one of the
    following situations:

    - If the CSV file cannot be opened (i.e., load_timeline raises an
      :class:`OSError`), this program will simply print the exception
      and end.

    - If the CSV file cannot be loaded (i.e., load_timeline raises a
      :class:`ValueError`), we will print an error messsage and end.

    - If the CSV file contains semantically incorrect data (i.e., a
      :class:`DataError <checkin_timeline.DataError>` is raised), we
      will print an error messsage and end.

    :param argparse.Namespace args: A Namespace that contains parsed
        command line arguments.

    :returns: None

    """
    grunt_poke, rocket_data = load_timeline(args.checkins)
    for chkin in rocket_data.rendezvous():

        if chkin[0].pokeball == chkin[1].pokeball:  # pokeball types match
            # Exchange Process Begin
            traded = grunt_poke[chkin[0].name]
            grunt_poke[chkin[0].name] = grunt_poke[chkin[1].name]
            grunt_poke[chkin[1].name] = traded
            # Exchange Process End

            if args.exchanges:  # exchanges flag
                print(chkin[0].name, "meets with", chkin[1].name,
                      "to exchange", grunt_poke[chkin[0].name], "for",
                      grunt_poke[chkin[1].name])
        else:
            if args.skip:  # skip flag
                print(chkin[0].name + " (with", str(chkin[0].pokeball) + ")",
                      "meets with " + chkin[1].name + " (with",
                      str(chkin[1].pokeball) + "),", "but nothing happened.")

    if args.pokemon != "":  # pokemon flag
        for pair in grunt_poke.items():
            if pair[1] == args.pokemon:
                print(pair[0], "had the", pair[1])
    else:
        pprint.pprint(grunt_poke, indent=4)

if __name__ == '__main__':
    # Initialize CLI argument parser
    parser = argparse.ArgumentParser(
        description='Determine rendezvous exchanges based on a '
        'spreadsheet of agent check-ins.'
    )

    # Add a positional argument for the checkins file.
    parser.add_argument('checkins',
                        help='A CSV file to read checkins from.')

    # Add an optional flag, so that the user can tell us which Pokemon
    # they want to see the owner of
    parser.add_argument('--pokemon', type=str, default='',
                        help='Filter to show who has a specific Pokemon')

    # Add an optional flag, that will tell us to print exchanges as
    # they occur (only if an exchange *actually* occurs).
    parser.add_argument('--exchanges', action='store_true',
                        help='Print all exchanges')

    # Add an optional flag, so that the user can tell us if they want
    # to see a message whenever two Team Rocket agents meet, but they
    # **do not** swap Poke Balls.
    parser.add_argument('--skip', action='store_true',
                        help='Print skipped exchanges')

    # Parse the arguments
    args = parser.parse_args()

    # GO!
    main(args)
