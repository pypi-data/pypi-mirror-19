#!/usr/bin/env python

import os
from setuptools import setup, find_packages

from distelli import distelli

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), 'r') as readme_file:
    readme = readme_file.read()

setup(
    name='distelli',
    version='0.1.0',
    description=u' '.join(distelli.__doc__.splitlines()).strip(),
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/maxpeterson/distelli-python/',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=['requests>=2.12.0,<2.13.0']
)
