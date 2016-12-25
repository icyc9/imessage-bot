#!/usr/bin/env python

import os
from setuptools import find_packages, setup

ENCODING = 'utf-8'
PACKAGE_NAME = 'pyimessage'


def get_requirements(requirement_file):
    requirements = list(
        open(requirement_file, 'r',
             encoding=ENCODING).read().strip().split('\r\n'))
    return requirements


setup(name=PACKAGE_NAME,
      packages=find_packages(exclude=('tests',)),
      package_data={
          '': ['*.txt', '*.sql', '*.json'],
      },
      include_package_data=True,
      license='BSD',
      description='Python imessage client',
      url='https://github.com/RobertChristopher/py-imessage.git',
      author='Robert Christopher',
      author_email='rob@icylabs.io',
      install_requires=get_requirements('requirements.txt'),
      scripts=['config.py'],
      zip_safe=False)