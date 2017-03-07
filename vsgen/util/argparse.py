# -*- coding: utf-8 -*-
"""
This module provides the neccessary defintions to extend the :mod:`argparse` module.
"""

import sys
import os
import argparse


class DirectoryType(object):
    """
    Factory for creating directory object types.

    Instances of DirectoryType are typically passed as ``type`` arguments to the :meth:`~argparse.ArgumentParser.add_argument` method.
    """

    def __call__(self, string):
        string = os.path.normcase(os.path.normpath(os.path.abspath(string)))
        if os.path.isdir(string):
            return string
        raise argparse.ArgumentTypeError("%s is not a valid directory" % (string, e))
