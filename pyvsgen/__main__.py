# -*- coding: utf-8 -*-
"""
This module provides the main command line interface to using Pyvsgen.
"""

import os
import sys

def main(argv=[]):
    """
    The entry point of the script.
    """
    import argparse
    from pyvsgen import PyvsgenSuite
    from pyvsgen import PyvsgenLogger

    # logger
    pylogger = PyvsgenLogger()

    # Process the command line.
    parser = argparse.ArgumentParser(description='Executes the Pyvsgen package as an application.')

    parser.add_argument('configuration_filenames', metavar='file', nargs='+', help='The configuration file that contains the [pyvsgen.*] sections contains the pyvsgen input')

    # Parse the arguments.
    args = parser.parse_args(argv[1:])

    # Create a PyvsgenSuite and execute it for each filename on the command line.
    for filename in args.configuration_filenames:
        suite = PyvsgenSuite(filename)
        suite.write(False)

    return 0

if __name__ == "__main__":
    # To use Pyvsgen as an application we need to correct the sys.path to treeat Pyvsgen as a package.
    module_path = os.path.dirname( os.path.realpath(__file__) )
    package_path = os.path.normpath(os.path.join(module_path, os.pardir))
    try:
        sys.path[sys.path.index(module_path)] = package_path
    except IndexError:
        sys.path.append(package_path)

    sys.exit(main(sys.argv))

