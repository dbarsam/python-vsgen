# -*- coding: utf-8 -*-
"""
This module provides the neccessary defintions to generate a Solution File.
"""

import os
import uuid
import errno

from vsgen.writer import VSGWritable


class VSGSolution(VSGWritable):
    """
    VSGSolution encapsulates the logic needed to create a ``.sln`` file.

    :ivar uuid GUID:     The GUI of the solution; if not provided one is generated automatically.
    :ivar str  FileName:  The absolute filename of the solution file; if not provided the value is ""
    :ivar str  Name:      The display name of the solution; if not provide the value is "".
    :ivar list Projects: The list of VSGProject derived classes; if not provide the value is [].
    """
    __writable_name__ = "VSG Solution"

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
        npath = os.path.normpath(self.FileName)
        (filepath, filename) = os.path.split(npath)
        try:
            os.makedirs(filepath)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        projectFileName = os.path.normpath(self.FileName)
        with open(projectFileName, 'wt') as f:
            f.write('Microsoft Visual Studio Solution File, Format Version 12.00\n')
            if self.VSVersion == 14.0:
                f.write('# Visual Studio 14\n')
                f.write('VisualStudioVersion = 14.0.23107.0\n')
                f.write('MinimumVisualStudioVersion = 10.0.40219.1\n')
            elif self.VSVersion == 12.0:
                f.write('# Visual Studio 2013\n')
                f.write('VisualStudioVersion = 12.0.31101.0\n')
                f.write('MinimumVisualStudioVersion = 10.0.40219.1\n')
            elif self.VSVersion == 11.0:
                f.write('# Visual Studio 2012\n')
            for pInfo in self.Projects:
                f.write('Project("{{{0}}}") = "{1}", "{2}", "{{{3}}}"\n'.format(self.upper(self.GUID), pInfo.Name, os.path.relpath(pInfo.FileName, filepath), pInfo.GUID))
                f.write('EndProject\n')
            f.write('Global\n')
            f.write('\tGlobalSection(SolutionConfigurationPlatforms) = preSolution\n')
            f.write('\t\tDebug|Any CPU = Debug|Any CPU\n')
            f.write('\t\tRelease|Any CPU = Release|Any CPU\n')
            f.write('\tEndGlobalSection\n')
            f.write('\tGlobalSection(ProjectConfigurationPlatforms) = postSolution\n')
            for pInfo in self.Projects:
                f.write('\t\t{{{0}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU\n'.format(self.upper(pInfo.GUID)))
                f.write('\t\t{{{0}}}.Release|Any CPU.ActiveCfg = Release|Any CPU\n'.format(self.upper(pInfo.GUID)))
            f.write('\tEndGlobalSection\n')
            f.write('\tGlobalSection(SolutionProperties) = preSolution\n')
            f.write('\t\tHideSolutionNode = FALSE\n')
            f.write('\tEndGlobalSection\n')
            f.write('\tGlobalSection(SolutionConfigurationPlatf.ms) = postSolution\n')
            for pInfo in self.Projects:
                f.write('\t\t{{{0}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU\n'.format(self.upper(pInfo.GUID)))
                f.write('\t\t{{{0}}}.Release|Any CPU.ActiveCfg = Release|Any CPU\n'.format(self.upper(pInfo.GUID)))
            f.write('\tEndGlobalSection\n')
            f.write('\tGlobalSection(SolutionConfigurationPlatf.ms) = preSolution\n')
            f.write('\t\tDebug|Any CPU = Debug|Any CPU\n')
            f.write('\t\tRelease|Any CPU = Release|Any CPU\n')
            f.write('\tEndGlobalSection\n')
            f.write('\tGlobalSection(ProjectConfigurationPlatf.ms) = postSolution\n')
            for pInfo in self.Projects:
                f.write('\t\t{{{0}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU\n'.format(self.upper(pInfo.GUID)))
                f.write('\t\t{{{0}}}.Debug|Any CPU.Build.0 = Debug|Any CPU\n'.format(self.upper(pInfo.GUID)))
                f.write('\t\t{{{0}}}.Release|Any CPU.ActiveCfg = Release|Any CPU\n'.format(self.upper(pInfo.GUID)))
                f.write('\t\t{{{0}}}.Release|Any CPU.Build.0 = Release|Any CPU\n'.format(self.upper(pInfo.GUID)))
            f.write('\tEndGlobalSection\n')
            f.write('EndGlobal\n')
