# -*- coding: utf-8 -*-
"""
This module provides the main command line interface to using Pymake.
"""

import os
import sys

def main(argv=[]):
    """
    The entry point of the script.
    """
    import argparse
    from pymake import PymakeSuite
    from pymake import PymakeLogger

    # logger
    pylogger = PymakeLogger()

    # Process the command line.
    parser = argparse.ArgumentParser(description='Executes the Pymake package as an application.')

    parser.add_argument('configuration_filenames', metavar='file', nargs='+', help='The configuration file that contains the [pymake.*] sections contains the pymake input')

    # Parse the arguments.
    args = parser.parse_args(argv[1:])

    # Create a PymakeSuite and execute it for each filename on the command line.
    for filename in args.configuration_filenames:
        suite = PymakeSuite(filename)
        suite.write(False)

    return 0

if __name__ == "__main__":
    # To use Pymake as an application we need to correct the sys.path to treeat Pymake as a package.
    module_path = os.path.dirname( os.path.realpath(__file__) )
    package_path = os.path.normpath(os.path.join(module_path, os.pardir))
    try:
        sys.path[sys.path.index(module_path)] = package_path
    except IndexError:
        sys.path.append(package_path)

    sys.exit(main(sys.argv))

