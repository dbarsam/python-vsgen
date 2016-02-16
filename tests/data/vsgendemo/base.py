# -*- coding: utf-8 -*-
"""
VSGDemo VSG Base

This module provides the neccessary defintions for VSGDemo base python projects and solutions.
"""
import os
from vsgen import PTVSProject, VSGSolution
from vsgendemo.settings import VSGDemoSettings


class VSGDemoBaseSolution(VSGSolution):
    """
    VSGDemoBaseSolution provides a base VSGSolution for all VSGSolutions in vsgendemo.vsgen.
    """

    def __init__(self, name, **kwargs):
        """
        Constructor.
        """
        super(VSGDemoBaseSolution, self).__init__(**kwargs)
        self.FileName = os.path.join(VSGDemoSettings.SolutionRoot, '{0}.sln'.format(name.lower()))
        self.Name = name

    def initialize(self):
        """
        Initializes the VSGSolution by overriding the default values with instance specific values.
        """
        pass

    def write(self):
        """
        Override the VSGDemoBaseProject write method.
        """
        self.initialize()
        return super(VSGDemoBaseSolution, self).write()


class VSGDemoBaseProject(PTVSProject):
    """
    VSGDemoBaseProject provides a base VSGProject for all VSGProjects in vsgendemo.vsgen.
    """

    def __init__(self, name, rootpath, **kwargs):
        """
        Constructor.
        """
        super(VSGDemoBaseProject, self).__init__(**kwargs)
        self.Name = name
        self.FileName = os.path.join(VSGDemoSettings.ProjectRoot, '{0}.pyproj'.format(name.lower()))
        self.ProjectHome = rootpath
        self.SearchPath.append(rootpath)
        self.WorkingDirectory = rootpath
        self.OutputPath = rootpath
        self.RootNamespace = 'VSGDemo'
        self.CompileInFilter.extend(['.py', '.pyw'])
        self.ContentInFilter.extend(['.bat', '.txt', '.cmd', '.ico', '.png', '.md'])

    def initialize(self):
        """
        Initializes the VSGSolution by overriding the default values with instance specific values.
        """
        pass

    def write(self):
        """
        Override the VSGDemoBaseProject write method.
        """
        self.initialize()
        return super(VSGDemoBaseProject, self).write()
