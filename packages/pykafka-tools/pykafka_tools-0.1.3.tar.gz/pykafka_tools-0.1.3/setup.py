#!/usr/bin/env python

from setuptools import setup
import pykafka_tools

__author__ = "Stephan Müller"
__copyright__ = "2016, Stephan Müller"
__license__ = "MIT"



setup(
    name='pykafka_tools',
    packages=['pykafka_tools'],
    version=pykafka_tools.__version__,
    license='MIT',
    description='Tools for an automated use of pykafka',
    author='Stephan Müller',
    author_email='stephan@mueller5.eu',
    url='https://github.com/smueller18/pykafka-tools',
    download_url='https://github.com/smueller18/pykafka-tools',
    classifiers=[
        "Programming Language :: Python :: 3.5",
    ],
    dependency_links=['https://github.com/Parsely/pykafka/tarball/bugfix/raise_connection_failures'],
)
