"""
hooks - git hooks

Usage:
    hooks install
    hooks ls
    hooks update
"""

from docopt import docopt


__version__ = '0.1'


def install(args):
    pass


def update(args):
    pass


def ls(args):
    pass


def dispatch(arguments):
    if arguments['install']:
        install(arguments)
    elif arguments['update']:
        update(arguments)
    elif arguments['ls']:
        ls(arguments)


def cli():
    arguments = docopt(__doc__, version=__version__)
    dispatch(arguments)