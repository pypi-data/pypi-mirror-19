import sys
import os
import json
from .settings import webloginBaseURL, userBaseURL, guestBaseURL  # Base URLs
import requests # Request library for interacting with API
from getpass import getpass # Allows password entry
from .document import Document
from .utils import getSelection, prompt, color_by_status, parse, make_acronym
import gnureadline
from .completer import Completer 
from builtins import input # So that Python 2 and 3 can both call input()

"""Represents a printing session.

A printing session is an authenticated session during which
the user sends a set of documents to be printed.
"""

class PrintSession:
  """Represents a printing session.

  A printing session is an authenticated session during which
  the user sends a set of documents to be printed.
  """

  completer = Completer()
  """For building and path tab completion."""

  session = requests.Session()
  """For communicating with API."""

  buildings = None
  """json object: Buildings menu."""
  floors = None
  """json object: Floors menu"""
  queues = None
  """json object: Queues menu"""

  building = None
  """json object: User's selected building"""
  floor = None
  """json object: User's selected floor"""
  queue = None
  """json object: User's selected queue"""

  documents = []
  """List of Documents to be printed."""

  sysArgs = None
  """dictionary: sys arguments.
  documents (list)
  buildingId
  floorId
  landscape
  range (list)
  copies (list)
  one
  short
  noscale
  quick
  color
  tabloid
  """

  def __init__(self):
    """Initializes a print session.
    
    Populates menus, parses and interprests sys args, authenticates user.
    """
    self.populateMenus()
    self.sysArgs = vars(parse())
    self.interpretSysArgs()
    self.authenticate()

  def interpretSysArgs(self):
    # Sets Document params based on sys args
    if self.sysArgs['landscape']:
      Document.params['orientation'] = Document.LANDSCAPE
    if self.sysArgs['one']:
      Document.params['sides'] = Document.ONE_SIDED
    if self.sysArgs['short']:
      Document.params['sided'] = Document.TWO_SIDED_SHORT
    if self.sysArgs['noscale']:
      Document.params['scale'] = Document.OFF;
    if self.sysArgs['range']: 
      if len(self.sysArgs['range']) != len(self.sysArgs['documents']):
        sys.exit('If specifying ranges, must do so for all documents')
    if self.sysArgs['copies']: 
      if len(self.sysArgs['copies']) != len(self.sysArgs['documents']):
        sys.exit('If specifying copies, must do so for all documents')

    # Checks that documents exist and appends them to documents with ranges and copies
    if self.sysArgs['documents']:
      for i, pathIn in enumerate(self.sysArgs['documents']):
        if not os.path.isfile(pathIn):
          sys.exit('\'' + pathIn + '\' is not a file.')
        if not pathIn.lower().endswith(Document.VALID_EXTENSIONS):
          sys.exit('Invalid file extension')
        doc = Document(pathIn)
        if self.sysArgs['copies']:
          if not self.sysArgs['copies'][i].isdigit():
            sys.exit('Copy arguments must be integers')
          doc.params['copies'] = int(self.sysArgs['copies'][i])
        if self.sysArgs['range']:
          start, end = self.sysArgs['range'][i].split('-')
          if not start.isdigit() or not end.isdigit() or int(end) < int(start):
            sys.exit('Range arguments must be of form \'a-b c-d...\'')
          doc.params['range'] = self.sysArgs['range'][i]
        self.documents.append(doc)

    # Populates building selection
    if self.sysArgs['buildingId']:
      try:
        self.building = list(filter(lambda dict: dict['id'] == self.sysArgs['buildingId'], self.buildings['result']))[0]
        if not self.building:
          sys.exit('Could not find specified building ID.')
      except IndexError:
        sys.exit('Could not find specified building.')

    # Populates floor selection
    if self.sysArgs['floorId']:
      try:
        self.floor = list(filter(lambda dict: dict['id'] == self.sysArgs['floorId'], self.floors['result']))[0]
        if not self.floor:
          sys.exit('Could not find specified floor ID.')
        buildingId = self.floor['building_id']
        self.building = list(filter(lambda dict: dict['id'] == buildingId, self.buildings['result']))[0]
      except IndexError:
        sys.exit('Could not find specified floor.')

  def authenticate(self):
    try:
      response = self.session.get(webloginBaseURL)
      self.completer.deactivate()
      response = self.session.post(webloginBaseURL, 
                                   data={'login':input(prompt('Enter username: ')), 
                                   'password':getpass(prompt=prompt('Enter password: '))}, 
                                   allow_redirects=False)

      # Redirect code means successful login
      if response.status_code != 302:
        sys.exit('Invalid credentials.')
    except KeyboardInterrupt:
      sys.exit()
    except requests.exceptions.RequestException:
      sys.exit('Problem calling mprint API. Check internet connection.')
   
  def populateMenus(self):
    try:
      # Populates buildings menu
      responseBuildings = self.session.get(guestBaseURL + 'buildings')
      if responseBuildings.status_code != 200:
        sys.exit('Could not retrieve buildings')
      self.buildings = responseBuildings.json()

      # Populates floors menu
      responseFloors = self.session.get(guestBaseURL + 'floors')
      if responseFloors.status_code != 200:
        sys.exit('Could not retrieve floors')
      self.floors = responseFloors.json()
    except KeyboardInterrupt:
      sys.exit()
    except requests.exceptions.RequestException:
      sys.exit('Problem calling mprint API. Check internet connection.') 

  def determineBuilding(self):
    """Determines user's desired building."""
    possibleBuildings = []
    self.completer.set_vocab_list([x['name'] for x in self.buildings['result']])
    inputString = input(prompt('Enter building name: '))
    for dictionary in self.buildings['result']:
      if inputString.lower() in dictionary['name'].lower() or inputString.lower() in dictionary['id'].lower() or inputString.lower() in make_acronym(dictionary['name']).lower():
        possibleBuildings.append(dictionary)
    if len(possibleBuildings) == 1:
      self.building = possibleBuildings[0]
      return
    self.building = getSelection('Select building', possibleBuildings, 'name', 'id')

  def determineFloor(self):
    """Determines user's desired floor."""
    try:
      possibleFloors = self.session.get(userBaseURL + 'floors', 
                                        params={'buildingId':self.building['id']}).json()['result']
      self.completer.deactivate()
      self.floor = getSelection('Select floor', possibleFloors, 'name', 'id')
      # If none selected, reset building choice too
      if not self.floor:
        self.building = None
    except KeyboardInterrupt:
      sys.exit()
    # except:
    except requests.exceptions.RequestException:
      sys.exit('Problem calling mprint API. Check internet connection.') 

  def determineQueue(self):
    """Determines user's desired queue."""
    try:
      p = {'floor':self.floor['id']}
      if self.sysArgs['color']:
        p['color'] = ""
      if self.sysArgs['tabloid']:
        p['tabloid'] = ""
      possibleQueues = self.session.get(userBaseURL + 'queues', 
                                        params=p).json()['result']
      self.completer.deactivate()
      if len(possibleQueues) == 1:
        self.queue = possibleQueues[0]
        return
      self.queue = getSelection('Select printer', possibleQueues, 'display_name', 'model_name', 'color', 'tabloid')
      # If none selected, reset floor choice too
      if not self.queue:
        self.floor = None
    except KeyboardInterrupt:
      sys.exit()
    except requests.exceptions.RequestException:
      sys.exit('Problem calling mprint API. Check internet connection.') 

  def determineDocs(self):
    """Determines documents to be printed."""
    if not self.documents:
      self.completer.set_path_completion()
      doc_strings = input(prompt('Enter document paths separated by spaces: ')).split()
      for doc_string in doc_strings:
        if not os.path.isfile(doc_string):
          sys.exit('\'' + doc_string + '\' is not a file')
        self.documents.append(Document(doc_string))

  def printDocs(self):
    try:
      self.summarizeJob() # Blocks until user input
      for doc in self.documents:
        doc_file = {'file': open(doc.filePath, 'rb')}
        doc_params = doc.params 
        doc_params['queue'] = self.queue['name']
        printStatus = self.session.post(userBaseURL + 'jobs', files=doc_file, params=doc_params).json()
        print(os.path.basename(doc.filePath) + ": " + color_by_status(printStatus['status']))
    except KeyboardInterrupt:
      sys.exit()
    except requests.exceptions.RequestException:
      sys.exit('Problem calling mprint API. Check internet connection.') 

  def summarizeJob(self):
    print("Building: " + self.building['name'])
    print("Floor: " + self.floor['name'])
    print("Queue: " + self.queue['display_name'])
    print("Documents: ") 
    for doc in self.documents:
      print(doc) 
    self.completer.deactivate()
    if not self.sysArgs['quick']:
      response = input(prompt("Enter nothing to continue, anything to quit: ")) 
      if response != "":
        sys.exit()

  def determineDestination(self):
    """Determines building, floor, queue."""
    while not self.building or not self.floor or not self.queue:
      if not self.building:
        self.determineBuilding()
      if self.building and not self.floor:
        self.determineFloor()
      if self.building and self.floor and not self.queue:
        self.determineQueue()
