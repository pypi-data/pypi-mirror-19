#!/usr/bin/env python

from setuptools import setup

setup(name='MqHelper',
      version='1.2.0',
      description='Message-Queue Helper for Mosquitto',
      author='Paul Klingelhuber',
      author_email='paul@paukl.at',
      url='https://github.com/nousername/MqHelper',
      license='BSD',
      package_dir = {'':'package'},
      py_modules = ['MqHelper'],
      install_requires=[
      	'paho-mqtt>=1.1'
      ]
     )