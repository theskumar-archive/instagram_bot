# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version = '1.1.5'

setup(
    name='instagram_bot',
    version=version,
    author='Saurabh Kumar',
    author_email='thes.kumar@gmail.com',
    packages=[
        'instagram_bot',
    ],
    include_package_data=True,
    install_requires=[
        'splinter==0.5.4',
        'Logbook==0.6.0',
    ],
    zip_safe=False,
    license='MIT',
    url='https://github.com/theskumar/instagram_bot',
)
