# -*- coding: utf-8 -*-

# from distutils.core import setup
from setuptools import setup, find_packages

setup(
  name = 'testpackageal',
  packages = find_packages(), # this must be the same as the name above
  version = '0.7',
  description = 'This is my first package.',
  author = 'Angel Lagunas',
  author_email = 'angel.david.lagunas@gmail.com',
  url = 'https://github.com/angellagunas/testpackageal', # use the URL to the github repo
  download_url = 'https://github.com/angellagunas/testpackageal/tarball/0.7', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
)
