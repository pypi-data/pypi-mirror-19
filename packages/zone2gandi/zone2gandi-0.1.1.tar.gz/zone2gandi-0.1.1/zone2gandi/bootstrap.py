# -*- coding: utf-8 -*-

"""zone2gandi.zone2gandi: provides entry point main()."""

__version__ = "0.1.0"

import sys
from .stuff import Stuff

def main():
    print("Executing bootstrap version %s." % __version__)
    print("List of argument strings: %s" % sys.argv[1:])
    print("Stuff and Boo():\n%s\n%s" % (Stuff, Boo()))


class Boo(Stuff):
    pass
