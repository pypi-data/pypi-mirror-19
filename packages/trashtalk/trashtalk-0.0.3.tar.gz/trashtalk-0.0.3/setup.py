#!  /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from sys import version_info
import trashtalk


requires = ['pathlib==1.0.1']

# bash completion
try:
    with open('/etc/bash_completion.d/completion', 'w') as eo:
        eo.write('test')
    data_files = [('/etc/bash_completion.d/', ['extra/python%s/trashtalk' % version_info[0]])]
except:
    data_files = []

setup(
    name='trashtalk',
    version=trashtalk.__version__,

    packages=find_packages(),

    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    description="simplify trash in command line",
    long_description=open('README.md').read(),
    author="PTank",
    author_email="akazian@student.42.fr",
    url="https://github.com/PTank/trashtalk",

    install_requires=requires,

    include_package_data=True,

    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Topic :: Utilities"
    ],

    data_files=data_files,

    entry_points={
        'console_scripts': [
            'trashtalk = trashtalk.core:trashtalk',
        ],
    }

)
