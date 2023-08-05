# -*- coding: utf-8 -*-

#from distutils.core import setup
from setuptools import setup

setup(
  name='py_support',
  packages=['py_support'],
  version='1.2',
  description='A small webdev support lib',
  author='Root Kid',
  author_email='shaman@born2fish.ru',
  url='https://github.com/r00tkid/py_support.git',
  download_url='https://github.com/r00tkid/py_support/tarball/1.2',
  keywords=['support', 'logging', 'webdev'],  # keywords
  classifiers=[],
  install_requires=[
      "colored",
      "termcolor",
      "python-telegram-bot",
      "emoji",
  ],
  )

