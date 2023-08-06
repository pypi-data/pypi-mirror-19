#-*- encoding: UTF-8 -*-
from setuptools import setup, find_packages
import sys, os

VERSION = '0.1.0'

with open('README.md') as f:
    long_description = f.read()

setup(
      name='drawbox',
      version=VERSION,
      description="a tiny handy cli tool for drawing stack-like box",
      long_description=long_description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ascii-art',
      author='c4pt0r',
      author_email='i@huangdx.net',
      license='MIT',
      packages=['drawbox'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
      ],
      entry_points={
        'console_scripts':[
            'drawbox  = drawbox:main' 
        ]
      },
)
