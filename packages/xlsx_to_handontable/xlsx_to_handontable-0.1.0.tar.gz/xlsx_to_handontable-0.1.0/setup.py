#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'pyyaml',
    'yaml_dump',
    'openpyxl',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='xlsx_to_handontable',
    version='0.1.0',
    description="xlsx_to_handontable",
    long_description=readme + '\n\n' + history,
    author="Fingul",
    author_email='fingul@gmail.com',
    url='https://github.com/fingul/xlsx_to_handontable',
    packages=[
        'xlsx_to_handontable',
    ],
    package_dir={'xlsx_to_handontable':
                 'xlsx_to_handontable'},
    entry_points={
        'console_scripts': [
            'xlsx_to_handontable=xlsx_to_handontable.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='xlsx_to_handontable',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
