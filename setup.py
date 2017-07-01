#!/usr/bin/env python

from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession

requirements = [i.strip() for i in open("requirements.txt").readlines()]

setup(name='rocket_telemetry',
      version='0.1',
      description='Collect rocket telemetry and store it in the cloud',
      author='Al Little',
      url='https://github.com/al-little/rocket_telemetry',
      install_requires=requirements)
