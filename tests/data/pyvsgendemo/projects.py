# -*- coding: utf-8 -*-
"""
This module provides the neccessary project defintions for PyvsgenDemo's PTVS projects
"""
import os
from pyvsgendemo.base import PyvsgenDemoBaseProject 
from pyvsgendemo.settings import PyvsgenDemoSettings

class PyvsgenProject(PyvsgenDemoBaseProject):
    """
    PyvsgenDemoProject provides a PyvsgenProject for the main Pyvsgen project
    """
    RootPath = os.path.join( PyvsgenDemoSettings.MainRoot, 'pyvsgen' )

    def __init__(self, **kwargs):
        super(PyvsgenProject, self).__init__('Pyvsgen', self.RootPath, **kwargs)

    def initialize(self):
        """
        Initializes the PyvsgenProject by overriding the default values with instance specific values.
        """
        self.insert_files(self.RootPath)

class PyvsgenDemoProject(PyvsgenDemoBaseProject):
    """
    PyvsgenDemoProject provides a PyvsgenProject for the PyvsgenDemo project
    """
    RootPath = os.path.join( PyvsgenDemoSettings.MainRoot, 'tests', 'data', 'pyvsgendemo' )

    def __init__(self, **kwargs):
        super(PyvsgenDemoProject, self).__init__('PyvsgenDemo', self.RootPath, **kwargs)

    def initialize(self):
        """
        Initializes the PyvsgenProject by overriding the default values with instance specific values.
        """
        self.insert_files(self.RootPath)

