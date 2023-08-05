#! /usr/bin/env python

import sys
from .printsession import PrintSession
from .document import Document
from colorama import init as colorama_init

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

