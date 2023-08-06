# -*- coding: utf-8 -*-
"""
stages
~~~~~~

Simple command line tool to run scripts in a
sequential manner.

Nutshell
--------

Here a quick interpreter demo:

    >>> from stages import Runner
    >>> runner = Runner("config_file", heading="Example run")
    >>> runner.run()

:copyright: (c) 2017 by Tobias Pleyer
:license: BSD, see LICENSE for more details.
"""
__version__ = '1.0.dev'

# high level interface
from .stages import Runner

__all__ = ['Runner']
