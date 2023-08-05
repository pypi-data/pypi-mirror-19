#! /usr/bin/env python

"""Set up PyFHI package

Copyright:

    setup.py setup pyfhi package
    Copyright (C) 2015  Alex Hyer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from distutils.core import setup

setup(
    name='pyfhi',
    version='1.0.4',
    packages=['pyfhi'],
    url='https://github.com/TheOneHyer/PyFHI',
    download_url='https://github.com/TheOneHyer/PyFHI/tarball/1.0.4',
    license='GPLv3',
    author='TheOneHyer',
    author_email='theonehyer@gmail.com',
    description='PyFHI is a single script designed to fix issues with Python '
                'file handling.See README for more details.',
    classifiers=[
        'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development'
    ],
    keywords='file handling python closer close all'
)
