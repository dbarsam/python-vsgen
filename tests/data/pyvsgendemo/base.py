# -*- coding: utf-8 -*-
"""
PymakeDemo Pymake Base

This module provides the neccessary defintions for PymakeDemo base python projects and solutions.
"""
import os
from pymake import PymakeProject, PymakeSolution
from pymakedemo.settings import PymakeDemoSettings

class PymakeDemoBaseSolution(PymakeSolution):
    """
    PymakeDemoBaseSolution provides a base PymakeSolution for all PymakeSolutions in pymakedemo.pymake.
    """
    def __init__(self, name, **kwargs):
        """
        Constructor.
        """
        super(PymakeDemoBaseSolution, self).__init__(**kwargs)
        self.FileName = os.path.join(PymakeDemoSettings.SolutionRoot, '{0}.sln'.format(name.lower()))
        self.Name = name

    def initialize(self):
        """
        Initializes the PymakeSolution by overriding the default values with instance specific values.
        """
        pass

    def write(self):
        """
        Override the PymakeDemoBaseProject write method.
        """
        self.initialize()
        return super(PymakeDemoBaseSolution, self).write()


class PymakeDemoBaseProject(PymakeProject):
    """
    PymakeDemoBaseProject provides a base PymakeProject for all PymakeProjects in pymakedemo.pymake.
    """
    def __init__(self, name, rootpath, **kwargs):
        """
        Constructor.
        """
        super(PymakeDemoBaseProject, self).__init__(**kwargs)
        self.Name = name
        self.FileName = os.path.join(PymakeDemoSettings.ProjectRoot, '{0}.pyproj'.format(name.lower()))
        self.ProjectHome = rootpath
        self.SearchPath.append(rootpath)
        self.WorkingDirectory = rootpath
        self.OutputPath = rootpath
        self.RootNamespace = 'PymakeDemo'
        self.CompileInFilter.extend([ '.py', '.pyw' ])
        self.ContentInFilter.extend(['.bat', '.txt', '.cmd', '.ico', '.png', '.md'])

    def initialize(self):
        """
        Initializes the PymakeSolution by overriding the default values with instance specific values.
        """
        pass

    def write(self):
        """
        Override the PymakeDemoBaseProject write method.
        """
        self.initialize()
        return super(PymakeDemoBaseProject, self).write()
    
