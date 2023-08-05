class Colorizer:
  HEADER = '\033[95m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  END = '\033[0m'

  @classmethod
  def colorize(cls, string, color):
    if color == 'bold':
      return cls.BOLD + string + cls.END
    elif color == 'underline':
      return cls.UNDERLINE + string + cls.END
    elif color == 'green':
      return cls.GREEN + string + cls.END
    elif color == 'red':
      return cls.RED + string + cls.END

