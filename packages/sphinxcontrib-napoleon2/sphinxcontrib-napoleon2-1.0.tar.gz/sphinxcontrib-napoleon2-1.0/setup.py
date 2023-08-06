# -*- coding: utf-8 -*-
# Copyright 2014 Rob Ruana
# Licensed under the BSD License, see LICENSE file for details.

"""Modified Sphinx "napoleon" extension."""

import os
import sys
from setuptools import setup, find_packages

reqs = open('requirements.txt', 'r').read().strip().splitlines()
reqs_test = open('requirements_test.txt', 'r').read().strip().splitlines()

# Package versioning solution originally found here:
# http://stackoverflow.com/q/458550
version_path = os.path.join('sphinxcontrib', 'napoleon', '_version.py')
exec(open(version_path).read())

setup(
    name='sphinxcontrib-napoleon2',
    version=__version__,
    url='https://sphinxcontrib-napoleon.readthedocs.io',
    download_url='http://github.com/LinxiFan/sphinxcontrib-napoleon',
    license='BSD',
    description=__doc__,
    long_description=open('README.rst', 'r').read(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Utilities',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs,
    test_suite='nose.collector',
    tests_require=reqs_test,
    namespace_packages=['sphinxcontrib']
)
