#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

setup_requirements = [
        'pytest-runner'
]

test_requirements = [
        'pytest'
]

setup(
    name='nether',
    version='0.1.0',
    description="The “Underworld” substrate for exchanging JSON/CBOR documents",
    long_description=readme + '\n\n' + history,
    author="Eugene M. Kim",
    author_email='astralblue@gmail.com',
    url='https://github.com/astralblue/nether',
    packages=[
        'nether',
    ],
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='nether',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements
)
