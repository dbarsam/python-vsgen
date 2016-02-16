# -*- coding: utf-8 -*-
"""
This module provides the neccessary defintions for VSGDemo's shared settings.
"""
import os


class VSGDemoSettings(object):
    """
    VSGDemoSettings provides a class for all static settings values in vsgendemo.vsgen.
    """
    # Directory Information
    LocalDir = os.path.dirname(os.path.realpath(__file__))
    MainRoot = os.path.normpath(os.path.join(LocalDir, '..', '..', '..'))
    BuildRoot = os.path.join(MainRoot, 'tests', 'data', '_output', )

    # Visual Studio Version
    VSVersion = 14.0

    # PTVS Output Directories
    SolutionRoot = os.path.join(BuildRoot, '_projects', 'vsgendemo', )
    ProjectRoot = os.path.join(BuildRoot, '_projects', 'vsgendemo', 'projs')
