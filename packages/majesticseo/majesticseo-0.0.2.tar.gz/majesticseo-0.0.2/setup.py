#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests'
]

test_requirements = [
    'requests'
]

setup(
    name='majesticseo',
    version='0.0.2',
    description="Python Wrapper around the MajesticSEO API",
    long_description=readme + '\n\n' + history,
    author="Philippe Oger",
    author_email='phil.oger@gmail.com',
    url='https://github.com/philippe2803/majesticseo',
    packages=[
        'majesticseo',
    ],
    package_dir={'majesticseo':
                 'majesticseo'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='majesticseo',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
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
