"""Git Conflict Finder

Usage:
  find_conflicts <repository>
  find_conflicts (-h | --help)

Options:
  -h --help     Show this screen
"""

import docopt

from . import repository


def main():
    arguments = docopt.docopt(__doc__)
    repo = repository.load_repository(arguments["repository"])
