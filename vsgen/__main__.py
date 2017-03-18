# -*- coding: utf-8 -*-
"""
This module provides the main command line interface to using VSG.
"""

import os
import sys
import argparse


def make_documentation_parser(**kwargs):
    """
    Generates the application's :class:`~argparse.ArgumentParser` instance for the documentation generator `sphinx-argparse <https://sphinx-argparse.readthedocs.io>`_
    """
    from vsgen import VSGSuite
    return VSGSuite.make_parser(**kwargs)


def main(argv=None):
    """
    The entry point of the script.
    """
    from vsgen import VSGSuite
    from vsgen import VSGLogger

    # Special case to use the sys.argv when main called without a list.
    if argv is None:
        argv = sys.argv

    # Initialize the application logger
    pylogger = VSGLogger()

    # Construct a command line parser and parse the command line
    args = VSGSuite.make_parser(description='Executes the vsgen package as an application.').parse_args(argv[1:])
    for s in VSGSuite.from_args(**vars(args)):
        s.write(False)
    return 0

if __name__ == "__main__":
    # To use this package as an application we need to correct the sys.path
    module_path = os.path.dirname(os.path.realpath(__file__))
    package_path = os.path.normpath(os.path.join(module_path, os.pardir))
    try:
        sys.path[sys.path.index(package_path)] = package_path
    except ValueError:
        sys.path.append(package_path)

    sys.exit(main(sys.argv))
