import readline
import sys
import os

class Completer:
  vocab_list = None

  # def __init__(self, vocab_list_in = None):
    # self.vocab_list = vocab_list_in

  def set_vocab_list(self, vocab_list_in = None):
    self.vocab_list = vocab_list_in
    readline.parse_and_bind('tab: complete')
    # Space must not be a delimiter since building names etc. can have spaces in them, and one is always specified
    readline.set_completer_delims('\t\n`!@#$%^&*()-=+[{]}\\|;:\'",<>?')
    readline.set_completer(self.completer)

  def set_path_completion(self):
    self.vocab_list = None
    readline.parse_and_bind('tab: complete')
    # Space must be a delimiter so that multiple docs can be specified
    readline.set_completer_delims(' \t\n`!@#$%^&*()-=+[{]}\\|;:\'",<>?') 
    readline.set_completer(self.completer)
    
  def deactivate(self):
    vocab_list = None
    readline.parse_and_bind('tab: self-insert')

  def list_from_path(self, path):
    if path.startswith(os.path.sep) or path.startswith('~'): # Absolute path 
      basedir = os.path.dirname(os.path.expanduser(path))
      contents = os.listdir(basedir)
      contents = [os.path.join(basedir, d) for d in contents]
    else: # Relative path
      if os.path.dirname(path) == '': # No directory yet specified
        contents = os.listdir(os.curdir)
      else: # At least one directory specified
        contents = os.listdir(os.path.dirname(path))
        contents = [os.path.join(os.path.dirname(path), d) for d in contents]
    contents = [d + os.path.sep if os.path.isdir(d) else d for d in contents]
    return contents

  def completer(self, text, state):
    if self.vocab_list:
      options = [x for x in self.vocab_list if x.startswith(text)]
      return options[state]
    options = [x for x in self.list_from_path(text) if x.startswith(os.path.expanduser(text))]
    return options[state]

  @staticmethod
  def set_no_complete():
    readline.set_completer(None)
    readline.parse_and_bind('tab: self-insert')
    readline.set_completer_delims(' \t\n`!@#$%^&*()-=+[{]}\\|;:\'",<>?')

def readline_init():
  readline.parse_and_bind('tab: complete')
  readline.set_completer_delims(' \t\n`!@#$%^&*()-=+[{]}\\|;:\'",<>?')

