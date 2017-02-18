# -*- coding: utf-8 -*-
"""
This module provides all functionality for extending Python's suite class of functionality.

The module defines the class VSGSuite.  The VSGSuite class groups the different functionalities into a single class.
"""

import sys
import os
import argparse

from vsgen.suite import VSGSuite
from vsgen.util.config import VSGConfigParser
from vsgen.util.argparse import DirectoryType


class PTVSSuite(VSGSuite):
    """
    VSGSuite extends :class:`~vsgen.suite.VSGSuite` with data and logic needed to create a `.pyproj` based suite.
    """
    __type__ = 'ptvs'

    __template__ = os.path.join(os.path.dirname(sys.modules['vsgen'].__file__), 'data', 'ptvs.cfg')

    def __init__(self, **kwargs):
        """
        Constructor.

        :param kwargs:         List of arbitrary keyworded arguments to be processed as instance variable data.
        """
        # Read the configuration file
        config = VSGConfigParser()
        if self.__template__ not in config.read([self.__template__]):
            raise ValueError('Could not read VSG template configuration file %s.' % __template__)

        # Override the template values with the override values.
        for s in config.sections():
            for o in config.options(s):
                override = kwargs.pop(o, None)
                if override:
                    config.set(s, o, override)

        super(PTVSSuite, self).__init__(config)

    @classmethod
    def make_parser(cls, **kwargs):
        """
        Creates a :class:`~argparse.ArgumentParser` instances to work with :class:`~vsgen.project.VSGProject` classes.

        :param kwargs:  List of additional keyworded arguments to be passed into the :class:`~argparse.ArgumentParser`.
        :return:  A :class:`~argparse.ArgumentParser` instance.
        """
        # Build a shared solution parser
        parser = argparse.ArgumentParser(**kwargs)

        parser.add_argument('--root', metavar='PATH', type=DirectoryType(), help='the project\'s root path')
        parser.add_argument('--name', help='name of the solution and project')
        parser.add_argument('--filename', metavar='PATH', help='absolute path to the project\;s filename location')
        parser.add_argument('--search_path', metavar='PATH', nargs='*', type=DirectoryType(), help='one or more absolute paths to be added to the python search path.')
        parser.add_argument('--output_path', metavar='PATH', type=DirectoryType(), help='absolute path to the project\'s output directory')
        parser.add_argument('--working_directory', metavar='PATH', type=DirectoryType(), help='absolute path to the project\'s working directory')
        parser.add_argument('--root_namespace', metavar='NAME', help='the root namespace of the project')
        parser.add_argument('--project_home', metavar='PATH', type=DirectoryType(), help='absolute path to the project\'s home directory')
        parser.add_argument('--startup_file', metavar='PATH', help='absolute path to the project\'s startup file')
        parser.add_argument('--compile_in_filter', metavar='FILTER', nargs='*', help='one or more fnmatch expressions to match included compile files')
        parser.add_argument('--compile_ex_filter', metavar='FILTER', nargs='*', help='one or more fnmatch expressions to match excluded compile files')
        parser.add_argument('--content_in_filter', metavar='FILTER', nargs='*', help='one or more fnmatch expressions to match included content files')
        parser.add_argument('--content_ex_filter', metavar='FILTER', nargs='*', help='one or more fnmatch expressions to match excluded content files')
        parser.add_argument('--directory_in_filter', metavar='FILTER', nargs='*', help='one or more fnmatch expressions to match included directories')
        parser.add_argument('--directory_ex_filter', metavar='FILTER', nargs='*', help='one or more fnmatch expressions to match excluded directories')
        parser.add_argument('--is_windows_application', metavar='FLAG', type=bool, help='switch to use console python.exe or pythonw.exe.')
        parser.add_argument('--python_interpreter_args', metavar='ARG', nargs='*', help='additional python interpreter arguments')

        return parser
