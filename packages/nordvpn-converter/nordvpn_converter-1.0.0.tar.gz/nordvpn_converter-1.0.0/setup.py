#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package test requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='nordvpn_converter',
    version='1.0.0',
    description="Conversion tool from OVPN files into NetworkManager compatible. ",
    long_description=readme + '\n\n' + history,
    author="Cristian Năvălici",
    author_email='cristian.navalici@gmail.com',
    url='https://bitbucket.org/cnavalici/nordvpn-converter/',
    packages=[
        'nordvpn_converter',
    ],
    package_dir={'nordvpn_converter':
                 'nordvpn_converter'},
    entry_points={
        'console_scripts': [
            'nordvpn_converter=nordvpn_converter.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='nordvpn_converter',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
