#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 14:22:50 2017

@author: Ahmad Albaqsami
"""

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='itermore',
      version='0.1.2',
      description='Additional function(s) to itertools: partial permutation',
      url='http://github.com/atinzad/itermore',
      author='Ahmad Albaqsami',
      author_email='ahmad_baq@hotmail.com',
      license='MIT',
      packages=['itermore'],
      zip_safe=False)