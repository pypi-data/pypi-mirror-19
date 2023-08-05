#! /usr/bin/env python

import sys
from .printsession import PrintSession
from .document import Document
from colorama import init as colorama_init

# TODO
# Test floor code flags -- add more shortcut flags -- try to minimize the minimum input
  # flag for color printing, tabloid flag
  # building specifier flag, and floor number? 
# Add way to print code cheat sheet?

def main(): 
  try:
    # Lets colored output work on Windows
    colorama_init()
    # Create new session; authenticates, populates menu
    session = PrintSession()
    # Determine printer
    session.determineDestination()
    # Determine documents
    session.determineDocs()
    # Print documenrs
    session.printDocs()
  except KeyboardInterrupt:
    sys.exit()


# if __name__ == "__main__":
  # main()
