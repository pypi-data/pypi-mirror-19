#!/usr/bin/env python

from setuptools import setup, find_packages
import os.path


setup(name='tap-referral-saasquatch',
      version='0.1.3',
      description='Taps Referral SaaSquatch data',
      author='Stitch',
      url='https://github.com/stitchstreams/tap-referral-saasquatch',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_referral_saasquatch'],
      install_requires=[
          'stitchstream-python>=0.5.0',
          'requests==2.12.4',
          'backoff==1.3.2',
          'python-dateutil==2.6.0',
      ],
      entry_points='''
          [console_scripts]
          tap-referral-saasquatch=tap_referral_saasquatch:main
      ''',
)
