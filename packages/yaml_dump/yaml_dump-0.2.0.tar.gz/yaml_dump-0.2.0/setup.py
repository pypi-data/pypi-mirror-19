#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'PyYAML',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='yaml_dump',
    version='0.2.0',
    description="Sane default for YAML dump",
    long_description=readme + '\n\n' + history,
    author="Fingul",
    author_email='fingul@gmail.com',
    url='https://bitbucket.com/fingul/yaml_dump',
    packages=[
        'yaml_dump',
    ],
    package_dir={'yaml_dump':
                 'yaml_dump'},
    entry_points={
        'console_scripts': [
            'yaml_dump=yaml_dump.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='yaml_dump',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
