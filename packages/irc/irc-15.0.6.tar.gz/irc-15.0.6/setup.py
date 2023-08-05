#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io
import sys

import setuptools

install_requires=[
    'six',
    'jaraco.collections',
    'jaraco.text',
    'jaraco.itertools>=1.8',
    'jaraco.logging',
    'jaraco.functools>=1.5',
    'jaraco.stream',
    'pytz',
    'more_itertools',
    'tempora>=1.6',
]

with io.open('README.rst', encoding='utf-8') as readme:
    long_description = readme.read()

needs_wheel = {'release', 'bdist_wheel', 'dists'}.intersection(sys.argv)
wheel = ['wheel'] if needs_wheel else []

name = 'irc'
description = 'IRC (Internet Relay Chat) protocol library for Python'

setup_params = dict(
    name=name,
    use_scm_version=True,
    author="Joel Rosdahl",
    author_email="joel@rosdahl.net",
    maintainer="Jason R. Coombs",
    maintainer_email="jaraco@jaraco.com",
    description=description or name,
    long_description=long_description,
    url="https://github.com/jaraco/" + name,
    packages=setuptools.find_packages(),
    include_package_data=True,
    namespace_packages=name.split('.')[:-1],
    install_requires=install_requires,
    extras_require={
    },
    setup_requires=[
        'setuptools_scm>=1.15.0',
    ] + wheel,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    entry_points={
    },
)
if __name__ == '__main__':
    setuptools.setup(**setup_params)
