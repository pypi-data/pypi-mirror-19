#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, Extension

jchash = Extension('jchash',
                   sources=['src/jchash.c'],
                   include_dirs=['src'])

setup(
    name='jchash',
    version='1.1',
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
