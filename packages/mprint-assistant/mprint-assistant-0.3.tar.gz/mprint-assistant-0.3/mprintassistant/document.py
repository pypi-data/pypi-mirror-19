"""For representing documents."""

class Document:
  """For representing documents."""

  VALID_EXTENSIONS = ('.ai', '.bmp', '.c', '.cpp', '.csv', '.doc', '.docx', 
                      '.eps', '.gif', '.h', '.ico', '.jp2', '.jpeg', '.jpg', 
                      '.m', '.odf', '.pdf', '.php', '.png', '.pps', '.ppsx', 
                      '.ppt', '.pptx', '.ps', '.psd', '.py', '.rtf', '.tif', 
                      '.tiff', '.txt', '.xls', '.xlsx', '.xml', '.xps')

  PORTRAIT = 'portrait'
  LANDSCAPE = 'landscape'

  TWO_SIDED_LONG = 'two-sided-long-edge'
  TWO_SIDED_SHORT = 'two-sided-short-edge'
  ONE_SIDED = 'one-sided'

  LETTER = 'letter'
  TABLOID = 'tabloid'
  CUSTOM = 'custom'

  ON = 'on'
  OFF = 'off'

  filePath = None
  params = {'copies': 1, 
            'scale': ON, 
            'sides': TWO_SIDED_LONG, 
            'range': None, 
            'orientation': PORTRAIT,
            'size': LETTER,
            'size_length': None,
            'size_width': None
            }

  def __init__(self, filePathIn):
    self.filePath = filePathIn
      
  def __str__(self):
    return self.filePath
