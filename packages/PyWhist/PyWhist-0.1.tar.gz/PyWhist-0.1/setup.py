#!/usr/bin/python3

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(name = 'PyWhist',
      version = '0.1',
      author = 'Andrew Warshall',
      author_email = 'warshall@99main.com',
      packages = find_packages(),
      entry_points = {'gui_scripts': ['bridge = pywhist.bridge:main']},
      description = 'A rather primitive bridge game',
      license = 'Eclipse Public License',
      url = 'http://practicealgebra.net/pywhist',
      classifiers = ['Development Status :: 3 - Alpha',
                     'Intended Audience :: End Users/Desktop',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python :: 3',
                     'Topic :: Games/Entertainment',
                     'License :: OSI Approved'])
