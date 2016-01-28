# -*- coding: utf-8 -*-
"""
PyvsgenDemo Pyvsgen Base

This module provides the neccessary defintions for PyvsgenDemo base python projects and solutions.
"""
import os
from pyvsgen import PyvsgenProject, PyvsgenSolution
from pyvsgendemo.settings import PyvsgenDemoSettings

class PyvsgenDemoBaseSolution(PyvsgenSolution):
    """
    PyvsgenDemoBaseSolution provides a base PyvsgenSolution for all PyvsgenSolutions in pyvsgendemo.pyvsgen.
    """
    def __init__(self, name, **kwargs):
        """
        Constructor.
        """
        super(PyvsgenDemoBaseSolution, self).__init__(**kwargs)
        self.FileName = os.path.join(PyvsgenDemoSettings.SolutionRoot, '{0}.sln'.format(name.lower()))
        self.Name = name

    def initialize(self):
        """
        Initializes the PyvsgenSolution by overriding the default values with instance specific values.
        """
        pass

    def write(self):
        """
        Override the PyvsgenDemoBaseProject write method.
        """
        self.initialize()
        return super(PyvsgenDemoBaseSolution, self).write()


class PyvsgenDemoBaseProject(PyvsgenProject):
    """
    PyvsgenDemoBaseProject provides a base PyvsgenProject for all PyvsgenProjects in pyvsgendemo.pyvsgen.
    """
    def __init__(self, name, rootpath, **kwargs):
        """
        Constructor.
        """
        super(PyvsgenDemoBaseProject, self).__init__(**kwargs)
        self.Name = name
        self.FileName = os.path.join(PyvsgenDemoSettings.ProjectRoot, '{0}.pyproj'.format(name.lower()))
        self.ProjectHome = rootpath
        self.SearchPath.append(rootpath)
        self.WorkingDirectory = rootpath
        self.OutputPath = rootpath
        self.RootNamespace = 'PyvsgenDemo'
        self.CompileInFilter.extend([ '.py', '.pyw' ])
        self.ContentInFilter.extend(['.bat', '.txt', '.cmd', '.ico', '.png', '.md'])

    def initialize(self):
        """
        Initializes the PyvsgenSolution by overriding the default values with instance specific values.
        """
        pass

    def write(self):
        """
        Override the PyvsgenDemoBaseProject write method.
        """
        self.initialize()
        return super(PyvsgenDemoBaseProject, self).write()
    
