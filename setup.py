#!/usr/bin/env python
from setuptools import setup, find_packages
from verbecc import __version__

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
    author='Brett Tolbert',
    author_email='brett.tolbert@gmail.com',
    url='http://verbe.cc',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=install_requires,
    test_suite="tests"
)