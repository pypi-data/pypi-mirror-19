#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import pykafka_tools

__author__ = u'Stephan Müller'
__copyright__ = u'2016, Stephan Müller'
__license__ = u'MIT'


setup(
    name='pykafka_tools',
    packages=['pykafka_tools'],
    version=pykafka_tools.__version__,
    license='MIT',
    description='The pykafka-tools extend the functionalities of python pykafka module.',
    author='Stephan Müller',
    author_email='stephan@mueller5.eu',
    url='https://github.com/smueller18/pykafka-tools',
    download_url='https://github.com/smueller18/pykafka-tools',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
        'pykafka==2.6.0.dev3'
    ],
    dependency_links=[
        'https://github.com/smueller18/pykafka/tarball/2.6.0.dev3#egg=pykafka-2.6.0.dev3'
    ],
)
