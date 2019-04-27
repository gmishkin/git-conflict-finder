"""Git Conflict Finder

Usage:
  find_conflicts [options] <repository>
  find_conflicts (-h | --help)

Options:
  -h --help               Show this screen
  --base-branch=<name>    Name of the branch trying to merge into [default: master]
  --days=<number>         Don't consider other branches older than this many days [default: 7]
"""

import datetime

import docopt

from . import repository


def main():
    arguments = docopt.docopt(__doc__)
    repo = repository.load_repository(
        arguments["<repository>"],
        arguments['--base-branch'],
        datetime.timedelta(days=int(arguments["--days"]))
    )
    branches = repo.filter_branches()
    print(branches)
