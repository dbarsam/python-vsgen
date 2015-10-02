# -*- coding: utf-8 -*-
"""
This module provides all functionality for extending Python's config parser functionality.

The module defines the class PymakeConfigParser.  The PymakeConfigParser class provides the main functionality of using Python's native config parser.
"""

import os
import glob
import configparser

class PymakeConfigParser( configparser.ConfigParser ):
    """
    The Pymake ConfigParser extends Python's ConfigParser class with Pymake specific functionality.
    """

    def getlist(self, section, option, fallback=[]):
        """
        A convenience method which coerces the option in the specified section to a list of strings.
        """
        v = self.get(section, option, fallback=fallback)
        return [l.strip() for l in v.split(',')] if v else fallback

    def getfile(self, section, option, fallback=""):
        """
        A convenience method which coerces the option in the specified section to a file.
        """
        v = self.get(section, option, fallback=fallback)
        return os.path.normpath(v) if os.path.isfile(v) else None

    def getdir(self, section, option, fallback=""):
        """
        A convenience method which coerces the option in the specified section to a directory.
        """
        v = self.get(section, option, fallback=fallback)        
        return os.path.normpath(v) if os.path.isdir(v) else None

    def getdirs(self, section, option, fallback=[]):
        """
        A convenience method which coerces the option in the specified section to a list of directories.
        """
        globs = self.getlist(section, option, [])
        return [f for g in globs for f in glob.glob(g) if os.path.isdir(f)]