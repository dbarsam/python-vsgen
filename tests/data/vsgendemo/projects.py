# -*- coding: utf-8 -*-
"""
This module provides the neccessary project defintions for VSGDemo's PTVS projects
"""
import os
from vsgendemo.base import VSGDemoBaseProject
from vsgendemo.settings import VSGDemoSettings


class VSGProject(VSGDemoBaseProject):
    """
    VSGDemoProject provides a VSGProject for the main VSG project
    """
    RootPath = os.path.join(VSGDemoSettings.MainRoot, 'vsgen')

    def __init__(self, **kwargs):
        super(VSGProject, self).__init__('VSG', self.RootPath, **kwargs)

    def initialize(self):
        """
        Initializes the VSGProject by overriding the default values with instance specific values.
        """
        self.insert_files(self.RootPath)


class VSGDemoProject(VSGDemoBaseProject):
    """
    VSGDemoProject provides a VSGProject for the VSGDemo project
    """
    RootPath = os.path.join(VSGDemoSettings.MainRoot, 'tests', 'data', 'vsgendemo')

    def __init__(self, **kwargs):
        super(VSGDemoProject, self).__init__('VSGDemo', self.RootPath, **kwargs)

    def initialize(self):
        """
        Initializes the VSGProject by overriding the default values with instance specific values.
        """
        self.insert_files(self.RootPath)
