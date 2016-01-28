# -*- coding: utf-8 -*-
"""
This module provides the neccessary project defintions for PymakeDemo's PTVS projects
"""
import os
from pymakedemo.base import PymakeDemoBaseProject 
from pymakedemo.settings import PymakeDemoSettings

class PymakeProject(PymakeDemoBaseProject):
    """
    PymakeDemoProject provides a PymakeProject for the main Pymake project
    """
    RootPath = os.path.join( PymakeDemoSettings.MainRoot, 'pymake' )

    def __init__(self, **kwargs):
        super(PymakeProject, self).__init__('Pymake', self.RootPath, **kwargs)

    def initialize(self):
        """
        Initializes the PymakeProject by overriding the default values with instance specific values.
        """
        self.insert_files(self.RootPath)

class PymakeDemoProject(PymakeDemoBaseProject):
    """
    PymakeDemoProject provides a PymakeProject for the PymakeDemo project
    """
    RootPath = os.path.join( PymakeDemoSettings.MainRoot, 'tests', 'data', 'pymakedemo' )

    def __init__(self, **kwargs):
        super(PymakeDemoProject, self).__init__('PymakeDemo', self.RootPath, **kwargs)

    def initialize(self):
        """
        Initializes the PymakeProject by overriding the default values with instance specific values.
        """
        self.insert_files(self.RootPath)

