#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

exec(open('verbecc/version.py').read())

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

requirements = [
    'lxml>=4.1.1',
    'mock>=2.0.0,<3.0.0',
    'pytest>=3.0.6,<4.0.0',
    'pytest-cov>=2.4.0,<3.0.0',
    'pylama>=7.4.1,<8.0.0',
    'cython',
    'numpy',
    'scipy',
    'scikit-learn>=0.20.3'
]

setup(
    name='verbecc',
    version=__version__,
    description='Verbs, Completely Conjugated - Conjugator for French and Spanish using ML techniques to conjugate any verb',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email='brett.tolbert@gmail.com',
    url='https://github.com/bretttolbert/verbecc',
    packages=find_packages(),
    package_data={'trained_models': ['verbecc/data/models/*']},
    include_package_data=True,
    install_requires=requirements,
    license=__license__,
    zip_safe=False,
    keywords='conjugate conjugator conjugation conjugaison conjugación'
             ' verbs verbes verbos ML machine-learning NLP linguistics linguistique linguistica sklearn',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: French',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    tests_require=requirements,
    test_suite="tests",
)