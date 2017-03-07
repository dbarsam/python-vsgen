# -*- coding: utf-8 -*-
"""
This module provides all functionality for extending Python's suite class of functionality.

The module defines the class VSGSuite.  The VSGSuite class groups the different functionalities into a single class.
"""

import sys
import os
import argparse
import pkg_resources

from vsgen.suite import VSGSuite
from vsgen.util.config import VSGConfigParser
from vsgen.util.argparse import DirectoryType


class VSGDemoSuite(VSGSuite):
    """
    VSGDemoSuite extends :class:`~vsgen.suite.VSGSuite` with data and logic required by the vsgendemo Python pacakge.
    """
    __template__ = os.path.abspath(os.path.join(os.path.dirname(__file__), 'vsgendemo.cfg'))

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

        super(VSGDemoSuite, self).__init__(config)

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
        parser.add_argument('--filename', metavar='PATH', help='absolute path to the project\'s filename location')

        return parser
