# -*- coding: utf-8 -*-
"""
This module provides all functionality for extending Python's config parser functionality.

The module defines the class VSGConfigParser.  The VSGConfigParser class provides the main functionality of using Python's native config parser.
"""

import os
import glob
import configparser


class VSGConfigParser(configparser.ConfigParser):
    """
    The VSG ConfigParser extends Python's ConfigParser class with VSG specific functionality.

    :note:  VSGConfigParser uses :class:`~configparser.ExtendedInterpolation` as the default interpolation.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor

        :param args:    List of arguments passed to the :class:`~configparser.ConfigParser`
        :param kwargs:  List of arbitrary keyworded arguments passed to :class:`~configparser.ConfigParser`
        """
        kwargs.setdefault('interpolation', configparser.ExtendedInterpolation())
        return super(VSGConfigParser, self).__init__(*args, **kwargs)

    def _convert_to_list(self, value):
        """
        Return a list value translating from other types if necessary.

        :param str value:  The value to convert.
        """
        return [l.strip() for l in value.split(',')] if value else []

    def _convert_to_path(self, value):
        """
        Return a os path value translating from other types if necessary.

        :param str value:  The value to convert.
        """
        return os.path.normpath(value)

    def getlist(self, section, option, raw=False, vars=None, fallback=[]):
        """
        A convenience method which coerces the option in the specified section to a list of strings.
        """
        v = self.get(section, option, raw=raw, vars=vars, fallback=fallback)
        return self._convert_to_list(v)

    def getfile(self, section, option, raw=False, vars=None, fallback="", validate=False):
        """
        A convenience method which coerces the option in the specified section to a file.
        """
        v = self.get(section, option, raw=raw, vars=vars, fallback=fallback)
        v = self._convert_to_path(v)
        return v if not validate or os.path.isfile(v) else fallback

    def getdir(self, section, option, raw=False, vars=None, fallback="", validate=False):
        """
        A convenience method which coerces the option in the specified section to a directory.
        """
        v = self.get(section, option, raw=raw, vars=vars, fallback=fallback)
        v = self._convert_to_path(v)
        return v if not validate or os.path.isdir(v) else fallback

    def getdirs(self, section, option, raw=False, vars=None, fallback=[]):
        """
        A convenience method which coerces the option in the specified section to a list of directories.
        """
        globs = self.getlist(section, option, fallback=[])
        return [f for g in globs for f in glob.glob(g) if os.path.isdir(f)]

    def set(self, section, option, value=None):
        """
        Extends :meth:`~configparser.ConfigParser.set` by auto formatting byte strings into unicode strings.
        """
        if isinstance(section, bytes):
            section = section.decode('utf8')

        if isinstance(option, bytes):
            option = option.decode('utf8')

        if isinstance(value, bytes):
            value = value.decode('utf8')

        return super(VSGConfigParser, self).set(section, option, value)

    def update(self, **kwargs):
        """
        Extends :meth:`~configparser.ConfigParser.set` by auto formatting byte strings into unicode strings.
        """
        # Override the template values with the override values.
        for s in config.sections():
            for o in config.options(s):
                override = kwargs.pop(o, None)
                if override:
                    config.set(s, o, override)
