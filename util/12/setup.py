#!/usr/bin/env python3
# -*-coding:utf-8-*-
#import sys, os, shutil, time
from distutils.core import setup
from Cython.Build import cythonize

#setup(ext_modules = cythonize("abstr.py"))
setup(
    name = 'Todisk',
    ext_modules = cythonize('abstr.pyx'),
    )
