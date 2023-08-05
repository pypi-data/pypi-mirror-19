# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import os
import sys

sys.path.insert(0, os.path.abspath('src'))

import restify  # noqa: need to change path before importing..


setup(
    name='restify',
    version=restify.__version__,
    description="Base wrappers for creating a REST API with Bottle",

    url="http://glow.dev.ramcloud.io/sjohnson/rest-api-template",
    author="Sean Johnson",
    author_email="sean.johnson@maio.me",

    license="Unlicense",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],

    packages=find_packages('src'),
    package_dir={
        '': 'src'
    },
    install_requires=[
        'malibu',
        'bottle',
        'raven',
    ],
    include_package_data=True,
    exclude_package_data={
        '': ['README.md'],
    },
    zip_safe=True,
)
