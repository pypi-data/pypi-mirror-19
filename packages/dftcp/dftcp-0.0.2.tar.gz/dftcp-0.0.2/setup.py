#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 12:46:59 2016

@author: chernov
"""

from distutils.core import setup
setup(
  name = 'dftcp',
  packages = ['dftcp'],
  version = '0.0.2',
  description = 'Tcp templates for dataforge (http://npm.mipt.ru/dataforge/)',
  author = 'Vasilii Chernov',
  author_email = 'kapot65@gmail.com',
  url = 'https://github.com/kapot65/python-df-tcp',
  download_url = 'https://github.com/kapot65/python-df-tcp/tarball/0.0.2',
  keywords = ['dataforge'],
  install_requires=[
   'dfparser>=0.0.2'
  ],
  classifiers = []
)
