#!/usr/bin/env python
import sys
from setuptools import setup


# make sure we run Python 3+ here
if sys.version_info.major < 3:
    sys.stderr.write('Sorry, eboxbw needs Python 3\n')
    sys.exit(1)


import delicolour


setup(name='delicolour',
      version=delicolour.__version__,
      description='colour finder',
      author='Philippe Proulx',
      author_email='eeppeliteloop@gmail.com',
      url='https://github.com/eepp/delicolour',
      packages=['delicolour'],
      package_data={
          'delicolour': [
              'res/*.png',
          ],
      },
      install_requires=[
          'colormath>=3',
      ],
      entry_points={
          'gui_scripts': [
              'delicolour = delicolour.main:run'
          ]
      })
