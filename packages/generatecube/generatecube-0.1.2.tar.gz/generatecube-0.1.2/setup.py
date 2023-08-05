#!/usr/bin/env python

from setuptools import setup

version = '0.1.2'

setup(name='generatecube',
      version=version,
      description='create scripts to launch gcubegen09d for each orbital independently to a gridengine queue',
      author='Davide Olianas',
      author_email='ubuntupk@gmail.com',
      packages=['cube'],
      entry_points={
            'console_scripts': [
                  'createcubegen=cube.cube:main']
      },
      requires=['pystache'],
      include_package_data=True
     )

