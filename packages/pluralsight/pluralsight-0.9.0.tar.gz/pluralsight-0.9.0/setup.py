#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pluralsight',
    version='0.9.0',
    description="Pluralsight client library for API management",
    long_description=readme + '\n\n' + history,
    author="Anthony Shaw",
    author_email='anthonyshaw@apache.org',
    url='https://github.com/tonybaloney/pluralsight',
    packages=[
        'pluralsight',
        'pluralsight.licensing',
        'pluralsight.reports',
        'pluralsight.models'
    ],
    package_dir={'pluralsight':
                 'pluralsight'},
    include_package_data=True,
    install_requires=requirements,
    license="APACHE2",
    zip_safe=False,
    keywords='pluralsight',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
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
