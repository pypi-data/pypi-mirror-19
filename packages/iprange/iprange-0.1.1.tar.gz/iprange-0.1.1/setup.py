#!/usr/bin/python3

from setuptools import setup

setup(
  name='iprange',
  version='0.1.1',
  description='IP-Range generator',
  author='Philip Stoop',
  author_email='stoop497@gmail.com',
  url='https://github.com/stoop4/py_iprange',
  py_modules=['iprange'],
  entry_points = {'console_scripts': ['iprange=iprange:main']}
)
