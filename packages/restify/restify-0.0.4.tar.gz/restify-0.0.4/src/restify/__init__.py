# -*- coding: utf-8 -*-
try:
    from restify import *
    from restify.dsn import *
    from restify.routing import *
    from restify.util import *
except ImportError:
    # A dependency is probably missing..
    pass

import subprocess

__git_label__ = ''
try:
    __git_label__ = subprocess.check_output(
        [
            'git',
            'rev-parse',
            '--short',
            'HEAD'
        ])
except (subprocess.CalledProcessError, OSError):
    # CalledProcessError -> subprocess returns a non-zero code
    # OSError            -> likely only happens when the executable can not
    #                       be found
    __git_label__ = 'RELEASE'

__version__ = '0.0.4'
__release__ = '{}-{}'.format(__version__, __git_label__).strip()

__description__ = """ restify is a small library that tries to make it easier
to write and maintain a small REST API system which runs on top of Bottle.
"""
