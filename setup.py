#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

exec(open('verbecc/version.py').read())

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

requirements = [
    'lxml>=4.9.3,<5.0.0',
    'mock>=5.1.0,<6.0.0',
    'pytest>=7.4.3,<8.0.0',
    'pytest-cov>=4.1.0,<5.0.0',
    'pylama>=8.4.1,<9.0.0',
    'cython>=3.0.6,<4.0.0',
    'numpy>=1.26.2,<2.0.0',
    'scipy>=1.11.4,<2.0.0',
    'scikit-learn>=1.3.2,<1.4.0'
]

setup(
    name='verbecc',
    version=__version__,
    description='Verbs Completely Conjugated: machine learning conjugator for French, Spanish, Portuguese, Italian and Romanian',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email='bretttolbert@gmail.com',
    maintainer=__maintainer__,
    maintainer_email='bretttolbert@gmail.com',
    url='https://github.com/bretttolbert/verbecc',
    packages=find_packages(),
    package_data={'trained_models': ['verbecc/data/models/*']},
    include_package_data=True,
    install_requires=requirements,
    license=__license__,
    zip_safe=False,
    keywords='french italian spanish portuguese romanian'
             ' français italiano español português română'
             ' conjugate coniugare conjuguer conjugado' 
             ' conjugator conjugueur conjugador'
             ' conjugation coniugazione conjugaison conjugación conjugação'
             ' verbs verbi verbes verbos'
             ' ML machine-learning apprentissage-automatique apprendimento-automatico aprendizaje-automático aprendizado-máquina învățarea-mașinilor'
             ' NLP linguistics linguistique linguistica lingvistică sklearn',
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
        'Natural Language :: Italian',
        'Natural Language :: Spanish',
        'Natural Language :: Portuguese',
        'Natural Language :: Romanian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    tests_require=requirements,
    test_suite="tests",
)