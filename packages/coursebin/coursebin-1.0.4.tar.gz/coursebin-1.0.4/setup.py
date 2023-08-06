#!/usr/coursemanager/env python

import os
from setuptools import setup, find_packages

__version__ = '1.0.4'

setup(
    name='coursebin',
    version=__version__,
    url='https://github.com/berkowitze/coursebin',
    author='Elias Berkowitz',
    author_email='eliberkowitz@gmail.com',

    description='Tools for undergraduate students to manage classes.',
    long_description=open('README.rst').read(),

    platforms='any',
    packages=find_packages(),
    
    requires=[
        'logging',
        'tabulate',
        'datetime',
        'ansicolors'],

    scripts=['bin/course-compile',
             'bin/course-complete',
             'bin/semester-complete',
             'bin/new-course',
             'bin/new-notes',
             'bin/new-semester',
             'bin/remove-course'],

    include_package_data=True,

    package_data={},

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
