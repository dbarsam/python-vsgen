# -*- coding: utf-8 -*-
"""
This module provides the neccessary solution definitions for VSGDemo's PTVS solutions.
"""
import os

from vsgen import VSGSolution
from vsgendemo.settings import VSGDemoSettings
from vsgendemo.projects import VSGCoreProject, VSGDemoProject


class VSGDemoSolution(VSGSolution):
    """
    VSGDemoSolution implements a single VSGSolution for all VSGCoreProjects in the VSG demo.
    """

    def __init__(self, **kwargs):
        """
        Constructor.
        """
        super(VSGDemoSolution, self).__init__(**kwargs)
        self.Name = 'VSGDemo'
        self.FileName = os.path.join(VSGDemoSettings.SolutionRoot, '{0}.sln'.format(self.Name.lower()))
        self.Projects.append(VSGCoreProject(VSVersion=self.VSVersion))
        self.Projects.append(VSGDemoProject(VSVersion=self.VSVersion))
