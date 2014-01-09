# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version = '0.1.0'

setup(
    name='instagram_bot',
    version=version,
    author='Saurabh Kumar',
    author_email='thes.kumar@gmail.com',
    packages=[
        'instagram_bot',
        'Logbook',
    ],
    include_package_data=True,
    install_requires=[
        'splinter==0.5.4',
    ],
    zip_safe=False,
    license='MIT',
    url='https://github.com/theskumar/instagram_bot',
)
