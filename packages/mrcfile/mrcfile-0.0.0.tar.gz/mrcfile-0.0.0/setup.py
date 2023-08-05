# Copyright (c) 2016, Science and Technology Facilities Council
# This software is distributed under a BSD licence. See LICENSE.txt.

# Import Python 3 features for future-proofing
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from setuptools import setup
import unittest

def readme():
    with open('README.rst') as f:
        return f.read()

def test_suite():
    return unittest.TestLoader().discover('tests', pattern='test_*.py')

setup(
    name='mrcfile',
    version='0.0.0',
    packages=['mrcfile'],
    install_requires=['numpy >= 1.11.0'],
    
    test_suite='setup.test_suite',
    
    author='Colin Palmer',
    author_email='colin.palmer@stfc.ac.uk',
    description='MRC file I/O library',
    long_description=readme(),
    license='BSD',
    url='https://github.com/ccpem/mrcfile',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
