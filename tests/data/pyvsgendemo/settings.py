# -*- coding: utf-8 -*-
"""
This module provides the neccessary defintions for PymakeDemo's shared settings.
"""
import os

class PymakeDemoSettings(object):
    """
    PymakeDemoSettings provides a class for all static settings values in pymakedemo.pymake.
    """
    # Directory Information
    LocalDir        = os.path.dirname( os.path.realpath(__file__) )
    MainRoot        = os.path.normpath( os.path.join( LocalDir, '..', '..', '..') )
    BuildRoot       = os.path.join( MainRoot, 'tests', 'data', '_output', )

    # Visual Studio Version
    VSVersion = 14.0

    # PTVS Output Directories
    SolutionRoot    = os.path.join( BuildRoot, '_projects', 'pymakedemo', ) 
    ProjectRoot     = os.path.join( BuildRoot, '_projects', 'pymakedemo', 'projs')
