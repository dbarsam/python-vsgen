# -*- coding: utf-8 -*-
"""
This module provides the neccessary solution definitions for VSGDemo's PTVS solutions.
"""
import os
from vsgendemo.projects import VSGProject, VSGDemoProject
from vsgendemo.base import VSGDemoBaseSolution


class VSGDemoSolution(VSGDemoBaseSolution):
    """
    VSGDemoSolution implements a single VSGSolution for all VSGProjects in the VSG demo.
    """

    def __init__(self, **kwargs):
        super(VSGDemoSolution, self).__init__('VSGDemo', **kwargs)
        self.Projects.append(VSGProject(VSVersion=self.VSVersion))
        self.Projects.append(VSGDemoProject(VSVersion=self.VSVersion))
