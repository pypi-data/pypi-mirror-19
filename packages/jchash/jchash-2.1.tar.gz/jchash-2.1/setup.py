#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, Extension

PACKAGE_VERSION = "2.1"

jchash = Extension('jchash',
                   define_macros=[
                       ('XSTR(s)', 'STR(s)'),
                       ('STR(s)', '#s'),
                       ('PACKAGE_VERSION', PACKAGE_VERSION)],
                   sources=['src/jchash.c', 'src/jchash.h'],
                   include_dirs=['src'])

setup(
    name='jchash',
    version=PACKAGE_VERSION,
    description='jchash - Jump Consistent Hash for Python',
    url='https://github.com/grapherd/jchash/',
    author='Louie Lu',
    author_email='me@louie.lu',
    license='MIT',
    keywords='hash jump consistent',
    test_suite='tests',
    ext_modules=[jchash],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
