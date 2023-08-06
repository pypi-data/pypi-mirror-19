#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, Extension

PACKAGE_NAME = 'jchash'
PACKAGE_VERSION = '2.2'

jchash = Extension(PACKAGE_NAME,
                   define_macros=[
                       ('XSTR(s)', 'STR(s)'),
                       ('STR(s)', '#s'),
                       ('JCHASH_MODULE_NAME', PACKAGE_NAME),
                       ('PACKAGE_VERSION', PACKAGE_VERSION)],
                   sources=['src/jchash.c'],
                   include_dirs=['src'])

setup(
    name=PACKAGE_NAME,
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
