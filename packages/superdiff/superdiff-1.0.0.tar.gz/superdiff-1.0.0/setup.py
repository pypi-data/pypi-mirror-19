#! /usr/bin/env python3

from setuptools import setup

setup(name='superdiff',
      version='1.0.0',
      description='A library for performing flexible diff checks.',
      long_description=('This library currently requires Python 3.5+. '
                        'Documentation can be found at '
                        'http://superdiff.readthedocs.io/en/latest/'),
      author='James Perretta',
      author_email='jameslp@umich.edu',
      license='GNU Lesser General Public License v3',
      url='https://github.com/james-perretta/superdiff',
      packages=['superdiff'],
      install_requires=[],
      classifiers=[
          'Programming Language :: Python :: 3.5',
      ])
