#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
    'requests-oauthlib==0.6.1',
    'purl==1.3'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pandadocs',
    version='0.1.2',
    description="Easy pythonic integration with Pandadocs' REST API",
    long_description=readme + '\n\n' + history,
    author="Alokin Software Pvt Ltd",
    author_email='rajeev@alokin.in',
    url='https://bitbucket.com/alokinplc/pandadocs/',
    packages=[
        'pandadocs',
    ],
    package_dir={'pandadocs': 'pandadocs'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pandadocs',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,

    entry_points = {
        'console_scripts': [
            'pandadocs-tokentool = pandadocs.tool:main',                  
        ],              
    },
)
