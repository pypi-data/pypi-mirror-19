import gnureadline
import sys
import os

"""For offering tab completion."""

class Completer:
  """For offering tab completion.

  If present, uses vocab list for completion;
  Otherwise uses filesystem paths.
  """

  vocab_list = None
  """list of strings"""

  def set_vocab_list(self, vocab_list_in = None):
    """Sets vocab_list, activates tab completion."""
    self.vocab_list = vocab_list_in
    gnureadline.parse_and_bind('tab: complete')
    # Space must not be a delimiter since building names etc. can have spaces in them, and one is always specified
    gnureadline.set_completer_delims('\t\n`!@#$%^&*()-=+[{]}\\|;:\'",<>?')
    gnureadline.set_completer(self.completer)

  def set_path_completion(self):
    """Sets vocab_list to Nonw, activates tab completion."""
    self.vocab_list = None
    gnureadline.parse_and_bind('tab: complete')
    # Space must be a delimiter so that multiple docs can be specified
    gnureadline.set_completer_delims(' \t\n`!@#$%^&*()-=+[{]}\\|;:\'",<>?') 
    gnureadline.set_completer(self.completer)
    
  def deactivate(self):
    """Deactivates tab completion."""
    vocab_list = None
    gnureadline.parse_and_bind('tab: self-insert')

  def list_from_path(self, path):
    """Generates a list of possible completion strings from part of a path."""
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
    """Function passed to gnureadline for tab completion."""
    if self.vocab_list:
      options = [x for x in self.vocab_list if x.lower().startswith(text.lower())]
      return options[state]
    options = [x for x in self.list_from_path(text) if x.startswith(os.path.expanduser(text))]
    return options[state]
