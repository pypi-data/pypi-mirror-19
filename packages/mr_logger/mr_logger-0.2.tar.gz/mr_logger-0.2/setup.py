# -*- coding: utf-8 -*-

#from distutils.core import setup
from setuptools import setup

setup(
  name='mr_logger',
  packages=['mr_logger'],
  version='0.2',
  description='Small colored logger',
  author='Root Kid',
  author_email='shaman@born2fish.ru',
  url='https://github.com/r00tkid/mr_logger.git',
  download_url='https://github.com/r00tkid/mr_logger/tarball/0.2',
  keywords=['support', 'logging', 'webdev'],  # keywords
  classifiers=[],
  install_requires=[
      "termcolor",
      'colored',
  ],
)

