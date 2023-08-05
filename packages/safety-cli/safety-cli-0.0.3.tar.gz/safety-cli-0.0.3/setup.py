#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click>=6.0',
    'requests',
    'packaging',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='safety-cli',
    version='0.0.3',
    description="Safety checks your installed dependencies for known security vulnerabilities",
    long_description=readme,
    author="safetydb.io",
    author_email='hi@safetydb.io',
    url='https://safetydb.io',
    packages=[
        'safety',
    ],
    package_dir={'safety':
                 'safety'},
    entry_points={
        'console_scripts': [
            'safety=safety.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='safety',
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
