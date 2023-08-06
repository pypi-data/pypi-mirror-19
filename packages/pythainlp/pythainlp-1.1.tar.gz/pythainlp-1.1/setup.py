﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages
import codecs
with codecs.open('README.rst','r',encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = [
    'pyicu>=1.9.3',
    'nltk>=3.2.2',
    'future>=0.16.0'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pythainlp',
    version='1.1',
    description="Thai NLP in python package.",
    long_description=readme,
    author='Wannaphong Phatthiyaphaibun',
    author_email='wannaphong@yahoo.com',
    url='https://github.com/wannaphongcom/pythainlp',
    packages=find_packages(),
    test_suite='pythainlp.test',
    package_data={'pythainlp.corpus':['thaipos.json','thaiword.txt','LICENSE_THA_WN','tha-wn.db']},
    include_package_data=True,
    install_requires=requirements,
    license='Apache Software License 2.0',
    zip_safe=False,
    keywords='pythainlp,nlp,thai',
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: Thai',
    'Topic :: Text Processing :: Linguistic',
    'Programming Language :: Python :: Implementation',
    'Programming Language :: Python :: 3',
    ],
)