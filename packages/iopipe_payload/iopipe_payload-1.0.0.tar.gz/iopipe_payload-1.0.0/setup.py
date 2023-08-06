#!/usr/bin/env python

from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import setup, find_packages

install_reqs = parse_requirements('./requirements.txt', session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(name='iopipe_payload',
      version='1.0.0',
      description='IOpipe payload schema & normalization library',
      author='IOpipe',
      author_email='support@iopipe.com',
      url='https://github.com/iopipe/iopipe-payload',
      packages=find_packages(),
      install_requires=reqs,
      setup_requires=[
          "flake8"
      ],
      extras_require={
          'dev': [
              'flake8'
          ]
      }
     )
