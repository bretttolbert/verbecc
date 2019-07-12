#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from verbecc import __version__, __author__, __license__

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    "lxml>=4.1.1",
    "mock>=2.0.0,<3.0.0",
    "pytest>=3.0.6,<4.0.0",
    "pytest-cov>=2.4.0,<3.0.0",
    "pylama>=7.4.1,<8.0.0"
]

setup(
    name='verbecc',
    version=__version__,
    description='Verbes, complètement conjugués - conjugueur français | Verbs, completely conjugated - French conjugator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email='brett.tolbert@gmail.com',
    url='https://github.com/bretttolbert/verbecc',
    license=__license__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords='conjugate conjugator conjugation conjugaison conjugación'
             ' verbs verbes verbos linguistics linguistique linguistica',
    install_requires=install_requires,
    tests_require=install_requires,
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Natural Language :: French",
        "Natural Language :: Spanish",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic"
    ],
)