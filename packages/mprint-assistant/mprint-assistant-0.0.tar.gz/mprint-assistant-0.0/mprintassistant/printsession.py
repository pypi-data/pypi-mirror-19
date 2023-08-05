import sys
import os
import json
from .settings import webloginBaseURL, userBaseURL, guestBaseURL  # Base URLs
import requests # Request library for interacting with API
from getpass import getpass # Allows password entry
from .document import Document
from .utils import getSelection, prompt, color_by_status, parse
import readline
from .completer import Completer, readline_init
from .colorizer import Colorizer
from builtins import input # So that Python 2 and 3 can both call input()

class PrintSession:
  # A printSession has a completer
  completer = Completer()

  # A printSession has a requestsSession for communicating with API
  session = requests.Session()

  # A print session has a buildings menu 
  buildings = None
  # A print session has a floors menu (populated after building selection)
  floors = None
  # A print session has a queues menu (populated after floor selection)
  queues = None

  # Building obj for user's desired building
  building = None
  # Floor obj for user's desired floor; within building 
  floor = None
  # Queue obj for user's desired floor
  queue = None

  # Print session has list of Document objects
  documents = []

  # Dictionary; Print session has command line arguments:
  # building 
  # noscale
  # documents ------- list
  # copies ---------- list
  # floorId
  # one
  # range ------------ list
  # short
  # landscape
  sysArgs = None

  def __init__(self):
    self.populateMenus()
    self.setSysArgs(vars(parse()))
    self.interpretSysArgs()
    self.authenticate()

  def setSysArgs(self, sysArgsIn):
    self.sysArgs = sysArgsIn

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

    if self.sysArgs['floorId']:
      self.floor = list(filter(lambda dict: dict['id'] == self.sysArgs['floorId'], self.floors['result']))[0]
      if not self.floor:
        sys.exit('Could not find specified floor ID.')
      buildingId = self.floor['building_id']
      self.building = list(filter(lambda dict: dict['id'] == buildingId, self.buildings['result']))[0]

  def authenticate(self):
    response = self.session.get(webloginBaseURL)
    Completer.set_no_complete()
    response = self.session.post(webloginBaseURL, 
                                 data={'login':input(prompt('Enter username: ')), 
                                 'password':getpass(prompt=prompt('Enter password: '))}, 
                                 allow_redirects=False)

    # Redirect code means successful login
    if response.status_code != 302:
      sys.exit('Invalid credentials.')
   
  def populateMenus(self):
    # Populates buildings menu
    responseBuildings = self.session.get(guestBaseURL + 'buildings')
    if responseBuildings.status_code != 200:
      sys.exit('Could not retrieve buildings')
    self.buildings = responseBuildings.json()

    # Populates floors menu with all floors TODO this is unneccessary?
    responseFloors = self.session.get(guestBaseURL + 'floors')
    if responseFloors.status_code != 200:
      sys.exit('Could not retrieve floors')
    self.floors = responseFloors.json()

  def determineBuilding(self):
    possibleBuildings = []
    # readline.set_completer(Completer([x['name'] for x in self.buildings['result']]).completer)
    # readline.parse_and_bind('tab: complete')
    self.completer.set_vocab_list([x['name'] for x in self.buildings['result']])
    inputString = input(prompt('Enter building name: '))
    for dictionary in self.buildings['result']:
      if inputString.lower() in dictionary['name'].lower():
        possibleBuildings.append(dictionary)
    if len(possibleBuildings) == 1:
      self.building = possibleBuildings[0]
      return
    self.building = getSelection('Select building', possibleBuildings, 'name', 'id')

  def determineFloor(self):
    possibleFloors = self.session.get(userBaseURL + 'floors', 
                                      params={'buildingId':self.building['id']}).json()['result']
    self.completer.deactivate()
    self.floor = getSelection('Select floor', possibleFloors, 'name', 'id')

  def determineQueue(self):
    possibleQueues = self.session.get(userBaseURL + 'queues', 
                                      params={'floor':self.floor['id']}).json()['result']
    self.completer.deactivate()
    self.queue = getSelection('Select printer', possibleQueues, 'display_name', 'model_name', 'color', 'tabloid')

  def determineDocs(self):
    if not self.documents:
      # readline.set_completer(Completer().completer)
      # readline.parse_and_bind('tab: complete')
      self.completer.set_path_completion()
      doc_strings = input(prompt('Enter document paths separated by spaces: ')).split()
      for doc_string in doc_strings:
        if not os.path.isfile(doc_string):
          sys.exit('\'' + doc_string + '\' is not a file')
        self.documents.append(Document(doc_string))

  def printDocs(self):
    self.summarizeJob()
    for doc in self.documents:
      doc_file = {'file': open(doc.filePath, 'rb')}
      doc_params = doc.params 
      doc_params['queue'] = self.queue['name']
      printStatus = self.session.post(userBaseURL + 'jobs', files=doc_file, params=doc_params).json()
      print(os.path.basename(doc.filePath) + ": " + color_by_status(printStatus['status']))

  def summarizeJob(self):
    print("Building: " + self.building['name'])
    print("Floor: " + self.floor['name'])
    print("Queue: " + self.queue['display_name'])
    print("Documents: ") 
    for doc in self.documents:
      print(doc) 
    # readline.set_completer(None)
    # readline.parse_and_bind('tab: self-insert')
    self.completer.deactivate()
    response = input(prompt("Press enter to continue")) # TODO

  def determineDestination(self):
    while not self.building:
      self.determineBuilding()
    while not self.floor:
      self.determineFloor()
    while not self.queue:
      self.determineQueue()
