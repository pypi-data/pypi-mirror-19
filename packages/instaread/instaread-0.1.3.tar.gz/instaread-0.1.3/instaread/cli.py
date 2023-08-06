#!/usr/bin/env python
'''instaread

Usage:
  instaread [--archive][--force]
  instaread putback
  instaread folders
  instaread unreads
  instaread archiveds
  instaread -h | --help
  instaread --version

Options:
  -h --help     Show this screen.
                Open last unread
  --archive     Open last unread and archive it
  --force       Force refresh token and secret
  --version     Show version.
'''
from docopt import docopt
import sys
from .instaread import AppException
from .instaread import login
from .instaread import sync
from .instaread import read_last_synced_bookmark
from .instaread import copy_read_assets
from .instaread import folders, unreads, archiveds
from .instaread import put_back

__version__ = "0.1.3"
__author__ = "Dat Truong"
__license__ = "MIT"


def main():
    '''Main entry point for the instaread CLI.'''
    args = docopt(__doc__, version=__version__)
    should_archive = args['--archive']
    should_force = args['--force']
    login(forced=should_force)

    if args['putback']:
        put_back()
        return

    if args['folders']:
        folders()
        return

    if args['unreads']:
        unreads()
        return

    if args['archiveds']:
        archiveds()
        return

    copy_read_assets()
    sync()
    read_last_synced_bookmark(should_archive=should_archive)


if __name__ == '__main__':
    try:
        main()
    except AppException as err:
        print("{}: {}".format(type(err).__name__, err))
        sys.exit()
