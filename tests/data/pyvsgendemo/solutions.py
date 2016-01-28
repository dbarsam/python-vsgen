# -*- coding: utf-8 -*-
"""
This module provides the neccessary solution definitions for PyvsgenDemo's PTVS solutions.
"""
import os
from pyvsgendemo.projects import PyvsgenProject, PyvsgenDemoProject
from pyvsgendemo.base import PyvsgenDemoBaseSolution

class PyvsgenDemoSolution(PyvsgenDemoBaseSolution):
    """
    PyvsgenDemoSolution implements a single PyvsgenSolution for all PyvsgenProjects in the Pyvsgen demo.
    """
    def __init__(self, **kwargs):
        super(PyvsgenDemoSolution, self).__init__('PyvsgenDemo', **kwargs)
        self.Projects.append(PyvsgenProject(VSVersion=self.VSVersion))
        self.Projects.append(PyvsgenDemoProject(VSVersion=self.VSVersion))

