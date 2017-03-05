# -*- coding: utf-8 -*-
"""
This module executes vsgen unittests (i.e. all tests in the current folder).  It exists as an alernative to the command line interface::

    > python -m unittest discover --start-directory . --pattern test*.py

For more testing options see the unittest documentation available at https://docs.python.org/3.5/library/unittest.html.

This module exposes an __main__ entry point useful for test development (usually from an Python IDE) and not recommeded for normal test execution.
"""
import os
import sys


def main(argv=[]):
    """
    Test main script
    """
    import argparse
    import unittest
    parser = argparse.ArgumentParser(description='Executes the vsgen unit tests.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', '--testname', help='Specifies the test name to execute.  This must be the fully qualified \'dotted\' path of the form \'package.module.class.function\' (e.g. \'tests.unit.test_feature.TestClass.test_function\').  If not provided all tests resolved from the internal test discovery process are executed.', action='append')
    parser.add_argument('-f', '--testpattern', help='Specifies the test file pattern to execute during test discovery.  If not provided all tests resolved from the internal test discovery process are executed.', default='test*.py')
    parser.add_argument('-p', '--testpath', help='Specifies the test path for test discovery.  If not provided, the internal test discovery uses the current directory.', default=os.path.dirname(os.path.realpath(__file__)))
    args = parser.parse_args(argv[1:])

    loader = unittest.TestLoader()
    if args.testname:
        testsuite = loader.loadTestsFromNames(args.testname)
    else:
        testsuite = loader.discover(args.testpath, args.testpattern)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(testsuite)
    return 0 if not result.failures and not result.errors else 1

if __name__ == '__main__':
    # To use this package as an application we need to correct the sys.path
    module_path = os.path.dirname(os.path.realpath(__file__))
    package_path = os.path.normpath(os.path.join(module_path, '..'))
    if package_path not in sys.path:
        sys.path.append(package_path)

    sys.exit(main(sys.argv))
