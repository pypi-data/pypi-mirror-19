# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='mprint-assistant', 
      version='0.0',
      description='Easy printing to U of M printers',
      long_description=long_description,
      author='Sam Adams',
      author_email='sam.h.adams@gmail.com',
      url='https://github.com/samharad/mprint-assistant',
      license='MIT',
      packages=['mprintassistant'],
      entry_points = {
        'console_scripts': ['mprint = mprintassistant.mprintassistant:main']
        },
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Printing'
        ],
      keywords='Michigan print mprint',
      install_requires=['colorama',
                        'requests',
                        'readline',
                        'argparse',
                        'future'
                        ] 
      )
