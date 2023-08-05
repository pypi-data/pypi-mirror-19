#! /usr/bin/env python

"""Setup metameta package

Copyright:

    setup.py initialize metameta package
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

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Inactive'
__version__ = '0.0.0.66'

from setuptools import setup

setup(name='metameta',
      version='0.0.0.66',
      description='Toolkit for analyzing '
                  + 'meta-transcriptome/metagenome mapping data',
      classifiers=[
          'Development Status :: 7 - Inactive',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.4',
          'Topic :: Scientific/Engineering :: Bio-Informatics'
      ],
      keywords='bioinformatics metadata metagenome metatranscriptome'
               + 'short reads mapping alignment',
      url='https://github.com/Brazelton-Lab/metameta/',
      download_url='https://github.com/Brazelton-Lab/metameta/tarball/'
                   + '0.0.0.66',
      author='Alex Hyer',
      author_email='theonehyer@gmail.com',
      license='GPL',
      packages=['metameta', 'metameta.bin', 'metameta.metameta_utils',
                'metameta.data'],
      include_package_data=True,
      package_data={
          'data': ['Documentation.txt'],
      },
      zip_safe=False,
      install_requires=[
          'bio_utils',
          'pysam',
          'screed',
          'statistics'
      ],
      entry_points={
          'console_scripts': ['metameta = metameta.bin.__main__:main']
      },
      )
