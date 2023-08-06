#!/usr/bin/env python

from pip.download import PipSession
from setuptools import setup, find_packages

setup(name='iopipe_payload',
      version='1.0.2',
      description='IOpipe payload schema & normalization library',
      author='IOpipe',
      author_email='support@iopipe.com',
      url='https://github.com/iopipe/iopipe-payload',
      packages=find_packages(),
      setup_requires=[
          "flake8"
      ],
      extras_require={
          'dev': [
              'flake8'
          ]
      }
     )
