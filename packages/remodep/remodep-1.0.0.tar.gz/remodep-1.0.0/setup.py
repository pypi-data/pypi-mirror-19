#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages
import fastentrypoints # Ensures fast startup
import sys

install_requires = []

if sys.version_info < (2, 7, 0):
    install_requires.append('argparse')


setup(
    name='remodep',
    version='1.0.0',
    author='Tarjei Husøy',
    author_email='git@thusoy.com',
    url='https://github.com/thusoy/remodep',
    description="List reverse kernel module dependencies",
    py_modules=['remodep'],
    install_requires=install_requires,
    extras_require={
        'test': [
            'pytest',
            'mock',
            'watchdog'
        ],
    },
    entry_points={
        'console_scripts': [
            'remodep = remodep:main',
        ],
    },
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
