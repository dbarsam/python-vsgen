# -*- coding: utf-8 -*-
"""
This module provides the main command line interface to using VSG.
"""

import os
import sys


def main(argv=None):
    """
    The entry point of the script.
    """
    import argparse
    from vsgen import VSGSuite
    from vsgen import VSGLogger

    # Special case to use the sys.argv when main called without a list.
    if argv is None:
        argv = sys.argv

    # logger
    pylogger = VSGLogger()

    # Process the command line.
    parser = argparse.ArgumentParser(description='Executes the VSG package as an application.')

    parser.add_argument('configuration_filenames', metavar='file', nargs='+', help='The configuration file that contains the [vsgen.*] sections contains the vsgen input')

    # Parse the arguments.
    args = parser.parse_args(argv[1:])

    # Create a VSGSuite and execute it for each filename on the command line.
    for filename in args.configuration_filenames:
        suite = VSGSuite(filename)
        suite.write(False)

    return 0

if __name__ == "__main__":
    # To use VSG as an application we need to correct the sys.path to treeat VSG as a package.
    module_path = os.path.dirname(os.path.realpath(__file__))
    package_path = os.path.normpath(os.path.join(module_path, os.pardir))
    try:
        sys.path[sys.path.index(module_path)] = package_path
    except IndexError:
        sys.path.append(package_path)

    sys.exit(main(sys.argv))
