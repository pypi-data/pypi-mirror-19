# -*- mode: python; coding: utf-8 -*-
"""tickler.py

Tickler can be used to create a tickler directory structure
automatically on the filesystem. It provides a utility function for
building tickler compatible file paths from a standard datetime
object. This function can also be accessed for scripting purposes by
using the --get-path argument and passing a dateutil compatible date
string.

"""

from argparse import ArgumentParser
from datetime import datetime
from dateutil.parser import parse
from isoweek import Week
from os import makedirs
from os.path import abspath
from os.path import join
import calendar
import sys

__version__ = "1.0.2a"
__all__ = ["get_path_for_datetime"]


def get_path_for_datetime(parentdir, date_time):
    return get_tickler_path(parentdir, Week.withdate(date_time))


def get_tickler_path(parentdir, week):
    month = week.monday().month
    year, week_number =  week.year_week()
    month_name = calendar.month_name[month].lower()
    quarter = ((month - 1) // 3) + 1
    path_args = [
        abspath(parentdir),
        str(year),
        "q%s" % quarter,
        "%d-%s" % (month, month_name),
        "week%s" % week_number
    ]
    return join(*path_args)


def parse_args(argv):
    current_year = datetime.now().year
    parser = ArgumentParser(prog="tickler", description="Creates a tickler-file style directory tree")
    parser.add_argument("parentdir", default=".", action="store", type=str,
                        help="The parent directory to create the tickler in")
    parser.add_argument("--year", required=False, action="store", type=int, default=current_year,
                        help="The year to create the tickler for")
    parser.add_argument("--dry-run", required=False, action="store_true", default=False,
                        help="Use this option to see the output without actually creating the directories")
    parser.add_argument("--get-path", required=False, action="store", type=str,
                        help="Pass any reasonably formatted date string and tickler will print out the tickler file path for it. Useful for scripting")
    return parser.parse_args(argv[1:])


def create_tickler_tree(parsed_args):
    for week in Week.weeks_of_year(parsed_args.year):
        tickler_path = get_tickler_path(parsed_args.parentdir, week)
        print("Creating directory: %s" % tickler_path)
        if not parsed_args.dry_run:
            makedirs(tickler_path)


def print_tickler_path(parsed_args):
    print(get_tickler_path(parsed_args.parentdir,
                           Week.withdate(parse(parsed_args.get_path))))


def main():
    parsed_args = parse_args(sys.argv)
    if parsed_args.get_path:
        print_tickler_path(parsed_args)
    else:
        create_tickler_tree(parsed_args)

if __name__ == "__main__":
    main()
