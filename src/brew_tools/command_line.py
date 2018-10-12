
import click

import sys
import logging

from brew_tools import __version__

__author__ = "Sven Steinbauer"
__copyright__ = "Sven Steinbauer"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def main(args):
    print("HELLO WORLD")


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
