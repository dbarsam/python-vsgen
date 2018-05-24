# -*- coding: utf-8 -*-
"""
This module provides the neccessary defintions to generate a Solution File.
"""

import os
import uuid
import errno
import pkg_resources

from vsgen.writer import VSGWritable, VSGJinjaRenderer


class VSGSolution(VSGWritable, VSGJinjaRenderer):
    """
    VSGSolution encapsulates the logic needed to create a ``.sln`` file.

    :ivar uuid GUID:     The GUI of the solution; if not provided one is generated automatically.
    :ivar str  FileName:  The absolute filename of the solution file; if not provided the value is ""
    :ivar str  Name:      The display name of the solution; if not provide the value is "".
    :ivar list Projects: The list of VSGProject derived classes; if not provide the value is [].
    """
    __writable_name__ = "VSG Solution"

    __jinja_template__ = pkg_resources.resource_filename('vsgen', 'data/sln.jinja')

    def __init__(self, **kwargs):
        """
        Constructor.

        :param kwargs:         List of arbitrary keyworded arguments to be processed as instance variable data
        """
        super(VSGSolution, self).__init__()

        self._import(kwargs)

    def _import(self, datadict):
        """
        Internal method to import instance variables data from a dictionary

        :param dict datadict: The dictionary containing variables values.
        """
        self.GUID = datadict.get("GUID", uuid.uuid1())
        self.FileName = datadict.get("FileName", "")
        self.Name = datadict.get("Name", "")
        self.Projects = datadict.get("Projects", [])
        self.VSVersion = datadict.get("VSVersion", None)

    def write(self):
        """
        Writes the ``.sln`` file to disk.
        """
        filters = {
            'MSGUID': lambda x: ('{%s}' % x).upper(),
            'relslnfile': lambda x: os.path.relpath(x, os.path.dirname(self.FileName))
        }
        context = {
            'sln': self
        }
        return self.render(self.__jinja_template__, self.FileName, context, filters)
