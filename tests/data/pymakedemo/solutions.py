# -*- coding: utf-8 -*-
"""
This module provides the neccessary solution definitions for PymakeDemo's PTVS solutions.
"""
import os
from pymakedemo.projects import PymakeProject, PymakeDemoProject
from pymakedemo.base import PymakeDemoBaseSolution

class PymakeDemoSolution(PymakeDemoBaseSolution):
    """
    PymakeDemoSolution implements a single PymakeSolution for all PymakeProjects in the Pymake demo.
    """
    def __init__(self):
        super(PymakeDemoSolution, self).__init__('PymakeDemo')
        self.Projects.append(PymakeProject())
        self.Projects.append(PymakeDemoProject())

